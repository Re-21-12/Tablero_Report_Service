from flask import Flask, send_file, make_response, jsonify
from reportlab.lib.pagesizes import LETTER, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm, inch, cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib import colors
import requests
from datetime import datetime
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

def Generar_Jugadores(token, id_Equipo):
    try:
        jugadores = dt.Obtener_Jugadores_Equipo(token, id_Equipo)
        equipo = dt.Obtener_Equipo(token, id_Equipo)
        if not jugadores or not isinstance(jugadores, list):
            return jsonify({"error": "El cuerpo debe ser una lista de jugadores"}), 400

        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4)
        elements = []
        styles = getSampleStyleSheet()

        # 🔸 Encabezado corporativo
        encabezado_pdf(elements, styles, f"Roster de Jugadores, equipo: {equipo["nombre"]}")

        # Título del reporte
        #elements.append(Paragraph(f"Reporte de Jugadores - Equipo {id_equipo}", styles["Title"]))
        elements.append(Spacer(1, 12))

        # Encabezado de la tabla
        table_data = [["Nombre", "Apellido", "Edad", "Estatura (cm)", "Posición", "Nacionalidad"]]

        # Agregar filas con los datos
        for j in jugadores:
            table_data.append([
                j.get("nombre", "N/D"),
                j.get("apellido", "N/D"),
                j.get("edad", "N/D"),
                j.get("estatura", "N/D"),
                j.get("posicion", "—") if j.get("posicion") else "—",
                j.get("nacionalidad", "N/D")
            ])

        # Crear tabla
        table = Table(table_data, colWidths=[60, 60, 40, 50, 60, 80])
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
            download_name=f"reporte_jugadores_equipo_{id_Equipo}.pdf",
            mimetype="application/pdf"
        )

    except Exception as e:
        return jsonify({"error": str(e)}), 500

def Generar_Historial_Partidos(token):
    try:
        partidos = dt.Obtener_Partidos_Marcador(token)

        if not partidos or not isinstance(partidos, list):
            return jsonify({"error": "El cuerpo debe ser una lista de partidos"}), 400

        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4)
        elements = []
        styles = getSampleStyleSheet()

        # 🔸 Encabezado corporativo
        encabezado_pdf(elements, styles, "Historial de todos los Partidos Jugados")

        # Título del reporte
        #elements.append(Paragraph("Historial de Partidos", styles["Title"]))
        elements.append(Spacer(1, 12))

        # Encabezado de la tabla
        table_data = [["Local", "Visitante", "Fecha / Hora", "Marcador"]]

        # Agregar filas con los datos
        for p in partidos:
            local = p.get("local", "N/D")
            visitante = p.get("visitante", "N/D")
            fecha_str = p.get("fecha", "")
            try:
                fecha = datetime.fromisoformat(fecha_str.replace("Z", "+00:00"))
                fecha_formateada = fecha.strftime("%d/%m/%Y %H:%M")
            except Exception:
                fecha_formateada = fecha_str

            resultado = p.get("resultado", {})
            marcador = f"{resultado.get('puntaje_local', 0)} - {resultado.get('puntaje_visitante', 0)}"

            table_data.append([local, visitante, fecha_formateada, marcador])

        # Crear tabla
        table = Table(table_data, colWidths=[80, 80, 100, 60])
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
            download_name="historial_partidos.pdf",
            mimetype="application/pdf"
        )

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
def Generar_Roster_Partido(token, id_partido):
    
    try:
        partido_info, jugadores_locales, jugadores_visitantes = dt.Obtener_Jugadores_Partido(token, id_partido)
      

        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4)
        elements = []
        styles = getSampleStyleSheet()

        # Encabezado corporativo
        encabezado_pdf(elements, styles, f'Roster de los equipos en el partido jugado en: {partido_info["fechaHora"]}, en la localidad {partido_info["localidad"]}')

        # Título
        #elements.append(Paragraph("Roster de Jugadores por Partido", styles["Title"]))
        elements.append(Spacer(1, 12))

        # Información del partido
        fecha_str = partido_info.get("fechaHora", "")
        try:
            fecha = datetime.fromisoformat(fecha_str)
            fecha_formateada = fecha.strftime("%d/%m/%Y %H:%M")
        except Exception:
            fecha_formateada = fecha_str

        partido_texto = f"{partido_info.get('local', 'N/D')} vs {partido_info.get('visitante', 'N/D')} - {fecha_formateada}"
        elements.append(Paragraph(partido_texto, styles["Heading2"]))
        elements.append(Spacer(1, 12))

        # Función para crear tabla de jugadores
        def crear_tabla_jugadores(jugadores, titulo_equipo):
            data = [["Nombre", "Apellido", "Edad", "Estatura", "Posición", "Nacionalidad"]]
            for j in jugadores:
                data.append([
                    j.get("nombre", "N/D"),
                    j.get("apellido", "N/D"),
                    j.get("edad", "N/D"),
                    j.get("estatura", "N/D"),
                    j.get("posicion") if j.get("posicion") else "—",
                    j.get("nacionalidad", "N/D")
                ])
            elements.append(Paragraph(titulo_equipo, styles["Heading3"]))
            table = Table(data, colWidths=[60, 60, 40, 50, 60, 80])
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
            elements.append(Spacer(1, 12))

        # Tablas de locales y visitantes
        crear_tabla_jugadores(jugadores_locales, f"Equipo Local: {partido_info.get('local', 'N/D')}")
        crear_tabla_jugadores(jugadores_visitantes, f"Equipo Visitante: {partido_info.get('visitante', 'N/D')}")

        # Generar PDF
        doc.build(elements)
        buffer.seek(0)
        return send_file(
            buffer,
            as_attachment=True,
            download_name=f"roster_partido_{partido_info.get('local', '')}_vs_{partido_info.get('visitante', '')}.pdf",
            mimetype="application/pdf"
        )

    except Exception as e:
        from flask import jsonify
        return jsonify({"error": str(e)}), 500


def Generar_Roster_Partido_delado(token, id_partido):
    try:
        partido_info, jugadores_locales, jugadores_visitantes = dt.Obtener_Jugadores_Partido(token, id_partido)

      


        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4)
        elements = []
        styles = getSampleStyleSheet()

        # Encabezado corporativo
        encabezado_pdf(elements, styles, f'Roster de los equipos en el partido jugado en: {partido_info["fechaHora"]}, en la localidad {partido_info["localidad"]}')

        # Título
        #elements.append(Paragraph("Roster de Jugadores por Partido", styles["Title"]))
        elements.append(Spacer(1, 12))

        # Información del partido
        fecha_str = partido_info["fechaHora"]
        try:
            fecha = datetime.fromisoformat(fecha_str)
            fecha_formateada = fecha.strftime("%d/%m/%Y %H:%M")
        except Exception:
            fecha_formateada = fecha_str

        partido_texto = f"{partido_info.get('local', 'N/D')} vs {partido_info.get('visitante', 'N/D')} - {fecha_formateada}"
        elements.append(Paragraph(partido_texto, styles["Heading2"]))
        elements.append(Spacer(1, 12))

        # Función para generar mini-tabla de jugadores
        def tabla_jugadores(jugadores):
            data = [["Nombre", "Apellido", "Edad", "Estatura", "Posición", "Nacionalidad"]]
            for j in jugadores:
                data.append([
                    j.get("nombre", "N/D"),
                    j.get("apellido", "N/D"),
                    j.get("edad", "N/D"),
                    j.get("estatura", "N/D"),
                    j.get("posicion") if j.get("posicion") else "—",
                    j.get("nacionalidad", "N/D")
                ])
            t = Table(data, colWidths=[50, 50, 30, 40, 50, 60])
            t.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#003366")),
                ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
                ('ALIGN', (0,0), (-1,-1), 'CENTER'),
                ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
                ('INNERGRID', (0,0), (-1,-1), 0.25, colors.gray),
                ('BOX', (0,0), (-1,-1), 0.25, colors.gray),
                ('BACKGROUND', (0,1), (-1,-1), colors.HexColor("#F9F9F9")),
            ]))
            return t

        # Crear mini-tablas
        tabla_local = tabla_jugadores(jugadores_locales)
        tabla_visitante = tabla_jugadores(jugadores_visitantes)

        # Tabla contenedora principal, lado a lado
        contenedor = Table(
            [[Paragraph(f"Equipo Local: {partido_info.get('local', 'N/D')}", styles["Heading3"]),
              Paragraph(f"Equipo Visitante: {partido_info.get('visitante', 'N/D')}", styles["Heading3"])],
             [tabla_local, tabla_visitante]],
            colWidths=[270, 270]
        )
        contenedor.setStyle(TableStyle([
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ]))

        elements.append(contenedor)
        elements.append(Spacer(1, 12))

        # Generar PDF
        doc.build(elements)
        buffer.seek(0)
        return send_file(
            buffer,
            as_attachment=True,
            download_name=f"roster_partido_{partido_info.get('local', '')}_vs_{partido_info.get('visitante', '')}.pdf",
            mimetype="application/pdf"
        )

    except Exception as e:
        from flask import jsonify
        return jsonify({"error": str(e)}), 500


def Generar_Reporte_Estadisticas_Jugador(token, id_jugador):
    try:
        # Obtener los datos desde tu método existente
        jugador, total_faltas, total_anotaciones = dt.Obtener_Estadisticas_Jugador(token, id_jugador)

        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4)
        elements = []
        styles = getSampleStyleSheet()

        # Encabezado corporativo
        encabezado_pdf(elements, styles, f"Estadísticas del Jugador: {jugador.get('nombre', '')} {jugador.get('apellido', '')}")

        elements.append(Spacer(1, 12))

        # Información del jugador
        info_texto = f"Jugador: {jugador.get('nombre', '')} {jugador.get('apellido', '')}"
        elements.append(Paragraph(info_texto, styles["Heading2"]))
        elements.append(Spacer(1, 12))

        # Tabla de Faltas
        if total_faltas:
            data_faltas = [["ID Partido", "Total Faltas"]]
            total_faltas_count = 0
            for f in total_faltas:
                data_faltas.append([
                    f.get("id_Partido", "N/D"),
                    f.get("total_faltas", 0)
                ])
                total_faltas_count += f.get("total_faltas", 0)
            elements.append(Paragraph("Faltas", styles["Heading3"]))
            table_faltas = Table(data_faltas, colWidths=[100, 100])
            table_faltas.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#003366")),
                ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
                ('ALIGN', (0,0), (-1,-1), 'CENTER'),
                ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
                ('INNERGRID', (0,0), (-1,-1), 0.25, colors.gray),
                ('BOX', (0,0), (-1,-1), 0.25, colors.gray),
                ('BACKGROUND', (0,1), (-1,-1), colors.HexColor("#F9F9F9")),
            ]))
            elements.append(table_faltas)
            elements.append(Spacer(1, 12))
        else:
            total_faltas_count = 0

        # Tabla de Anotaciones
        if total_anotaciones:
            data_anot = [["ID Partido", "Total Anotaciones"]]
            total_anot_count = 0
            for a in total_anotaciones:
                data_anot.append([
                    a.get("id_partido", "N/D"),
                    a.get("total_anotaciones", 0)
                ])
                total_anot_count += a.get("total_anotaciones", 0)
            elements.append(Paragraph("Anotaciones", styles["Heading3"]))
            table_anot = Table(data_anot, colWidths=[100, 100])
            table_anot.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#003366")),
                ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
                ('ALIGN', (0,0), (-1,-1), 'CENTER'),
                ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
                ('INNERGRID', (0,0), (-1,-1), 0.25, colors.gray),
                ('BOX', (0,0), (-1,-1), 0.25, colors.gray),
                ('BACKGROUND', (0,1), (-1,-1), colors.HexColor("#F9F9F9")),
            ]))
            elements.append(table_anot)
            elements.append(Spacer(1, 12))
        else:
            total_anot_count = 0

        # Tabla resumen final
        data_resumen = [["Total Faltas", "Total Anotaciones"]]
        data_resumen.append([total_faltas_count, total_anot_count])
        elements.append(Paragraph("Resumen General", styles["Heading3"]))
        table_resumen = Table(data_resumen, colWidths=[120, 120])
        table_resumen.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#003366")),
            ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('INNERGRID', (0,0), (-1,-1), 0.25, colors.gray),
            ('BOX', (0,0), (-1,-1), 0.25, colors.gray),
            ('BACKGROUND', (0,1), (-1,-1), colors.HexColor("#F9F9F9")),
        ]))
        elements.append(table_resumen)
        elements.append(Spacer(1, 12))

        # Generar PDF
        doc.build(elements)
        buffer.seek(0)
        return send_file(
            buffer,
            as_attachment=True,
            download_name=f"estadisticas_jugador_{jugador.get('nombre', '')}_{jugador.get('apellido', '')}.pdf",
            mimetype="application/pdf"
        )

    except Exception as e:
        return jsonify({"error": str(e)}), 500

