import json
import re
import sys

from more_itertools import first, intersperse

from CLIppy import convert_date, dedupe, fail_gracefully, flatten, pprint_header_with_lines, soup_me


@fail_gracefully
def get_dishes(date='today', joinstr='    ~',
               stations=('Home', 'Stockpot', 'rotating')):

    date_str = convert_date(date) # str -> datetime

    BASE_URL = 'https://mit.cafebonappetit.com/cafe/koch-cafe/{}'.format(
        date_str)

    print('Reading the menu...')
    soup = soup_me(BASE_URL)

    KEY = "Bamco.menu_items"

    try:
        script = first((sc.text for sc in soup.find_all('script')
                        if any((l.startswith(KEY) for l in sc.text.split()))))

        messymenujsonstr = first((l for l in script.split('\n')
                                  if l.strip().startswith(KEY)))

    except(ValueError): # no menu items found
        return []

    menujsonstr = re.sub(';\s*$', '',                           # strip trailing ;
                         re.sub('\s*{}\s*=\s*'.format(KEY), '', # strip `KEY = `
                                messymenujsonstr))
    menujson = json.loads(menujsonstr)

    dishes = flatten(intersperse(
        (joinstr,), ((dish['label'] for dish in menujson.values()
                      if station in dish['station'])
                     for station in stations)))

    #return dedupe(dishes)
    return dishes


if __name__ == '__main__':
    kwargs = {}
    try:
        kwargs['date'] = sys.argv[1]
    except(IndexError):
        pass # default to today

    header = 'How about'
    food = get_dishes(**kwargs)

    if food:
        print(); pprint_header_with_lines(header, food); print()
        #print(); print('__How about__'); print('\n'.join(food)); print()
    else:
        print('...nothing on the menu')
