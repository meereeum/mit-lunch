from collections import OrderedDict
from datetime import datetime, timedelta
import requests
import sys

from bs4 import BeautifulSoup
from dateutil import parser


def get_dishes(date='today', menu='Classic Cuisine'):
    date = convert_date(date) # str -> datetime
    date_str = date.strftime('%Y-%m-%d')

    BASE_URL = 'http://mit.campusdish.com/Commerce/Catalog/Menus.aspx'
    PARAMS = [('LocationId', '4932'), # Koch cafe
              ('PeriodId', '1440'), # lunch
              ('MenuDate', date_str),
              ('Mode', 'day')]

    print('Reading the menu...')
    soup = BeautifulSoup(requests.get(BASE_URL, PARAMS).content, 'lxml')

    dishes = [dish.string for section in soup('div', class_='menu-details-station')
              for dish in section('a', rel='prettyPhotoiFrameWithoutNavigation')
              if section.h2.string == menu]

    return dedupe(dishes)

# via https://stackoverflow.com/questions/6197409/ordered-sets-python-2-7
def dedupe(lst):
    """list -> deduped iterable of items, in order"""
    return OrderedDict((item, None) for item in lst).keys()

def convert_date(date_in):
    """Convert string to `datetime`"""
    D_CONVERSIONS = {
        'today': datetime.now(),
        'tomorrow': datetime.now() + timedelta(days=1),
        'tom': datetime.now() + timedelta(days=1),
        'mon': 'monday',
        'tues': 'tuesday',
        'wed': 'wednesday',
        'thurs': 'thursday',
        'fri': 'friday'
    }

    try: # if abbrev, uncompress for parser
        date_out = D_CONVERSIONS[date_in]
    except(KeyError):
        date_out = date_in

    try: # if str, convert to datetime
        date_out = parser.parse(date_out)
    except(AttributeError, TypeError):
        date_out = date_out
    except(ValueError):
        print("I don't recognize that date.. try again ?")
        sys.exit(0)

    return date_out

if __name__ == '__main__':
    kwargs = {}
    try:
        kwargs['date'] = sys.argv[1]
    except(IndexError):
        pass # default to today

    food = get_dishes(**kwargs)
    print(''); print('__How about__'); print('\n'.join(food)); print('')
