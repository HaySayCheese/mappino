# #coding=utf-8
# import json
#
# from core.users.models import Users
# from django.test import Client
# from django.utils import unittest
#
#
# class TestAccountInfoUpdating(unittest.TestCase):
# 	@classmethod
# 	def setUpClass(cls):
# 		cls.client = Client()
# 		cls.user = Users.objects.create_user('mail@mail.com', '+380954699151', 'password')
# 		cls.user.is_active = True # за замовчуванням аккаунти вимкнені
# 		cls.user.save()
#
# 		cls.client.login(username='+380954699151', password='password')
#
#
# 	@classmethod
# 	def tearDownClass(cls):
# 		Users.objects.all().delete()
#
#
# 	def test_first_name_update(self):
# 		# empty
# 		response = self.client.post(
# 			'/ajax/api/cabinet/account/', json.dumps({
# 				"f": "first_name",
# 				"v": ""
# 			}), content_type='application/ajax')
# 		self.assertEqual(response.status_code, 400) # field is required
#
#
# 		# good
# 		name = 'test_name'
# 		response = self.client.post(
# 			'/ajax/api/cabinet/account/', json.dumps({
# 				"f": "first_name",
# 				"v": "test_name",
# 			}), content_type='application/ajax')
# 		self.assertEqual(response.status_code, 200)
#
# 		data = json.loads(response.content)
# 		self.assertTrue('code' in data)
# 		self.assertEqual(data['code'], 0)
#
# 		user = Users.objects.get(id=self.user.id)
# 		self.assertEqual(user.first_name, name)
#
#
# 	def test_last_name_update(self):
# 		# empty
# 		response = self.client.post(
# 			'/ajax/api/cabinet/account/', json.dumps({
# 				"f": "last_name",
# 				"v": ""
# 			}), content_type='application/ajax')
# 		self.assertEqual(response.status_code, 400) # field is required
#
#
# 		# good
# 		name = 'test_name'
# 		response = self.client.post(
# 			'/ajax/api/cabinet/account/', json.dumps({
# 				"f": "last_name",
# 				"v": "test_name",
# 			}), content_type='application/ajax')
# 		self.assertEqual(response.status_code, 200)
#
# 		data = json.loads(response.content)
# 		self.assertTrue('code' in data)
# 		self.assertEqual(data['code'], 0)
#
# 		user = Users.objects.get(id=self.user.id)
# 		self.assertEqual(user.last_name, name)
#
#
# 	def test_email_update(self):
# 		# empty
# 		response = self.client.post(
# 			'/ajax/api/cabinet/account/', json.dumps({
# 				"f": "email",
# 				"v": ""
# 			}), content_type='application/ajax')
# 		self.assertEqual(response.status_code, 400) # field is required
#
#
# 		# invalid
# 		response = self.client.post(
# 			'/ajax/api/cabinet/account/', json.dumps({
# 				"f": "email",
# 				"v": "invalid-email"
# 			}), content_type='application/ajax')
# 		self.assertEqual(response.status_code, 200)
#
# 		data = json.loads(response.content)
# 		self.assertTrue('code' in data)
# 		self.assertEqual(data['code'], 10)
#
#
# 		# duplicate with other user
# 		Users.objects.create_user('test_dup_email@email.com', '+3809512345', 'password')
# 		response = self.client.post(
# 			'/ajax/api/cabinet/account/', json.dumps({
# 				"f": "email",
# 				"v": "test_dup_email@email.com"
# 			}), content_type='application/ajax')
# 		self.assertEqual(response.status_code, 200)
#
# 		data = json.loads(response.content)
# 		self.assertTrue('code' in data)
# 		self.assertEqual(data['code'], 11)
#
#
# 		# duplicate with work email
# 		self.user.work_email = 'test_work@mail.com'
# 		self.user.save()
# 		response = self.client.post(
# 			'/ajax/api/cabinet/account/', json.dumps({
# 				"f": "email",
# 				"v": "test_work@mail.com"
# 			}), content_type='application/ajax')
# 		self.assertEqual(response.status_code, 200)
#
# 		data = json.loads(response.content)
# 		self.assertTrue('code' in data)
# 		self.assertEqual(data['code'], 11)
#
#
# 		# good
# 		response = self.client.post(
# 			'/ajax/api/cabinet/account/', json.dumps({
# 				"f": "email",
# 				"v": "good@email.com",
# 			}), content_type='application/ajax')
# 		self.assertEqual(response.status_code, 200)
#
# 		data = json.loads(response.content)
# 		self.assertTrue('code' in data)
# 		self.assertEqual(data['code'], 0)
#
# 		user = Users.objects.get(id=self.user.id)
# 		self.assertEqual(user.email, 'good@email.com')
#
#
# 		# the same
# 		response = self.client.post(
# 			'/ajax/api/cabinet/account/', json.dumps({
# 				"f": "email",
# 				"v": "good@email.com",
# 			}), content_type='application/ajax')
# 		self.assertEqual(response.status_code, 200)
#
# 		data = json.loads(response.content)
# 		self.assertTrue('code' in data)
# 		self.assertEqual(data['code'], 0)
#
# 		user = Users.objects.get(id=self.user.id)
# 		self.assertEqual(user.email, 'good@email.com')
#
#
# 	def test_phone_update(self):
# 		# empty
# 		response = self.client.post(
# 			'/ajax/api/cabinet/account/', json.dumps({
# 				"f": "mobile_phone",
# 				"v": ""
# 			}), content_type='application/ajax')
# 		self.assertEqual(response.status_code, 400) # field is required
#
#
# 		# invalid
# 		response = self.client.post(
# 			'/ajax/api/cabinet/account/', json.dumps({
# 				"f": "mobile_phone",
# 				"v": "invalid"
# 			}), content_type='application/ajax')
# 		self.assertEqual(response.status_code, 200)
#
# 		data = json.loads(response.content)
# 		self.assertTrue('code' in data)
# 		self.assertEqual(data['code'], 20)
#
#
# 		# duplicate with other user
# 		Users.objects.create_user('test_dup_email@email.com', '+380951234567', 'password')
# 		response = self.client.post(
# 			'/ajax/api/cabinet/account/', json.dumps({
# 				"f": "mobile_phone",
# 				"v": "+380951234567"
# 			}), content_type='application/ajax')
# 		self.assertEqual(response.status_code, 200)
#
# 		data = json.loads(response.content)
# 		self.assertTrue('code' in data)
# 		self.assertEqual(data['code'], 21)
#
#
# 		# duplicate with add mobile phone
# 		self.user.add_mobile_phone = '+380950101001'
# 		self.user.save()
# 		response = self.client.post(
# 			'/ajax/api/cabinet/account/', json.dumps({
# 				"f": "mobile_phone",
# 				"v": "+380950101001"
# 			}), content_type='application/ajax')
# 		self.assertEqual(response.status_code, 200)
#
# 		data = json.loads(response.content)
# 		self.assertTrue('code' in data)
# 		self.assertEqual(data['code'], 21)
#
#
# 		# good
# 		response = self.client.post(
# 			'/ajax/api/cabinet/account/', json.dumps({
# 				"f": "mobile_phone",
# 				"v": "+380950000000",
# 			}), content_type='application/ajax')
# 		self.assertEqual(response.status_code, 200)
#
# 		data = json.loads(response.content)
# 		self.assertTrue('code' in data)
# 		self.assertEqual(data['code'], 0)
#
# 		user = Users.objects.get(id=self.user.id)
# 		self.assertEqual(user.mobile_phone, 'good@email.com')
#
#
# 		# the same
# 		response = self.client.post(
# 			'/ajax/api/cabinet/account/', json.dumps({
# 				"f": "mobile_phone",
# 				"v": "+380950000000",
# 			}), content_type='application/ajax')
# 		self.assertEqual(response.status_code, 200)
#
# 		data = json.loads(response.content)
# 		self.assertTrue('code' in data)
# 		self.assertEqual(data['code'], 0)
#
# 		user = Users.objects.get(id=self.user.id)
# 		self.assertEqual(user.mobile_phone, 'good@email.com')
#
#
# 	def test_work_email_update(self):
# 		# empty
# 		response = self.client.post(
# 			'/ajax/api/cabinet/account/', json.dumps({
# 				"f": "work_email",
# 				"v": ""
# 			}), content_type='application/ajax')
# 		self.assertEqual(response.status_code, 200) # field may be empty
#
# 		user = Users.objects.get(id=self.user.id)
# 		self.assertEqual(user.work_email, '')
#
#
# 		# invalid
# 		response = self.client.post(
# 			'/ajax/api/cabinet/account/', json.dumps({
# 				"f": "work_email",
# 				"v": "invalid-email"
# 			}), content_type='application/ajax')
# 		self.assertEqual(response.status_code, 200)
#
# 		data = json.loads(response.content)
# 		self.assertTrue('code' in data)
# 		self.assertEqual(data['code'], 10)
#
#
# 		# duplicate with other user
# 		other_user = Users.objects.create_user('test_dup_email@email.com', '+3809512345', 'password')
# 		other_user.work_email = 'test_work_dup@email.com'
#
# 		response = self.client.post(
# 			'/ajax/api/cabinet/account/', json.dumps({
# 				"f": "work_email",
# 				"v": "test_work_dup@email.com"
# 			}), content_type='application/ajax')
# 		self.assertEqual(response.status_code, 200)
#
# 		data = json.loads(response.content)
# 		self.assertTrue('code' in data)
# 		self.assertEqual(data['code'], 11)
#
#
# 		# duplicate with main email
# 		response = self.client.post(
# 			'/ajax/api/cabinet/account/', json.dumps({
# 				"f": "work_email",
# 				"v": self.user.email,
# 			}), content_type='application/ajax')
# 		self.assertEqual(response.status_code, 200)
#
# 		data = json.loads(response.content)
# 		self.assertTrue('code' in data)
# 		self.assertEqual(data['code'], 11)
#
#
# 		# good
# 		response = self.client.post(
# 			'/ajax/api/cabinet/account/', json.dumps({
# 				"f": "work_email",
# 				"v": "good_work@email.com",
# 			}), content_type='application/ajax')
# 		self.assertEqual(response.status_code, 200)
#
# 		data = json.loads(response.content)
# 		self.assertTrue('code' in data)
# 		self.assertEqual(data['code'], 0)
#
# 		user = Users.objects.get(id=self.user.id)
# 		self.assertEqual(user.email, 'good@email.com')
#
#
# 		# the same
# 		response = self.client.post(
# 			'/ajax/api/cabinet/account/', json.dumps({
# 				"f": "work_email",
# 				"v": "good_work@email.com",
# 			}), content_type='application/ajax')
# 		self.assertEqual(response.status_code, 200)
#
# 		data = json.loads(response.content)
# 		self.assertTrue('code' in data)
# 		self.assertEqual(data['code'], 0)
#
# 		user = Users.objects.get(id=self.user.id)
# 		self.assertEqual(user.email, 'good@email.com')
#
#
# 	def test_add_mobile_phone_update(self):
# 		# empty
# 		response = self.client.post(
# 			'/ajax/api/cabinet/account/', json.dumps({
# 				"f": "add_mobile_phone",
# 				"v": ""
# 			}), content_type='application/ajax')
# 		self.assertEqual(response.status_code, 200) # field may be empty
#
# 		user = Users.objects.get(id=self.user.id)
# 		self.assertEqual(user.work_email, '')
#
#
# 		# invalid
# 		response = self.client.post(
# 			'/ajax/api/cabinet/account/', json.dumps({
# 				"f": "add_mobile_phone",
# 				"v": "invalid-phone"
# 			}), content_type='application/ajax')
# 		self.assertEqual(response.status_code, 200)
#
# 		data = json.loads(response.content)
# 		self.assertTrue('code' in data)
# 		self.assertEqual(data['code'], 20)
#
#
# 		# duplicate with other user
# 		other_user = Users.objects.create_user('test_dup_email@email.com', '+3809512345', 'password')
# 		other_user.add_mobile_phone = '+380951234500'
#
# 		response = self.client.post(
# 			'/ajax/api/cabinet/account/', json.dumps({
# 				"f": "add_mobile_phone",
# 				"v": "+380951234500"
# 			}), content_type='application/ajax')
# 		self.assertEqual(response.status_code, 200)
#
# 		data = json.loads(response.content)
# 		self.assertTrue('code' in data)
# 		self.assertEqual(data['code'], 21)
#
#
# 		# duplicate with main phone
# 		response = self.client.post(
# 			'/ajax/api/cabinet/account/', json.dumps({
# 				"f": "add_mobile_phone",
# 				"v": self.user.mobile_phone,
# 			}), content_type='application/ajax')
# 		self.assertEqual(response.status_code, 200)
#
# 		data = json.loads(response.content)
# 		self.assertTrue('code' in data)
# 		self.assertEqual(data['code'], 21)
#
#
# 		# good
# 		response = self.client.post(
# 			'/ajax/api/cabinet/account/', json.dumps({
# 				"f": "add_mobile_phone",
# 				"v": "+380930000000",
# 			}), content_type='application/ajax')
# 		self.assertEqual(response.status_code, 200)
#
# 		data = json.loads(response.content)
# 		self.assertTrue('code' in data)
# 		self.assertEqual(data['code'], 0)
#
# 		user = Users.objects.get(id=self.user.id)
# 		self.assertEqual(user.mobile_phone, '+380930000000')
#
#
# 		# the same
# 		response = self.client.post(
# 			'/ajax/api/cabinet/account/', json.dumps({
# 				"f": "add_mobile_phone",
# 				"v": "+380930000000",
# 			}), content_type='application/ajax')
# 		self.assertEqual(response.status_code, 200)
#
# 		data = json.loads(response.content)
# 		self.assertTrue('code' in data)
# 		self.assertEqual(data['code'], 0)
#
# 		user = Users.objects.get(id=self.user.id)
# 		self.assertEqual(user.mobile_phone, '+380930000000')
#
#
# 	# todo: дописати решту тестів.. замучився..
