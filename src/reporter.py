# src/reporter.py

import os
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle


def generar_reporte(resultados: dict, ticker: str, ruta_salida: str = "reportes"):
    """
    Genera un reporte en PDF con los resultados del análisis de datos financieros.

    Parámetros:
        resultados (dict): Diccionario con los indicadores del análisis.
        ticker (str): Símbolo del activo analizado (ej: 'AAPL').
        ruta_salida (str): Carpeta donde se guardará el reporte.
    """
    if not resultados:
        print("⚠️ No hay resultados para generar el reporte.")
        return

    # Crear carpeta si no existe
    os.makedirs(ruta_salida, exist_ok=True)

    # Nombre del archivo
    nombre_archivo = f"Reporte_{ticker}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    ruta_archivo = os.path.join(ruta_salida, nombre_archivo)

    # Documento base
    doc = SimpleDocTemplate(ruta_archivo, pagesize=A4)
    elementos = []

    # Estilos
    estilos = getSampleStyleSheet()
    estilo_titulo = ParagraphStyle(
        "Titulo",
        parent=estilos["Title"],
        fontSize=20,
        leading=24,
        alignment=1,
        textColor=colors.HexColor("#003366"),
        spaceAfter=20,
    )
    estilo_subtitulo = ParagraphStyle(
        "Subtitulo",
        parent=estilos["Heading2"],
        fontSize=13,
        textColor=colors.HexColor("#005599"),
        spaceAfter=10,
    )
    estilo_normal = estilos["BodyText"]

    # Encabezado
    elementos.append(Paragraph(f"📊 Reporte Financiero - {ticker}", estilo_titulo))
    elementos.append(Paragraph(f"Fecha de generación: {datetime.now().strftime('%d/%m/%Y %H:%M')}", estilo_normal))
    elementos.append(Spacer(1, 15))

    # Subtítulo
    elementos.append(Paragraph("Resumen Estadístico del Análisis", estilo_subtitulo))

    # Convertir resultados a tabla
    data = [["Métrica", "Valor"]]
    for k, v in resultados.items():
        data.append([k, f"{v}"])

    tabla = Table(data, colWidths=[250, 150])
    tabla.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#005599")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, 0), 12),
                ("BOTTOMPADDING", (0, 0), (-1, 0), 8),
                ("BACKGROUND", (0, 1), (-1, -1), colors.whitesmoke),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.gray),
            ]
        )
    )

    elementos.append(tabla)
    elementos.append(Spacer(1, 25))

    # Interpretación textual
    elementos.append(Paragraph("Interpretación del desempeño:", estilo_subtitulo))

    sharpe = resultados.get("Sharpe Ratio", 0)
    drawdown = resultados.get("Máximo Drawdown (%)", 0)

    interpretacion = []

    if sharpe > 1:
        interpretacion.append("✅ El activo presenta una buena relación entre riesgo y rendimiento.")
    elif sharpe > 0:
        interpretacion.append("⚠️ El rendimiento del activo es moderado en relación con el riesgo.")
    else:
        interpretacion.append("❌ El activo no ofrece un rendimiento adecuado frente al riesgo asumido.")

    if drawdown < -30:
        interpretacion.append("⚠️ El activo ha tenido caídas significativas en el periodo analizado.")
    else:
        interpretacion.append("👍 Las caídas máximas históricas se mantienen dentro de rangos aceptables.")

    for linea in interpretacion:
        elementos.append(Paragraph(linea, estilo_normal))

    # Cierre
    elementos.append(Spacer(1, 20))
    elementos.append(Paragraph("Generado automáticamente por el sistema de análisis de datos financieros.", estilo_normal))

    # Crear PDF
    doc.build(elementos)
    print(f"✅ Reporte generado correctamente: {ruta_archivo}")


# --- Prueba local ---
if __name__ == "__main__":
    from data_loader import cargar_datos
    from analyzer import analizar_datos

    # Ejemplo: Apple (últimos 2 años)
    ticker = "AAPL"
    df = cargar_datos(ticker, dias=730)
    resultados = analizar_datos(df)

    if resultados:
        generar_reporte(resultados, ticker)