#   python "d:/Trading/Python/Code/Trading system v6.py"
#   Trading system v6 - 
'''
1)      In the first table instead of printing a sorted current RSI values in descending order
rather print the average of all the RSI values of that stock calculating for that current day alone
-   average should be calculated for the 2 minute candle interval data's RSI values

2)      Using jugaad data to print out the next 2 holidays & check if today is a GH or not

3)      THESE ARE THE STOCKS WHICH ARE COMMON IN BOTH THE TABLES
-   print the a separate entire table for these common stocks 

4)      In the 2nd BO table print only the stocks with total volume more than 2 lakh

5)      use the pchange calculator module to calculate pchange from the current day's open price
to the current close price and not from the yesterday's close price, to avoid the gap up and
gap down figures 
-   print only 2 tables as total, one with this sorted pchange value which is calculated from
the current day open value to avoid any gap up and gapdown value second table with sorted BO % value

6)      Print a warning message if any of the current close price of the stocks in the 3 tables that
are PRINTED AS FINAL OUTPUT TABLE is within the 1% of the below given upper or lower circuit prices
-   q[priceInfo][lowerCP]
-   q[priceInfo][upperCP]

7)      Give a ranking system for the Top 10  BREAKOUT percentages that should have the rank score and also
they should have the number of iterations they have been given the mark mentioned along with the score in
the bracket

8)     Give a  Above 20MA or Below 20MA status -
in the Total volume column, along with the volume change numbers, also mention if the current volume bar is
above or below the volume 20MA & how many percentage above is above or below the Volume MA 
For ex - 5% Above 20MA, 30% Below 20MA

9)      When the Jugaad data fails to download a particular stock's data it does not retry, so write a code to retry fetching the same data
for five times. If the retry exceeds 5 times, the program can simply quit and fill that stock's data as 0


10)     then print a separate ORB table which sorted in ascending order of the ORB percentage

11)     While creating OBV also check if those stocks have -
Today's Day candle Low is == to Lowest price q[priceInfo](intradayLowPrice) for a BULLISH OBV trend
Today's Day candle High is == to Hishest price q[priceInfo](intradayHighPrice) for a BEARISH OBV trend
.
Print the stock's name with their current pchange values alone and not a separate table for them
.
Day open == day low OR (day open - 1% of day open)

12)     Print a list of top 5 stocks without a table, where the stocks which have given the 5 minute candle 
breakout and 10 minute candle breakout too
'''


from SCHEDULER import *
from APPENDER import *
from PRINTER import *


from jugaad_data.nse import NSELive
import multiprocessing
import time
import sys
from datetime import datetime

current_process = multiprocessing.current_process()
process_name = current_process.name
event = multiprocessing.Event()

try:
    n = NSELive()
except Exception as e:
    print ('\n\n\n\n\n\n',repr(e))
    print ('There is NO INTERNET CONNECTION dude...!!\n\n\n\n\n\n')
    sys.exit(1)



eqList = [
    "AARTIIND.NS", "ABB.NS", "ABBOTINDIA.NS", "ABCAPITAL.NS", "ABFRL.NS", "ACC.NS", "ADANIENT.NS", "ADANIPORTS.NS",
    "ALKEM.NS", "AMBUJACEM.NS", "APOLLOHOSP.NS", "APOLLOTYRE.NS", "ASHOKLEY.NS", "ASIANPAINT.NS", "ASTRAL.NS",
    "ATUL.NS", "AUBANK.NS", "AUROPHARMA.NS", "AXISBANK.NS", "BAJAJ-AUTO.NS", "BAJAJFINSV.NS", "BAJFINANCE.NS",
    "BALKRISIND.NS", "BALRAMCHIN.NS", "BANDHANBNK.NS", "BANKBARODA.NS", "BATAINDIA.NS", "BEL.NS", "BERGEPAINT.NS",
    "BHARATFORG.NS", "BHARTIARTL.NS", "BHEL.NS", "BIOCON.NS", "BOSCHLTD.NS", "BPCL.NS", "BRITANNIA.NS", "BSOFT.NS",
    "CANBK.NS", "CANFINHOME.NS", "CHAMBLFERT.NS", "CHOLAFIN.NS", "CIPLA.NS", "COALINDIA.NS", "COFORGE.NS", "COLPAL.NS",
    "CONCOR.NS", "COROMANDEL.NS", "CROMPTON.NS", "CUB.NS", "CUMMINSIND.NS", "DABUR.NS", "DALBHARAT.NS", "DEEPAKNTR.NS",
    "DELTACORP.NS", "DIVISLAB.NS", "DIXON.NS", "DLF.NS", "DRREDDY.NS", "EICHERMOT.NS", "ESCORTS.NS", "EXIDEIND.NS",
    "FEDERALBNK.NS", "GAIL.NS", "GLENMARK.NS", "GMRINFRA.NS", "GNFC.NS", "GODREJCP.NS", "GODREJPROP.NS", "GRANULES.NS",
    "GRASIM.NS", "GUJGASLTD.NS", "HAL.NS", "HAVELLS.NS", "HCLTECH.NS", "HDFCAMC.NS", "HDFCBANK.NS", "HDFCLIFE.NS",
    "HEROMOTOCO.NS", "HINDALCO.NS", "HINDCOPPER.NS", "HINDPETRO.NS", "HINDUNILVR.NS", "IBULHSGFIN.NS", "ICICIBANK.NS",
    "ICICIGI.NS", "ICICIPRULI.NS", "IDEA.NS", "IDFC.NS", "IDFCFIRSTB.NS", "IEX.NS", "IGL.NS", "INDHOTEL.NS", "INDIACEM.NS",
    "INDIAMART.NS", "INDIGO.NS", "INDUSINDBK.NS", "INDUSTOWER.NS", "INFY.NS", "IOC.NS", "IPCALAB.NS", "IRCTC.NS",
    "ITC.NS", "JINDALSTEL.NS", "JKCEMENT.NS", "JSWSTEEL.NS", "JUBLFOOD.NS", "KOTAKBANK.NS", "LTF.NS", "LALPATHLAB.NS",
    "LAURUSLABS.NS", "LICHSGFIN.NS", "LT.NS", "LTIM.NS", "LTTS.NS", "LUPIN.NS", "M&M.NS", "M&MFIN.NS", "MANAPPURAM.NS",
    "MARICO.NS", "MARUTI.NS", "UNITDSPR.NS", "MCX.NS", "METROPOLIS.NS", "MFSL.NS", "MGL.NS", "MOTHERSON.NS", "MPHASIS.NS",
    "MRF.NS", "MUTHOOTFIN.NS", "NATIONALUM.NS", "NAUKRI.NS", "NAVINFLUOR.NS", "NESTLEIND.NS", "NMDC.NS", "NTPC.NS",
    "OBEROIRLTY.NS", "OFSS.NS", "ONGC.NS", "PAGEIND.NS", "PEL.NS", "PERSISTENT.NS", "PETRONET.NS", "PFC.NS", "PIDILITIND.NS",
    "PIIND.NS", "PNB.NS", "POLYCAB.NS", "POWERGRID.NS", "PVRINOX.NS", "RAMCOCEM.NS", "RBLBANK.NS", "RECLTD.NS", "RELIANCE.NS",
    "SAIL.NS", "SBICARD.NS", "SBILIFE.NS", "SBIN.NS", "SHREECEM.NS", "SHRIRAMFIN.NS", "SIEMENS.NS", "SRF.NS", "SUNPHARMA.NS",
    "SUNTV.NS", "SYNGENE.NS", "TATACHEM.NS", "TATACOMM.NS", "TATACONSUM.NS", "TATAMOTORS.NS", "TATAPOWER.NS", "TATASTEEL.NS",
    "TCS.NS", "TECHM.NS", "TITAN.NS", "TORNTPHARM.NS", "TRENT.NS", "TVSMOTOR.NS", "UBL.NS", "ULTRACEMCO.NS", "UPL.NS",
    "VEDL.NS", "VOLTAS.NS", "WIPRO.NS", "ZEEL.NS", "ZYDUSLIFE.NS"
]


#eqList = ["INFY.NS", "AUBANK.NS","ITC.NS","WIPRO.NS","TCS.NS", 'HDFCBANK.NS', 'ICICIBANK.NS','BHARTIARTL.NS', 'SBIN.NS', "HEROMOTOCO.NS"]


# Nifty 200 stocks
'''
eqList = ["ABB.NS", "ACC.NS","APLAPOLLO.NS", "AUBANK.NS", "ADANIENSOL.NS", "ADANIENT.NS", "ADANIGREEN.NS", "ADANIPORTS.NS", "UNITDSPR.NS",
"ADANIPOWER.NS", "ATGL.NS", "ABCAPITAL.NS", "ABFRL.NS", "ALKEM.NS", "AMBUJACEM.NS", "APOLLOHOSP.NS", "APOLLOTYRE.NS", "ASHOKLEY.NS", 
"ASIANPAINT.NS", "ASTRAL.NS", "AUROPHARMA.NS", "DMART.NS", "AXISBANK.NS", "BSE.NS", "BAJAJ-AUTO.NS", "BAJFINANCE.NS", "BAJAJFINSV.NS", 
"BAJAJHLDNG.NS", "BALKRISIND.NS", "BANDHANBNK.NS", "BANKBARODA.NS", "BANKINDIA.NS", "MAHABANK.NS", "BERGEPAINT.NS", "BDL.NS",  
"BHARATFORG.NS", "BHEL.NS", "BPCL.NS", "BHARTIARTL.NS", "BIOCON.NS", "BOSCHLTD.NS", "BRITANNIA.NS", "CGPOWER.NS", "CANBK.NS", "CHOLAFIN.NS", 
"CIPLA.NS", "COALINDIA.NS", "COFORGE.NS", "COLPAL.NS", "CONCOR.NS", "CUMMINSIND.NS", "DLF.NS", "DABUR.NS", "DALBHARAT.NS", "DEEPAKNTR.NS", 
"DELHIVERY.NS", "DIVISLAB.NS", "DIXON.NS", "LALPATHLAB.NS", "DRREDDY.NS", "EICHERMOT.NS", "ESCORTS.NS", "NYKAA.NS", "FEDERALBNK.NS", 
"FACT.NS", "FORTIS.NS", "GAIL.NS", "GMRINFRA.NS", "GLAND.NS", "GODREJCP.NS", "GODREJPROP.NS", "GRASIM.NS", "GUJGASLTD.NS", "HCLTECH.NS", 
"HDFCAMC.NS", "HDFCBANK.NS", "HDFCLIFE.NS", "HAVELLS.NS", "HEROMOTOCO.NS", "HINDALCO.NS", "HAL.NS", "HINDPETRO.NS", "HINDUNILVR.NS", 
"ICICIBANK.NS", "ICICIGI.NS", "ICICIPRULI.NS", "IDBI.NS", "IDFCFIRSTB.NS", "ITC.NS", "INDIANB.NS", "INDHOTEL.NS", "IOC.NS", "SIEMENS.NS",
"IRFC.NS", "IGL.NS", "INDUSTOWER.NS", "INDUSINDBK.NS", "NAUKRI.NS", "INFY.NS", "INDIGO.NS", "IPCALAB.NS","JSWENERGY.NS", "JSWINFRA.NS",
"JSWSTEEL.NS", "JINDALSTEL.NS", "JIOFIN.NS", "JUBLFOOD.NS", "KPITTECH.NS", "KALYANKJIL.NS","BEL.NS","IRCTC.NS","PNB.NS","M&MFIN.NS",
"KOTAKBANK.NS", "LTF.NS", "LTTS.NS", "LICHSGFIN.NS", "LTIM.NS", "LT.NS", "LAURUSLABS.NS", "LICI.NS", "LUPIN.NS", "MRF.NS", "LODHA.NS", 
"M&M.NS", "MANKIND.NS", "MARICO.NS", "MARUTI.NS", "MFSL.NS", "MAXHEALTH.NS", "MPHASIS.NS", "NHPC.NS", "NMDC.NS", "NTPC.NS",
"NESTLEIND.NS", "OBEROIRLTY.NS", "ONGC.NS", "OIL.NS", "PAYTM.NS", "OFSS.NS", "POLICYBZR.NS", "PIIND.NS", "PAGEIND.NS", "PATANJALI.NS",
"PERSISTENT.NS", "PETRONET.NS", "PIDILITIND.NS", "PEL.NS", "POLYCAB.NS", "POONAWALLA.NS", "PFC.NS", "POWERGRID.NS", "PRESTIGE.NS", 
"RECLTD.NS", "RVNL.NS", "RELIANCE.NS", "SBICARD.NS", "SBILIFE.NS", "SJVN.NS", "SRF.NS", "MOTHERSON.NS", "SHREECEM.NS", "SHRIRAMFIN.NS", 
"SONACOMS.NS", "SBIN.NS", "SAIL.NS", "SUNPHARMA.NS", "SUNTV.NS", "SUPREMEIND.NS", "SUZLON.NS", "SYNGENE.NS", "TVSMOTOR.NS", "TATACHEM.NS",
"TATACOMM.NS", "TCS.NS", "TATACONSUM.NS", "TATAELXSI.NS", "TATAMTRDVR.NS", "TATAMOTORS.NS", "TATAPOWER.NS", "TATASTEEL.NS", "TATATECH.NS",
"TECHM.NS", "TITAN.NS", "TORNTPHARM.NS", "TORNTPOWER.NS", "TRENT.NS", "TIINDIA.NS", "UPL.NS", "ULTRACEMCO.NS", "UNIONBANK.NS", "ZYDUSLIFE.NS",
"VBL.NS", "VEDL.NS", "IDEA.NS", "VOLTAS.NS", "WIPRO.NS", "YESBANK.NS", "ZEEL.NS", "ZOMATO.NS", "MAZDOCK.NS"]
'''


# RUN THIS CODE FROM THE START OF THE MARKET AT - 9:19:30am
#   Enable this daily morning in    ====>    SCHEDULER python file in while loop of SCHEDULE_TASK() function
#   Also disbale the trading_system_start_time variable current time assignment in the below given Main function
target_start_hour, target_start_minute, target_start_second = 9, 16, 40 
trading_system_start_time = datetime.now().replace(hour=target_start_hour, minute=target_start_minute, second=target_start_second)


def THE_MAIN(j,Stock,pChange,total_traded_volume,last_three_volume,twenty_ma,up_and_low_circuit,orb,ten_min_bo_dict,five_min_bo_dict,two_min_RSI_avg,five_min_RSI_avg,
            breakout,bopp,yfd_dict,lock,final_ORB_dict,ten_min_bo,five_min_bo,processes,final_pchange_output_dict,final_breakout_dict,
            final_upper_lower_circuit_dict,jg_stock_quote,ranking_iter,ranking_dict):
    while True:
        # use this start_time for automating the server to run from 9:16:40
        start_time = datetime.now()
        #start_time = start_time.replace(hour=9, minute=16, second=0, microsecond=0)
        j += 1
        
        target_change_hour, target_change_minute, target_change_second = 9, 45, 0
        period_change_time_1 = datetime.now().replace(hour=target_change_hour, minute=target_change_minute, second=target_change_second)
        
        target_change_hour, target_change_minute, target_change_second = 11, 00, 0
        period_change_time_2 = datetime.now().replace(hour=target_change_hour, minute=target_change_minute, second=target_change_second)
        
        current_time = datetime.now()
        
        if current_time <= period_change_time_1:
            period_for_2m = 'before'
        else:
            period_for_2m = 'after'
        
        if current_time <= period_change_time_2:
            period_for_5m = 'before'
        else:
            period_for_5m = 'after'
        
        i=0
        y=0
        
        curr_time = datetime.now()
        print ('\n\n\n\n\n\n\nSTARTING TO FETCH YFINANCE DATA AT = ',curr_time.strftime("%H:%M:%S"))
        
        for i in range(0,2):
            y+=1
            data_fetching_process = multiprocessing.Process(
                target=SCHEDULE_TASK,                        ############## SCHEDULER.py file
                args=(y,yfd_dict,lock,period_for_2m,period_for_5m,trading_system_start_time,event,eqList))
            processes.append(data_fetching_process)
            data_fetching_process.start()
        for process in processes:
            process.join()
        
        ct = datetime.now()
        print ('YFINANCE DATA FETCHING ENDED AT = ',ct.strftime("%H:%M:%S"))
        time_diff = ct - curr_time
        time_diff = time_diff.total_seconds()
        print(f'It took = {time_diff} seconds to fetch the YAHOO FINANCE data')
        print ('\n\n')

        i=0
        num_processor_cores = multiprocessing.cpu_count()
        chunk_size = len(eqList) // num_processor_cores
        
        for i in range(num_processor_cores):            
            start = i * chunk_size
            end = start + chunk_size if i < num_processor_cores - 1 else len(eqList)
            
            data_processing_process = multiprocessing.Process(
                target=DATA_PROCESSOR,                         ##############  APPENDER.py file
                args=(start,end,yfd_dict,period_for_5m,two_min_RSI_avg, five_min_RSI_avg, Stock,
                total_traded_volume, pChange, lock, breakout, bopp,twenty_ma,up_and_low_circuit,orb,
                last_three_volume,eqList,event,n,jg_stock_quote,ten_min_bo,five_min_bo))
            processes.append(data_processing_process)
            data_processing_process.start()

        for process in processes:
            process.join()
        
        border_line = []
        for i in range(len(Stock)):
            border_line.append('|')


        def JUGAAD_DATA(n,l):
            l+=1
            try:
                nifty200 = n.live_index("NIFTY 200")
            except Exception as e:
                print ('\n\n\n\n\n\n',repr(e))
                print ('\n\n\n\n\n\nERROR = Couldnt reach the NSE server for the LIVE INDEX data,\nSo retrying again to fetch the data..........\n\n\n\n\n\n')
                if l < 5:
                    JUGAAD_DATA(n,l)
            return nifty200
        l=0
        nifty200 = JUGAAD_DATA(n,l)
        advances = int(nifty200['advance']['advances'])
        declines = int(nifty200['advance']['declines'])
        unchanged = int(nifty200['advance']['unchanged'])
        
        final_upper_lower_circuit_dict.update({'Stock': list(Stock)})
        final_upper_lower_circuit_dict.update({'Circuit level': list(up_and_low_circuit)})
        
        final_pchange_output_dict.update({'pChange': list(pChange)})
        #final_pchange_output_dict.update({'Avg RSI(14) 2m': list(two_min_RSI_avg)})
        # final_pchange_output_dict.update({'RSI(14) 5m': list(five_min_RSI_avg)})
        # If you want to print the above column, remove the commenting on RSI average calucator function in Appender.py file in Data_processor() function
        final_pchange_output_dict.update({'Stock': list(Stock)})
        final_pchange_output_dict.update({'BO price percentage': list(bopp)})
        final_pchange_output_dict.update({'Last 3 Volume changes': list(last_three_volume)})
        final_pchange_output_dict.update({'Volume 20 Moving Avg': list(twenty_ma)})
        final_pchange_output_dict.update({'Total Volume': list(total_traded_volume)})
        
        #final_breakout_dict.update({'Avg 2mRSI': list(two_min_RSI_avg)})
        final_breakout_dict.update({'pChange': list(pChange)})
        final_breakout_dict.update({'|': list(border_line)})
        # final_breakout_dict.update({'RSI(14) 5m': list(five_min_RSI_avg)})
                # If you want to print the above column, remove the commenting on
                # RSI average calucator function in Appender.py file in Data_processor() function
        #final_breakout_dict.update({'Total Volume': list(total_traded_volume)})
        #final_breakout_dict.update({'Volume 20 Moving Avg': list(twenty_ma)})
        #final_breakout_dict.update({'Last 3 Volume changes': list(last_three_volume)})
                # When you uncomment these above lines of volume columns, also uncomment
                # the ["Total Volume"] line in the DATAFRAME_GENERATOR() function
        final_breakout_dict.update({'BO Trend': list(breakout)})
        final_breakout_dict.update({'-': list(border_line)})
        final_breakout_dict.update({'Stock': list(Stock)})
        final_breakout_dict.update({'=': list(border_line)})
        final_breakout_dict.update({'ORB %': list(orb)})
        final_breakout_dict.update({'*': list(border_line)})
        final_breakout_dict.update({'BO price percentage': list(bopp)})
        final_breakout_dict.update({'+': list(border_line)})
        
        
        final_ORB_dict.update({'Stock': list(Stock)})
        final_ORB_dict.update({'|': list(border_line)})
        #final_ORB_dict.update({'Avg 2mRSI': list(two_min_RSI_avg)})
        #final_ORB_dict.update({'-': list(border_line)})
        final_ORB_dict.update({'BO Trend': list(breakout)})
        final_ORB_dict.update({'=': list(border_line)})
        final_ORB_dict.update({'BO price percentage': list(bopp)})
        final_ORB_dict.update({'+': list(border_line)})
        final_ORB_dict.update({'ORB %': list(orb)})
        
        
        ten_min_bo_dict.update({'|': list(border_line)})
        ten_min_bo_dict.update({'Stock': list(Stock)})
        ten_min_bo_dict.update({'+': list(border_line)})
        ten_min_bo_dict.update({'10min BO': list(ten_min_bo)})
        
        
        five_min_bo_dict.update({'|': list(border_line)})
        five_min_bo_dict.update({'Stock': list(Stock)})
        five_min_bo_dict.update({'+': list(border_line)})
        five_min_bo_dict.update({'5min BO': list(five_min_bo)})
        
        
        
        df_generating_process = multiprocessing.Process(
                target=DATAFRAME_GENERATOR,             #############  PRINTER.py file
                args=(advances,declines,unchanged,j,final_pchange_output_dict,final_breakout_dict,final_upper_lower_circuit_dict,
                    jg_stock_quote,ranking_iter,ranking_dict,eqList,final_ORB_dict,ten_min_bo_dict,five_min_bo_dict))
        df_generating_process.start()
        df_generating_process.join()
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        #       Remove the Nifty 200 stocks and include the 180 FnO stocks by getting the list of fno stocks using nselib
        
        #       Write the meaning of = Todays strong BULLISH stocks are :-
        #       &  Todays strong BEARISH stocks are :-
        
        
        
        #       For the first 5 min of the market just print the 5min BO,
        #       then the first 10 min of the market print the both 5min & 10min BO and so on............
        
        #       Remove the = The top sorted ORB STOCKS are :- table & 
        #       Instead add a simple Volume breakout table, with the number of times increase of the current 5min volume bar
        #       For this create a simple table where all the stock's current 5 min volume is divided by their 
        #       total volume average and then if the difference is more than 4 times append it to the table
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        # This loop checks for both, Day open = Day low & Day open = Day High stocks
        
        for i in range(len(eqList)):
            yf_all_stocks_data = yfd_dict['5m']
            yf_data = yf_all_stocks_data[(eqList[i])]
            
            strong_bullish_stocks = []
            bullish_pchg = []
            strong_bearish_stocks = []
            bearish_pchg = []
            
            if period_for_5m == 'before': 
                todays_data = yf_data[yf_data.index.date == pd.to_datetime('today').date()]  
                todays_open_data = list(todays_data['Open'])
                day_open = todays_open_data[-1]
            
            if period_for_5m == 'after': 
                todays_open_data = list(yf_data['Open'])
                day_open = todays_open_data[-1]
            
            jg_stock_data = jg_stock_quote[eqList[i].replace(".NS", "")]
            
            a = (day_open/100) * 99.5
            b = (day_open/100) * 100.5
            
            
            #if day_open >= jg_stock_data[3]:
            if a <=jg_stock_data[3]:
                strong_bullish_stocks.append(eqList[i].replace(".NS", ""))
                bullish_pchg.append(pChange[i])

            #if day_open <= jg_stock_data[4]:
            if b >=jg_stock_data[4]:
                strong_bearish_stocks.append(eqList[i].replace(".NS", ""))
                bearish_pchg.append(pChange[i])
        
        print ('\n\n')
        print ('='*83)
        print ('='*83)
        print('\nTodays strong BULLISH stocks are :-')
        for i in range(len(strong_bullish_stocks)):
            print (f'{strong_bullish_stocks[i]} ({bullish_pchg[i]}%)')
        print('Todays strong BEARISH stocks are :-')
        for i in range(len(strong_bearish_stocks)):
            print (f'{strong_bearish_stocks[i]} ({bearish_pchg[i]}%)')
        
        
        
        
        
        
        Stock = manager.list()
        pChange = manager.list()
        total_traded_volume = manager.list()
        twenty_ma = manager.list()
        last_three_volume = manager.list()
        ten_min_bo = manager.list()
        five_min_bo = manager.list()
        two_min_RSI_avg = manager.list()
        five_min_RSI_avg = manager.list()
        
        breakout = manager.list()
        bopp = manager.list()
        yfd_dict = manager.dict()
        jg_stock_quote = manager.dict()
        up_and_low_circuit = manager.list()
        orb = manager.list()
        
        
        processes = []
        final_pchange_output_dict = {}
        final_breakout_dict = {}
        final_upper_lower_circuit_dict = {}
        final_ORB_dict = {}
        ten_min_bo_dict = {}
        five_min_bo_dict = {}

        current_time = datetime.now()
        # Calculate the time difference between now and the start time
        
        time_difference = current_time - start_time
        time_difference = time_difference.total_seconds()
        
        if 150 > time_difference:
            time_left = 150 - time_difference
            print (f'\nIt took {time_difference} seconds to run & complete the {ranking_iter.value - 1}th iteration of this program')
        else:
            time_left = 1
            print (f'\nIt took {time_difference} seconds to run & complete the {ranking_iter.value - 1}th iteration of this program\nAs it has crossed 2 minutes, so rerunning this program just after the next {time_left} seconds............')
        
        # print ('*'*150)
        # print ('*'*150)
        time.sleep(time_left)
        #sys.exit(1)



if __name__ == '__main__':
    multiprocessing.freeze_support()
    manager = multiprocessing.Manager()
    
    print ('\n\nthe code has started to run.......')
    
    #   Disable the below line before enabling the live server just before the market time
    trading_system_start_time = datetime.now()
    
    if trading_system_start_time < datetime.now():
        print (f"Adangomma, the specified time {trading_system_start_time} has already passed daa....!!")
        print ("exiting the program !!")
        sys.exit(1)


    orb = manager.list()
    bopp = manager.list()
    Stock = manager.list()
    pChange = manager.list()
    breakout = manager.list()
    twenty_ma = manager.list()
    ten_min_bo = manager.list()
    five_min_bo = manager.list()
    two_min_RSI_avg = manager.list()
    five_min_RSI_avg = manager.list()
    last_three_volume = manager.list()
    up_and_low_circuit = manager.list()
    total_traded_volume = manager.list()
    
    yfd_dict = manager.dict()
    ranking_dict = manager.dict()
    jg_stock_quote = manager.dict()
    
    lock = manager.Lock()
    
    ranking_iter = manager.Value('i', 1)
    
    processes = []
    final_pchange_output_dict = {}
    final_breakout_dict = {}
    final_ORB_dict = {}
    final_upper_lower_circuit_dict = {}
    ten_min_bo_dict = {}
    five_min_bo_dict = {}

    j = 0
    
    THE_MAIN(j,Stock,pChange,total_traded_volume,last_three_volume,twenty_ma,up_and_low_circuit,orb,ten_min_bo_dict,five_min_bo_dict,
        two_min_RSI_avg,five_min_RSI_avg,breakout,bopp,yfd_dict,lock,final_ORB_dict,ten_min_bo,five_min_bo,
        processes,final_pchange_output_dict,final_breakout_dict,final_upper_lower_circuit_dict,jg_stock_quote,ranking_iter,ranking_dict)