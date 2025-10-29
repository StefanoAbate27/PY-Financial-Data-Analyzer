import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from fpdf import FPDF
import io

st.set_page_config(page_title="Financial Data Analyzer", layout="wide")

st.title("📊 Financial Data Analyzer")
st.markdown("Analiza datos financieros públicos usando **Yahoo Finance** 🧠")

# --- Sidebar ---
st.sidebar.header("Configuración")
ticker = st.sidebar.text_input("Símbolo del activo (ej: AAPL, TSLA, BTC-USD)", "AAPL")
start_date = st.sidebar.date_input("Fecha de inicio", pd.to_datetime("2020-01-01"))
end_date = st.sidebar.date_input("Fecha de fin", pd.to_datetime("today"))

# --- Cargar datos ---
@st.cache_data
def load_data(symbol, start, end):
    data = yf.download(symbol, start=start, end=end)
    data['Return'] = data['Adj Close'].pct_change()
    data.dropna(inplace=True)
    return data

try:
    data = load_data(ticker, start_date, end_date)
except Exception as e:
    st.error("Error al cargar los datos. Verifica el símbolo o tu conexión.")
    st.stop()

# --- Mostrar tabla ---
st.subheader(f"Datos de {ticker}")
st.dataframe(data.tail(10))

# --- Estadísticas ---
st.subheader("📈 Estadísticas descriptivas")
returns = data['Return']
stats = {
    "Retorno promedio (%)": returns.mean() * 100,
    "Volatilidad (%)": returns.std() * 100,
    "Retorno acumulado (%)": ((data['Adj Close'][-1] / data['Adj Close'][0]) - 1) * 100
}
st.json(stats)

# --- Gráfico de precios ---
fig_price = go.Figure()
fig_price.add_trace(go.Scatter(x=data.index, y=data['Adj Close'], name="Precio Ajustado"))
fig_price.update_layout(title=f"Precio ajustado de {ticker}", xaxis_title="Fecha", yaxis_title="Precio")
st.plotly_chart(fig_price, use_container_width=True)

# --- Gráfico de retornos ---
fig_ret = go.Figure()
fig_ret.add_trace(go.Scatter(x=data.index, y=data['Return'], name="Retorno Diario", line=dict(color='orange')))
fig_ret.update_layout(title="Retorno Diario (%)", xaxis_title="Fecha", yaxis_title="Retorno")
st.plotly_chart(fig_ret, use_container_width=True)

# --- Exportar a PDF ---
def generar_reporte(ticker, stats):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(200, 10, f"Reporte Financiero - {ticker}", ln=True, align="C")
    pdf.set_font("Arial", size=12)
    for k, v in stats.items():
        pdf.cell(200, 10, f"{k}: {v:.2f}", ln=True)
    output = io.BytesIO()
    pdf.output(output)
    return output.getvalue()

if st.button("📄 Descargar Reporte PDF"):
    pdf_bytes = generar_reporte(ticker, stats)
    st.download_button("Descargar PDF", data=pdf_bytes, file_name=f"reporte_{ticker}.pdf", mime="application/pdf")