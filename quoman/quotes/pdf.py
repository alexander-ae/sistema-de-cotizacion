from reportlab.pdfgen import canvas
from reportlab.platypus import Table
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.platypus import BaseDocTemplate, PageTemplate, Frame, Paragraph, Image
from reportlab.platypus import TableStyle
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.enums import TA_CENTER, TA_RIGHT
from reportlab.lib import colors

from . import config as settings
from quoman.models import Config

FONT_FAMILY = 'Helvetica'


class CustomCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        canvas.Canvas.__init__(self, *args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)

            self.translate(0, 29.7 * cm)
            self.setFont(FONT_FAMILY, 11)

            # métodos personalizados
            self.draw_page_number(num_pages)
            self.draw_header()
            self.draw_footer()

            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def draw_page_number(self, page_count):
        self.setFont(FONT_FAMILY, 11)
        self.drawRightString(19 * cm, - 28.5 * cm,
                             'Página {} de {}'.format(self._pageNumber, page_count))

    def draw_header(canvas):
        canvas.setStrokeColorRGB(0, 0.2, 0.4)
        canvas.setFillColorRGB(0.2, 0.2, 0.2)
        canvas.drawString(16 * cm, -1 * cm, 'Massive Dinamycs')
        canvas.drawInlineImage(settings.INV_LOGO, 1 * cm, -1 * cm, 180, 16, preserveAspectRatio=True)
        canvas.setLineWidth(2)
        canvas.line(0.75 * cm, -1.20 * cm, 20 * cm, -1.20 * cm)

    def draw_footer(canvas):
        canvas.setStrokeColorRGB(0, 0.2, 0.4)
        canvas.setFillColorRGB(0.2, 0.2, 0.2)
        canvas.setLineWidth(2)

        canvas.line(0.75 * cm, -28.00 * cm, 20 * cm, -28 * cm)
        canvas.drawString(2 * cm, -28.5 * cm, '10/01/2016')


def draw_pdf(buffer, cotizacion):
    """ Genera el pdf de la cotización """
    # configuracion
    config, created = Config.objects.get_or_create(pk=1)

    # pdf
    doc = BaseDocTemplate(buffer, pagesize=A4,
                          rightMargin=72,
                          leftMargin=72,
                          topMargin=72,
                          bottomMargin=72)

    pHeight, pWidth = doc.pagesize
    myFrame = Frame(0, 0, pHeight, pWidth, 50, 60, 50, 50, id='myFrame')
    mainTemplate = PageTemplate(id='mainTemplate', frames=[myFrame])
    doc.addPageTemplates([mainTemplate])

    elements = []
    styles = getSampleStyleSheet()
    styleN = styles['Normal']

    # cabecera
    logo = Image(settings.INV_LOGO)
    elements.append(logo)

    header_info = [
        ('Domilio Fiscal', config.direccion),
        ('RUC', config.ruc),
        ('Teléfono', cotizacion.propietario_id.userprofile.telefono),
        ('Email', cotizacion.propietario_id.userprofile.email)
    ]

    style_header = ParagraphStyle(name='Normal',
                                  fontName=FONT_FAMILY,
                                  fontSize=10,
                                  leading=12,
                                  spaceAfter=4,
                                  spaceBefore=8)

    for header_item in header_info:
        elements.append(Paragraph('<b>{}: </b> {}'.format(header_item[0], header_item[1], ), style_header))

    style_title = ParagraphStyle(name='header',
                                 fontName=FONT_FAMILY,
                                 fontSize=14,
                                 spaceAfter=10,
                                 spaceBefore=10,
                                 alignment=TA_CENTER)

    elements.append(Paragraph('<b>Cotización 2017-0014</b>', style_title))

    # datos de la empresa



    # productos a cotizar
    s = getSampleStyleSheet()
    s = s['BodyText']
    s.wordWrap = 'CJK'

    styleR = styleN
    styleR.alignment = TA_RIGHT
    data = [['Item', 'Producto', 'Cantidad', 'Precio x unidad', 'Subtotal']]
    for i, producto in enumerate(cotizacion.productos_a_cotizar.all()):
        data.append([
            str(i + 1),
            Paragraph('{}: {}'.format(producto.nombre, producto.detalle), s),
            producto.cantidad,
            'S/ {}'.format(producto.precio),
            'S/ {}'.format(producto.subtotal)
        ])

    data.append(['', 'Nota: Los precios no incluyen IGV', '', Paragraph('<b>SubTotal</b>', styleR),
                 'S/ {}'.format(cotizacion.calcula_subtotal_productos())])
    data.append(
        ['', '', '', Paragraph('<b>Envío</b>', styleR), 'S/ {}'.format(cotizacion.costo_de_envio)])
    data.append(
        ['', '', 'IGV', Paragraph('<b>{} %</b>'.format(cotizacion.igv), styleR),
         'S/ {:.2f}'.format(cotizacion.calcula_igv())])
    data.append(['', '', '', Paragraph('<b>Total</b>', styleR), 'S/ {}'.format(cotizacion.total)])

    tableThatSplitsOverPages = Table(data, repeatRows=1, colWidths=[1 * cm, 8 * cm, 2 * cm, 3.5 * cm, 3 * cm])
    tableThatSplitsOverPages.hAlign = 'LEFT'
    tblStyle = TableStyle([('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
                           ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                           ('ALIGN', (2, 0), (2, -1), 'CENTER'),
                           ('ALIGN', (3, 0), (3, -1), 'RIGHT'),
                           ('ALIGN', (4, 0), (4, -1), 'RIGHT'),
                           ('LINEBELOW', (0, 0), (-1, -1), 1, colors.black),
                           ('BOX', (0, 0), (-1, -1), 1, colors.black),
                           ('GRID', (0, 0), (-1, -5), 1, colors.black),
                           ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
                           ('BACKGROUND', (0, 1), (-1, -1), colors.white)
                           ])

    tableThatSplitsOverPages.setStyle(tblStyle)
    elements.append(tableThatSplitsOverPages)

    # texto final


    doc.build(elements, canvasmaker=CustomCanvas)
