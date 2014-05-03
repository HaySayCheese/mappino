#coding=utf-8
import json

from django.test.client import Client
from django.utils import unittest

from core.users.models import Users, PersonalPagesAliases



class ValidateAliasesAnonymousAccess(unittest.TestCase):
	@classmethod
	def setUpClass(cls):
		cls.client = Client()
		cls.user = Users.objects.create_user('mail@mail.com', '+380954699', 'password')
		cls.user.is_active = True # за замовчуванням аккаунти вимкнені
		cls.user.save()


	@classmethod
	def tearDownClass(cls):
		Users.objects.all().delete()


	def test_authorized_only(self):
		"""
		Анонімам доступ заборонено
		"""
		response = self.client.post('/ajax/api/cabinet/settings/personal-page-aliases/validate/')
		self.assertEqual(response.status_code, 403)



class ValidateAliasesAuthorizedAccess(unittest.TestCase):
	@classmethod
	def setUpClass(cls):
		cls.client = Client()
		cls.user = Users.objects.create_user('mail@mail.com', '+380954699', 'password')
		cls.user.is_active = True # за замовчуванням аккаунти вимкнені
		cls.user.save()
		cls.client.login(username='+380954699', password='password')


	@classmethod
	def tearDownClass(cls):
		Users.objects.all().delete()


	def test_empty_request(self):
		response = self.client.post('/ajax/api/cabinet/settings/personal-page-aliases/validate/',
			content_type='application/json')
		self.assertEqual(response.status_code, 400)


	def test_empty_alias(self):
		response = self.client.post('/ajax/api/cabinet/settings/personal-page-aliases/validate/',
			json.dumps({
				'alias': ''
			}), content_type='application/json')
		self.assertEqual(response.status_code, 400)


	def test_invalid_symbols(self):
		for symbol in ['.', ',', ' ', '/', '\\', '?']:
			response = self.client.post('/ajax/api/cabinet/settings/personal-page-aliases/validate/',
				json.dumps({
					'alias': symbol
				}), content_type='application/json')

			data = json.loads(response.content)

			self.assertEqual(response.status_code, 200) # request is correct but must be rejected
			self.assertTrue('code' in data)
			self.assertEqual(data['code'], 1)


	def test_uppercase(self):
		response = self.client.post('/ajax/api/cabinet/settings/personal-page-aliases/validate/',
			json.dumps({
				'alias': 'UPPER'
			}), content_type='application/json')

		data = json.loads(response.content)

		self.assertEqual(response.status_code, 200) # request is correct but must be rejected
		self.assertTrue('code' in data)
		self.assertEqual(data['code'], 1)


	def test_cyrillic(self):
		response = self.client.post('/ajax/api/cabinet/settings/personal-page-aliases/validate/',
			json.dumps({
				'alias': 'Кирилица'
			}), content_type='application/json')

		data = json.loads(response.content)

		self.assertEqual(response.status_code, 200) # request is correct but should be rejected
		self.assertTrue('code' in data)
		self.assertEqual(data['code'], 1)


	def test_normal(self):
		response = self.client.post('/ajax/api/cabinet/settings/personal-page-aliases/validate/',
			json.dumps({
				'alias': 'test'
			}), content_type='application/json')

		data = json.loads(response.content)

		self.assertEqual(response.status_code, 200) # request is correct but should be rejected
		self.assertTrue('code' in data)
		self.assertEqual(data['code'], 0)



class ValidateAliasesDuplicates(unittest.TestCase):
	@classmethod
	def setUpClass(cls):
		cls.client = Client()
		cls.user = Users.objects.create_user('mail@mail.com', '+380954699', 'password')
		cls.user.is_active = True # за замовчуванням аккаунти вимкнені
		cls.user.save()
		cls.client.login(username='+380954699', password='password')

		PersonalPagesAliases.objects.create(
			user = cls.user,
		    alias = 'test'
		)


		cls.other_user = Users.objects.create_user('mail2@mail.com', '+380954698', 'password2')
		cls.other_user.is_active = True # за замовчуванням аккаунти вимкнені
		cls.other_user.save()

		PersonalPagesAliases.objects.create(
			user = cls.other_user,
		    alias = 'duplicate'
		)


	@classmethod
	def tearDownClass(cls):
		Users.objects.all().delete()
		PersonalPagesAliases.objects.all().delete()


	def test_duplicate(self):
		response = self.client.post('/ajax/api/cabinet/settings/personal-page-aliases/validate/',
			json.dumps({
				'alias': 'duplicate'
			}), content_type='application/json')

		data = json.loads(response.content)

		self.assertEqual(response.status_code, 200)
		self.assertTrue('code' in data)
		self.assertEqual(data['code'], 2)


	def test_normal(self):
		response = self.client.post('/ajax/api/cabinet/settings/personal-page-aliases/validate/',
			json.dumps({
				'alias': 'test'
			}), content_type='application/json')

		data = json.loads(response.content)

		self.assertEqual(response.status_code, 200)
		self.assertTrue('code' in data)
		self.assertEqual(data['code'], 0)



class AliasesCreatingAnonymous(unittest.TestCase):
	@classmethod
	def setUpClass(cls):
		cls.client = Client()
		cls.user = Users.objects.create_user('mail@mail.com', '+380954699', 'password')
		cls.user.is_active = True # за замовчуванням аккаунти вимкнені
		cls.user.save()


	@classmethod
	def tearDownClass(cls):
		Users.objects.all().delete()


	def test_authorized_only(self):
		response = self.client.post('/ajax/api/cabinet/settings/personal-page-aliases/')
		self.assertEqual(response.status_code, 403)



class AliasesCreatingAuthorized(unittest.TestCase):
	@classmethod
	def setUpClass(cls):
		cls.client = Client()
		cls.user = Users.objects.create_user('mail@mail.com', '+380954699', 'password')
		cls.user.is_active = True # за замовчуванням аккаунти вимкнені
		cls.user.save()
		cls.client.login(username='+380954699', password='password')


	@classmethod
	def tearDownClass(cls):
		Users.objects.all().delete()
		PersonalPagesAliases.objects.all().delete()


	def test_empty_request(self):
		response = self.client.post('/ajax/api/cabinet/settings/personal-page-aliases/',
		    content_type='application/json')
		self.assertEqual(response.status_code, 400) # request is incorrect


	def test_empty_alias(self):
		response = self.client.post('/ajax/api/cabinet/settings/personal-page-aliases/',
			json.dumps({
				'alias': ''
			}), content_type='application/json')
		self.assertEqual(response.status_code, 400) # request is incorrect


	def test_invalid_symbols(self):
		for symbol in ['.', ',', ' ', '/', '\\', '#']:
			response = self.client.post('/ajax/api/cabinet/settings/personal-page-aliases/',
				json.dumps({
					'alias': symbol
				}), content_type='application/json')

			data = json.loads(response.content)

			self.assertEqual(response.status_code, 200) # request is correct but should be rejected
			self.assertTrue('code' in data)
			self.assertEqual(data['code'], 1)


	def test_uppercase(self):
		response = self.client.post('/ajax/api/cabinet/settings/personal-page-aliases/',
			json.dumps({
				'alias': 'UPPER'
			}), content_type='application/json')

		data = json.loads(response.content)

		self.assertEqual(response.status_code, 200) # request is correct but should be rejected
		self.assertTrue('code' in data)
		self.assertEqual(data['code'], 1)


	def test_cyrillic(self):
		response = self.client.post('/ajax/api/cabinet/settings/personal-page-aliases/',
			json.dumps({
				'alias': 'Кирилица'
			}), content_type='application/json')

		data = json.loads(response.content)

		self.assertEqual(response.status_code, 200) # request is correct but should be rejected
		self.assertTrue('code' in data)
		self.assertEqual(data['code'], 1)


	def test_normal(self):
		response = self.client.post('/ajax/api/cabinet/settings/personal-page-aliases/',
			json.dumps({
				'alias': 'test'
			}), content_type='application/json')

		data = json.loads(response.content)

		self.assertEqual(response.status_code, 200)
		self.assertTrue('code' in data)
		self.assertEqual(data['code'], 0)



class AliasesCreatingDuplicates(unittest.TestCase):
	@classmethod
	def setUpClass(cls):
		cls.client = Client()
		cls.user = Users.objects.create_user('mail@mail.com', '+380954699', 'password')
		cls.user.is_active = True # за замовчуванням аккаунти вимкнені
		cls.user.save()
		cls.client.login(username='+380954699', password='password')

		PersonalPagesAliases.objects.create(
			user = cls.user,
		    alias = 'test'
		)


		cls.other_user = Users.objects.create_user('mail2@mail.com', '+380954698', 'password2')
		cls.other_user.is_active = True # за замовчуванням аккаунти вимкнені
		cls.other_user.save()

		PersonalPagesAliases.objects.create(
			user = cls.other_user,
		    alias = 'test2'
		)


	@classmethod
	def tearDownClass(cls):
		Users.objects.all().delete()
		PersonalPagesAliases.objects.all().delete()


	def test_duplicate_update(self):
		"""
		Хоч в БД і є запис "test" користувача "user",
		але його заміна на ткий самий самий не вважається дублікатом.
		"""
		response = self.client.post('/ajax/api/cabinet/settings/personal-page-aliases/',
			json.dumps({
				'alias': 'test'
			}), content_type='application/json')

		data = json.loads(response.content)

		self.assertEqual(response.status_code, 200)
		self.assertTrue('code' in data)
		self.assertEqual(data['code'], 0)

		record = PersonalPagesAliases.objects.filter(user=self.user)[0]
		self.assertEqual(record.alias, 'test')


	def test_duplicate(self):
		response = self.client.post('/ajax/api/cabinet/settings/personal-page-aliases/',
			json.dumps({
				'alias': 'test2'
			}), content_type='application/json')

		data = json.loads(response.content)

		self.assertEqual(response.status_code, 200)
		self.assertTrue('code' in data)
		self.assertEqual(data['code'], 2)


	def test_update(self):
		response = self.client.post('/ajax/api/cabinet/settings/personal-page-aliases/',
			json.dumps({
				'alias': 'new-value'
			}), content_type='application/json')

		data = json.loads(response.content)

		self.assertEqual(response.status_code, 200)
		self.assertTrue('code' in data)
		self.assertEqual(data['code'], 0)

		record = PersonalPagesAliases.objects.filter(user=self.user)[0]
		self.assertEqual(record.alias, 'new-value')