import sys

from CLIppy import convert_date, dedupe, pprint_header_with_lines, soup_me


def get_dishes(date='today', menu='Classic Cuisine'):
    date_str = convert_date(date) # str -> datetime

    BASE_URL = 'http://mit.campusdish.com/Commerce/Catalog/Menus.aspx'
    PARAMS = [('LocationId', '4932'), # Koch cafe
              ('PeriodId', '1440'), # lunch
              ('MenuDate', date_str),
              ('Mode', 'day')]

    print('Reading the menu...')
    soup = soup_me(BASE_URL, PARAMS)

    menu_div = soup.find('div', attrs={'aria-label': menu})
    dishes = [dish.string for dish in menu_div('a', rel='prettyPhotoiFrameWithoutNavigation')]

    return dedupe(dishes)


if __name__ == '__main__':
    kwargs = {}
    try:
        kwargs['date'] = sys.argv[1]
    except(IndexError):
        pass # default to today

    header = 'How about'
    food = get_dishes(**kwargs)
    print(''); pprint_header_with_lines(header, food); print('')
    #print(''); print('__How about__'); print('\n'.join(food)); print('')
