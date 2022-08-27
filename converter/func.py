import requests
import re


def available_currencies():
	"""
	:return: dict with available currencies to convert
	"""
	url = 'https://api.exchangerate.host/symbols'
	vldt = validate_request(url)
	if vldt[0]:
		data = vldt[1]
		for k, v in data['symbols'].items():
			if 'code' in v:
				v.pop('code')
		return data
	else:
		return 'Connection error'


def convert_currency(val_from_to: str, need_print=False):
	"""
	:param val_from_to: example: "1 USD to EUR"
	:param need_print: func print string if True
	:return: converted number (float)
	"""
	pattern = r'[\d]*\.?\d* \w* to \w*'
	vldt_input = re.search(pattern, val_from_to).group()
	if vldt_input:
		dict_currencies = available_currencies()['symbols']
		amount = float(vldt_input.split()[0])
		from_cur = vldt_input.split()[1].upper()
		to_cur = vldt_input.split()[3].upper()
		if from_cur and to_cur in dict_currencies:
			params = {'from': from_cur, 'to': to_cur, 'amount': amount}
			url = f'https://api.exchangerate.host/convert/'
			vldt = validate_request(url, params)
			if vldt[0]:
				data = vldt[1]
				converted_amount = data.get('result')
				converted_amount = round(converted_amount, 2)
				if need_print:
					print(f'{amount} {from_cur} = {converted_amount} {to_cur}')
				return converted_amount
		return 'Invalid currencies'
	return 'Invalid input'


def validate_request(url, params=None):
	response = requests.get(url, params=params)
	if response.status_code == requests.codes.ok:
		data = response.json()
		if data['success']:
			return True, data
