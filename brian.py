
##### MAIN CONTROL FILE
import sys
from multiprocessing import Process
from multiprocessing import Queue as mQueue
from queue import Queue as tQueue
from threading import Thread
#from queue import Queue
import time

from workers import *
import json

from time import time

### PROCESSES
## EXCHANGE MONITOR - initialises data, checks for candles, runs calcs and determines entry points, opens websockets to monitor candles,
## trade placer - 1 thread for each user - thread monitors all trades 



def exchange_monitor():    ######  action queue (signals only)
 
   flow_queue = tQueue()
 
   for x in range(1):      # 1 worker threads
      watcher = Watcher(flow_queue)
      watcher.daemon = False
      watcher.start()

	  
   flow_queue.join()



	

if __name__ == "__main__":



    #signal_queue = mQueue()
  #  action_queue = mQueue()
  #  user_control_data_thread_queue = mQueue()
   # tracking_queue = mQueue()


   # p0 = Process(target=test_user_process, args=(action_queue,))
    p0 = Process(target=exchange_monitor)

    
   # p1 = Process(target=user_process, args=(action_queue,user_control_data_thread_queue,))
    #p2 = Process(target=tracker, args=(action_queue,tracking_queue,))
		 		 
    p0.start()
  #  p1.start()
    #p2.start()
    p0.join()
 #   p1.join()
    #p2.join()        