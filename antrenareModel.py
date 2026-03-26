import pandas as pd
import numpy as np
import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import joblib
import os

BASE_PATH = r'C:\Users\user\Desktop\python\modelBursa'


print("Încărcare CSV...")
csv_path = os.path.join(BASE_PATH, 'BIG_DATASET_BURSA.csv')
df = pd.read_csv(csv_path)

feature_cols = [
    'RSI', 'Price_vs_SMA50', 'Volume', 
    'Forward_PE', 'Trailing_EPS', 'Profit_Margins', 
    'Debt_to_Equity', 'Return_on_Equity', 'Revenue_Growth'
]

df_clean = df.dropna(subset=feature_cols)

X = df_clean[feature_cols].values
y = df_clean['Target'].values

print(f"Antrenăm pe {len(X)} exemple de tranzacționare.")


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=True)

scaler = StandardScaler()

X_train_scaled = scaler.fit_transform(X_train)

X_test_scaled = scaler.transform(X_test)

scaler_path = os.path.join(BASE_PATH, 'scaler_universal.pkl')
joblib.dump(scaler, scaler_path) 
print(f"Scaler salvat în: {scaler_path}")

model = tf.keras.models.Sequential([
    tf.keras.layers.Input(shape=(X_train_scaled.shape[1],)),
    
    tf.keras.layers.Dense(128, activation='relu'),
    tf.keras.layers.Dropout(0.3),
    
    tf.keras.layers.Dense(64, activation='relu'),
    tf.keras.layers.Dropout(0.3),
    
    tf.keras.layers.Dense(32, activation='relu'),
    
    tf.keras.layers.Dense(1, activation='sigmoid')
])

model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
              loss='binary_crossentropy',
              metrics=['accuracy'])

history = model.fit(X_train_scaled, y_train, 
                    epochs=20, 
                    batch_size=64, 
                    validation_data=(X_test_scaled, y_test))

loss, acc = model.evaluate(X_test_scaled, y_test)
print(f"Acuratețe pe date noi: {acc*100:.2f}%")

model_save_path = os.path.join(BASE_PATH, 'model_universal_bursa.keras')
model.save(model_save_path)
print(f"Model salvat în: {model_save_path}")