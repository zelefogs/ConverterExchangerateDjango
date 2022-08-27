from django.shortcuts import render
import requests
from .func import validate_request, convert_currency, available_currencies
from django.forms.forms import BaseForm

def home(request):
	if request.method == "GET":
		avlbl_cur = available_currencies()
		cur_first = 'USD'
		cur_second = 'RUB'
		return render(request, 'converter/home.html', {
			'data': avlbl_cur['symbols'],
			'help_amount': convert_currency(f'1 USD to RUB'),
			'help2_amount': convert_currency(f'1 RUB to USD'),
			'cur_first': cur_first,
			'cur_second': cur_second,
		})
	else:
		avlbl_cur = available_currencies()
		first_amount = request.POST.get('first')
		cur_first = request.POST.get('cur_first')
		cur_second = request.POST.get('cur_second')
		return render(request, 'converter/home.html', {
			'data': avlbl_cur['symbols'],
			'first_amount': first_amount,
			'cur_first': cur_first,
			'cur_second': cur_second,
			'second_amount': convert_currency(f'{first_amount} {cur_first} to {cur_second}'),
			'help_amount': convert_currency(f'1 {cur_first} to {cur_second}'),
			'help2_amount': convert_currency(f'1 {cur_second} to {cur_first}'),

		})


def validate_request(url, params=None):
	response = requests.get(url, params=params)
	if response.status_code == requests.codes.ok:
		data = response.json()
		if data['success']:
			return True, data

