from reportlab.pdfgen import canvas
from reportlab.platypus import Table
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.platypus import BaseDocTemplate, PageTemplate, Frame, Paragraph, Image
from reportlab.platypus import TableStyle
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.enums import TA_CENTER

from reportlab.lib import colors

try:
    from django.utils import importlib
except ImportError:
    import importlib

from . import config as settings

FONT_FAMILY = 'Helvetica'


class NumberedCanvas(canvas.Canvas):
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
        ('Domilio Fiscal', 'Av NoSeDondeEstoy 123 - Lima '),
        ('RUC', '285714142'),
        ('Teléfono', '(01) 543 1428'),
        ('Email', 'hola@acme.com')
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

    # productos a cotizar
    data = [['Producto', 'Cantidad', 'Precio x unidad', 'Subtotal']]
    for i in range(1, 50):
        data.append(['producto #' + str(i), str(24), 'S/ 5.00', 'S/ 120.00'])

    data.append(['', '', 'Total', 'S/ 1800.00'])

    tableThatSplitsOverPages = Table(data, repeatRows=1)
    tableThatSplitsOverPages.hAlign = 'LEFT'
    tblStyle = TableStyle([('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
                           ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                           ('LINEBELOW', (0, 0), (-1, -1), 1, colors.black),
                           ('BOX', (0, 0), (-1, -1), 1, colors.black),
                           ('BOX', (0, 0), (0, -1), 1, colors.black)])
    tblStyle.add('BACKGROUND', (0, 0), (3, 0), colors.lightblue)
    tblStyle.add('BACKGROUND', (0, 1), (-1, -1), colors.white)

    tableThatSplitsOverPages.setStyle(tblStyle)
    elements.append(tableThatSplitsOverPages)

    # texto final


    doc.build(elements, canvasmaker=NumberedCanvas)
