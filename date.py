import yfinance as yf
import pandas as pd
import pandas_ta as ta
import requests
import io


import requests
import pandas as pd
import io

def get_sp500_tickers():
    url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    response = requests.get(url, headers=headers)
    
    
    if response.status_code != 200:
        print(f"Eroare la accesarea Wikipedia: Cod {response.status_code}")
        return []

    try:
        df = pd.read_html(io.BytesIO(response.content))[0]
        
        tickers = df['Symbol'].tolist()
        tickers = [t.replace('.', '-') for t in tickers]
        
        return tickers
        
    except Exception as e:
        print(f"Nu am putut extrage tabelul: {e}")
        return []
def process_ticker(ticker):
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        
        fundamentals = {
            'Forward_PE': info.get('forwardPE', np.nan),
            'Trailing_EPS': info.get('trailingEps', np.nan),
            'Profit_Margins': info.get('profitMargins', np.nan),
            'Debt_to_Equity': info.get('debtToEquity', np.nan),
            'Return_on_Equity': info.get('returnOnEquity', np.nan),
            'Revenue_Growth': info.get('revenueGrowth', np.nan)
        }
        
        df = stock.history(period="2y")
        
        if len(df) < 200: return None 

        df['RSI'] = ta.rsi(df['Close'], length=14)
        df['SMA_50'] = ta.sma(df['Close'], length=50)
        
        df['Price_vs_SMA50'] = df['Close'] / df['SMA_50']
        
        for key, value in fundamentals.items():
            df[key] = value
            
        df['Ticker'] = ticker
        
        df['Target'] = (df['Close'].shift(-1) > df['Close']).astype(int)
        
        df.dropna(inplace=True)
        return df
        
    except Exception as e:
        print(f"  Eroare la {ticker}: {e}")
        return None

import numpy as np

tickers = get_sp500_tickers()

print(f"Am găsit {len(tickers)} companii. Încep descărcarea (asta va dura)...")

all_data = []
for i, t in enumerate(tickers):
    print(f"[{i+1}/{len(tickers)}] Procesez {t}...")
    df_ticker = process_ticker(t)
    if df_ticker is not None:
        all_data.append(df_ticker)

print("Concatenare date...")
if all_data:
    final_df = pd.concat(all_data)
    final_df.to_csv('C:/Users/user/Desktop/python/modelBursa/BIG_DATASET_BURSA.csv')
    print(f"GATA! Dataset salvat cu {len(final_df)} rânduri.")
    print("Coloane:", final_df.columns.tolist())
else:
    print("Nu am putut descărca date.")