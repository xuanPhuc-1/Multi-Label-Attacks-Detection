#Appendix C: Collection and Entropy & Response Time Computation 

import math
import time

class Entropy(object):

    def start(self):
        #trich xuat ip_dst
        file_ip_dst = None
        with open('data/ipdst.csv', 'r') as t2:
            file_ip_dst = t2.readlines()
        # print(file_ip_dst)
        #thu thap ip_dst
        self.num_ip = len(file_ip_dst)
        for ip_dst in file_ip_dst:
            # print(ip_dst)
            self.collectStats(ip_dst)

    def collectStats(self, element):
        self.count += 1
        self.destIP.append(element)
        self.responseTime(element)	#######
        if self.count == self.num_ip:
            # print(self.destIP)
            for i in self.destIP:
                if i not in self.destFrequency:
                    self.destFrequency[i] = 0
                self.destFrequency[i] += 1
            self.findEntropy(self.destFrequency)
            self.destFrequency = {}
            self.destIP = []
            self.count = 0   
          
    def responseTime(self, element): #######
        self.destIP2.append(element)	######
        for j in self.destIP2:	######
            if self.destIP2.count(j) >= 8  and self.flag != 1:	######
                self.flag = 1	######
                self.startMarker()	######
        if len(self.destIP2) == 100:	######
            self.destIP2 = []	######
          
    def startMarker(self):	#######
        start = time.time()	#######
        self.startList.append(start)	#######
        if len(self.startList) == 50:	######
            #del self.startList[:]	######
            self.startList = []
        return self.startList[0]	#######
      
    def findEntropy (self, lists):
        l = self.num_ip
        entropyList = []
        for k,p in lists.items():
            c = p/float(l)
            c = abs(c)
            entropyList.append(-c * math.log(c,10))
            self.destEntropy.append(sum(entropyList))
      		
        if(len(self.destEntropy)) == 50:
            self.destEntropy = []
        self.value = sum(entropyList)
      	
    def __init__(self) -> None:
        self.num_ip = 0
        self.count = 0
        self.flag = 0 #######
        self.destFrequency = {}
        self.destIP = []
        self.destEntropy = []
        self.value = 1
        self.startList = []	#######
        self.destIP2 = []	#######
        pass

    
        
      	
      	


