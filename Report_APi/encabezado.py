from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import Image, Paragraph, Spacer, Table, TableStyle
from datetime import datetime

def encabezado_pdf(contenido, estilos, titulo_encabezado):
    '''Agrega encabezado estándar con logo, título y fecha.'''
    try:
        logo_path = 'D:\\Universidad\\Logo.png'  
        img = Image(logo_path, width=1*inch, height=1*inch)
    except Exception:
        img = Paragraph('🏀', estilos['Title']) 

    titulo = Paragraph(f"<b>{titulo_encabezado}</b>", estilos['Title'])
    fecha = Paragraph(f"<font size=10>Generado el {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}</font>", estilos['Normal'])

    
    header_table = Table([[img, titulo, fecha]], colWidths=[80, 300, 160])
    header_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('ALIGN', (2, 0), (2, 0), 'RIGHT'),
    ]))

    contenido.append(header_table)
    contenido.append(Spacer(1, 0.2 * inch))

    
    contenido.append(Table(
        [['']], colWidths=[540],
        style=[('LINEBELOW', (0, 0), (-1, -1), 1, colors.HexColor('#1F4E78'))]
    ))
    contenido.append(Spacer(1, 0.3 * inch))
