# Commodity Channel Index Python Code

# Load the necessary packages and modules
import pandas as pd
import numpy as np

# Commodity Channel Index 
def CCI(data, ndays): 
    TP = (data['high'] + data['low'] + data['close']) / 3 
    CCI = pd.Series((TP - TP.rolling(ndays).mean()) / (0.015 * TP.rolling(ndays).std()),
                    name = 'CCI') 
    data = data.join(CCI) 
    return data

# Ease Of Movement (EVM) Code

# Load the necessary packages and modules
 
# Ease of Movement 
def EVM(data, ndays): 
    dm = ((data['high'] + data['low'])/2) - ((data['high'].shift(1) + data['low'].shift(1))/2)
    br = (data['volume'] / 100000000) / ((data['high'] - data['low']))
    EVM = dm / br 
    EVM_MA = pd.Series(EVM.rolling(ndays).mean(), name = 'EVM') 
    data = data.join(EVM_MA)
    data['EVM'] = EVM_MA
    return data 

# Simple Moving Average 
def SMA(data, ndays): 
    SMA = pd.Series(data['close'].rolling(ndays).mean(), name = 'SMA') 
    data = data.join(SMA)
    data['SMA'] = SMA
    return data

# Exponentially-weighted Moving Average 
def EWMA(data, ndays): 
    EMA = pd.Series(data['close'].ewm(span = ndays, min_periods = ndays - 1).mean(), 
                    name = 'EWMA_' + str(ndays)) 
    data = data.join(EMA) 
    data['EWMA'] = EMA
    return data

# Rate of Change (ROC)
def ROC(data,n):
    N = data['close'].diff(n)
    D = data['close'].shift(n)
    ROC = pd.Series(N/D,name='Rate of Change')
    data = data.join(ROC)
    data['ROC'] = ROC
    return data 

# Force Index 
def ForceIndex(data, ndays): 
    FI = pd.Series(data['close'].diff(ndays) * data['volume'], name = 'ForceIndex') 
    data = data.join(FI) 
    data['FI'] = FI
    return data


def DMI(data, n=14, n_ADX=14):
    i = 0
    UpI = [0]
    DoI = [0]

    while i + 1 <= data.index[-1] :
        UpMove = data.loc[i + 1, "high"] - data.loc[i, "high"]
        DoMove = data.loc[i, "low"] - data.loc[i+1, "low"]
        if UpMove > DoMove and UpMove > 0 :
            UpD = UpMove
        else :
            UpD = 0
        UpI.append(UpD)
        if DoMove > UpMove and DoMove > 0 :
            DoD = DoMove
        else :
            DoD = 0
        DoI.append(DoD)
        i = i + 1

    i = 0
    TR_l = [0]
    while i < data.index[-1]:
        TR = max(data.loc[i + 1, 'high'], data.loc[i, 'close']) - min(data.loc[i + 1, 'low'], data.loc[i, 'close'])
        TR_l.append(TR)
        i = i + 1
    TR_s = pd.Series(TR_l)
    ATR = pd.Series(TR_s.ewm(span=n, min_periods=1).mean())
    UpI = pd.Series(UpI)
    DoI = pd.Series(DoI)
    PosDI = pd.Series(UpI.ewm(span=n, min_periods=1).mean() / ATR)
    NegDI = pd.Series(DoI.ewm(span=n, min_periods=1).mean() / ATR)
    ADX = pd.Series((abs(PosDI - NegDI) / (PosDI + NegDI)).ewm(span=n_ADX, min_periods=1).mean(),
                    name='ADX_' + str(n) + '_' + str(n_ADX))
                    
    data["PDI"],data["MDI"],data["ADX"] = PosDI, NegDI, ADX

    return data


# 30이하면 과매도, 70 이상이면 과매수
def fnRSI(df, m_N=7):
    delta = df['close'].diff()

    dUp, dDown = delta.copy(), delta.copy()
    dUp[dUp < 0] = 0
    dDown[dDown > 0] = 0

    RolUp = pd.DataFrame(dUp).rolling(window=14).mean()
    RolDown = pd.DataFrame(dDown).rolling(window=14).mean().abs()

    RS = RolUp / RolDown
    RSI = RS / (1+RS)
    RSI_MACD = pd.DataFrame(RSI).rolling(window=6).mean()
    df['RSI_MACD'] = RSI_MACD

    return df

def faster_OBV(data):
    close, volume = data['close'], data['volume']
    # obv 값이 저장될 리스트를 생성합니다.
    obv_value = [None] * len(close)
    obv_value[0] = volume.iloc[0]
    # 마지막에 사용할 인덱스를 저장해 둡니다.
    index = close.index

    # 연산에서 사용하기 위해 리스트 형태로 바꾸어 줍니다.
    close = list(close)
    volume = list(volume)
    
    # OBV 산출공식을 구현
    for i in range(1,len(close)):
    
        if close[i] > close[i-1] : 
            obv_value[i] = obv_value[i-1] + volume[i]
            
        elif close[i] < close[i-1] :
            obv_value[i] = obv_value[i-1] - volume[i]
            
        else:
            obv_value[i] = obv_value[i-1]
            
    # 계산된 리스트 결과물을 마지막에 Series 구조로 변환해 줍니다.
    obv = pd.Series(obv_value, index=index)
    data['OBV'] = obv
    return data
