S&P 500 Trend Predictor

I built this project to explore how machine learning can be applied to financial markets. The goal wasn't to build a magical trading bot, but rather to see if a deep neural network could identify patterns combining a company's technical indicators (like RSI and Moving Averages) with its fundamental data (like P/E ratios and Profit Margins).

The project is structured into a three-step pipeline:
1. Data Engineering: A script that scrapes the S&P 500 list from Wikipedia and pulls 1-year historical and fundamental data for each company using the Yahoo Finance API.
2. Model Training: A TensorFlow/Keras deep learning model (built with dense layers and dropout for regularization) that takes the scaled data and learns to classify whether a stock's closing price is likely to go up or down the next day.
3. Live Testing: A prediction script where you can input any ticker symbol to fetch its current live data, scale it, and get an immediate prediction confidence score from the trained model.

Tech Stack:
- Python
- TensorFlow / Keras (Deep Learning)
- Scikit-Learn (Data Preprocessing / StandardScaler)
- Pandas & pandas_ta (Data Manipulation & Technical Analysis)
- yfinance (Live Market Data)

Note: For storage efficiency, the generated CSV datasets and the compiled .keras model files might not be included in this repository. However, the scripts to generate the data and train the model from scratch are fully provided. 

Disclaimer: This project is strictly for educational and research purposes. It is not financial advice and should not be used for real-world trading.
