from flask import Flask, send_file, make_response, jsonify
from reportlab.lib.pagesizes import LETTER, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm, inch, cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib import colors
import requests
from encabezado import encabezado_pdf
import data as dt
import io




def Generar_Equipos(token):
    try:
        data = dt.Obtener_Equipos(token)

        if not data or not isinstance(data, list):
            return jsonify({"error": "El cuerpo debe ser una lista de equipos"}), 400

        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4)
        elements = []
        styles = getSampleStyleSheet()
        encabezado_pdf(elements, styles, "Reporte Equipos Registrados")
        # Título
        #elements.append(Paragraph("Reporte de Equipos Registrados", styles["Title"]))
        elements.append(Spacer(1, 12))

        # Encabezado de la tabla
        table_data = [["Logo", "Nombre", "Localidad"]]

        # Agregar filas con los datos
        for equipo in data:
            nombre = equipo.get("nombre", "N/D")
            localidad = equipo.get("localidad", "N/D")
            logo_url = equipo.get("url")

            # Intentar descargar el logo (opcional)
            try:
                if logo_url:
                    response = requests.get(logo_url, timeout=3)
                    if response.status_code == 200:
                        logo = Image(io.BytesIO(response.content), width=2*cm, height=2*cm)
                    else:
                        logo = Paragraph("Sin logo", styles["Normal"])
                else:
                    logo = Paragraph("Sin logo", styles["Normal"])
            except Exception:
                logo = Paragraph("Sin logo", styles["Normal"])

            table_data.append([logo, nombre, localidad])

        # Crear tabla
        table = Table(table_data, colWidths=[3*cm, 6*cm, 5*cm])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#003366")),
            ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('INNERGRID', (0,0), (-1,-1), 0.25, colors.gray),
            ('BOX', (0,0), (-1,-1), 0.25, colors.gray),
            ('BACKGROUND', (0,1), (-1,-1), colors.HexColor("#F9F9F9")),
        ]))

        elements.append(table)
        doc.build(elements)

        buffer.seek(0)
        return send_file(
            buffer,
            as_attachment=True,
            download_name="reporte_equipos.pdf",
            mimetype="application/pdf"
        )

    except Exception as e:
        return jsonify({"error": str(e)}), 500


