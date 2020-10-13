import requests
import time
from exmo import ExmoAPI
import json
import telebot
import datetime

bot = telebot.TeleBot('961756482:AAF6DWHh0sW7PPIK1ivdst9rafxl911SFqs')
api_key = "K-96058d8097384af0c3ea99a887881f7fdfdbb49e"
api_secret = "S-d8f83f81d241f929f63357618409416604550938"


obj = ExmoAPI(api_key, api_secret)


def average_in_list(lst : list):
    try:
        return sum (lst) / len(lst)
    except:
        return None




def long_difference(obj, current_pair, start_time, count):
        try:
            response = requests.get("https://api.exmo.com/v1/trades/?pair=BTC_USD&limit=10000")
        except :
            bot.send_message("@buyingapples", "Connection error : apple tree is not avaliable now...\n" )
            return None
        Unix_time = int(time.time())
        previous_orders =  []
        if start_time > 300:
            part_time = start_time//3
            average_in_part = [0, 0, 0, 0]
            k = 0
            for order in response.json()[current_pair]:
                if(Unix_time - order["date"] < start_time):
                        previous_orders.append(float(order["price"]))
                        if k >= 0 and k < count and Unix_time - order["date"] > part_time:
                            average_in_part[1] += float(order["price"])
                            k+=1
                        if k >= count and k < count*2 and Unix_time - order["date"] > part_time*2:
                            average_in_part[2] += float(order["price"])
                            k+=1
            average_in_part[0] = average_in_list(previous_orders[0:count])
            average_in_part[1] = average_in_part[1]/count
            average_in_part[2] = average_in_part[2]/count
            average_in_part[3] = average_in_list(previous_orders[-1:-count-1:-1])
            return average_in_part
        else:
            for order in response.json()[current_pair]:
                if(Unix_time - order["date"] < start_time):
                        previous_orders.append(float(order["price"]))
            average_in_part = [0, 0]
            average_in_part[0] = previous_orders[0]
            average_in_part[1] = previous_orders[-1]
            return average_in_part





def analysis_six_hours(obj, current_pair):
        diff = 50
        average_in_part = long_difference(obj,current_pair,21600, 5)
        if (average_in_part != None):
            print("6 hours differences: " + str(average_in_part)+ " difference = " + str(average_in_part[3] - average_in_part[0]))
            if (average_in_part[3] - average_in_part[0] >= diff):
                res = {"result": True, "difference": average_in_part[3] - average_in_part[0]}
                return res
            else:
                res = {"result": False, "difference": average_in_part[3] - average_in_part[0]}
                return res
        else:
            return None
def analysis_three_hours(obj, current_pair):
        diff = 45
        average_in_part = long_difference(obj,current_pair,10800, 5)
        if (average_in_part != None):
            print("3 hours differences: " + str(average_in_part)+ " difference = " + str(average_in_part[3] - average_in_part[0]))
            if (average_in_part[3] - average_in_part[0] >= diff):
                res = {"result": True, "difference": average_in_part[3] - average_in_part[0]}
                return res
            else:
                res = {"result": False, "difference": average_in_part[3] - average_in_part[0]}
                return res
        else:
            return None
def analysis_hour(obj, current_pair):
        diff = 35
        average_in_part = long_difference(obj,current_pair,3600, 3)
        if (average_in_part != None):
            print("1 hour differences: " + str(average_in_part)+ " difference = " + str(average_in_part[3] - average_in_part[0]))
            if (average_in_part[3] - average_in_part[0] >= diff):
                res = {"result": True, "difference": average_in_part[3] - average_in_part[0]}
                return res
            else:
                res = {"result": False, "difference": average_in_part[3] - average_in_part[0]}
                return res
        else:
            return None
def analysis_30_min(obj, current_pair):
        diff = 25
        average_in_part = long_difference(obj,current_pair,1800, 3)
        if (average_in_part != None):
            print("30 minutes differences: " + str(average_in_part) + " difference = " + str(average_in_part[3] - average_in_part[0]))
            if (average_in_part[3] - average_in_part[0] >= diff):
                res = {"result": True, "difference": average_in_part[3] - average_in_part[0]}
                return res
            else:
                res = {"result": False, "difference": average_in_part[3] - average_in_part[0]}
                return res
        else:
            return None


def analysis_5_min(obj, current_pair ):
        diff = 10
        average_in_part = long_difference(obj, current_pair, 300, 3)
        if (average_in_part != None):
            print("5 minutes differences: " + str(average_in_part) + " difference = " + str(average_in_part[1] - average_in_part[0]))
            if (average_in_part[1] - average_in_part[0] >= diff):
                res = {"result": True, "difference": average_in_part[1] - average_in_part[0]}
                return res
            else:
                res = {"result": False, "difference": average_in_part[1] - average_in_part[0]}
                return res
        else:
            return None



def buy(obj,current_pair:str):
    can_spend = 1.5

    while True:
        try:
            response = requests.get("https://api.exmo.com/v1/trades/?pair=BTC_USD&limit=100")
        except :
            bot.send_message("@buyingapples", "Connection error : apple tree is not avaliable now...\n" )
            return None
        Unix_time = int(time.time())
        previous_orders =  []
        for order in response.json()[current_pair]:
            if(order["type"] == "buy" and (Unix_time - order["date"]) < 120):
                previous_orders.append(order["price"])
        try:
            sum = 0.0
            for  i  in previous_orders:
                sum += float(i)
            price = sum/len(previous_orders)
        except ZeroDivisionError:
            time.sleep(30)
            continue
        avg_buy_price = price
        buy_dict : dict = {"pair":current_pair,"quantity": float(can_spend/avg_buy_price),"price": avg_buy_price-float(can_spend/avg_buy_price)*0.002*avg_buy_price-avg_buy_price*0.002,"type":"buy"}
        while True:
            result : dict = obj.api_query("order_create" , buy_dict)
            if (result["result"] == False):
                bot.send_message("@buyingapples", "Waiting for order_create to buy ...\n" )
                time.sleep(10)
            else:
                break
        for i in range(8):
            time.sleep(5)
            open_orders : dict = obj.api_query("user_open_orders")
            if len(open_orders)!= 0:
                if len(open_orders) == 1:
                    if open_orders[current_pair][0]["type"] == "sell":
                        break
                    
                    
        open_orders : dict = obj.api_query("user_open_orders")
        if len(open_orders)!= 0:
            if len(open_orders) == 1:
                if open_orders[current_pair][0]["type"] == "buy":
                    obj.api_query("order_cancel",params = {"order_id":open_orders[current_pair][0]["order_id"]})
                    return None
            else:
                if open_orders[current_pair][0]["type"] == "buy":
                    obj.api_query("order_cancel",params = {"order_id":open_orders[current_pair][0]["order_id"]})
                    return None
                if open_orders[current_pair][1]["type"] == "buy":
                    obj.api_query("order_cancel",params = {"order_id":open_orders[current_pair][1]["order_id"]})
                    return None
        return avg_buy_price            
    


def all_for_sell(obj , current_pair , sell_price):
    user_info = obj.api_query("user_info")
    sell_dict : dict = {"pair":current_pair,"quantity": float(user_info["balances"]["BTC"]) ,"price": sell_price,"type":"sell"}
    while True:
        result : dict = obj.api_query("order_create" , sell_dict)
        if (result["result"] == False):
            time.sleep(120)
            bot.send_message("@buyingapples", "Waiting for order_create to sell ...\n" )
        else:
            break
    #user_info = obj.api_query("user_info")
    #bot.send_message("@buyingapples", "Current apples quantity: " + user_info["balances"]["USD"])





def divide_money (obj , current_pair):
    can_spend = 1.5
    while True:
        user_info = obj.api_query("user_info")
        while float(user_info["balances"]["USD"]) >= can_spend:
            print(datetime.datetime.now().time())
            six_hours = analysis_six_hours(obj, current_pair)
            print("Result: ",six_hours["result"])
            three_hours = analysis_three_hours(obj, current_pair)
            print("Result: ",three_hours["result"])
            one_hour = analysis_hour(obj, current_pair)
            print("Result: ",one_hour["result"])
            _30_min = analysis_30_min(obj, current_pair)
            print("Result: ",_30_min["result"])
            _5_min = analysis_5_min(obj, current_pair)
            print("Result: ",_5_min["result"])


            if (six_hours["result"] and three_hours["result"] and one_hour["result"] and _30_min["result"] and _5_min["result"]):
                buy_price = buy(obj, current_pair)
                if buy_price != None:
                    all_for_sell(obj, current_pair, buy_price + 70)
                    user_info = obj.api_query("user_info")
                    time.sleep(300)
                    continue

            if (six_hours["result"] and three_hours["result"] and one_hour["result"] and not( _30_min["result"]) and _5_min["result"]):
                buy_price = buy(obj, current_pair)
                if buy_price != None:
                    all_for_sell(obj, current_pair, buy_price + 50)
                    user_info = obj.api_query("user_info")
                    time.sleep(300)
                    continue

            if (six_hours["result"] and three_hours["result"] and not (one_hour["result"]) and _30_min["result"] and _5_min["result"]):
                buy_price = buy(obj, current_pair)
                if buy_price != None:
                    all_for_sell(obj, current_pair, buy_price + 50)
                    user_info = obj.api_query("user_info")
                    time.sleep(300)
                    continue

            if (six_hours["result"] and three_hours["result"] and not (one_hour["result"]) and not(_30_min["result"]) and _5_min["result"]):
                buy_price = buy(obj, current_pair)
                if buy_price != None:
                    all_for_sell(obj, current_pair, buy_price + 30)
                    user_info = obj.api_query("user_info")
                    time.sleep(300)
                    continue

            if (six_hours["result"] and not(three_hours["result"]) and one_hour["result"] and _30_min["result"] and _5_min["result"]):
                buy_price = buy(obj, current_pair)
                if buy_price != None:
                    all_for_sell(obj, current_pair, buy_price + 50)
                    user_info = obj.api_query("user_info")
                    time.sleep(300)
                    continue

            if (six_hours["result"] and not(three_hours["result"]) and one_hour["result"] and not(_30_min["result"]) and _5_min["result"]):
                buy_price = buy(obj, current_pair)
                if buy_price != None:
                    all_for_sell(obj, current_pair, buy_price + 40)
                    user_info = obj.api_query("user_info")
                    time.sleep(300)
                    continue


            if (six_hours["result"] and not(three_hours["result"]) and not(one_hour["result"]) and _30_min["result"] and _5_min["result"]):
                buy_price = buy(obj, current_pair)
                if buy_price != None:
                    all_for_sell(obj, current_pair, buy_price + 40)
                    user_info = obj.api_query("user_info")
                    time.sleep(300)
                    continue

            if (not(six_hours["result"] )and three_hours["result"] and one_hour["result"] and _30_min["result"] and _5_min["result"]):
                buy_price = buy(obj, current_pair)
                if buy_price != None:
                    all_for_sell(obj, current_pair, buy_price + 40)
                    user_info = obj.api_query("user_info")
                    time.sleep(300)
                    continue


            if (not(six_hours["result"]) and three_hours["result"] and one_hour["result"] and not(_30_min["result"]) and _5_min["result"]):
                buy_price = buy(obj, current_pair)
                if buy_price != None:
                    all_for_sell(obj, current_pair, buy_price + 40)
                    user_info = obj.api_query("user_info")
                    time.sleep(300)
                    continue


            if (not(six_hours["result"]) and three_hours["result"] and not(one_hour["result"]) and _30_min["result"] and _5_min["result"]):
                buy_price = buy(obj, current_pair)
                if buy_price != None:
                    all_for_sell(obj, current_pair, buy_price + 30)
                    user_info = obj.api_query("user_info")
                    time.sleep(300)
                    continue

            if (not(six_hours["result"]) and not(three_hours["result"]) and not(one_hour["result"]) and _30_min["result"] and _5_min["result"]):
                buy_price = buy(obj, current_pair)
                if buy_price != None:
                    all_for_sell(obj, current_pair, buy_price + 30)
                    user_info = obj.api_query("user_info")
                    time.sleep(300)
                    continue

            if (one_hour["difference"] <=0 and one_hour["difference"] >= - 20 and _5_min["difference"] >=5):
                buy_price = buy(obj, current_pair)
                if buy_price != None:
                    all_for_sell(obj, current_pair, buy_price + 25)
                    user_info = obj.api_query("user_info")
                    time.sleep(300)
                    continue

        time.sleep(30)
        user_info = obj.api_query("user_info")
        print("\n\n\n\n")







def trade(obj):
    currency1 = "BTC"
    currency2 = "USD"

    current_pair = currency1 + "_" + currency2

    user_info = obj.api_query("user_info")
    #############Если бот вылетел############################
    if (float(user_info["balances"]["BTC"])!= 0):
       bot.send_message("@buyingapples", "BTC is not empty ...\n" )
       return
    open_orders : dict = obj.api_query("user_open_orders")
    if len(open_orders)!= 0:
        if len(open_orders) == 1:
            if open_orders[current_pair][0]["type"] == "buy":
                obj.api_query("order_cancel",params = {"order_id":open_orders[current_pair][0]["order_id"]})
        else:
            if open_orders[current_pair][0]["type"] == "buy":
                    obj.api_query("order_cancel",params = {"order_id":open_orders[current_pair][0]["order_id"]})
            if open_orders[current_pair][1]["type"] == "buy":
                obj.api_query("order_cancel",params = {"order_id":open_orders[current_pair][1]["order_id"]})
        open_orders : dict = obj.api_query("user_open_orders")
        while len(open_orders) != 0:
            time.sleep(120)
            open_orders : dict = obj.api_query("user_open_orders")
    ##########################################################

    print("Programm is starting...")
    divide_money(obj,current_pair)



trade(obj)