from django.http import HttpResponse, JsonResponse, FileResponse
from oauth2_provider.views.generic import ScopedProtectedResourceView
from protected_api.utils.smartgrid import Smartgrid
import protected_api.utils.services as services
from protected_api.utils.common import APPLICATION_TYPE_USER, getProjectDir
import logging

SCOPE = APPLICATION_TYPE_USER
logger = logging.getLogger(__name__)

class ApiUser(ScopedProtectedResourceView):
    required_scopes = [SCOPE]

    def get(self, request, *args, **kwargs):
        """return user info"""
        consumer = services.bearer_from_access_token(request.META.get('HTTP_AUTHORIZATION', None).replace('Bearer ', ''))
        if consumer.tipo != SCOPE:
            return HttpResponse(JsonResponse({'message': 'no grants for this operation', 'success':False}), status=403)

        try:
            sm = Smartgrid(consumer.gestore.remote_db)
            user_id = consumer.smartgrid_client_id
            data = sm.getUser(user_id)
            if data is None:
                return HttpResponse(JsonResponse({'message': 'no such user: %d' %int(user_id), 'success': False}), status=404)
            else:
                return HttpResponse(JsonResponse({'data':data, 'success':True}))
        except Exception as e:
            error_message = "internal error {0} : {1}".format(str(self.__class__.__name__), str(e))
            logger.error(error_message)
            return HttpResponse(JsonResponse({'message': error_message, 'success': False}), status=500)


class ApiContracts(ScopedProtectedResourceView):
    required_scopes = [SCOPE]

    def get(self, request, *args, **kwargs):
        """returns user's contracts info"""
        consumer = services.bearer_from_access_token(request.META.get('HTTP_AUTHORIZATION', None).replace('Bearer ', ''))
        if consumer.tipo != SCOPE:
            return HttpResponse(JsonResponse({'message': 'no grants for this operation', 'success':False}), status=403)

        try:
            sm = Smartgrid(consumer.gestore.remote_db)
            user_id = consumer.smartgrid_client_id
            data = sm.getContracts(user_id)
            if data is None:
                return HttpResponse(JsonResponse({'message': 'no contracts for user: %d' %int(user_id), 'success': False}), status=404)
            else:
                return HttpResponse(JsonResponse({'data':data, 'success':True}))
        except Exception as e:
            error_message = "internal error {0} : {1}".format(str(self.__class__.__name__), str(e))
            logger.error(error_message)
            return HttpResponse(JsonResponse({'message': error_message, 'success': False}), status=500)


class ApiMeasures(ScopedProtectedResourceView):
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

            if not sm.checkContract(contract_id, consumer.smartgrid_client_id):
                return HttpResponse(JsonResponse({'message': 'no grants for this operation', 'success':False}), status=403)

            data = sm.getMeasures(contract_id)
            return HttpResponse(JsonResponse({'data':data, 'success':True}))
        except Exception as e:
            error_message = "internal error {0} : {1}".format(str(self.__class__.__name__), str(e))
            logger.error(error_message)
            return HttpResponse(JsonResponse({'message': error_message, 'success': False}), status=500)


class ApiAlarmSmartmeter(ScopedProtectedResourceView):
    required_scopes = [SCOPE]

    def get(self, request, *args, **kwargs):
        """returns data if allarm are present on sm"""
        consumer = services.bearer_from_access_token(request.META.get('HTTP_AUTHORIZATION', None).replace('Bearer ', ''))
        if consumer.tipo != SCOPE:
            return HttpResponse(JsonResponse({'message': 'no grants for this operation', 'success':False}), status=403)

        contract_id = request.GET.get('contract_id', None)
        if contract_id is None:
            return HttpResponse(JsonResponse({'message': 'invalid parameter', 'success':False}), status=400)

        try:
            sm = Smartgrid(consumer.gestore.remote_db)

            if not sm.checkContract(contract_id, consumer.smartgrid_client_id):
                return HttpResponse(JsonResponse({'message': 'no grants for this operation', 'success':False}), status=403)

            data = sm.getAlarmSmartmeter(contract_id)
            return HttpResponse(JsonResponse({'data':data, 'success':True}))
        except Exception as e:
            error_message = "internal error {0} : {1}".format(str(self.__class__.__name__), str(e))
            logger.error(error_message)
            return HttpResponse(JsonResponse({'message': error_message, 'success': False}), status=500)


class ApiMessages(ScopedProtectedResourceView):
    required_scopes = [SCOPE]

    def get(self, request, *args, **kwargs):
        """returns user specific messages"""

        consumer = services.bearer_from_access_token(request.META.get('HTTP_AUTHORIZATION', None).replace('Bearer ', ''))
        if consumer.tipo != SCOPE:
            return HttpResponse(JsonResponse({'message': 'no grants for this operation', 'success': False}), status=403)
        try:
            sm = Smartgrid(consumer.gestore.remote_db)
            user_id = consumer.smartgrid_client_id
            data = sm.getMessages(user_id)
            if data is None:
                return HttpResponse(JsonResponse({'message': 'no messages for user: %d' % int(user_id), 'success': False}), status=404)
            else:
                return HttpResponse(JsonResponse({'data': data, 'success': True}))
        except Exception as e:
            error_message = "internal error {0} : {1}".format(str(self.__class__.__name__), str(e))
            logger.error(error_message)
            return HttpResponse(JsonResponse({'message': error_message, 'success': False}), status=500)



class ApiPotenze(ScopedProtectedResourceView):
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

            if not sm.checkContract(contract_id, consumer.smartgrid_client_id):
                return HttpResponse(JsonResponse({'message': 'no grants for this operation', 'success':False}), status=403)

            data = sm.getPotenze(contract_id)
            if data is None:
                return HttpResponse(JsonResponse({'message': 'contract %s not found' %str(contract_id), 'success': False}), status=404)
            else:
                return HttpResponse(JsonResponse({'data':data, 'success':True}))
        except Exception as e:
            error_message = "internal error {0} : {1}".format(str(self.__class__.__name__), str(e))
            logger.error(error_message)
            return HttpResponse(JsonResponse({'message': error_message, 'success': False}), status=500)


class ApiInvoice(ScopedProtectedResourceView):
    required_scopes = [SCOPE]

    def get(self, request, *args, **kwargs):
        """returns an user invoice file"""

        consumer = services.bearer_from_access_token(request.META.get('HTTP_AUTHORIZATION', None).replace('Bearer ', ''))
        if consumer.tipo != SCOPE:
            return HttpResponse(JsonResponse({'message': 'no grants for this operation', 'success':False}), status=403)

        contract_id = request.GET.get('contract_id', None)
        invoice_id = request.GET.get('invoice_id', None)

        if contract_id is None or invoice_id is None:
            return HttpResponse(JsonResponse({'message': 'invalid parameters', 'success':False}), status=400)

        try:
            sm = Smartgrid(consumer.gestore.remote_db)

            if not sm.checkContract(contract_id, consumer.smartgrid_client_id):
                return HttpResponse(JsonResponse({'message': 'no grants for this operation', 'success':False}), status=403)

            fileName = sm.getInvoiceFileName(contract_id, invoice_id)

            if fileName is None:
                return HttpResponse(JsonResponse({'message': 'invoice %s for contract %s not found' % ((str(invoice_id)), str(contract_id)), 'success':False}), status=404)
            else:
                from protected_api.utils.s3Bucket import S3Bucket
                s3_file_name = 'prod/{file_name}'.format(file_name=fileName)
                bucket = S3Bucket(consumer.gestore.remote_db)
                response = FileResponse(bucket.getFileAsString(s3_file_name), content_type='application/pdf')
                response['Content-Disposition'] = 'attachment; filename="fattura.pdf"'
                return HttpResponse(response)
        except Exception as e:
            error_message = "internal error {0} : {1}".format(str(self.__class__.__name__), str(e))
            logger.error(error_message)
            return HttpResponse(JsonResponse({'message': error_message, 'success': False}), status=500)


class ApiInvoiceList(ScopedProtectedResourceView):
    required_scopes = [SCOPE]

    def get(self, request, *args, **kwargs):
        """returns user specific invoice list"""

        consumer = services.bearer_from_access_token(request.META.get('HTTP_AUTHORIZATION', None).replace('Bearer ', ''))
        if consumer.tipo != SCOPE:
            return HttpResponse(JsonResponse({'message': 'no grants for this operation', 'success': False}), status=403)

        contract_id = request.GET.get('contract_id', None)
        if contract_id is None:
            return HttpResponse(JsonResponse({'message': 'invalid parameter', 'success': False}), status=400)

        try:
            sm = Smartgrid(consumer.gestore.remote_db)

            if not sm.checkContract(contract_id, consumer.smartgrid_client_id):
                return HttpResponse(JsonResponse({'message': 'no grants for this operation', 'success':False}), status=403)

            data = sm.getInvoiceList(contract_id)
            if data is None:
                return HttpResponse(JsonResponse({'message': 'contract %s not found' % str(contract_id), 'success': False}), status=404)
            else:
                return HttpResponse(JsonResponse({'data':data, 'success':True}))
        except Exception as e:
            error_message = "internal error {0} : {1}".format(str(self.__class__.__name__), str(e))
            logger.error(error_message)
            return HttpResponse(JsonResponse({'message': error_message, 'success': False}), status=500)


class ApiContractStatistics(ScopedProtectedResourceView):
    required_scopes = [SCOPE]

    def get(self, request, *args, **kwargs):
        """returns user monthly consumption statistics"""

        consumer = services.bearer_from_access_token(request.META.get('HTTP_AUTHORIZATION', None).replace('Bearer ', ''))
        if consumer.tipo != SCOPE:
            return HttpResponse(JsonResponse({'message': 'no grants for this operation', 'success':False}), status=403)

        contract_id = request.GET.get('contract_id', None)
        if contract_id is None:
            return HttpResponse(JsonResponse({'message': 'invalid parameter', 'success':False}), status=400)
        try:
            sm = Smartgrid(consumer.gestore.remote_db)

            if not sm.checkContract(contract_id, consumer.smartgrid_client_id):
                return HttpResponse(JsonResponse({'message': 'no grants for this operation', 'success':False}), status=403)

            data = sm.getContractStatistics(contract_id)
            if data is None:
                return HttpResponse(JsonResponse({'message': 'contract %s not found' %str(contract_id), 'success': False}), status=404)
            else:
                return HttpResponse(JsonResponse({'data':data, 'success':True}))
        except Exception as e:
            error_message = "internal error {0} : {1}".format(str(self.__class__.__name__), str(e))
            logger.error(error_message)
            return HttpResponse(JsonResponse({'message': error_message, 'success': False}), status=500)


