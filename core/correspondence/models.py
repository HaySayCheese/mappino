#coding=utf-8
from django.db import models, transaction
from core.publications.constants import HEAD_MODELS

from core.users.models import Users


class Clients(models.Model):
	"""
	Даний клас описує клієнтів рієлторів.
	Із даними клієнтами пов’язуються повідомлення та запити на зворотні дзвінки.
	Всі поля за замовчуванням пусті. Передбачається що система по мірі надходження даних
	сама заповнюватиме даний об’єкт відомостями про клієнтів, але така можливість є і в рієлтора.
	"""
	# todo: (1.1) продумати і додати за потреби індексацію повідомлень в sphinx
	name = models.TextField(null=True)
	email = models.EmailField(null=True, unique=True)
	phone_number = models.CharField(null=True, unique=True, max_length=15) # з запасом, для форматів інших країн, окрім України
	description = models.TextField(null=True) # короткий опис клієнта рієлтором (примітка)

	@classmethod
	def id_by_email(cls, email):
		"""
		Повертає id клієнта з email = @email,
		або None, якщо такого емейла немає серед клієнтів.
		"""
		results = cls.objects.filter(email=email).only('id')[:1]
		if not results:
			return None
		else:
			return results[0].id


	@classmethod
	def id_by_phone_number(cls, phone_number):
		"""
		Повертає id клієнта з phone_number = @phone_number,
		або None, якщо такого номера немає серед клієнтів.
		"""
		results = cls.objects.filter(phone_number=phone_number).only('id')[:1]
		if not results:
			return None
		else:
			return results[0].id



class EventsThreads(models.Model):
	"""
	Даний клас покликаний стати менеджером всіх подій, які пов’язані з клієнтами і про які слід повідомити рієлтора.
	Стандартна модель діалогів клієнт-рієлтор не дуже підходить, оскільки спілкування може відбуватись не лише
	з допомогою повідомлень. Клієнти можуть залишати запити на зворотні дзвінки,
	а в перспективі рієлтор буде мати можливість залишати про клієнтів коротки записи,
	які допомагатимуть йому орієнтуватись у власних взіємовідносинах з клієнтами.

	Даний клас для кожного окремого клієнта створює окремий потік подій.
	Таким чином всі події пов’язуються з їх ініціаторами.
	Події від одного і того ж клієнта потрапляють в один і то й же потік.
	"""
	EVENTS_SEPARATOR = ';'
	EVENTS_TYPES = {
		'message': 'm',
	    'call_request': 'cr',
	}
	RECORD_DATA_SEPARATOR = ':'

	# Моделей для оголошень є декілька і вони в різних таблицях.
	# Немає змоги створити поле, яке б посилалось на одну з декількох таблиць.
	# Тому в даному полі буде зберігатись у текстовому вигляді інформація про таблицю,
	# та про запис, на які відбувається псилання.
	related_publication = models.TextField()
	realtor = models.ForeignKey(Users)
	client = models.ForeignKey(Clients)

	# Упорядочена послідовність записів ідентифікаторів подій.
	# Оскільки типів подій є декілька то реляційно зберігати їх накладно.
	# Тому всі id подій зберігаютьсяв даному полі у форматі "тип:id події".
	# Розділювач — див. RECORD_DATA_SEPARATOR
	# Типи подій — див. EVENTS_TYPES
	events_queue = models.TextField(default='')

	new_messages_count = models.SmallIntegerField(default=0) # к-сть непрочитаних повідомлень
	new_call_requests_count = models.SmallIntegerField(default=0) # к-сть нових запитів на зворотний дзвінок.


	@classmethod
	def add_message_from_client(cls, publication_tid, publication_hid, email, message, name=None):
		"""
		Args:
			publication_tid:    тип об’єкта оголошення.
			publication_hid:    id head-запису оголошення.
			email:              ел. адреса клієнта, на яку слід відправити відповідь рієлтора.
								Саме за даною адресою іднетифікується потік, в який слід додати повідомлення.
			message:            Повідомлення.
			name:               Ім’я клієнта.
								На фронтенді воно не є обов’зковим, тому може прийти, а може і не прийти.
								Якщо прийшло — автоматично додасться у відомості про клієнта.

		Метод позначено статичним оскільки саме клієнт ініціює потік подій.
		Якщо повідомлення, яке слід додати в потік, виявиться першим, то спочатку слід
		створити запис про клієнта в БД і запис про потік подій і лише тоді додавати повідомлення.
		"""
		if not message:
			raise ValueError('Empty message.')

		model = HEAD_MODELS.get(publication_tid)
		if model is None:
			raise ValueError('Invalid publication tid.')

		publication = model.objects.filter(id = publication_hid).only('id', 'owner')[:0]
		if not publication:
			raise ValueError('Invalid publication hid.')
		publication = publication[0]

		client_id = Clients.id_by_email(email)
		if client_id is None:
			# Немає клієнта - немає його потоку. Створюємо обох.
			with transaction.atomic():
				client = Clients.objects.create(
					email = email,
				    name = name, # записуємо, якщо передано
				)
				thread = cls.objects.create(
					related_publication_id = cls.__publication_id(publication_tid, publication_hid),
				    realtor = publication.owner,
				    client_id = client.id,
				)
				thread.__add_client_message(message) # немає необхідності викликати save().

		else:
			# Клієнт є.
			# Якщо у функцію передано ім’я, а в клієнта воно пусте - оновимо.
			if name is not None:
				client = Clients.objects.filter(id=client_id).only('name')[:1][0]
				client.name = name
				client.save()

			# Беремо його потік, якщо є, якщо немає — створюємо.
			thread = cls.objects.filter(
				client_id = client_id,

			    # один клієнт може писати різним рієлторам і про різні оголошення
				related_publication_id = cls.__publication_id(publication_tid, publication_hid),
			).only('events_queue', 'new_messages_count')[:1]

			with transaction.atomic():
				if thread:
					thread = thread[0]
				else:
					thread = cls.objects.create(
						related_publication_id = publication.id,
					    realtor = publication.owner,
					    client_id = client_id,
					)
				thread.__add_client_message(message) # немає необхідності викликати save().

		# todo: додати надсилання повідомлення на пошту рієлторам
		# todo: додати sms рієлторам


	@classmethod
	def add_call_request_from_client(cls, publication_tid, publication_hid, phone_number, name=None):
		"""
		Args:
			publication_tid:    тип об’єкта оголошення.
			publication_hid:    id head-запису оголошення.
			phone_number:       номер телефону клієнта, на який слід передзвонити.
								Саме за цим номером іднетифікується потік, в який слід додати повідомлення.
			name:               Ім’я клієнта.
								На фронтенді воно не є обов’зковим, тому може прийти, а може і не прийти.
								Якщо прийшло — автоматично додасться у відомості про клієнта.

		Додасть повідомлення від клієнта в потік.
		Якщо потоку, пов’язаного з даним клієнтом і даним оголошенням не існуватиме - його буде створено.

		Метод позначено статичним оскільки саме клієнт ініціює потік подій.
		Якщо повідомлення, яке слід додати в потік, виявиться першим, то спочатку слід
		створити запис про клієнта в БД і запис про потік подій і лише тоді додавати повідомлення.
		"""
		if not phone_number:
			raise ValueError('Invalid phone number.')

		model = HEAD_MODELS.get(publication_tid)
		if model is None:
			raise ValueError('Invalid publication tid.')

		publication = model.objects.filter(id = publication_hid).only('id', 'owner')[:0]
		if not publication:
			raise ValueError('Invalid publication hid.')
		publication = publication[0]

		# todo: перевірити чи немає досі запитів на даний номер по даному оголошенню

		client_id = Clients.id_by_phone_number(phone_number)
		if client_id is None:
			# Немає клієнта - немає його потоку. Створюємо обох.
			with transaction.atomic():
				client = Clients.objects.create(
					phone_number = phone_number,
				    name = name, # записуємо, якщо передано
				)
				thread = cls.objects.create(
					related_publication_id = cls.__publication_id(publication_tid, publication_hid),
				    realtor = publication.owner,
				    client_id = client.id,
				)
				thread.__add_client_call_request(phone_number) # немає необхідності викликати save().

		else:
			# Клієнт є.
			# Якщо у функцію передано ім’я, а в клієнта воно пусте - оновимо.
			if name is not None:
				client = Clients.objects.filter(id=client_id).only('name')[:1][0]
				client.name = name
				client.save()

			# Беремо його потік, якщо є, якщо немає — створюємо.
			thread = cls.objects.filter(
				client_id = client_id,

			    # один клієнт може писати різним рієлторам і про різні оголошення
				related_publication_id = cls.__publication_id(publication_tid, publication_hid),
			).only('events_queue', 'new_call_requests_count')[:1]

			with transaction.atomic():
				if thread:
					thread = thread[0]
				else:
					thread = cls.objects.create(
						related_publication_id = publication.id,
					    realtor = publication.owner,
					    client_id = client_id,
					)
				thread.__add_client_call_request(phone_number) # немає необхідності викликати save().

		# todo: додати sms рієлтору
		# todo: (1.1) продумати і додати за потреби індексацію повідомлень в sphinx


	@classmethod
	def add_message_from_realtor(cls, publication_tid, publication_hid, realtor_id, message):
		"""
		Args:
			publication_tid:    тип об’єкта оголошення.
			publication_hid:    id head-запису оголошення.
			realtor_id:         id рієлтора, зареєстрованого в системі.
			message:            Повідомлення.

		Додасть повідомлення від рієлтора в потік.
		Якщо потоку, пов’язаного з даним рієлтором і даним оголошенням не існуватиме - буде викинуто викл. ситуацію.
		(Оскільки, рієлтор не може виступати інціатором створення потоку повідомлень сам собі).
		"""
		if not message:
			raise ValueError('Empty message.')

		model = HEAD_MODELS.get(publication_tid)
		if model is None:
			raise ValueError('Invalid publication tid.')

		publication = model.objects.filter(id = publication_hid).only('id', 'owner')[:0]
		if not publication:
			raise ValueError('Invalid publication hid.')

		realtor = Users.objects.filter(id = realtor_id).only('id')[:1]
		if not realtor:
			raise ValueError('Invalid realtor_id.')

		# Шукаємо відповідний потік.
		# WARNING:
		#   Якщо відповідного потоку немає — створювати не можна.
		#   Рєілтор не повинен виступати ініціатором переписки.
		thread = cls.objects.filter(
			realtor_id = realtor.id,

		    # один клієнт може писати різним рієлторам і про різні оголошення
			related_publication_id = cls.__publication_id(publication_tid, publication_hid),
		).only('events_queue', 'new_messages_count')[:1]
		if thread:
			thread = thread[0]
		else:
			raise Exception('No such event thread.')

		with transaction.atomic(savepoint=False):
			thread.__add_client_message(message) # немає необхідності викликати save().


	def __add_client_message(self, message):
		with transaction.atomic(savepoint=False):
			message_record = Messages.objects.create(
				message = message,
			    sender_tid = Messages.SENDER_TYPES['client']
			)

			self.events_queue += self.EVENTS_TYPES['message'] + \
			                     self.RECORD_DATA_SEPARATOR + \
			                     unicode(message_record.id) + self.EVENTS_SEPARATOR
			self.new_messages_count += 1
			self.save()


	def __add_realtor_message(self, message):
		with transaction.atomic(savepoint=False):
			message_record = Messages.objects.create(
				message = message,
			    sender_tid = Messages.SENDER_TYPES['realtor']
			)

			self.events_queue += self.EVENTS_TYPES['message'] + \
			                     self.RECORD_DATA_SEPARATOR + \
			                     unicode(message_record.id) + self.EVENTS_SEPARATOR
			self.new_messages_count += 1
			self.save()


	def __add_client_call_request(self, phone_number):
		with transaction.atomic(savepoint=False):
			record = CallRequests.objects.create(
				phone_number = phone_number,
			)
			self.events_queue += self.EVENTS_TYPES['call_request'] + \
			                     self.RECORD_DATA_SEPARATOR + \
			                     unicode(record.id) + self.EVENTS_SEPARATOR
			self.new_call_requests_count += 1
			self.save()


	def __message_ids_from_events_queue(self):
		result = []
		for record in self.events_queue.split(self.EVENTS_SEPARATOR):
			type, id = record.split(self.RECORD_DATA_SEPARATOR)
			if type == self.EVENTS_TYPES['message']:
				result.append(id)


	def __call_requests_ids_from_events_queue(self):
		result = []
		for record in self.events_queue.split(self.EVENTS_SEPARATOR):
			type, id = record.split(self.RECORD_DATA_SEPARATOR)
			if type == self.EVENTS_TYPES['call_request']:
				result.append(id)


	@staticmethod
	def __publication_id(tid, hid):
		"""
		Повертає id оголошення для вставки в поля з неявним зв’язком.
		"""
		return unicode(tid) + ':' + unicode(hid)



class Messages(models.Model):
	SENDER_TYPES = {
		'client': 'c',
		'realtor': 'r',
	}

	created = models.DateTimeField(auto_created=True)
	message = models.TextField()
	sender_tid = models.CharField(max_length=2) # щоб мати змогу відрізняти хто є автором повідомлення.

	def delete(self, using=None):
		# Заборонити використання цього методу.
		# Зв’язки між повідомленнями та потоком подій неявні і на рівні БД відслідковувані не будуть.
		# Зроблено задля забезпечення цілісності системи.
		raise Exception('Use appropriate method of Events Thread.')



class CallRequests(models.Model):
	created = models.DateTimeField(auto_created=True)
	phone_number = models.TextField()

	def delete(self, using=None):
		# Заборонити використання цього методу.
		# Зв’язки між запитами та потоком подій неявні і на рівні БД відслідковувані не будуть.
		# Зроблено задля забезпечення цілісності системи.
		raise Exception('Use appropriate method of Events Thread.')


