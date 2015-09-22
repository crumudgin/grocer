__author__ = 'zac'
import requests
import bs4
import Target
import walmart
import mysql.connector
import bayesFilter
import heap



root = 'http://pyvideo.org'

class grocer:

    def __init__(self):
        self.database = mysql.connector.connect(user='test', password='Grisly12', database="grocer")
        self.cursor = self.database.cursor(buffered=True)

    def baseHTML(site):
        r = requests.get(site)
        soup = bs4.BeautifulSoup(r.text)
        return soup

    def narrowHTML(self, soup, peram):
        links = soup.select(peram)
        return links

    def getURLs(self, URL):
        data = {}
        r = requests.get(root + URL)
        soup = bs4.BeautifulSoup(r.text)

    def compairPrice(self, item1, item2):
        if item1.p < item2.p:
            return item1
        return item2

    def findDuplicate(self, item,search):

        # querySearch = ("SELECT id, search, points From search_type")
        queryItem = ("SELECT * FROM food WHERE name = %s and weight = %s and location = %s")
        self.cursor.execute(queryItem, (item.n, item.w, item.s))
        result = self.cursor.fetchall()
        print(len(result))
        if len(result) > 0:
            # print(result[0][0])

            search_data = (result[0][4], search, 0)
            self.cursor.execute(("INSERT INTO search_type "
                            "(id, search, points) "
                            "VALUES (%s, %s, %s)"), search_data)
            self.database.commit()
            return 1



        # for i in cursor:
        #     print(i)
        return 0


    def buildData(self, search):

        lst = []
        counter = 0
        counterTotal = 0

        t = Target.mkTarget(search)

        add_food = ("INSERT INTO food "
                   "(name, price, weight, location) "
                   "VALUES (%s, %s, %s, %s)")

        add_search = ("INSERT INTO search_type "
                   "(id, search, points) "
                   "VALUES (%s, %s, %s)")

        add_fc = ("INSERT INTO fc "
                   "(category, count, search, feature) "
                   "VALUES (%s, %s, %s, %s)")

        add_cc = ("INSERT INTO cc "
                   "(count, search, category) "
                   "VALUES (%s, %s, %s)")

        self.cursor.execute(add_cc, (0, search,1))
        self.database.commit()
        self.cursor.execute(add_cc, (0, search,0))
        self.database.commit()
        print("hi")
        for i in t:
            counterTotal += 1

        #    print(i.n +' '+ str(i.p))

            if self.findDuplicate(i,search) == 1:
                print("i'm in here all ready")

            else:
                print("i'm here to stay bitches")
                lst.append(i)
                try:
                    food_data = (i.n, float(i.p), float(i.w), "target")
                    self.cursor.execute(add_food,food_data)
                    self.database.commit()
                    foodID = self.cursor.lastrowid
                    search_data = (foodID, search, 0)
                    self.cursor.execute(add_search,search_data)
                    counter += 1
                    print("holy fuck I worked")

                except:
                    print("i have failed")


        w = walmart.mkWalmart(search)
        for i in w:
            counterTotal += 1
            if self.findDuplicate(i,search) == 1:
                print("i'm in here all ready")
            else:
                print("i'm here to stay bitches")
                lst.append(i)
                try:
                    food_data = (i.n, float(i.p), float(i.w), "walmart")
                    self.cursor.execute(add_food,food_data)
                    foodID = self.cursor.lastrowid
                    search_data = (foodID, search, 0)
                    self.cursor.execute(add_search, search_data)
                    self.database.commit()
                    print(i.n)
                    counter += 1;
                except:
                    print("i have failed")
        try:
            add_searchs = ("INSERT INTO search "
                        "(name, popularity)"
                        "VALUE (%s, %s)")
            self.cursor.execute(add_searchs, (search, 0))
            self.database.commit()
        except:
            print("boo")
        # cursor.close()
        # database.close
        print(counter)
        print(counterTotal)
        try:
            for i in lst:
                print(i.n)
        except:
            print("it couldn't fucking print!")



    def training(self, item):
        lst = self.search(item,5,2)
        for i in lst:
            print(i.data)
        c = bayesFilter.naivebayes(bayesFilter.getwords, item, self.database, self.cursor)
        print("\nbegin input\n")
        for i in lst:
            print(i.data)
            yn = input("y/n")
            if(yn == 'y'):
                print("yay")
                c.train(i.data[0],1)
            elif(yn =='n'):
                print("boo")
                c.train(i.data[0], 0)
            else:
                for k in lst:
                    print(k.data)
                    print(str(c.prob(k.data[0],"good")))
                    # print(c.prob(k.data[0], "good"))
                    # print(k.data[0] + "  :  " + str(c.prob(k.data[0], "good")) + "  :  " + str(c.classify(k.data[0])))

                    try:
                        # print(k.data[0])
                        # print(str(k.data[0]) + "  :  " + str(c.prob(k.data[0],"good")))
                        pass
                        # print(k.data[0] + "  :  " + str(c.prob(k.data[0], "good")) + "  :  " + str(c.classify(k.data[0])))
                    except:
                        print("aww man I suck")
                        print(k.data)
                return

        # print(i.data[0] + "  :  " + str(c.prob(i.data[0], "good")) + "  :  " + str(c.classify(i.data[0])))
        return


    def search(self, searchTerm, glst, quantity):

        c = bayesFilter.naivebayes(bayesFilter.getwords, searchTerm, self.database, self.cursor)
        querySearchTerm = ("SELECT * FROM search WHERE name = %s")
        self.cursor.execute(querySearchTerm, (searchTerm,))
        results = self.cursor.fetchall()
        if len(results) == 0:
            self.buildData(searchTerm)
            self.search(searchTerm,glst, quantity)
            return
        querySearch = ("SELECT * FROM search_type WHERE search = %s")
        self.cursor.execute(querySearch, (searchTerm,))
        curs1 = self.cursor.fetchall()

        # results = cursor.fetchall()
        lst = []
        for i in curs1:
            queryItem = ("SELECT * FROM food WHERE id = %s")
            self.cursor.execute(queryItem, (i[0],))
            r = self.cursor.fetchone()
            # print(r)
            toup = (r[0], r[1], r[2], r[3], r[1]/r[2], r[4])
            lst.append(toup)
        h = heap.heap(1)
        # print("hi")
        for i in lst:
            h.push(i)
        finalForm = h.sort()
        for i in finalForm:
            print(i.data)
            yn = input("is this the item you are looking for? y/n")
            if yn == "y":
                c.train(i.data[0],1)
                self.cursor.execute("INSERT INTO list_items "
                        "(food_id, list_id, quantity) "
                        "VALUES (%s,%s,%s)",(i.data[5],glst,quantity))
                self.database.commit()
                self.cursor.execute("UPDATE search_type SET points = points + 1 WHERE id = %s", (i.data[5],))
                self.database.commit()
                # print(finalForm)
                return finalForm
            c.train(i.data[0],0)
        return finalForm

        # for i in lst:
        #     # print(i)
        #     if i[1] != -1:
        #         if i[4] < cheapestPrice:
        #             cheapestPrice = i[4]
        #             cheapestItem = i
        # print(i)


        # h = []
        # for i in lst:
        #     heapq.heappush(h,i)
        # print(h)
        # print(heapq.heappop(h)[0])
        # lst = [heapq.heappop(h) for i in range(len(h))]
        # print(lst)
        # for i in lst:
        #     if i[4] >0:
        #         print(i)
        #         pass

    def mkGLst(self, name, user):
        self.cursor.execute("INSERT INTO grocery_list "
                        "(name) "
                        "VALUES (%s)",(name,))
        self.database.commit()
        self.assignLst(user,name)

    def viewGLst(self, name):
        # print(name)
        self.cursor.execute("SELECT * FROM grocery_list WHERE name = %s",(name,))
        lstInfo = self.cursor.fetchone()
        # print(lstInfo)
        self.cursor.execute("SELECT * FROM list_items WHERE list_id = %s",(lstInfo[1],))
        result = self.cursor.fetchall()
        for i in result:
            self.cursor.execute("SELECT * FROM food WHERE id = %s", (i[0],))
            r = self.cursor.fetchone()
            print(r)


    def mkUser(self, name):
        self.cursor.execute("INSERT INTO user "
                        "(first_name) "
                        "VALUES (%s)",(name,))
        self.database.commit()
        self.mkGLst(name+"'s lst", name)


    def assignLst(self, user, lst):
        self.cursor.execute("SELECT * FROM user WHERE first_name = %s",(user,))
        userInfo = self.cursor.fetchone()
        self.cursor.execute("SELECT * FROM grocery_list WHERE name = %s",(lst,))
        lstInfo = self.cursor.fetchone()
        self.cursor.execute("INSERT INTO user_list "
                        "(user_id,list_id) "
                        "VALUES (%s, %s)",(userInfo[0],lstInfo[1]))
        self.database.commit()

    def runOnCommandLine(self):
        searchTerm = input("what would you like to add to your list")
        while(searchTerm != "quit"):
            if searchTerm == "l":
                self.viewGLst("andrew's lst")

            else:
                # searchTerm = input("what would you like to add to your list")
                self.search(searchTerm,6,int(input("how many: ")))
            searchTerm = input("what would you like to add to your list")

    def singleStore(self, lst):
        targLst = []
        wallLst = []

        a = heap.heap(1)
        b = heap.heap(2)
        for i in lst:
            print(i.data)
            # print(i.data)
            if i.data[3] == "target":
                targLst.append(i)
                self.cursor.execute("SELECT * FROM search_type WHERE id = %s", (i.data[5],))
                searchTerm = self.cursor.fetchone()[1]
                c = bayesFilter.naivebayes(bayesFilter.getwords, searchTerm, self.database, self.cursor)
                self.cursor.execute("SELECT * FROM search_type WHERE search = %s", (searchTerm,))
                results = self.cursor.fetchall()
                for j in results:
                    if j[3] == "walmart":
                        pass
                    else:
                        toup = (j.data[0], j.data[1], j.data[2], j.data[3], c.prob(j.data[0], 1), j.data[4])
                        a.push(toup)
                targLst.append(a.sort()[0])
            else:
                wallLst.append(i)
                self.cursor.execute("SELECT * FROM search_type WHERE id = %s", (i.data[5],))
                searchTerm = self.cursor.fetchone()[1]
                c = bayesFilter.naivebayes(bayesFilter.getwords, searchTerm, self.database, self.cursor)
                self.cursor.execute("SELECT * FROM search_type WHERE search = %s", (searchTerm,))
                results = self.cursor.fetchall()
                # print(results)
                for j in results:
                    self.cursor.execute("SELECT * FROM food WHERE id = %s", (j[0],))
                    r = self.cursor.fetchone()
                    if r[3] == "target":
                        pass
                    else:
                        toup = (r[0], r[1], r[2], r[3], c.prob(r[0], 1), r[4])
                        a.push(toup)
                wallLst.append(a.sort()[0])

        targTot = 0
        wallTot = 0
        for i in targLst:
            targTot += i.data[4]
        for i in wallLst:
            wallTot += i.data[4]
        print(targTot)
        print(wallTot)
        return (targLst,wallLst)






m = grocer()
# m.search("oreo",5,2)
# m.viewGLst("andrew's lst")
# m.mkUser("andrew")
# m.runOnCommandLine()
m.singleStore(m.search("oreo",5,1))