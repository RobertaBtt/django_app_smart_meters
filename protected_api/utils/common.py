
def decimal_default(obj):
    import decimal
    if isinstance(obj, decimal.Decimal):
        return float(obj)
    raise TypeError

def getProjectDir():
    import os.path
    import manage
    return os.path.dirname(manage.__file__) + '/'


APPLICATION_TYPE_USER = 'user'
APPLICATION_TYPE_WEBAPP = 'webapp'
APPLICATION_TYPE_ERP = 'erp'
