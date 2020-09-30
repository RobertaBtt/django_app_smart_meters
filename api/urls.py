"""api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from protected_api.views.public_views import ApiGridStats,ApiGridAlarms, ApiOldAuth, ApiEnergia24
from protected_api.views.webapp_views import ApiRegister, ApiRegisterCheck, ApiUnregister
from protected_api.views.user_views import ApiUser, ApiAlarmSmartmeter, ApiMeasures, ApiMessages, ApiPotenze, ApiInvoice, ApiInvoiceList, ApiContracts, ApiContractStatistics
from protected_api.views.erp_views import ApiErpAlarmSmartmeter, ApiErpMeasures, ApiErpPotenze, ApiErpGridStats, ApiErpGridAlarms
from protected_api.views.erp_views import   ApiErpGetData, ApiErpScanSmartmeters, ApiErpGetSmartmeterData, ApiErpGetTransmissionsCount, ApiErpGetLastTransmission

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    url(r'^api/', include('protected_api.urls', namespace='api')),

    url(r'^grid/stats', ApiGridStats.as_view()),
    url(r'^grid/alarms', ApiGridAlarms.as_view()),

    url(r'^auth', ApiOldAuth.as_view()),
    url(r'^verify', ApiRegisterCheck.as_view()),
    url(r'^register', ApiRegister.as_view()),
    url(r'^delete', ApiUnregister.as_view()),

    url(r'^contract/energia24h', ApiEnergia24.as_view()),

    url(r'^user', ApiUser.as_view()),

    url(r'^contracts', ApiContracts.as_view()),
    url(r'^measures', ApiMeasures.as_view()),
    url(r'^alarm/sm', ApiAlarmSmartmeter.as_view()),
    url(r'^messages', ApiMessages.as_view()),
    url(r'^powers', ApiPotenze.as_view()),
    url(r'^contract_stats', ApiContractStatistics.as_view()),
    url(r'^getinvoice', ApiInvoice.as_view()),
    url(r'^invoice_list', ApiInvoiceList.as_view()),
    url(r'^erp/grid/stats', ApiErpGridStats.as_view()),
    url(r'^erp/grid/alarms', ApiErpGridAlarms.as_view()),
    url(r'^erp/measures', ApiErpMeasures.as_view()),
    url(r'^erp/alarm/sm', ApiErpAlarmSmartmeter.as_view()),
    url(r'^erp/powers', ApiErpPotenze.as_view()),
    #roby
    url(r'^erp/get_data', ApiErpGetData.as_view()), #prima query di prova, primo approccio al progetto
    url(r'^erp/smartmeters/all/$', ApiErpScanSmartmeters.as_view()),
    url(r'^erp/smartmeter/$', ApiErpGetSmartmeterData.as_view()),
    url(r'^erp/smartmeters/transmissions/count/$', ApiErpGetTransmissionsCount.as_view()),
    url(r'^erp/smartmeters/transmissions/last/$', ApiErpGetLastTransmission.as_view())

]



