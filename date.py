import yfinance as yf
import pandas as pd
import pandas_ta as ta
import requests
import io

# 1. Funcție pentru a obține lista S&P 500 automat
# Asigură-te că ai aceste importuri la începutul fișierului
import requests
import pandas as pd
import io

def get_sp500_tickers():
    url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
    
    # --- FIXUL ESTE AICI: Headers ---
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    # Trimitem cererea cu headers
    response = requests.get(url, headers=headers)
    
    # Verificăm dacă am primit acces (Cod 200 = OK)
    if response.status_code != 200:
        print(f"Eroare la accesarea Wikipedia: Cod {response.status_code}")
        return []

    # Citim tabelele din conținutul primit
    try:
        # Wikipedia are mai multe tabele, de obicei lista firmelor este primul [0]
        df = pd.read_html(io.BytesIO(response.content))[0]
        
        tickers = df['Symbol'].tolist()
        # Curățăm tickerii (transformăm BRK.B în BRK-B pentru Yahoo Finance)
        tickers = [t.replace('.', '-') for t in tickers]
        
        return tickers
        
    except Exception as e:
        print(f"Nu am putut extrage tabelul: {e}")
        return []
# 2. Funcție pentru a extrage date fundamentale și tehnice
def process_ticker(ticker):
    try:
        # A. Date Fundamentale (Info despre companie)
        # Acestea sunt statice (valabile la ultimul raport)
        stock = yf.Ticker(ticker)
        info = stock.info
        
        # Extragem doar ce ne interesează (gestiune erori dacă lipsesc date)
        fundamentals = {
            'Forward_PE': info.get('forwardPE', np.nan),
            'Trailing_EPS': info.get('trailingEps', np.nan),
            'Profit_Margins': info.get('profitMargins', np.nan),
            'Debt_to_Equity': info.get('debtToEquity', np.nan),
            'Return_on_Equity': info.get('returnOnEquity', np.nan),
            'Revenue_Growth': info.get('revenueGrowth', np.nan)
        }
        
        # B. Date Tehnice (Prețuri istorice - ultimii 2 ani)
        df = stock.history(period="2y")
        
        if len(df) < 200: return None # Ignorăm companiile fără istoric suficient

        # Calculăm Indicatori Tehnici
        df['RSI'] = ta.rsi(df['Close'], length=14)
        df['SMA_50'] = ta.sma(df['Close'], length=50)
        
        # TRUC: Nu folosim prețuri absolute ($150 vs $10). Folosim procente!
        # Cât e prețul față de media mobilă? (1.05 înseamnă 5% peste medie)
        df['Price_vs_SMA50'] = df['Close'] / df['SMA_50']
        
        # C. Combinăm Fundamentalele cu Tehnicele
        # Adăugăm datele fundamentale pe fiecare rând (ele sunt constante pe termen scurt)
        for key, value in fundamentals.items():
            df[key] = value
            
        df['Ticker'] = ticker
        
        # D. Targetul (Prezicem dacă crește mâine)
        df['Target'] = (df['Close'].shift(-1) > df['Close']).astype(int)
        
        # Curățenie
        df.dropna(inplace=True)
        return df
        
    except Exception as e:
        print(f"  Eroare la {ticker}: {e}")
        return None

# --- Rulare Principală ---
import numpy as np

# Pentru testare rapidă, iau doar primele 50. 
# Șterge [:50] ca să le iei pe toate 500!
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