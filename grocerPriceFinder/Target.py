__author__ = 'zac'
import requests
import bs4
from FoodItem import *



def getPrice(item, num, target):
    try:
        #print(target)
        #target = baseHTML('http://www.target.com/s?searchTerm=' + item + '&category=0%7CAll%7Cmatchallpartial%7Call+categories&lnk=snav_sbox_'+ item)
        tproducts = target.select('#productListForm')
        #links = [a.attrs['href'] for a in narrowHTML(HTML, "#video-summary-content a[href^=/video]")]
        links2 = tproducts[0].select('.pricecontainer')
        t = links2[num].select('p')
        #print(t)
        i = str(t[0]).split('\n')
        #print((i[len(i)-1].strip('</p>').strip('\t').strip('$').strip(' ')))

        #print((i[len(i)-1].strip('</p>').strip('\t').strip('$').strip(' ')))
        return float(i[len(i)-1].strip('</p>').strip('\t').strip('$').strip(' '))
    except:
        return -1

def getName(item, num, target):
    #target = baseHTML('http://www.target.com/s?searchTerm=' + item + '&category=0%7CAll%7Cmatchallpartial%7Call+categories&lnk=snav_sbox_'+ item)
    #links = [a.attrs['href'] for a in target.select("#video-summary-content a[href^=/video]")]
    overall = target.select('.tileImage')
    line = overall[num].select('a[href]')

    name = (str(overall[num]).split("alt=")[1].split("' ")[0].split('" ')[0])
    # print(name)
    try:
        weightIni = name.strip(" oz").split(" ")
        weightMid= weightIni[len(weightIni)-1]
        weight = float(weightMid)
        print("oh god i'm so fat")
    except:
        weight = 1
        print("gravaty does not effect me")
    nw = [name,weight]
    return nw


def mkTarget(item):
    lst = []
    soup = baseHTML('http://www.target.com/s?searchTerm=' + item + '&category=0%7CAll%7Cmatchallpartial%7Call+categories&lnk=snav_sbox_'+ item)
    c = soup.select('#resultInfo2')
    c = str(c[0]).split('\n')
    currNum = c[len(c)-2].strip('\t')
    totNum = c[len(c)-1].strip('\t').strip('</p>').strip('of ')
    if(int(totNum)%int(currNum) != 0):
        pages = (int(totNum)//int(currNum) + 1)
    else:
        pages = print(int(totNum)//int(currNum))
    if type(pages) != int:
        pages = 1

    for i in range(1, pages):
        soup = baseHTML('http://www.target.com/s?searchTerm='+item + '&category=0&view=medium&sort=relevance&iec=1&resultsPerPage=60&page=' + str(i) + '&s=y')
        for k in range(0,59):
            nw = getName(item,k,soup)
            lst.append(FoodItem(nw[0], getPrice(item, k, soup), "target", nw[1]))
    return lst

def mkTargetFromNum(num):
    return mkTarget(num)

