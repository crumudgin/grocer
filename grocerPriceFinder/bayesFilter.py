__author__ = 'zac'
import re
import math
import mysql.connector



def getwords(doc):
    splitter=re.compile('\\W*')
    # Split the words by non-alpha characters
    words=[s.lower( ) for s in splitter.split(doc)
           if len(s)>=2 and len(s)<=20]

    # Return the unique set of words only
    return dict([(w,1) for w in words])

    # database = mysql.connector.connect(user='test', password='Grisly12', database="grocer")
    # cursor = database.cursor()
    # cursor.close()
    # database.close()

class classifier:
    def __init__ (self,getfeatures,search, database, cursor ,filename=None):
        # Counts of feature/category combinations
        self.fc={}
        # Counts of documents in each category
        self.cc={}
        self.getfeatures=getfeatures
        self.search = search
        self.database = database
        self.cursor = cursor


    # Increase the count of a feature/category pair
    def incf(self,f,cat):
        self.cursor.execute("select * from fc where feature = %s and category = %s and search = %s", (f,cat,self.search))
        result = self.cursor.fetchall()
        if len(result) == 0:
            self.cursor.execute("INSERT INTO fc "
               "(category, count, search, feature) "
               "VALUES (%s, %s, %s, %s)", (cat, 1, self.search, f))
        else:
            self.cursor.execute("UPDATE fc SET count = count + 1 WHERE feature = %s and category = %s and search = %s", (f,cat,self.search))
        self.database.commit()
        # self.fc.setdefault(f,{})
        # self.fc[f].setdefault(cat,0)
        # self.fc[f][cat]+=1

    # Increase the count of a category
    def incc(self,cat):
        self.cursor.execute("UPDATE cc SET count = count + 1 WHERE category = %s and search = %s", (cat,self.search))
        self.database.commit()
        # self.cc.setdefault(cat,0)
        # self.cc[cat]+=1

    # The number of times a feature has appeared in a category
    def fcount(self,f,cat):
        self.cursor.execute("select count from fc where feature = %s and category = %s and search = %s", (f,cat,self.search))
        result = self.cursor.fetchone()
        try:
            return float(result[0])
        except:
            return 0
        # if f in self.fc and cat in self.fc[f]:
        #     return float(self.fc[f][cat])
        # return 0.0

    # The number of items in a category
    def catcount(self,cat):
        try:
            self.cursor.execute("select count from fc where category = %s and search = %s", (cat,self.search))
            result = self.cursor.fetchone()
            # print(result[0])
            # print(type(result))

            return float(result[0])
        except:
            return 0
        # if cat in self.cc:
        #     return float(self.cc[cat])
        # return 0
    # The total number of items
    def totalcount(self):
        self.cursor.execute("select * from cc")
        result = self.cursor.fetchone()
        return len(result)/2

    # The list of all categories
    def categories(self):
        # lst = []
        # database = mysql.connector.connect(user='test', password='Grisly12', database="grocer")
        # cursor = database.cursor()
        # cursor.execute("select category from cc")
        # result = cursor.fetchone()
        # # cursor.close()
        # # database.close
        # for i in result:
        #     if i%2 == 0:
        #         lst.append(i)
        # # return self.cc.keys( )
        # return lst
        return[1,0]

    def train(self,item,cat):
        features=self.getfeatures(item)
        # Increment the count for every feature with this category
        for f in features:
            self.incf(f,cat)
        # Increment the count for this category
        self.incc(cat)

    def fprob(self,f,cat):
        if self.catcount(cat)==0: return 0
        # The total number of times this feature appeared in this
        # category divided by the total number of items in this category
        # print(self.fcount(f,cat))
        return self.fcount(f,cat)/self.catcount(cat)

    def weightedprob(self,f,cat,prf,weight=1.0,ap=0.5):
        # Calculate current probability
        basicprob=prf(f,cat)
        # Count the number of times this feature has appeared in
        # all categories
        totals=sum([self.fcount(f,c) for c in self.categories( )])
        # Calculate the weighted average
        bp=((weight*ap)+(totals*basicprob))/(weight+totals)
        return bp



class naivebayes(classifier):
    def __init__(self, getfeatures, search, database, cursor):
        classifier.__init__(self,getfeatures,search, database, cursor)
        self.thresholds={}
        # self.search = search

    def docprob(self,item,cat):
        features=self.getfeatures(item)
        # Multiply the probabilities of all the features together
        p=1
        for f in features: p*=self.weightedprob(f,cat,self.fprob)
        return p

    def prob(self,item,cat):
        val1 = self.catcount(cat)
        val2 = self.totalcount( )
        catprob=val1/val2
        docprob=self.docprob(item,cat)
        # print(catprob)
        # print(docprob)
        return docprob*catprob

    def setthreshold(self,cat,t):
        self.thresholds[cat]=t

    def getthreshold(self,cat):
        if cat not in self.thresholds: return 1.0
        return self.thresholds[cat]

    def classify(self,item,default=0):
        probs={}
        best = default
        # Find the category with the highest probability
        max=0.0
        for cat in self.categories( ):
            probs[cat]=self.prob(item,cat)
        if probs[cat]>max:
            max=probs[cat]
            best=cat
        # Make sure the probability exceeds threshold*next best
        for cat in probs:
            if cat==best: continue
            # print(self.getthreshold(best))
            if probs[cat]*self.getthreshold(best)>probs[best]: return default
        return best




