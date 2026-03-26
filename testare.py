import numpy as np
import pandas as pd
import pandas_ta as ta
import yfinance as yf
import tensorflow as tf
import joblib
import os

MODEL_PATH = 'C:\\Users\\user\\Desktop\\modelBursa\\model_universal_bursa.keras'
SCALER_PATH = 'C:\\Users\\user\\Desktop\\modelBursa\\scaler_universal.pkl'

FEATURE_COLS = [
    'RSI', 'Price_vs_SMA50', 'Volume', 
    'Forward_PE', 'Trailing_EPS', 'Profit_Margins', 
    'Debt_to_Equity', 'Return_on_Equity', 'Revenue_Growth'
]

def get_live_data(ticker):
    print(f"--- Colectez date live pentru {ticker} ---")
    try:
        stock = yf.Ticker(ticker)
        df = stock.history(period="1y")
        
        if len(df) < 50:
            print("Nu am destule date istorice pentru indicatori.")
            return None
            
        df['RSI'] = ta.rsi(df['Close'], length=14)
        df['SMA_50'] = ta.sma(df['Close'], length=50)
        df['Price_vs_SMA50'] = df['Close'] / df['SMA_50']
        
        last_row = df.iloc[-1].copy()
        
        info = stock.info
        
        last_row['Forward_PE'] = info.get('forwardPE', 0)
        last_row['Trailing_EPS'] = info.get('trailingEps', 0)
        last_row['Profit_Margins'] = info.get('profitMargins', 0)
        last_row['Debt_to_Equity'] = info.get('debtToEquity', 0)
        last_row['Return_on_Equity'] = info.get('returnOnEquity', 0)
        last_row['Revenue_Growth'] = info.get('revenueGrowth', 0)
        
        input_data = pd.DataFrame([last_row])
        
        input_data = input_data[FEATURE_COLS]
        
        input_data = input_data.fillna(0)
        
        return input_data

    except Exception as e:
        print(f"Eroare la descărcare date: {e}")
        return None

def predict(ticker):
    if not os.path.exists(MODEL_PATH) or not os.path.exists(SCALER_PATH):
        print("LIPSEȘTE Modelul sau Scalerul!")
        print("Ai rulat 'train_universal.py' și ai salvat scaler-ul?")
        return

    data_df = get_live_data(ticker)
    if data_df is None:
        return

    print("\nDatele extrase pentru analiză:")
    print(data_df.T) 

    model = tf.keras.models.load_model(MODEL_PATH)
    scaler = joblib.load(SCALER_PATH)

   
    data_scaled = scaler.transform(data_df.values)

    prediction = model.predict(data_scaled)
    score = prediction[0][0] 

    print("\n" + "="*40)
    print(f"REZULTAT PENTRU {ticker.upper()}:")
    print(f"Scor Model: {score:.4f}")
    
    if score > 0.5:
        confidence = (score - 0.5) * 2 * 100 
        print(f" SEMNAL: BUY (Cumpără)")
        print(f"Încredere: {confidence:.2f}%")
        if score > 0.8: print("(Semnal Foarte Puternic!)")
    else:
        confidence = (0.5 - score) * 2 * 100
        print(f" SEMNAL: SELL / AVOID (Evită)")
        print(f"Încredere: {confidence:.2f}%")
    print("="*40)

if __name__ == "__main__":
    ticker_input = input("Introdu simbolul companiei (ex: AAPL): ").strip().upper()
    predict(ticker_input)