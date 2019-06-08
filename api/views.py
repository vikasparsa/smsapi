from django.views.generic import View
from django.http import JsonResponse
import json
import time
import arrow
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from decorators import Authorization
from django.core.cache import cache
from models import phone_number
import logging

logger = logging.getLogger('api')

class InBoundSMS(View):
    @csrf_exempt
    def dispatch(self, *args, **kwargs):
        return super(InBoundSMS, self).dispatch(*args, **kwargs)

    @method_decorator(Authorization)
    def post(self, request, *args, **kwargs):
        try:
            post_data = json.loads(request.body)
            from_ = post_data.get('from',None)
            to = post_data.get('to',None)
            text = post_data.get('text',None)
            if from_ is None:
                return JsonResponse({"message": "", "error": "from is missing"})
            if to is None:
                return JsonResponse({"message": "", "error": "to is missing"})
            if text is None:
                return JsonResponse({"message": "", "error": "text is missing"})
            if type(from_).__name__ != 'unicode':
                return JsonResponse({"message": "", "error": "from is invalid"})
            else:
                from_ = str(from_)
                from_length = len(from_)
                if from_length < 6 or from_length > 16:
                    return JsonResponse({"message": "", "error": "from is invalid"})
            if type(to).__name__ != 'unicode':
                return JsonResponse({"message": "", "error": "to is invalid"})
            else:
                to = str(to)
                to_length = len(to)
                if to_length < 6 or to_length > 16:
                    return JsonResponse({"message": "", "error": "to is invalid"})
            if type(text).__name__ != 'unicode':
                return JsonResponse({"message": "", "error": "text is invalid"})
            else:
                text = str(text)
                text_length = len(text)
                if text_length < 1 or text_length > 120:
                    return JsonResponse({"message": "", "error": "text is invalid"})
            account_id = kwargs['account_id']
            if not phone_number.objects.filter(account_id=account_id,number=to).exists():
                return JsonResponse({"message": "", "error": "to parameter not found"})
            if text in ['STOP','STOP\n','STOP\r','STOP\r\n']:
                key = from_ + to
                cache.set(key,key,14400)
            return JsonResponse({"message": "inbound sms ok", "error": ""})
        except Exception as e:
            logger.exception('Error while processing in bound sms')
            return JsonResponse({"message": "", "error": "unknown failure"}, status=500)

class OutBoundSMS(View):
    @csrf_exempt
    def dispatch(self, *args, **kwargs):
        return super(OutBoundSMS, self).dispatch(*args, **kwargs)

    @method_decorator(Authorization)
    def post(self, request, *args, **kwargs):
        try:
            post_data = json.loads(request.body)
            from_ = post_data.get('from',None)
            to = post_data.get('to',None)
            text = post_data.get('text',None)
            if from_ is None:
                return JsonResponse({"message": "", "error": "from is missing"})
            if to is None:
                return JsonResponse({"message": "", "error": "to is missing"})
            if text is None:
                return JsonResponse({"message": "", "error": "text is missing"})
            if type(from_).__name__ != 'unicode':
                return JsonResponse({"message": "", "error": "from is invalid"})
            else:
                from_ = str(from_)
                from_length = len(from_)
                if from_length < 6 or from_length > 16:
                    return JsonResponse({"message": "", "error": "from is invalid"})
            if type(to).__name__ != 'unicode':
                return JsonResponse({"message": "", "error": "to is invalid"})
            else:
                to = str(to)
                to_length = len(to)
                if to_length < 6 or to_length > 16:
                    return JsonResponse({"message": "", "error": "to is invalid"})
            if type(text).__name__ != 'unicode':
                return JsonResponse({"message": "", "error": "text is invalid"})
            else:
                text = str(text)
                text_length = len(text)
                if text_length < 1 or text_length > 120:
                    return JsonResponse({"message": "", "error": "text is invalid"})
            key = from_ + to
            if cache.get(key):
                return JsonResponse({"message": "", "error": "sms from {} to {} blocked by STOP request".format(from_,to)})
            if cache.get(from_):
                number_cache_details = cache.get(from_)
                number_of_calls = number_cache_details.get('count')
                expires_at = number_cache_details.get('expires_at')
                if expires_at and arrow.utcnow().timestamp > number_cache_details.get('expires_at'):
                    cache.delete(from_)
                    number_of_calls = 0
                if number_of_calls>50:
                    return JsonResponse({"message": "", "error": "limit reached for from {}".format(from_)})
                cache.set(from_,{'count':number_of_calls+1,'expires_at':expires_at})
            else:
                cache.set(from_,{'count':1,'expires_at':arrow.utcnow().replace(days=+1).timestamp})
            account_id = kwargs['account_id']
            if not phone_number.objects.filter(account_id=account_id,number=from_).exists():
                return JsonResponse({"message": "", "error": "from parameter not found"})
            return JsonResponse({"message": "outbound sms ok", "error": ""})
        except Exception as e:
            logger.exception('Error while processing out bound sms')
            return JsonResponse({"message": "", "error": "unknown failure"}, status=500)
