# src/analyzer.py

import pandas as pd
import numpy as np
from data_loader import cargar_datos

def analizar_datos(df: pd.DataFrame):
    """
    Calcula estadísticas financieras básicas de un DataFrame cargado desde Yahoo Finance.
    """
    if df.empty:
        print("⚠️ El DataFrame está vacío, no se puede analizar.")
        return {}

    # --- Asegurarse de que exista la columna de retornos ---
    if "Return" not in df.columns:
        print("⚠️ No existe la columna 'Return' para análisis.")
        return {}

    # --- Eliminar NaN ---
    df = df.dropna(subset=["Return"])

    # --- Estadísticas básicas ---
    retorno_prom = df["Return"].mean()
    volatilidad = df["Return"].std()
    retorno_acum = (1 + df["Return"]/100).prod() - 1

    # --- Sharpe ratio (supuesto riesgo libre = 0) ---
    sharpe_ratio = retorno_prom / volatilidad if volatilidad != 0 else np.nan

    # --- Max Drawdown ---
    cumulative = (1 + df["Return"]/100).cumprod()
    max_dd = ((cumulative / cumulative.cummax()) - 1).min() * 100

    resultados = {
        "Retorno Promedio (%)": retorno_prom,
        "Volatilidad (%)": volatilidad,
        "Retorno Acumulado (%)": retorno_acum*100,
        "Sharpe Ratio": sharpe_ratio,
        "Máximo Drawdown (%)": max_dd
    }

    return resultados

# --- Prueba local ---
if __name__ == "__main__":
    ticker = "AAPL"
    df = cargar_datos(ticker, dias=365)
    if not df.empty:
        print("\n🔍 Iniciando análisis estadístico...\n")
        resultados = analizar_datos(df)
        print("📊 Resultados del análisis:")
        for k, v in resultados.items():
            print(f"   {k}: {v:.2f}")
    else:
        print("⚠️ No se puede analizar un DataFrame vacío.")