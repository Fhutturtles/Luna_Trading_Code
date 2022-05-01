API_KEY = "Enter your API Key"
SECRET_KEY = "Enter your Secret Key"
from pickle import FALSE
from tracemalloc import start
from coinexpy.coinex import Coinex
import json
import requests
import sched, time 
import math
import numpy as np
import seaborn as sns
import scipy.stats as stats
import tkinter #this controls graph dont touch
import pandas as pd
import matplotlib
matplotlib.use("TkAgg") #this controls the graph Especially dont touch this Brian
import matplotlib.pyplot as plt#this controls graph dont touch
s = sched.scheduler(time.time, time.sleep)#this is the timer function that executes a market sweep every deffined times
coinex = Coinex(API_KEY, SECRET_KEY)
tval = 8
test_market_prices = []
arr_difference = []
store_quick_prices = []
loc = 0
start_time_amount = 0
graph_time_hits = 3 #change this to decide when to show the graph (either every time you update which is 1 or every 1000 updates or so)
def getupdated_data_items():

  balance = coinex.get_balance()
  usdt_balance = coinex.get_available('USDT') #PLEASE MAKE SURE THE COIN VALUE YOU OBTAINED IS ON THE LIST VISIT https://api.coinex.com/v1/market/list TO VIEW LIST
  luna_balance = coinex.get_available('LUNA') #PLEASE MAKE SURE THE COIN VALUE YOU OBTAINED IS ON THE LIST VISIT https://api.coinex.com/v1/market/list TO VIEW LIST
  luna_price = coinex.get_last_price('LUNAUSDT') #PLEASE MAKE SURE THE COIN VALUE YOU OBTAINED IS ON THE LIST VISIT https://api.coinex.com/v1/market/list TO VIEW LIST

  print('Available balance: ', balance)
  print('Available USDT balance: ',usdt_balance)
  print('Available LUNA balance: ', luna_balance)
  print('Last trading price of LUNA: ', luna_price)

def get_luna_price(sc): #this function loops and grabs the current price of luna so far
  get_val = coinex.get_last_price('LUNAUSDT')
  test_market_prices.append(get_val)
  '''
  the general idea is that to be able to preform a t star statistic 
  for a confidence interval you would need to have two differnet samples
  the first is a continous array/ sample that checks the entire market
  the second sample is a non-continuous array that is constantly being chnaged based on a sample of 30 transactions in the market
  the second grabs 30 transactions initially then deviates from the first by changing instead of addign and remains at only 30 transactions 
  '''
  #this is what this does 
  if(len(store_quick_prices) <= 30):
    store_quick_prices.append(get_val)
  else:
    global loc
    if(loc <= 29):
      store_quick_prices[loc] = get_val
      loc = loc + 1
    else:
      loc = 0 #FIX THIS
  #print(test_market_prices)
  #print(len(test_market_prices))
  s.enter(tval, 1, get_luna_price, (sc,))
  #print("Average of data: " + str(np.average(test_market_prices)))
  data_average()
  global start_time_amount
  start_time_amount += 1
  print("Start time size of test_array: " + str(start_time_amount))
  ''' this section of code is commented out but what it does is call the ploting diagram from sesaborn
  if(len(test_market_prices)%graph_time_hits == 0):
    line_plot_seaborn()
  '''
  

def execution_trades():#this is if you decide to execute trades

  try:
      #coinex.market_buy('LUNAUSDT', usdt_balance)  # buy usdt BALANCE worth of luna at the market price
      print('Market buy order executed: BUY LUNA')
      #coinex.market_sell('LUNAUSDT', 5.1639)  # SELL 5.1639 LUNA worth of luna FOR USDT at the market price
      print('Market sell order executed: SOLD LUNA')
  except:
      print('Could not execute trade')
    
def data_average():
  get_updated_price = coinex.get_last_price('LUNAUSDT')
  arr_difference.append(get_updated_price - np.average(test_market_prices))
  print("---------------------------")
  print("Average of test_data: " + str(np.average(test_market_prices))+ " Average of quick_data: "+ str(np.average(store_quick_prices)) + " price of LUNA: " + str(get_updated_price) + " Difference: " + str(get_updated_price - np.average(test_market_prices)))
  stndrd_deviation_test = np.std(test_market_prices) #THIS PIECE OF DATA IS THE STANDARD DEVIATION OF THE PAST MARKET VALUES
  print("The Standard Deviation of the test_data: " + str(stndrd_deviation_test))
  stndrd_deviation_quick = np.std(store_quick_prices)
  print("The Standard Deviation of the quick_data: " + str(stndrd_deviation_quick))
  t_statistic, p_value = stats.ttest_1samp(a=store_quick_prices, popmean=get_updated_price)
  print(t_statistic , p_value)
  print("Confidence interval for the stored quick values based on changing market conditions: ")
  print(str(get_updated_price+(t_statistic)*(stndrd_deviation_quick/math.sqrt(len(store_quick_prices))))+ " ---- " + str(get_updated_price-(t_statistic)*(stndrd_deviation_quick/math.sqrt(len(store_quick_prices)))) )
  

def line_plot_seaborn():
  
  dataframe = pd.DataFrame({"Time_in_Market": list(range(0,len(test_market_prices))), "Price_Difference" : arr_difference})
 # plt.ion()#dont touch for plotting
  plt.show()#dont touch for plotting
  sns.lineplot( data=dataframe,x='Time_in_Market', y='Price_Difference')
  plt.draw() #use this instead of plt.show() as .show is a blocking method that doesnt allow for the plot ot be cleared
  plt.pause(0.01) #this allows for the graph to be plotted and no MAJOR error occurs
  plt.close('all') #this clears all or any plots that are old or redundant
  #figure out how to deal with te failed to allocate bitmap error

s.enter(tval,1 , get_luna_price, (s,))#this is the call function that is executed that loops every tval 
#seconds and checks the current price of lunam, it goes to the get_luna_price function it does not execute trades for luna at all
s.run()


