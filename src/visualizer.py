# src/visualizer.py

import streamlit as st
import pandas as pd
import plotly.express as px
from data_loader import cargar_datos
from analyzer import analizar_datos

def crear_graficos(df: pd.DataFrame, ticker: str):
    if df.empty:
        st.warning("No hay datos para graficar.")
        return None

    # --- Seleccionar columna de precio de cierre ---
    if "Close" not in df.columns:
        st.error("No se encontró columna 'Close' en los datos descargados.")
        return None

    # --- Gráfico de precios ---
    fig_precio = px.line(
        df,
        x="Date",
        y="Close",
        title=f"{ticker.upper()} - Precio de Cierre (Últimos {len(df)} días)",
        labels={"Close": "Precio de Cierre", "Date": "Fecha"}
    )

    # --- Gráfico de retornos ---
    if "Return" in df.columns:
        fig_retorno = px.bar(
            df,
            x="Date",
            y="Return",
            title=f"{ticker.upper()} - Retornos Diarios (%)",
            labels={"Return": "Retorno (%)", "Date": "Fecha"}
        )
    else:
        fig_retorno = None

    return {"precio": fig_precio, "retorno": fig_retorno}


def ejecutar_dashboard():
    st.set_page_config(page_title="Analizador Financiero", layout="wide")
    st.title("📊 Analizador de Datos Financieros")
    st.markdown("Visualiza y analiza precios históricos de activos financieros en segundos.")

    ticker = st.text_input("Introduce el símbolo del activo (ej: AAPL, TSLA, MSFT):", "AAPL")
    dias = st.slider("Número de días a analizar:", 7, 365*5, value=365, step=1)

    if st.button("Cargar y Analizar Ahora") and ticker:
        try:
            df = cargar_datos(ticker, dias=dias)
        except Exception as e:
            st.error(f"No se pudieron obtener datos: {e}")
            return

        if df.empty:
            st.error("No se pudieron obtener datos para el ticker ingresado.")
            return

        # Mostrar datos
        st.subheader(f"📋 Datos de los últimos {dias} días")
        st.dataframe(df)

        # Estadísticas
        st.subheader("📈 Estadísticas del activo")
        resultados = analizar_datos(df)
        if resultados:
            for k, v in resultados.items():
                st.write(f"**{k}:** {v:.2f}")
        else:
            st.warning("No se pudieron calcular estadísticas.")

        # Gráficos
        st.subheader("📊 Visualizaciones")
        graficos = crear_graficos(df, ticker)
        if graficos:
            st.plotly_chart(graficos["precio"], use_container_width=True)
            if graficos["retorno"]:
                st.plotly_chart(graficos["retorno"], use_container_width=True)


if __name__ == "__main__":
    ejecutar_dashboard()