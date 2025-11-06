import pandas as pd
from datetime import datetime, timedelta
import requests

def cargar_datos(ticker: str, dias: int = 365):
    print("📊 Probando carga de datos con Stooq...\n")

    fin = datetime.today()
    inicio = fin - timedelta(days=dias)

    # Stooq usa formato AAAAMMDD
    url = f"https://stooq.com/q/d/l/?s={ticker.lower()}.us&i=d"

    try:
        df = pd.read_csv(url)

        if df.empty:
            raise ValueError("No se descargaron datos del ticker.")

        df["Date"] = pd.to_datetime(df["Date"])
        df = df[df["Date"] >= inicio]
        df["Return"] = df["Close"].pct_change() * 100

        print("✅ Datos descargados correctamente desde Stooq:\n")
        print(df.head())

        print("\n📈 Resumen estadístico:")
        print(f"   Retorno Promedio (%): {df['Return'].mean():.2f}")
        print(f"   Volatilidad (%): {df['Return'].std():.2f}")
        print(f"   Retorno Acumulado (%): {((1 + df['Return']/100).prod() - 1)*100:.2f}")

        return df

    except Exception as e:
        print(f"[ERROR] No se pudieron obtener los datos de {ticker}: {e}")
        return pd.DataFrame()


if __name__ == "__main__":
    ticker = "MSFT"
    df = cargar_datos(ticker, dias=365)
    if not df.empty:
        print("\n✅ Prueba finalizada correctamente.")
    else:
        print("⚠️ No se descargaron datos.")