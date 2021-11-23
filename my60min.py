import pyupbit 
import pandas 
import datetime 
import time
import telegram

# 60분봉 이평선 기준 120이평선 돌파시 매수전략
# 매수조건>>
# 조건 1 : 직전 20이평선 < 직전 120이평선
# 조건 2 : 직전 고가 < 직전 120이평선
# 조건 3 : 현재가 >= 현재 120이평선

# 매도조건>>
# 조건 1 : RSI 70 이상
# 조건 2 : 수익율 2% 이상


def get_now_120_ma60(coin):
    """60분봉 120 이동 평균선 조회"""
    df = pyupbit.get_ohlcv(coin, interval="minute60", count=200)
    now_120_ma60 = df['close'].rolling(120).mean().iloc[-1]
    return now_120_ma60
    # ma60 = get_ma60(coinlist[i])

def get_recent_20_ma60(coin):
    """60분봉 직전 20 이동 평균선 조회"""
    df = pyupbit.get_ohlcv(coin, interval="minute60", count=200)
    recent_20_ma60 = df['close'].rolling(20).mean().iloc[-2]
    return recent_20_ma60
    # recent_20_ma60 = get_recent_20_ma60(coinlist[i])

def get_recent_120_ma60(coin):
    """60분봉 직전 120 이동 평균선 조회"""
    df = pyupbit.get_ohlcv(coin, interval="minute60", count=200)
    recent_120_ma60 = df['close'].rolling(120).mean().iloc[-2]
    return recent_120_ma60
    # recent_120_ma60 = get_recent_120_ma60(coinlist[i])

def get_recent_high(coin):
    """직전 고가 구하기"""
    df = pyupbit.get_ohlcv(coin, interval="minute60", count=200)
    recent_price = df.iloc[-2]
    #now_open = rescent_price['close']
    recent_high = recent_price['high']
    #recent_low = recent_recent['low']
    #target = now_open + (recent_high - recent_low) * 0.5
    return recent_high
    # recent_high = get_recent_high(coinlist[i])
    # recent_120_ma60 = get_recent_120_ma60(coinlist[i])
    # recent_20_ma60 = get_recent_20_ma60(coinlist[i])
    # ma60 = get_ma60(coinlist[i])

def rsi(ohlc: pandas.DataFrame, period: int = 14):
    delta = ohlc["close"].diff()
    ups, downs = delta.copy(), delta.copy()
    ups[ups < 0] = 0 
    downs[downs > 0] = 0
    
    AU = ups.ewm(com = period-1, min_periods = period).mean() 
    AD = downs.abs().ewm(com = period-1, min_periods = period).mean() 
    RS = AU/AD

    return pandas.Series(100 - (100/(1 + RS)), name = "RSI")

# 시장가 매수 함수 
def buy(coin): 
    money = upbit.get_balance("KRW")

    if money > 50500 : 
        res = upbit.buy_market_order(coin, 50000) 
        print(coin, "120 dolpa buy")
    return

    
# 시장가 매도 함수 
def sell(coin): 
    amount = upbit.get_balance(coin) 
    cur_price = pyupbit.get_current_price(coin) 
    total = amount * cur_price 
    
    if total > 5000 : 
        res = upbit.sell_market_order(coin, amount) 
        print(coin, "120 dolpa sold")
    return


# """ Send MSG""" # Send Msg
# bot = telegram.Bot(token='2110067438:AAF8-6tHX0u2HrrH1wmEgygEsa389gub3n8')
# chat_id = 1860357696


# 이용할 코인 리스트 
coinlist_all = pyupbit.get_tickers(fiat="KRW")
coinlist_rsi = ["KRW-BTC", "KRW-XRP", "KRW-ETC", "KRW-ETH", "KRW-POWR", "KRW-CRO", "KRW-VET", "KRW-AQT", "KRW-AXS", "KRW-EOS", "KRW-BORA", "KRW-PLA", "KRW-WAXP", "KRW-MANA", "KRW-SAND", "KRW-QKC", "KRW-HIVE", "KRW-HUNT", "KRW-DOGE", "KRW-CHZ", "KRW-ADA", "KRW-MOC", "KRW-DOT"] # Coin ticker 추가 
c1 = set(coinlist_all)
c2 = set(coinlist_rsi)
c3 = c1 - c2
coinlist = list(c3)

# 스위치 생성
dolpa_120 = []

# initiate
for i in range(len(coinlist)):
    dolpa_120.append(False)

# 거래시작
access = "access key"   
secret = "secret key"   
upbit = pyupbit.Upbit(access, secret)


while(True):
    for i in range(len(coinlist)):
        try:
            recent_high = get_recent_high(coinlist[i])
            recent_120_ma60 = get_recent_120_ma60(coinlist[i])
            recent_20_ma60 = get_recent_20_ma60(coinlist[i])
            now_120_ma60 = get_now_120_ma60(coinlist[i])
            amount = upbit.get_balance(coinlist[i])
            av_buy = float(upbit.get_avg_buy_price(coinlist[i]))
            profit_price = round(av_buy*1.02, 4)   
            cur_price = pyupbit.get_current_price(coinlist[i]) 
            total = amount * cur_price
            data_1 = pyupbit.get_ohlcv(ticker=coinlist[i], interval="minute60")
            now_rsi_60 = rsi(data_1, 14).iloc[-1]
            print(coinlist[i], "< RSI 60 > :", now_rsi_60)
            
            if recent_20_ma60 < recent_120_ma60 and recent_high < recent_120_ma60 and cur_price >= now_120_ma60 :
                dolpa_120 = True
                # print(coinlist[i], "120 dolpa")
            elif dolpa_120 == True and total < 95000 :
                buy(coinlist[i])             
                print(coinlist[i], "120 dolpa buy")
#                 sendMsg = str(coinlist[i]), "< 120 Dolpa Breakout >" 
#                 bot.sendMessage(chat_id=chat_id, text=sendMsg)
            elif now_rsi_60 >= 70 and cur_price >= profit_price :
                sell(coinlist[i])
                dolpa_120 = False
                print(coinlist[i], "120 dolpa sold")
#                 sendMsg = str(coinlist[i]), "< 120 Dolpa Breakout >" 
#                 bot.sendMessage(chat_id=chat_id, text=sendMsg)
            time.sleep(0.1)
            
        except Exception as e:
            print(e)
            time.sleep(0.1)        
