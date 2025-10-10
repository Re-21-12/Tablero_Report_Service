from flask import Flask, send_file, make_response
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
import data as dt
import io

app = Flask(__name__)
token = ""
usuario = {}

@app.route("/reporte/pdf", methods=["GET"])
def generar_reporte():
    global token, usuario
    usuario = {
        "nombre": "Macario",
        "contrasena": "apple123"
    }

    # Obtener token y datos desde la API .NET
    dt.set_user(usuario)
    token = dt.obtener_token()
    jugadores = dt.Obtener_Jugadores(token)
    print("Jugadores recibidos:", jugadores)

    # === Crear un buffer en memoria ===
    buffer = io.BytesIO()
    pdf = SimpleDocTemplate(
        buffer,
        pagesize=LETTER,
        rightMargin=40,
        leftMargin=40,
        topMargin=60,
        bottomMargin=40
    )

    contenido = []
    estilos = getSampleStyleSheet()
    titulo = estilos["Heading1"]
    texto = estilos["BodyText"]

    # === Encabezado ===
    contenido.append(Paragraph("🏆 Reporte de Jugadores Registrados", titulo))
    contenido.append(Spacer(1, 0.2 * inch))
    contenido.append(Paragraph("Listado completo de jugadores con información detallada por equipo.", texto))
    contenido.append(Spacer(1, 0.2 * inch))

    # === Texto descriptivo ===
    contenido.append(Paragraph(
        "Este documento fue generado automáticamente con Flask y ReportLab.",
        texto
    ))
    contenido.append(Spacer(1, 0.3 * inch))

    # === Tabla de jugadores ===
    encabezados = ["Nombre", "Apellido", "Edad", "Estatura (cm)", "Posición", "Nacionalidad", "ID Equipo"]
    datos_tabla = [encabezados]

    for j in jugadores:
        datos_tabla.append([
            j.get("nombre", ""),
            j.get("apellido", ""),
            j.get("edad", ""),
            j.get("estatura", ""),
            j.get("posicion") or "—",
            j.get("nacionalidad", ""),
            j.get("id_Equipo", "")
        ])

    tabla = Table(datos_tabla, hAlign="CENTER", colWidths=[80, 80, 40, 70, 80, 100, 50])
    tabla.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#4F81BD")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, 0), 11),
        ("FONTSIZE", (0, 1), (-1, -1), 10),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F7F7F7")]),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]))
    contenido.append(tabla)

    # === Pie de página ===
    contenido.append(Spacer(1, 0.3 * inch))
    contenido.append(Paragraph("📅 Reporte generado dinámicamente — © 2025", texto))

    # === Construir el PDF ===
    pdf.build(contenido)
    buffer.seek(0)

    # === Devolver el PDF al cliente ===
    response = make_response(buffer.getvalue())
    response.headers["Content-Type"] = "application/pdf"
    response.headers["Content-Disposition"] = "inline; filename=reporte_jugadores.pdf"
    return response


if __name__ == "__main__":
    app.run(port=5233, debug=True)
