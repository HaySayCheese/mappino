#coding=utf-8
from django.core import serializers
from core.dirtags.models import DirTags


def publication_data(tid, record):
	head = serializers.serialize(
		'python', [record], fields=('created', 'actual', 'for_rent', 'for_sale', 'state_sid',
		                            'degree_lat', 'degree_lng', 'segment_lat', 'segment_lng',
		                            'pos_lat', 'pos_lng','address'))[0]['fields']

	# Переформатувати дату створення оголошення у прийнятний для десериалізації формат
	created = head['created']
	if created is not None:
		head['created'] = created.isoformat()

	# Переформатувати дату завершального терміну актуальності оголошення
	# у прийнятний для десериалізації формат
	actual = head['actual']
	if actual is not None:
		head['actual'] = actual.isoformat()


	body = serializers.serialize('python', [record.body])[0]['fields']

	# Якщо оголошення призначено для продажу - підгрузити і сериалізувати цю інформацію.
	# Дана інформація не грузиться автоматично щоб уникнути потенційно-зайвих селектів.
	if record.for_sale:
		sale_terms = serializers.serialize('python', [record.sale_terms])[0]['fields']
	else:
		sale_terms = None

	# Якщо оголошення призначено для оренди - підгрузити і сериалізувати цю інформацію.
	# Дана інформація не грузиться автоматично щоб уникнути потенційно-зайвих селектів.
	if record.for_rent:
		rent_terms = serializers.serialize('python', [record.rent_terms])[0]['fields']
	else:
		rent_terms = None

	# Фото
	photos = [photo.dump() for photo in record.photos_model.objects.filter(hid = record.id)]
	if not photos:
		photos = None

	# Перелік тегів, якими позначене оголошення.
	tags = {
		tag.id: True for tag in DirTags.contains_publications(tid, [record.id])
	}

	data = {
		'head': head,
		'body': body,
		'sale_terms': sale_terms,
		'rent_terms': rent_terms,
	    'photos': photos,
	    'tags': tags,
	}
	return format_output_data(data)


def format_output_data(data):
	# maps coordinates
	head = data.get('head')
	if head is None:
		raise ValueError('@head can not be None.')

	degree_lat = head.get('degree_lat')
	degree_lng = head.get('degree_lng')
	if (degree_lat is None) or (degree_lng is None):
		coordinates = {
			'lat': None,
		    'lng': None,
		}
	else:
		segment_lat = head.get('segment_lat')
		segment_lng = head.get('segment_lng')
		if (segment_lat is None) or (segment_lng is None):
			coordinates = {
				'lat': None,
			    'lng': None,
			}
		else:
			pos_lat = head.get('pos_lat')
			pos_lng = head.get('pos_lng')
			if (pos_lat is None) or (pos_lng is None):
				coordinates = {
					'lat': None,
				    'lng': None,
				}
			else:
				coordinates = {
					'lat': str(degree_lat) + '.' + str(segment_lat) + str(pos_lat),
				    'lng': str(degree_lng) + '.' + str(segment_lng) + str(pos_lng),
				}

	del data['head']['degree_lat']
	del data['head']['degree_lng']
	del data['head']['segment_lat']
	del data['head']['segment_lng']
	del data['head']['pos_lat']
	del data['head']['pos_lng']
	data['head'].update(coordinates)


	# sale terms
	s_terms = data.get('sale_terms')
	if s_terms:
		s_price = s_terms.get('price')
		if s_price:
			if int(s_price) == s_price:
				# Якщо після коми лише нулі - повернути ціле значення
				data['sale_terms']['price'] = "%.0f" % s_price
			else:
				# Інакше - округлити до 2х знаків після коми
				data['sale_terms']['price'] = "%.2f" % s_price


	# rent terms
	r_terms = data.get('rent_terms')
	if r_terms:
		r_price = r_terms.get('price')
		if r_price:
			if int(r_price) == r_price:
				# Якщо після коми лише нулі - повернути ціле значення
				data['rent_terms']['price'] = "%.0f" % r_price
			else:
				# Інакше - округлити до 2х знаків після коми
				data['rent_terms']['price'] = "%.2f" % r_price

	return data