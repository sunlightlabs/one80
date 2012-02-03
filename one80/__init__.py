import yql

from django.conf import settings


def spellcheck(str):
    y = yql.Public()
    query = 'select * from microsoft.bing.spell where query="%s" and appid="%s"' % (str, settings.BING_APIKEY)
    params = {'env': "store://datatables.org/alltableswithkeys"}

    try:
        return y.execute(query, **params).rows[0]['Value']
    except:
        return str

