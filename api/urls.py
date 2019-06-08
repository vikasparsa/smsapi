from django.conf.urls import include, url
from views import InBoundSMS, OutBoundSMS

urlpatterns = [
    url(r'^inbound/sms/', InBoundSMS.as_view(), name='in_bound_sms'),
    url(r'^outbound/sms/', OutBoundSMS.as_view(), name='out_bound_sms'),
]
