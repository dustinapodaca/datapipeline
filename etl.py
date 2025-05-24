import pandas as pd

def load_data(path):
    return pd.read_csv(path)

def clean_data(df):
    df_clean = df.dropna()
    df_clean = df_clean[df_clean['quantity'] > 0]
    return df_clean

def feature_engineering(df):
    df['total_amount'] = df['quantity'] * df['price']
    return df

if __name__ == "__main__":
    df = load_data("data/raw/transactions.csv")
    df = clean_data(df)
    df = feature_engineering(df)
    df.to_csv("data/processed/transactions_clean.csv", index=False)
    print("ETL pipeline completed successfully!")