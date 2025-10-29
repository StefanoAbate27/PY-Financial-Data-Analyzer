# src/data_loader.py

import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

def cargar_datos(ticker: str, dias: int = 365):
    """
    Descarga y prepara datos financieros desde Yahoo Finance usando Ticker.history()
    """
    print("📊 Probando carga de datos con Yahoo Finance...\n")

    fin = datetime.today()
    inicio = fin - timedelta(days=dias)

    try:
        ticker_obj = yf.Ticker(ticker)
        data = ticker_obj.history(start=inicio, end=fin, auto_adjust=False)

        if data.empty:
            raise ValueError("No se descargaron datos del ticker.")

        # --- Asegurar que existan columnas básicas ---
        required_cols = ["Open", "High", "Low", "Close", "Volume"]
        for col in required_cols:
            if col not in data.columns:
                raise KeyError(f"No se encontró la columna '{col}' en los datos descargados.")

        # Renombrar Adj Close si existe
        if "Adj Close" in data.columns:
            data = data.rename(columns={"Adj Close": "Adj_Close"})
            base_col = "Adj_Close"
        else:
            base_col = "Close"

        # Calcular retornos diarios %
        data["Return"] = data[base_col].pct_change() * 100
        data["Date"] = data.index

        # Información del activo
        info = ticker_obj.info

        print("✅ Datos descargados correctamente:\n")
        print(data.head(5))
        print("\nℹ️ Información del activo:")
        print(f"   nombre: {info.get('longName', 'N/A')}")
        print(f"   sector: {info.get('sector', 'N/A')}")
        print(f"   industria: {info.get('industry', 'N/A')}")
        print(f"   descripcion: {info.get('longBusinessSummary', 'N/A')[:200]}...")
        print(f"   moneda: {info.get('currency', 'N/A')}")
        print(f"   mercado: {info.get('market', 'N/A')}")
        print("\n📈 Resumen estadístico:")
        print(f"   Retorno Promedio (%): {data['Return'].mean():.2f}")
        print(f"   Volatilidad (%): {data['Return'].std():.2f}")
        print(f"   Retorno Acumulado (%): {((1 + data['Return']/100).prod() -1)*100:.2f}")

        return data

    except Exception as e:
        print(f"[ERROR] No se pudieron obtener los datos de {ticker}: {e}")
        return pd.DataFrame()


# --- Prueba local ---
if __name__ == "__main__":
    ticker = "AAPL"
    df = cargar_datos(ticker, dias=365)
    if not df.empty:
        print("\n✅ Prueba finalizada correctamente.")
        print(df.head())
    else:
        print("⚠️ No se descargaron datos.")