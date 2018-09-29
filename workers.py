## workers

import sys
from multiprocessing import Process
from multiprocessing import Queue as mQueue
from queue import Queue as tQueue
from threading import Thread
#from queue import Queue
import time
import json
from binance.client import Client
import datetime
from binance.websockets import BinanceSocketManager
from binance.exceptions import BinanceAPIException
from binance.depthcache import DepthCacheManager
from binance.enums import *
#from support import *
from decimal import Decimal, ROUND_DOWN
#from stopo import *
import ast
from datetime import datetime,timedelta
import requests
from tabulate import tabulate
from operator import itemgetter

	


class Watcher(Thread):
   # monitors orderbook (depth websocket), trade volume (websocket), current price 
   def __init__(self,flow_queue):
       Thread.__init__(self)
       self.flow_queue = flow_queue


   def run(self):
       with open("pairs.txt","r") as sigf:   ####### get starting pairs and candle intervals from file 
         pairs_list = sigf.read()
         pairs_list = eval(pairs_list)

      # client = Client("","")


       for item in pairs_list:
         base_currency,second_currency,interval = item.split(":")
         upper_symbol = base_currency + second_currency
		 
         for x in range(1):      # Create one worker for each item in pair list
           socket_worker = SocketWorker(self.flow_queue,item)
           socket_worker.daemon = False
           socket_worker.start()
         self.flow_queue.join()
		 
		 
class SocketWorker(Thread):
   # monitors orderbook (depth websocket), trade volume (websocket), current price 
   def __init__(self,flow_queue,item):
       Thread.__init__(self)
       base_currency,second_currency,interval = item.split(":")
       self.base_currency = base_currency
       self.second_currency = second_currency
       self.upper_symbol = self.base_currency + self.second_currency
       self.interval = interval
       self.base_second_inner = []	   
       self.base_second_inner.append(self.upper_symbol)
       self.base_second_inner.append(self.base_currency)
       self.base_second_inner.append(self.second_currency)
	   

       lower_symbol = self.upper_symbol.lower()
       self.nub_listb = []
       nubb = lower_symbol + "@kline_3m"
       self.nub_listb.append(nubb)
       self.base_second_list = []
       self.client = Client("","")
       asset_data = self.client.get_exchange_info()
       time.sleep(3)
       for item in asset_data['symbols']:
         if item['symbol'] == self.upper_symbol:
          for items in item['filters']:
           if items['filterType'] == "LOT_SIZE":
            self.step_size = items['stepSize']
           if items['filterType'] == "PRICE_FILTER":
            self.tick_size = items['tickSize']
     #  print (step_size)
     #  print (tick_size)
       self.base_second_inner = []
       self.base_second_inner.append(self.step_size)
       self.base_second_inner.append(self.interval)
       self.base_second_inner.append(self.tick_size)
       self.base_second_list.append(self.base_second_inner)		 
       #print ("this is base second list: ", self.base_second_list)		 

       self.flow_queue = flow_queue

      # self.asset_data = asset_data


       tick_size_int = str(self.tick_size)
       #slick_size = Decimal(tick_size)
       junk1,tick_size_int = tick_size_int.split(".")
       tick_size_int,junk1 = tick_size_int.split("1")
       self.tick_size_int = len(tick_size_int) + 1
       self.last_price = 0	   
       self.stop_price = 0
       self.trade_on = 0  
       self.buy_price = 0
       self.sell_price = 0  
       self.new_price = 0
       self.count = 1	
       go_go = 0		   
   def run(self):

       filename = str(self.upper_symbol) + "-price.csv"
       now = time.time()
       header = "date,price\n"
       firstline = []
       try:
        with open(filename, "r") as sym:
          head = sym.readlines() 
        if len(head) > 2:
          firstline = head[1].split(",")
       except FileNotFoundError:
        with open(filename,"w") as sym:
          sym.write(header)
       if len(firstline) > 1:
         if Decimal(now) - (Decimal(firstline[1]) / 1000) > 172800:
          with open(filename,"w") as sym:
            sym.write(header)
       def process_m_message(msg):
        print(msg)
        print(self.upper_symbol)
        if msg['data']['k']['x'] == True:
          print(msg)
          print ("Received New Candle")
          print (self.count)
          self.last_price = Decimal(msg['data']['k']['c'])
          self.date = Decimal(msg['data']['k']['t'])
          filename = str(self.upper_symbol) + "-price.csv"           
          datar = str(self.date) + "," + str(self.last_price) + "\n"
          with open(filename,"a") as syma:
            syma.write(datar)
          #  print ("last: ",self.last_price)
         #   print ("stop: ",self.stop_price)
         #   print ("tradeon: ",self.trade_on)
          #  print ("buy_price: ",self.buy_price)
          #  print ("sell_price: ",self.sell_price)            
          #  print ("new_price: ",self.new_price)
      


        #  print ("NO ERROR")# process message normally
          #print("stream: {} data: {}".format(msg['stream'], msg['data']))
          #print (msg['data']['k']['s'])
		  



             # - get the time of the close and compare this to our times 
          #   this_close = int(datetime.utcfromtimestamp(((float(msg['data']['k']['t'])/1000)+1)).strftime("%M")) + 1


        
       bm = BinanceSocketManager(self.client)
       bm.start_multiplex_socket(self.nub_listb, process_m_message)
       bm.start()			
 

 
 
 
 
 
 
 
		 
		 

