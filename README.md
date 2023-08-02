django app for clients smartmeters
======================================

Raw messages from smartmeters are converted in a normalized data
inside Amazon RDS.

The module **api** inside the module **django_app_smart_meters** reads the content of the tables MySQL were read and made visible inside the Frontend of the End Users 
and inside the Django admin backend.

These data are then shown in a separate frontend for all the clients,
and only for those that had activated a smartmeter, can read the meter readings 
as provided from the backend infrastructure.

![SmartMeters_data_backend.jpg](static%2Fdoc%2FSmartMeters_data_backend.jpg)
