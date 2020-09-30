from ..models import Application, Gestore
from django.contrib.auth.models import User
from django.db.utils import IntegrityError
from oauth2_provider.models import AccessToken
from protected_api.utils.common import APPLICATION_TYPE_USER


def is_already_registered(smartgrid_client_id, id_gestore):
    """

    :param smartgrid_client_id:
    :return:
    """
    result = Application.objects.filter(smartgrid_client_id=smartgrid_client_id, gestore_id=id_gestore)
    return (len(result) > 0)

def create_application(nome_univoco, smartgrid_client_id, nome_gestore, client_id=None, tipo=0):
    """
    creates an application
    :param nome_univoco: name of the application
    :type nome_univoco: str
    :param nome_gestore:
    :type nome_gestore: str
    :param client_id: client id if needed. If none is provided a random value will be used
    :type client_id: str
    :return: returns the application. None is returned in case a duplicate is found
    :rtype: Application
    """
    utente_django = User.objects.get(username='api')
    gestore = Gestore.objects.get(name = nome_gestore)
    tipo = APPLICATION_TYPE_USER

    if not Application.objects.filter(name=nome_univoco):
        try:
            if client_id is None:
                application = Application(gestore=gestore, smartgrid_client_id=smartgrid_client_id, tipo=tipo, name=nome_univoco, authorization_grant_type='client-credentials', client_type='confidential', user=utente_django)
            else:
                application = Application(gestore=gestore, smartgrid_client_id=smartgrid_client_id, tipo=tipo, name=nome_univoco, authorization_grant_type='client-credentials', client_type='confidential', user=utente_django, client_id=client_id)
            application.save()
            return application
        except IntegrityError:
            return None


def bearer_from_access_token(bearer_token):
    """
    returns the bearer object give the access token
    :param bearer_token: the token used to access a resource
    :type bearer_token: str
    :return: the application that made the request
    :rtype: Application
    """
    if bearer_token is None:
        return None
    token = AccessToken.objects.get(token = bearer_token)
    return token.application


def deleteApplication(client_id, smartgrid_client_id):
    application = Application.objects.filter(smartgrid_client_id=smartgrid_client_id, client_id=client_id)[0]
    if application is None:
        return False
    application.delete()
    return True