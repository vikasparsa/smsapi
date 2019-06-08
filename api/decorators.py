import re
import base64
from django.http import JsonResponse, HttpResponseForbidden
from models import account

def Authorization(function):
	def verify(request, *args, **kwargs):
		try:
			auth_header = request.META['HTTP_AUTHORIZATION']
			encoded_credentials = auth_header.split(' ')[1]
			decoded_credentials = base64.b64decode(encoded_credentials).decode("utf-8").split(':')
			username = decoded_credentials[0]
			password = decoded_credentials[1]
			if account.objects.filter(username=username,auth_id=password).exists():
				kwargs['account_id'] = account.objects.filter(username=username,auth_id=password).first().id
				return function(request, *args, **kwargs)
			else:
				return HttpResponseForbidden()
		except Exception as e:
			return HttpResponseForbidden()
	return verify
