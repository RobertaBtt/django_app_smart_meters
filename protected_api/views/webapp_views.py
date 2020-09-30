from django.http import HttpResponse, JsonResponse
from oauth2_provider.views.generic import ScopedProtectedResourceView
from protected_api.utils.smartgrid import Smartgrid
import protected_api.utils.services as services
from protected_api.utils.common import APPLICATION_TYPE_WEBAPP
import logging

logger = logging.getLogger(__name__)
SCOPE = APPLICATION_TYPE_WEBAPP


class ApiRegisterCheck(ScopedProtectedResourceView):
    required_scopes = [SCOPE]

    def get(self, request, *args, **kwargs):
        consumer = services.bearer_from_access_token(request.META.get('HTTP_AUTHORIZATION', None).replace('Bearer ', ''))
        if consumer.tipo != SCOPE:
            return HttpResponse(JsonResponse({'message': 'no grants for this operation', 'success':False}), status=403)

        fiscal_sn = request.GET.get('fiscal_sn', None)
        verification_code = request.GET.get('verification_code', None)

        if fiscal_sn is None or verification_code is None:
            return HttpResponse(JsonResponse({'message': 'invalid parameters', 'success':False}), status=400)

        try:
            #l'utente corrente = l'applicazione consumer
            sm = Smartgrid(consumer.gestore.remote_db)
            user_id = sm.getUserId(fiscal_sn, verification_code) #codice univoco solo entro il db del gestore

            if user_id is None:
                return HttpResponse(JsonResponse({'message': 'parameter mismatch', 'success':False}), status=404)
            else:
                already_registered = services.is_already_registered(user_id, consumer.gestore.id)
                if already_registered:
                    return HttpResponse(JsonResponse({'message': 'already registered', 'success':False}), status=405)
                else:
                    return HttpResponse(JsonResponse({'check':True, 'success':True}))
        except Exception as e:
            error_message = "internal error {0} : {1}".format(str(self.__class__.__name__), str(e))
            logger.error(error_message)
            return HttpResponse(JsonResponse({'message': error_message, 'success': False}), status=500)


class ApiRegister(ScopedProtectedResourceView):
    required_scopes = [SCOPE]

    def get(self, request, *args, **kwargs):
        consumer = services.bearer_from_access_token(request.META.get('HTTP_AUTHORIZATION', None).replace('Bearer ', ''))
        if consumer.tipo != SCOPE:
            return HttpResponse(JsonResponse({'message': 'no grants for this operation', 'success':False}), status=403)

        fiscal_sn = request.GET.get('fiscal_sn', None)
        verification_code = request.GET.get('verification_code', None)

        if fiscal_sn is None or verification_code is None:
            return HttpResponse(JsonResponse({'message': 'invalid parameters', 'success':False}), status=400)

        try:
            # l'utente corrente = l'applicazione consumer
            sm = Smartgrid(consumer.gestore.remote_db)

            user_id = sm.getUserId(fiscal_sn, verification_code) # codice univoco solo entro il db del gestore

            if user_id is None:
                return HttpResponse(JsonResponse({'message': 'parameter mismatch', 'success':False}), status=404)
            else:
                # crea  l'applicazione
                id_cliente = '' + str(consumer.gestore.name) + '-' + str(user_id) + '-' + str(fiscal_sn)
                application = services.create_application(fiscal_sn, user_id, consumer.gestore.name, id_cliente)

                if application is None:
                    return HttpResponse(JsonResponse({'message': 'cannot register user', 'success':False}), status=405)
                else:
                    data = {'user_id':user_id, 'client_id':application.client_id, 'client_secret':application.client_secret}
                    return HttpResponse(JsonResponse({'data':data, 'success':True}))
        except Exception as e:
            error_message = "internal error {0} : {1}".format(str(self.__class__.__name__), str(e))
            logger.error(error_message)
            return HttpResponse(JsonResponse({'message': error_message, 'success': False}), status=500)


class ApiUnregister(ScopedProtectedResourceView):
    required_scopes = [SCOPE]

    def get(self, request, *args, **kwargs):
        consumer = services.bearer_from_access_token(request.META.get('HTTP_AUTHORIZATION', None).replace('Bearer ', ''))
        if consumer.tipo != SCOPE:
            return HttpResponse(JsonResponse({'message': 'no grants for this operation', 'success':False}), status=403)

        client_id = request.GET.get('client_id', None)
        sm_user_id = request.GET.get('user_id', None)

        try:
            if sm_user_id is None or client_id is None:
                return HttpResponse(JsonResponse({'message': 'invalid parameters', 'success':False}), status=400)

            if not services.deleteApplication(client_id, sm_user_id):
                return HttpResponse(JsonResponse({'message': 'parameter mismatch', 'success':False}), status=404)
            else:
                return HttpResponse(JsonResponse({'message': 'user unregistered', 'success':True}))
        except Exception as e:
            error_message = "internal error {0} : {1}".format(str(self.__class__.__name__), str(e))
            logger.error(error_message)
            return HttpResponse(JsonResponse({'message': error_message, 'success': False}), status=500)



