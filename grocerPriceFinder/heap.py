__author__ = 'zac'

import node

class heap:
    def __init__(self,name):
        self.h = []
        self.name = name
        self.badLst = []



    def heapify(self, i):
        lc = ((i+1) *2)-1
        rc = lc +1
        if lc > len(self.h)-1:
            return
        if self.h[lc].sortBy < self.h[i].sortBy:
            self.swap(i,lc)
            self.heapify(lc)
        if rc > len(self.h)-1:
            return
        if self.h[rc].sortBy < self.h[i].sortBy:
            self.swap(i,rc)
            self.heapify(rc)




    def swap(self, i, val):
        # print(val)
        temp = self.h[val]
        self.h[val] = self.h[i]
        self.h[i] = temp




    def push(self, item):
        itemNode = self.mkNode(item)
        if itemNode.sortBy <= 0:
            self.badLst.append(itemNode)
            return
        if len(self.h) == 0:
            self.h.append(itemNode)
        else:
            self.h = [itemNode] + self.h
            self.heapify(0)
            # self.reorder(len(self.h))
        # print(self.h)



    def pop(self):
        item = self.h[0]
        self.h[0] = self.h[len(self.h)-1]
        self.h = self.h[:-1]
        # print(self.h)
        # print(self.h)
        # if len(self.h) > 1:
        self.heapify(0)
        # for i in range (len(self.h),0,-1):
        #     self.reorder(i)
        # print(self.h)
        return item

    def mkNode(self,item):
        return node.node(item,item[4])

    def sort(self):
        lst = []
        for i in self.h:
            lst.append(self.pop())
        return lst

