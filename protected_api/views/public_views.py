from django.http import HttpResponse, JsonResponse
from django.views.generic.base import View
from protected_api.utils.smartgrid import Smartgrid
import protected_api.utils.old_auth as old_auth
import random
import datetime
import logging

logger = logging.getLogger(__name__)


class ApiGridStats(View):
    def get(self, request, *args, **kwargs):
        """get smart grid total consumption/production stats"""
        token = request.GET.get('token', default=None)
        zone_id = request.GET.get('zone_id', default=None)
        remote_db = request.GET.get('remote_db', default='')
        if token is None or zone_id is None:
            return HttpResponse(JsonResponse({'message': 'invalid parameters'}), status=400)
        elif not old_auth.check_token(token):
            return HttpResponse(JsonResponse({'message': 'invalid or expired token'}), status=401)

        try:
            sm = Smartgrid(remote_db)
            data = sm.getStats(zone_id)
            return HttpResponse(JsonResponse(data))
        except Exception as e:
            logger.error("{0} : {1}".format(str(self.__class__.__name__), str(e)))
            return HttpResponse(JsonResponse({'message': 'internal error %s' % str(e) }), status=500)

class ApiGridAlarms(View):
    def get(self, request, *args, **kwargs):
        """get smart grid total alarms stats"""
        token = request.GET.get('token', default=None)
        zone_id = request.GET.get('zone_id', default=None)
        remote_db = request.GET.get('remote_db', default='')
        if token is None or zone_id is None:
            return HttpResponse(JsonResponse({'message': 'invalid parameters'}), status=400)
        elif not old_auth.check_token(token):
            return HttpResponse(JsonResponse({'message': 'invalid or expired token'}), status=401)

        try:
            sm = Smartgrid(remote_db)
            data = sm.getAlarms(zone_id)
            return HttpResponse(JsonResponse(data))
        except Exception as e:
            logger.error("{0} : {1}".format(str(self.__class__.__name__), str(e)))
            return HttpResponse(JsonResponse({'message': 'internal error %s' % str(e) }), status=500)



class ApiOldAuth(View):
    def get(self, request, *args, **kwargs):
        """authenticate an application via api_key and secret_key"""
        api_key = request.GET.get('api_key', default=None)
        secret_key = request.GET.get('secret_key', default=None)
        if api_key is None or secret_key is None:
            return HttpResponse(JsonResponse({'message': 'invalid parameters'}), status=400)
        else:
            token = old_auth.create_token(api_key, secret_key)
            if token is None:
                return HttpResponse(JsonResponse({'message': 'invalid app_key/secret_key pair'}), status=401)
            else:
                return HttpResponse(JsonResponse({'token':token}))


class ApiEnergia24(View):

    def get(self, request, *args, **kwargs):
        """returns user specific messages"""

        token = request.GET.get('token', default=None)
        contract_id = request.GET.get('contract_id', None)

        if token is None or contract_id is None:
            return HttpResponse(JsonResponse({'message': 'invalid parameter', 'success': False}), status=400)
        elif not old_auth.check_token(token):
            return HttpResponse(JsonResponse({'message': 'invalid or expired token', 'success': False}), status=401)

        label = random.choice(('energia_prelevata', 'energia_immessa'))
        now = datetime.datetime.now().replace(minute=0, second=0, microsecond=0)
        data = {}

        for i in range(1, 25):
            hour = {
                'timestamp': (now - datetime.timedelta(hours=25-i)).isoformat(),
                label : random.randint(1, 150)
            }

            data['timestamp_%d' % i] = hour

        if data is None:
            return HttpResponse(JsonResponse({'message': 'cannot retrieve data for contract %s' % str(contract_id)}), status=500)
        else:
            return HttpResponse(JsonResponse({'data':data, 'success':True}))

