import time
import yfinance as yf
from datetime import datetime


def DATA_FETCHER(per,inte,event,eqList):
    yf_all_stocks_data = yf.download(eqList, group_by='Ticker', period=per, interval=inte)
    event.set() #1
    return yf_all_stocks_data


def SCHEDULE_TASK(y,yfd_dict,lock,period_for_2m,period_for_5m,trading_system_start_time,event,eqList):
    
    if period_for_2m == 'before':
        period_interval_2m = {
            1 : ["2d",'2m'],
        }
    
    if period_for_2m == 'after':
        period_interval_2m = {
            1 : ["1d",'2m'],
        }
    
    if period_for_5m == 'before':
        period_interval_5m = {
            2 : ["2d",'5m'],
        }
    
    if period_for_5m == 'after':
        period_interval_5m = {
            2 : ["1d",'5m'],
        }
    
    while True:
        #   Enable the below line every morning before the market starts
        #current_time = datetime.now()
        current_time = trading_system_start_time
        if current_time >= trading_system_start_time:
            if y == 1:
                pi_2m = period_interval_2m[y]
                yf_all_stocks_data = DATA_FETCHER(pi_2m[0],pi_2m[1],event,eqList) 
                with lock:
                    yfd_dict.update({pi_2m[1]:yf_all_stocks_data})
            if y == 2:
                pi_5m = period_interval_5m[y]
                yf_all_stocks_data = DATA_FETCHER(pi_5m[0],pi_5m[1],event,eqList)
                with lock:
                    yfd_dict.update({pi_5m[1]:yf_all_stocks_data})
            '''
            if y == 3:
                yf_all_stocks_data = DATA_FETCHER('1d','1d',event,eqList)
                with lock:
                    yfd_dict.update({'1d':yf_all_stocks_data})
            '''
            event.wait()    #1
            break
        print(current_time,' =======>>> ',trading_system_start_time)
        time.sleep(5)


if __name__ == "__main__":
    print ('\n\n\nTrading_system_v6.py has the MAIN() function file. So Execute that file.....!!!\n\n\n')