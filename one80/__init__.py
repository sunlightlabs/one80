import inboxinfluence
import crunchbase
import os
import pickle
import yql

from django.conf import settings
from linkedin import linkedin

def spellcheck(str):
    y = yql.Public()
    query = 'select * from microsoft.bing.spell where query="%s" and appid="%s"' % (str, settings.BING_APIKEY)
    params = {'env': "store://datatables.org/alltableswithkeys"}

    try:
        return y.execute(query, **params).rows[0]['Value']
    except:
        return str

class PersonifyError(Exception):
    pass

class Personify(object):

    first_name = ''
    last_name = ''
    middle_name = ''
    organization = ''
    title = ''
    uri = ''
    extra = {}

    def __init__(self, text=None, *args, **kwargs):
        if text is not None:
            self.personify(text)
        else:
            raise PersonifyError('You must instantiate Personify with a name: Personify("Steve Jobs")')
        super(Personify, self).__init__()

    def __repr__(self):
        return '%s(%r)' % (self.__class__.__name__, self.__dict__)

    def personify(self, text):
        try:
            self._inboxinfluence(text)
        except:
            try:
                self._crunchbase(text)
            except:
                try:
                    self._linkedin(text)
                except:
                    raise PersonifyError('No matches for %s' % text)

    def _inboxinfluence(self, text):
        ''' gets a person entity from the inbox influence API '''
        ie = inboxinfluence.inboxinfluence()
        ie.apikey = settings.SUNLIGHT_APIKEY
        data = ie.contextualize(text)
        self.first_name = data[0].entity_data['name'].split()[0]
        self.last_name = ' '.join(data[0].entity_data['name'].split()[1:])
        self.organiztion = data[0].entity_data['seat_label']

    def _crunchbase(self, text):
        ''' gets a person entity from the crunchbase API '''
        cb = crunchbase.crunchbase()
        data = cb.getPersonData(text)

        self.first_name = data.first_name
        self.last_name = data.last_name
        self.url = data.crunchbase_url
        try:
            self.organization = data.relationships[0]['firm']['name']
        except:
            pass
        try:
            self.title = data.relationships[0]['title']
        except:
            pass
        self.extra = data.__dict__

    def _linkedin(self, text):
        ''' queries Bing for the top linkedin result for a name,
            and retrieves that account by url from the linkedin API '''
        y = yql.Public()
        query = 'select * from microsoft.bing.web where query="%s site:linkedin.com" and appid="%s"' % (text, settings.BING_APIKEY)
        params = {'env': "store://datatables.org/alltableswithkeys"}
        url = y.execute(query, **params).rows[0]['DisplayUrl']
        li = linkedin.LinkedIn(settings.LINKEDIN_APIKEY, settings.LINKEDIN_API_SECRET, '')
        li.access_token = settings.LINKEDIN_ACCESS_TOKEN
        li.access_token_secret = settings.LINKEDIN_ACCESS_TOKEN_SECRET
        data = li.GetProfile(url="http://%s" % url)

        self.first_name = data.first_name
        self.last_name = data.last_name
        self.url = url
        self.extra = data.__dict__
        try:
            self.organization = data.positions[0].company
        except:
            pass
        try:
            self.title = data.positions[0].title
        except:
            pass

# Merge local settings from os.environ

try:
    from local_settings import *
except ImportError:
    if 'LOCAL_SETTINGS' in os.environ.keys():
        settings.__dict__.update(pickle.loads(os.environ['LOCAL_SETTINGS']))
