__author__ = 'zac'
import requests
import bs4

def baseHTML(site):
    r = requests.get(site)
    soup = bs4.BeautifulSoup(r.text)
    return soup

class FoodItem:
    def __init__(self, name, price, store, weight):
        self.n = name
        self.p = price

        self.s = store
        self.w = weight


