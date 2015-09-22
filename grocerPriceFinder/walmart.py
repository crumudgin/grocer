__author__ = 'zac'
import requests
import bs4
from threading import *
from FoodItem import *

lst = []
def getHTML(item, num):
    newWord = ""
    for i in range(0,len(item)):
        if item[i] == " ":
            newWord += "%20"
        else:
            newWord += item[i].strip("%")
    # print(newWord)
    soup = baseHTML('http://www.walmart.com/search/?query='+ newWord + "&page=" + str(num) + "&cat_id=0")
    return soup

def getItem(item, num, pageNum):
    soup = getHTML(item, pageNum)
    # print(item)
    # print(soup)
    #soup = soup.select(".js-tile js-tile-landscape tile-landscape") #goal foor finding the info
    soup = soup.find_all(attrs={"class":"js-tile js-tile-landscape tile-landscape"}) #problem area
    # print(soup)
    soup = soup[num-1].select("a[href]")
    link = (str(soup[0]).split('href="'))[1].split('">')


    return(baseHTML("http://www.walmart.com/" +link[0]))


def getPrice(soup):
    area = soup.find_all(attrs={"class":"btn btn-inverse btn-block js-btn-add-to-registry btn-add-to-registry"})
    section = str(area).split('"')
    #print(section)
    for i in range(0,len(section)):
        if section[i] ==  ' data-product-price=':
            return float(section[i+1])

def getName(soup):

    #print(soup)
    '''
    area = soup.find_all(attrs={"class":"js-product-title"})
    part = str(area[28]).split('<')
    name = str(part[1]).split('>')
    return(name[1])
    '''
    try:
        area = str(soup).split("meta content=")
        parts = area[4].strip('"').split(',')
        # print(parts)
        name = [parts[0],parts[1]]
        return name
    except:
        return -1


def mkWalmart(item):

    s = getHTML(item, 1)
    #print(s)
    line = s.find_all(attrs={"class":"result-summary-container"})
    line = str(line[0]).split("Showing ")
    perPage = str(line[1]).split(" of ")[0]
    total = str(line[1]).split(" of ")[1].split(" ")[0].replace(",", "")
    pages = int(total)//int(perPage)
    if pages > 50:
        pages = 50
    soup = getItem(item, 1, 1)
    loop = 0
    threads = []
    for i in range(1,int(pages)+1):
        # for k in range(1,int(perPage) +1):
            # while loop == 0:
            #     try:
            #        loop = 1
            # print("page " + str(i) +" : " + str(k))
            # soup = getItem(item, k, i)
        t = Thread(target=construction, args=(i, int(perPage), item,))
            #t.start()
        threads.append(t)
            # threads[len(threads)-1].start()
            # lst.append(fi)
            # print(fi.n + "  :  " + str(fi.p))
                # except:
                #     print("GOD DAM MOTHER FUCKING WALLMART")
                #     loop = 0
    print("threads starting")
    for i in threads:
        i.start()
    for i in threads:
        i.join()


    return lst

def construction(i,perPage, item):
    # print("hi")

    for k in range(1,perPage):
        print(str(i) + " : " + str(k))
        soup = getItem(item, k, i)
        # print("soup gotten")
        nw = getName(soup)
        name = nw[0]
        try:
            print("oh god i'm so fat")
            weight = float(nw[1].strip(" oz"))
        except:
            print("gravaty does not effect me")
            weight = 1
        # print(weight)
        price = getPrice(soup)


        if type(price) is not float:
            price = -1
    # try:
    #     area = str(soup).split("meta content=")
    #     parts = area[4].strip('"').split(',')
    #     name = parts[0]
    # except:
    #     name = "--"
    #
    # area = soup.find_all(attrs={"class":"btn btn-inverse btn-block js-btn-add-to-registry btn-add-to-registry"})
    # section = str(area).split('"')
    # #print(section)
    # for i in range(0,len(section)):
    #     if section[i] ==  ' data-product-price=':
    #         if section[i+1] == None:
    #             price = -1
    #         else:
    #             price = float(section[i+1])
    #         break
    #     else:
    #         price = -1
    #print(name + "  :  " + str(price))
        if type(name) is str:
            lst.append(FoodItem(name,price, "walmart", weight))

def constructFromNum(num):
    soup = baseHTML('http://www.upcdatabase.com/item/' + str(num))
    lines = str(soup.select("#content")[0]).split('\n')
    line = lines[6].split("<")
    word = line[6].split('>')
    # print(word)
    item = getItem(word[1],1,1)
    p = getPrice(item)
    nw = getName(item)
    n = nw[0]
    w = nw[1]
    return [FoodItem(n,p,"walmart",w)]


