from collections import OrderedDict
from datetime import datetime, timedelta
import requests
import sys

from bs4 import BeautifulSoup
from dateutil import parser


def get_dishes(date="today", menu="Classic Cuisine"):
    date = (datetime.now() if date is "today" else date)
    date_str = "-".join([str(date.year), "{:02d}".format(date.month),
                         "{:02d}".format(date.day)])

    BASE_URL = "http://mit.campusdish.com/Commerce/Catalog/Menus.aspx"
    PARAMS = [("LocationId", "4932"), # Koch cafe
              ("PeriodId", "1440"), # lunch
              ("MenuDate", date_str),
              ("Mode", "day")]

    print("Reading the menu...")
    soup = BeautifulSoup(requests.get(BASE_URL, PARAMS).content, "lxml")

    dishes = [dish.string for section in soup("div", class_="menu-details-station")
              for dish in section("a", rel="prettyPhotoiFrameWithoutNavigation")
              if section.h2.string == menu]

    return dedupe(dishes)

# via https://stackoverflow.com/questions/6197409/ordered-sets-python-2-7
def dedupe(lst):
    """list -> deduped iterable of items, in order"""
    return OrderedDict((item, None) for item in lst).keys()


if __name__ == "__main__":
    kwargs = {}
    try:
        date = (datetime.now() + timedelta(days=1)
                if sys.argv[1] in ("tomorrow", "tom")
                else parser.parse(sys.argv[1]))
        kwargs["date"] = date
    except(IndexError):
        pass # default to today
    except(ValueError):
        print("I don't recognize that date.. try again ?")
        sys.exit(0)

    food = get_dishes(**kwargs)
    print(""); print("__How about__"); print("\n".join(food)); print("")
