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

    # Columna segura: se ajusta según los nombres reales de Yahoo Finance
    if "Adj Close" in df.columns:
        y_col = "Adj Close"
        precio_label = "Precio Ajustado"
    elif "Close" in df.columns:
        y_col = "Close"
        precio_label = "Precio Cierre"
    else:
        st.error("No se encontró columna 'Close' ni 'Adj Close' en los datos.")
        return None

    fig_precio = px.line(
        df, x="Date", y=y_col,
        title=f"{ticker} - {precio_label} Últimos {len(df)} Días",
        labels={y_col: precio_label, "Date": "Fecha"}
    )

    if "Return" in df.columns:
        fig_retorno = px.bar(
            df, x="Date", y="Return",
            title=f"{ticker} - Retornos Diarios (%)",
            labels={"Return": "Retorno (%)", "Date": "Fecha"}
        )
    else:
        fig_retorno = None

    return {"precio": fig_precio, "retorno": fig_retorno}

def ejecutar_dashboard():
    st.set_page_config(page_title="Analizador Financiero", layout="wide")
    st.title("📊 Analizador de Datos Financieros con Python")
    st.markdown("Visualiza datos históricos exactos según los días seleccionados.")

    ticker = st.text_input("Introduce el símbolo del activo (ej: AAPL, TSLA, MSFT):", "AAPL")
    dias = st.slider("Número de días a analizar (mínimo 7):", 7, 365*5, value=7, step=1)

    if st.button("Cargar y Analizar Ahora") and ticker:
        try:
            # Descargar datos suficientes para cubrir días hábiles
            df = cargar_datos(ticker, dias=dias*2)
        except Exception as e:
            st.error(f"No se pudieron obtener datos: {e}")
            return

        if df.empty:
            st.error("No se pudieron obtener datos para el ticker ingresado.")
            return

        # Tomar solo los últimos N días
        df = df.tail(dias)

        # Mostrar tabla
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
        st.subheader("📊 Gráficos")
        graficos = crear_graficos(df, ticker)
        if graficos:
            st.plotly_chart(graficos["precio"], use_container_width=True)
            if graficos["retorno"]:
                st.plotly_chart(graficos["retorno"], use_container_width=True)

if __name__ == "__main__":
    ejecutar_dashboard()