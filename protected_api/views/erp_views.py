from django.http import HttpResponse, JsonResponse
from oauth2_provider.views.generic import ScopedProtectedResourceView
from protected_api.utils.smartgrid import Smartgrid
import protected_api.utils.services as services
from protected_api.utils.common import APPLICATION_TYPE_ERP
import logging


logger = logging.getLogger(__name__)
SCOPE = APPLICATION_TYPE_ERP


class ApiErpMeasures(ScopedProtectedResourceView):
    required_scopes = [SCOPE]

    def get(self, request, *args, **kwargs):
        """returns user consumption measures"""
        consumer = services.bearer_from_access_token(request.META.get('HTTP_AUTHORIZATION', None).replace('Bearer ', ''))
        if consumer.tipo != SCOPE:
            return HttpResponse(JsonResponse({'message': 'no grants for this operation', 'success':False}), status=403)

        contract_id = request.GET.get('contract_id', None)
        if contract_id is None:
            return HttpResponse(JsonResponse({'message': 'invalid parameter', 'success':False}), status=400)
        try:
            sm = Smartgrid(consumer.gestore.remote_db)

            data = sm.getMeasures(contract_id)
            return HttpResponse(JsonResponse({'data':data, 'success':True}))
        except Exception as e:
            error_message = "internal error {0} : {1}".format(str(self.__class__.__name__), str(e))
            logger.error(error_message)
            return HttpResponse(JsonResponse({'message': error_message, 'success': False}), status=500)


class ApiErpAlarmSmartmeter(ScopedProtectedResourceView):
    required_scopes = [SCOPE]

    def get(self, request, *args, **kwargs):
        """returns data if allarm are present on sm"""
        consumer = services.bearer_from_access_token(request.META.get('HTTP_AUTHORIZATION', None).replace('Bearer ', ''))
        print "consumer: ", consumer

        if consumer.tipo != SCOPE:
            return HttpResponse(JsonResponse({'message': 'no grants for this operation', 'success':False}), status=403)

        contract_id = request.GET.get('contract_id', None)
        if contract_id is None:
            return HttpResponse(JsonResponse({'message': 'invalid parameter', 'success':False}), status=400)

        try:
            sm = Smartgrid(consumer.gestore.remote_db)

            data = sm.getAlarmSmartmeter(contract_id)
            return HttpResponse(JsonResponse({'data':data, 'success':True}))
        except Exception as e:
            error_message = "internal error {0} : {1}".format(str(self.__class__.__name__), str(e))
            logger.error(error_message)
            return HttpResponse(JsonResponse({'message': error_message, 'success': False}), status=500)


class ApiErpPotenze(ScopedProtectedResourceView):
    required_scopes = [SCOPE]

    def get(self, request, *args, **kwargs):
        """returns user instant consumption"""

        consumer = services.bearer_from_access_token(request.META.get('HTTP_AUTHORIZATION', None).replace('Bearer ', ''))
        if consumer.tipo != SCOPE:
            return HttpResponse(JsonResponse({'message': 'no grants for this operation', 'success':False}), status=403)

        contract_id = request.GET.get('contract_id', None)
        if contract_id is None:
            return HttpResponse(JsonResponse({'message': 'invalid parameter', 'success':False}), status=400)
        try:
            sm = Smartgrid(consumer.gestore.remote_db)
            data = sm.getPotenze(contract_id)
            if data is None:
                return HttpResponse(JsonResponse({'message': 'contract %s not found' %str(contract_id), 'success': False}), status=404)
            else:
                return HttpResponse(JsonResponse({'data':data, 'success':True}))
        except Exception as e:
            error_message = "internal error {0} : {1}".format(str(self.__class__.__name__), str(e))
            logger.error(error_message)
            return HttpResponse(JsonResponse({'message': error_message, 'success': False}), status=500)


class ApiErpGridStats(ScopedProtectedResourceView):
    required_scopes = [SCOPE]

    def get(self, request, *args, **kwargs):
        """get smart grid total consumption/production stats"""

        consumer = services.bearer_from_access_token(request.META.get('HTTP_AUTHORIZATION', None).replace('Bearer ', ''))
        if consumer.tipo != SCOPE:
            return HttpResponse(JsonResponse({'message': 'no grants for this operation', 'success':False}), status=403)

        zone_id = request.GET.get('zone_id', default=None)
        if zone_id is None:
            return HttpResponse(JsonResponse({'message': 'invalid parameters', 'success':False}), status=400)
        
        try:
            sm = Smartgrid(consumer.gestore.remote_db)
            data = sm.getStats(zone_id)
            return HttpResponse(JsonResponse({'data':data, 'success':True}))
        except Exception as e:
            error_message = "internal error {0} : {1}".format(str(self.__class__.__name__), str(e))
            logger.error(error_message)
            return HttpResponse(JsonResponse({'message': error_message, 'success': False}), status=500)

class ApiErpGridAlarms(ScopedProtectedResourceView):
    required_scopes = [SCOPE]

    def get(self, request, *args, **kwargs):
        """get smart grid total alarms stats"""

        consumer = services.bearer_from_access_token(request.META.get('HTTP_AUTHORIZATION', None).replace('Bearer ', ''))
        print "consumer ", consumer
        print "consumer.tipo ", consumer.tipo

        if consumer.tipo != SCOPE:
            return HttpResponse(JsonResponse({'message': 'no grants for this operation', 'success':False}), status=403)

        zone_id = request.GET.get('zone_id', default=None)
        if zone_id is None:
            return HttpResponse(JsonResponse({'message': 'invalid parameters', 'success':False}), status=400)
        try:
            sm = Smartgrid(consumer.gestore.remote_db)
            data = sm.getAlarms(zone_id)
            return HttpResponse(JsonResponse({'data':data, 'success':True}))
        except Exception as e:
            error_message = "internal error {0} : {1}".format(str(self.__class__.__name__), str(e))
            logger.error(error_message)
            return HttpResponse(JsonResponse({'message': error_message, 'success': False}), status=500)

class ApiErpGetData(ScopedProtectedResourceView):

    required_scopes = [SCOPE]

    def get(self, request, *args, **kwargs):
        """returns user instant consumption"""


        consumer = services.bearer_from_access_token(request.META.get('HTTP_AUTHORIZATION', None).replace('Bearer ', ''))
        if consumer.tipo != SCOPE:
            return HttpResponse(JsonResponse({'message': 'no grants for this operation', 'success':False}), status=403)

        nome_campo_select = request.GET.get('nome_campo_select', None)
        nome_tabella = request.GET.get('nome_tabella', None)
        nome_campo_where = request.GET.get('nome_campo_where', None)
        valore_campo_where = request.GET.get('valore_campo_where', None)



        if nome_campo_select is None:
            return HttpResponse(JsonResponse({'message': 'parameter nome_campo_select not specified', 'success':False}), status=400)

        if nome_tabella is None:
            return HttpResponse(JsonResponse({'message': 'parameter nome_tabella not specified', 'success':False}), status=400)

        if nome_campo_where is None:
            return HttpResponse(JsonResponse({'message': 'parameter nome_campo_where not specified', 'success':False}), status=400)

        if valore_campo_where is None:
            return HttpResponse(JsonResponse({'message': 'parameter valore_campo_where not specified', 'success':False}), status=400)
        try:
            print "Remote db = " + consumer.gestore.remote_db
            sm = Smartgrid(consumer.gestore.remote_db)

            data = sm.getData(nome_campo_select, nome_tabella, nome_campo_where, valore_campo_where)

            if data is None:
                print "ApiErpGetData : data is None :("
                return HttpResponse(JsonResponse({'message': 'No values found' , 'success': False}), status=404)
            else:
                print "ApiErpGetData : data is not None ! :)"
                return HttpResponse(JsonResponse({'data':data, 'success':True}))
        except Exception as e:
            error_message = "internal error {0} : {1}".format(str(self.__class__.__name__), str(e))
            print "Error message:" + error_message
            if logger is None:
                print "Il logger risulta None"
            else:
                logger.error(error_message)
            return HttpResponse(JsonResponse({'message': error_message, 'success': False}), status=500)


class ApiErpScanSmartmeters(ScopedProtectedResourceView):
    required_scopes = [SCOPE]

    def get(self, request, *args, **kwargs):
        """returns user instant consumption"""

        consumer = services.bearer_from_access_token(request.META.get('HTTP_AUTHORIZATION', None).replace('Bearer ', ''))

        if consumer.tipo != SCOPE:
            return HttpResponse(JsonResponse({'message': 'no grants for this operation', 'success':False}), status=403)

        nome_tabella = request.GET.get('nome_tabella', None)

        if nome_tabella is None:
            return HttpResponse(JsonResponse({'message': 'parameter nome_tabella not specified', 'success':False}), status=400)

        try:
            print "ApiErpScanSmartmeters remote db = " + consumer.gestore.remote_db
            sm = Smartgrid(consumer.gestore.remote_db)

            data = sm.scanSmartmeters(nome_tabella)

            if data is None:
                print "Scan Smartmeter : data is None :("
                return HttpResponse(JsonResponse({'message': 'No smartmeters found' , 'success': False}), status=404)
            else:
                print "Scan Smartmeters : data is not None ! :)"
                return HttpResponse(JsonResponse({'data':data, 'success':True}))
        except Exception as e:
            error_message = "internal error {0} : {1}".format(str(self.__class__.__name__), str(e))
            print "Error message:" + error_message
            if logger is None:
                print "Il logger risulta None"
            else:
                logger.error(error_message)
            return HttpResponse(JsonResponse({'message': error_message, 'success': False}), status=500)

class ApiErpGetSmartmeterData(ScopedProtectedResourceView):
    required_scopes = [SCOPE]

    def get(self, request, *args, **kwargs):
        """returns user instant consumption"""

        consumer = services.bearer_from_access_token(request.META.get('HTTP_AUTHORIZATION', None).replace('Bearer ', ''))

        if consumer.tipo != SCOPE:
            return HttpResponse(JsonResponse({'message': 'no grants for this operation', 'success':False}), status=403)

        nome_tabella = request.GET.get('nome_tabella', None)
        sender_id = request.GET.get('sender_id', None)
        data_da = request.GET.get('data_da', None)
        data_a = request.GET.get('data_a', None)


        if nome_tabella is None:
            return HttpResponse(JsonResponse({'message': 'parameter nome_tabella not specified', 'success':False}), status=400)

        try:
            print "ApiErpGetSmartmeterData remote db = " + consumer.gestore.remote_db
            sm = Smartgrid(consumer.gestore.remote_db)

            print "data_da:", data_da
            print "data_a:", data_a

            data = sm.getSmartmeterData(sender_id, nome_tabella, data_da, data_a)


            if data is None:
                print "Not data found for smartmeter", sender_id
                return HttpResponse(JsonResponse({'message': 'No smartmeters found' , 'success': False}), status=404)
            else:
                print "Found data for smartmeter", sender_id
                return HttpResponse(JsonResponse({'data':data, 'success':True}))

        except Exception as e:
            error_message = "internal error {0} : {1}".format(str(self.__class__.__name__), str(e))
            print "Error message for get smartmeter data :" + error_message
            if logger is None:
                print "Il logger risulta None"
            else:
                logger.error(error_message)
            return HttpResponse(JsonResponse({'message': error_message, 'success': False}), status=500)


class ApiErpGetTransmissionsCount(ScopedProtectedResourceView):
    required_scopes = [SCOPE]

    def get(self, request, *args, **kwargs):
        """returns user instant consumption"""

        consumer = services.bearer_from_access_token(request.META.get('HTTP_AUTHORIZATION', None).replace('Bearer ', ''))

        if consumer.tipo != SCOPE:
            return HttpResponse(JsonResponse({'message': 'no grants for this operation', 'success':False}), status=403)

        nome_tabella = request.GET.get('nome_tabella', None)
        data_da = request.GET.get('data_da', None)
        data_a = request.GET.get('data_a', None)


        if nome_tabella is None:
            return HttpResponse(JsonResponse({'message': 'parameter nome_tabella not specified', 'success':False}), status=400)

        try:
            print "ApiErpGetTransmissionsCount remote db = " + consumer.gestore.remote_db
            sm = Smartgrid(consumer.gestore.remote_db)

            print "data_da:", data_da
            print "data_a:", data_a

            data = sm.getTransmissionsCount(nome_tabella, data_da, data_a)


            if data is None:
                print "Not data found for getTransmissionsCount",
                return HttpResponse(JsonResponse({'message': 'No data found' , 'success': False}), status=404)
            else:
                print "Found data for getTransmissionsCount",
                return HttpResponse(JsonResponse({'data':data, 'success':True}))

        except Exception as e:
            error_message = "internal error {0} : {1}".format(str(self.__class__.__name__), str(e))
            print "Error message for getTransmissionsCount:" + error_message
            if logger is None:
                print "Il logger risulta None"
            else:
                logger.error(error_message)
            return HttpResponse(JsonResponse({'message': error_message, 'success': False}), status=500)


class ApiErpGetLastTransmission(ScopedProtectedResourceView):
    required_scopes = [SCOPE]

    def get(self, request, *args, **kwargs):
        """returns user instant consumption"""

        consumer = services.bearer_from_access_token(request.META.get('HTTP_AUTHORIZATION', None).replace('Bearer ', ''))

        if consumer.tipo != SCOPE:
            return HttpResponse(JsonResponse({'message': 'no grants for this operation', 'success':False}), status=403)

        nome_tabella = request.GET.get('nome_tabella', None)
        sender_id = request.GET.get('sender_id', None)


        if nome_tabella is None:
            return HttpResponse(JsonResponse({'message': 'parameter nome_tabella not specified', 'success':False}), status=400)

        try:
            print "ApiErpGetLastTransmission remote db = " + consumer.gestore.remote_db
            sm = Smartgrid(consumer.gestore.remote_db)

            data = sm.getLastTransmission(sender_id, nome_tabella)


            if data is None:
                print "Not data found for last transmission of smartmeter: ", sender_id
                return HttpResponse(JsonResponse({'message': 'No smartmeters found' , 'success': False}), status=404)
            else:
                print "Found data for last transmission of smartmeter: ", sender_id
                return HttpResponse(JsonResponse({'data':data, 'success':True}))

        except Exception as e:
            error_message = "internal error {0} : {1}".format(str(self.__class__.__name__), str(e))
            print "Error message for getLastTransmission :" + error_message
            if logger is None:
                print "Il logger risulta None"
            else:
                logger.error(error_message)
            return HttpResponse(JsonResponse({'message': error_message, 'success': False}), status=500)
