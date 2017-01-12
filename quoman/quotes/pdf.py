import os
from io import BytesIO
from django.utils import timezone
from django.template.loader import get_template
from django.template import Context
from django.core.mail import EmailMessage
from django.conf import settings

from reportlab.pdfgen import canvas
from reportlab.platypus import Table
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.platypus import BaseDocTemplate, PageTemplate, Frame, Paragraph, Image
from reportlab.platypus import TableStyle
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.enums import TA_CENTER, TA_RIGHT, TA_LEFT
from reportlab.lib import colors

from quoman.models import Config
from .utils import bold

FONT_FAMILY = 'Helvetica'


class CustomCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        canvas.Canvas.__init__(self, *args, **kwargs)
        self._saved_page_states = []
        self.config, created = Config.objects.get_or_create(pk=1)

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
            self.setAuthor('quoman')
            self.draw_page_number(num_pages)
            self.draw_header()
            self.draw_footer()

            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def draw_page_number(self, page_count):
        self.setFont(FONT_FAMILY, 11)
        self.drawRightString(19 * cm, - 28.5 * cm,
                             'Página {} de {}'.format(self._pageNumber, page_count))

    def draw_header(self):
        self.setStrokeColorRGB(0, 0.2, 0.4)
        self.setFillColorRGB(0.2, 0.2, 0.2)
        self.drawString(16 * cm, -1 * cm, self.config.razon_social)
        # self.drawInlineImage(settings.INV_LOGO, 1 * cm, -1 * cm, 180, 16, preserveAspectRatio=True)
        self.setLineWidth(2)
        self.line(0.75 * cm, -1.20 * cm, 20 * cm, -1.20 * cm)

    def draw_footer(self):
        self.setStrokeColorRGB(0, 0.2, 0.4)
        self.setFillColorRGB(0.2, 0.2, 0.2)
        self.setLineWidth(2)

        self.line(0.75 * cm, -28.00 * cm, 20 * cm, -28 * cm)
        fecha_actual = timezone.now().strftime('%d/%m/%Y')
        self.drawString(2 * cm, -28.5 * cm, fecha_actual)


def draw_pdf(buffer, cotizacion):
    """ Genera el pdf de la cotización """
    # configuracion
    config, created = Config.objects.get_or_create(pk=1)

    # pdf
    doc = BaseDocTemplate(buffer, pagesize=A4,
                          rightMargin=72,
                          leftMargin=72,
                          topMargin=72,
                          bottomMargin=72,
                          title=cotizacion.codigo)
    # doc.canv.setTitle()
    pHeight, pWidth = doc.pagesize
    myFrame = Frame(0, 0, pHeight, pWidth, 50, 60, 50, 50, id='myFrame')
    mainTemplate = PageTemplate(id='mainTemplate', frames=[myFrame])
    doc.addPageTemplates([mainTemplate])

    elements = []
    styles = getSampleStyleSheet()
    styleN = styles['Normal']

    # cabecera
    logo = Image(os.path.join(settings.MEDIA_ROOT, config.logo.path))
    elements.append(logo)

    header_info = [
        ('Domilio Fiscal', config.direccion),
        ('RUC', config.ruc),
        ('Teléfono', cotizacion.propietario_id.userprofile.telefono),
        ('Email', cotizacion.propietario_id.userprofile.email),
        ('Representante asignado', cotizacion.propietario_id.userprofile.full_name())
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
                                 fontSize=16,
                                 spaceAfter=20,
                                 spaceBefore=20,
                                 alignment=TA_CENTER)

    elements.append(Paragraph('<b>Cotización {}</b>'.format(cotizacion.codigo), style_title))

    # datos de la empresa
    info_empresa = [
        ('Empresa:', cotizacion.empresa_razon_social, 'RUC:', cotizacion.ruc),
        ('Dirección:', cotizacion.empresa_direccion, 'Fecha:', cotizacion.fecha_de_creacion.strftime('%d/%m/%Y')),
        ('Atención:', cotizacion.representante, 'Teléfono:', cotizacion.empresa_telefono),
        ('Tiempo de Entrega:', cotizacion.tiempo_de_entrega, 'Método de pago:', cotizacion.forma_de_pago)
    ]

    data_empresa = []
    styleLeft = ParagraphStyle(name='Normal',
                               fontName=FONT_FAMILY,
                               fontSize=10,
                               leading=12,
                               alignment=TA_LEFT,
                               wordWrap='CJK'
                               )

    for line in info_empresa:
        _p1 = Paragraph(bold(line[0]), styleN)
        _p2 = Paragraph(line[1], styleLeft)
        _p3 = Paragraph(bold(line[2]), styleN)
        _p4 = Paragraph(line[3], styleLeft)

        data_empresa.append(
            (_p1, _p2, _p3, _p4)
        )

    tableEmpresa = Table(data_empresa, colWidths=[3 * cm, 6.5 * cm, 3.5 * cm, 4.5 * cm], spaceAfter=20, hAlign='LEFT')
    styleTableEmpresa = TableStyle([
        ('ALIGN', (1, 0), (1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ])
    tableEmpresa.setStyle(styleTableEmpresa)

    elements.append(tableEmpresa)

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
            Paragraph(bold(producto.nombre), s),
            producto.cantidad,
            'S/ {}'.format(producto.precio),
            'S/ {}'.format(producto.subtotal)
        ])
        data.append([
            '',
            Paragraph(producto.detalle, s),
            '',
            '',
            ''
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

    if cotizacion.aplica_detraccion:
        _style = styleN
        _style.fontSize = 10
        _style.textColor = colors.HexColor(0x666666)
        _style.spaceBefore = 20

        elements.append(Paragraph(config.detraccion_texto, _style))

    doc.build(elements, canvasmaker=CustomCanvas)

    return doc


def envia_cotizacion(cotizacion):
    config, created = Config.objects.get_or_create(pk=1)

    htmly = get_template('quotes/email-quote.html')
    d = Context({
        'config': config,
        'cotizacion': cotizacion,
        'SITE_URL': settings.SITE_URL
    })

    html_content = htmly.render(d)
    asunto = u'Cotización {}'.format(cotizacion.codigo)
    mail = '{0}<{1}>'.format(settings.PROJECT_NAME, settings.DEFAULT_FROM_EMAIL)
    emails_destino = cotizacion.quotereceiver_set.all().values_list('email', flat=True)

    msg = EmailMessage(asunto, html_content, mail, emails_destino)
    msg.content_subtype = "html"

    buffer = BytesIO()
    draw_pdf(buffer, cotizacion)

    msg.attach('cotizacion.pdf', buffer.getvalue(), 'application/pdf')
    msg.send()

    try:
        msg.send()
        return {
            'status_code': 200,
            'mensaje': 'El correo ha sido enviado'
        }
    except:
        return {
            'status_code': 503,
            'mensaje': 'El servicio de envío de correos tiene problemas'
        }
