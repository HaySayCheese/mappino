#coding=utf-8
import hashlib
import random
import string

from collective.exceptions import EmptyArgument
from collective.http.cookies import set_signed_cookie
from core.sms_dispatcher import check_codes_sms_sender
from mappino.wsgi import redis_connections


class MobilePhoneChecker(object):
	class AlreadyInQueue(Exception):
		def __init__(self, message, sms_sent):
			super(self, MobilePhoneChecker.AlreadyInQueue).__init__(message)
			self.sms_sent = sms_sent


	_redis = redis_connections['steady']
	_record_prefix = 'mcheck_'

	_transaction_ttl = 60 * 60 * 4 # (seconds).
	_max_sms_per_transaction = 2

	_cookie_name = 'mcheck'
	_cookie_salt = 'JMH2FWWYa1ogCJR0gW4z'


	@classmethod
	def begin_check(cls, account_id, mobile_phone, request, response):
		# В якості поля з якого знімається хеш використовується телефон.
		# Це дає змогу уберегтись від дублікатів записів,
		# (id аккаунта з кожною реєстрацією буде новим, а, відповідно, і хеш буде новим).
		phone_hash = cls._get_phone_hash(mobile_phone)


		record_id = cls._record_prefix + phone_hash
		if cls._redis.exists(record_id):
			# Запис вже присутній.
			# Передаємо на фронтенд кількість вже надісланих sms на цей номер для того,
			# щоб не дати користувачу можливості запитувати sms поза ліміт.

			record = cls._get_record(record_id, only='sms_sent')
			if record:
				raise MobilePhoneChecker.AlreadyInQueue('', record['sms_sent'])
			# Якщо record==None - швидше за все він був видалений по ttl. Продовжуємо.


		check_code = ''.join(random.choice(string.digits) for x in range(6))


		# Зберігаємо дані в redis.
		pipe = cls._redis.pipeline()
		pipe.hset(record_id, 'id', account_id)
		pipe.hset(record_id, 'code', check_code)
		pipe.hset(record_id, 'phone', mobile_phone)
		pipe.hset(record_id, 'sms_sent', 0)
		pipe.expire(record_id, cls._transaction_ttl)
		pipe.execute()


		# Створємо куку з ідентифікатором запису в redis щоб мати змогу пізніше відновити дані та
		# провести необхідні перевірки.
		set_signed_cookie(response, cls._cookie_name, phone_hash,
		                  salt=cls._cookie_salt, seconds_expire=cls._transaction_ttl, http_only=False)

		# note: даний метод здійснює низку перевірок перед тим як вислати sms
		cls._send_code(record_id, mobile_phone, check_code, request)


	@classmethod
	def check_is_started(cls, request):
		if cls._cookie_name in request.COOKIES:
			record_id = cls._record_prefix + request.get_signed_cookie(cls._cookie_name, salt=cls._cookie_salt)
			return cls._redis.exists(record_id)
		else:
			return False


	@classmethod
	def check_code(cls, code, request, response):
		if not code:
			raise EmptyArgument('"code" is empty or None.')


		record_id = cls._record_prefix + request.get_signed_cookie(cls._cookie_name, salt=cls._cookie_salt)
		record = cls._get_record(record_id)
		if not record:
			# Якщо record==None - швидше за все він був видалений по ttl.
			response.delete_cookie(cls._cookie_name)
			return False, None


		# check
		if code != record['code']:
			return False, None


		# seems to be ok
		cls._redis.delete(record_id)
		response.delete_cookie(cls._cookie_name)
		return True, {'id': record['id']}


	@classmethod
	def resend_sms(cls, request):
		record_id = cls._record_prefix + request.get_signed_cookie(cls._cookie_name, salt=cls._cookie_salt)
		record = cls._get_record(record_id, only=['phone', 'code'])

		# note: даний метод здійснює низку перевірок перед тим як вислати sms
		cls._send_code(record_id, record['phone'], record['code'], request, resend=True)


	@classmethod
	def cancel_check(cls, request, response):
		record_id = cls._record_prefix + request.get_signed_cookie(cls._cookie_name, salt=cls._cookie_salt)
		if not cls._redis.exists(record_id):
			# todo: suspicious operation
			return

		cls._redis.delete(record_id)
		response.delete_cookie(cls._cookie_name)


	@classmethod
	def _send_code(cls, record_id, mobile_phone, code, request, resend=False):
		"""
		Перевірить чи на вказаний номер не перевищено ліміт надсилань.
		Якщо не перевищено - надішле sms з кодом.
		"""
		def send():
			if resend:
				check_codes_sms_sender.resend(mobile_phone, code, resend)
			else:
				check_codes_sms_sender.send(mobile_phone, code, request)


		sms_sent = cls._redis.hget(record_id, 'sms_sent')
		if sms_sent is None:
			send()
			cls._redis.hset(record_id, 'sms_sent', 1) # set

		elif int(sms_sent) < cls._max_sms_per_transaction:
			send()
			cls._redis.hincrby(record_id, 'sms_sent', 1) # increment


	@staticmethod
	def _get_phone_hash(mobile_phone):
		"""
		Повертає підсолений хеш з мобільного телефону користувача.
		"""
		h = hashlib.sha256()
		h.update(str(mobile_phone))
		h.update('E66bLuTGzEkDqQHmrSNU') # salt
		return h.hexdigest()


	@classmethod
	def _get_record(cls, record_id, only=None):
		"""
		Повертає запис з record_id якщо він існує і якщо всі поля цього запису не None.
		Інакше поверне None.
		"""
		if not cls._redis.exists(record_id):
			return None

		if only is None:
			record = {
				'id': cls._redis.hget(record_id, 'id'),
				'code': cls._redis.hget(record_id, 'code'),
				'phone': cls._redis.hget(record_id, 'phone'),
				'sms_sent': cls._redis.hget(record_id, 'sms_sent'),
			}
			return record if None not in record.values() else None

		else:
			record = {}
			if 'id' in only:
				record['id'] = cls._redis.hget(record_id, 'id')
			if 'code' in only:
				record['code'] = cls._redis.hget(record_id, 'code')
			if 'phone' in only:
				record['phone'] = cls._redis.hget(record_id, 'phone')
			if 'sms_sent' in only:
				record['sms_sent'] = cls._redis.hget(record_id, 'sms_sent')
			return record



