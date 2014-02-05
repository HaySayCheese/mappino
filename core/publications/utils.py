#coding=utf-8
from django.core import serializers


def publication_data(record):
	#-- head
	head = serializers.serialize('python', [record], fields=(
		'created', 'actual', 'for_rent', 'for_sale', 'state_sid',
		'degree_lat', 'degree_lng', 'segment_lat', 'segment_lng', 'pos_lat', 'pos_lng',
		'address'))[0]['fields']

	created_dt = head['created']
	if created_dt is not None:
		head['created'] = created_dt.isoformat()

	actual_dt = head['actual']
	if actual_dt is not None:
		head['actual'] = actual_dt.isoformat()

	#-- body
	body = serializers.serialize('python', [record.body])[0]['fields']

	#-- for sale
	if record.for_sale:
		sale_terms = serializers.serialize('python', [record.sale_terms])[0]['fields']
	else:
		sale_terms = None

	#-- for sale
	if record.for_sale:
		rent_terms = serializers.serialize('python', [record.rent_terms])[0]['fields']
	else:
		rent_terms = None

	data = {
		'head': head,
		'body': body,
		'sale_terms': sale_terms,
		'rent_terms': rent_terms,
	}
	return __format_output_data(data)


def __format_output_data(data):
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