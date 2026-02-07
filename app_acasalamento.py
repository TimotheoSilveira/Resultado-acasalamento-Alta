"""
Sistema de Geração de Relatórios PDF - Acasalamento de Animais
"""

import streamlit as st
import pandas as pd
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib.enums import TA_CENTER
from reportlab.pdfgen import canvas
from datetime import datetime
import io
import os
import math

# =====================================================
# STREAMLIT CONFIG
# =====================================================
st.set_page_config(
    page_title="Gerador de Relatórios - Acasalamento",
    page_icon="🐄",
    layout="wide"
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOGO_PATH = os.path.join(BASE_DIR, "Logo Alta_com frase.jpg")

# =====================================================
# FUNÇÕES AUXILIARES
# =====================================================
def calculate_max_rows_per_page(font_size):
    page_height = landscape(A4)[1]
    available = page_height - (3 * cm) - (2.5 * cm)
    return max(10, int(available / (font_size + 8)))

# =====================================================
# CANVAS COM LOGO
# =====================================================
class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, header_left="", header_right="", logo_path=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.header_left = header_left
        self.header_right = header_right
        self.logo_path = logo_path
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        total = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_header_footer(total)
            super().showPage()
        super().save()

    def draw_header_footer(self, total_pages):
        if self._pageNumber == 1:
            return

        w, h = landscape(A4)

        # LOGO
        text_x = 2 * cm
        if self.logo_path and os.path.exists(self.logo_path):
            self.drawImage(
                self.logo_path,
                2 * cm,
                h - 2.2 * cm,
                width=3.5 * cm,
                height=1.2 * cm,
                preserveAspectRatio=True,
                mask="auto"
            )
            text_x = 6 * cm

        # HEADER
        self.setFont("Helvetica", 10)
        self.drawString(text_x, h - 2 * cm, self.header_left)
        self.drawRightString(w - 2 * cm, h - 2 * cm, self.header_right)

        self.setStrokeColor(colors.grey)
        self.line(2 * cm, h - 2.35 * cm, w - 2 * cm, h - 2.35 * cm)

        # FOOTER
        self.setFont("Helvetica", 9)
        self.drawCentredString(
            w / 2,
            1.5 * cm,
            f"Página {self._pageNumber - 1} de {total_pages - 1}"
        )

# =====================================================
# CAPA
# =====================================================
def create_cover(client):
    styles = getSampleStyleSheet()
    elems = [Spacer(1, 4 * cm)]

    if os.path.exists(LOGO_PATH):
        img = Image(LOGO_PATH, width=8 * cm, height=8 * cm, kind="proportional")
        img.hAlign = "CENTER"
        elems.extend([img, Spacer(1, 2 * cm)])

    elems.append(
        Paragraph(
            "RELATÓRIO DE ACASALAMENTO",
            ParagraphStyle(
                "title",
                fontSize=34,
                alignment=TA_CENTER,
                fontName="Helvetica-Bold",
                textColor=colors.HexColor("#1f77b4")
            )
        )
    )

    elems.append(Spacer(1, 1.5 * cm))
    elems.append(Paragraph(client, ParagraphStyle("c", fontSize=26, alignment=TA_CENTER)))
    elems.append(Spacer(1, 3 * cm))
    elems.append(Paragraph(datetime.now().strftime("%d/%m/%Y"), ParagraphStyle("d", alignment=TA_CENTER)))
    elems.append(PageBreak())
    return elems

# =====================================================
# TABELAS
# =====================================================
def create_tables(df, rows, font):
    elements = []
    pages = math.ceil(len(df) / rows)

    for p in range(pages):
        chunk = df.iloc[p * rows:(p + 1) * rows]
        data = [chunk.columns.tolist()] + chunk.astype(str).values.tolist()

        table = Table(data, repeatRows=1)
        table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1f77b4")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, -1), font),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f2f2f2")])
        ]))

        elements.append(table)
        if p < pages - 1:
            elements.append(PageBreak())

    return elements

# =====================================================
# PDF
# =====================================================
def generate_pdf(df, client, header_l, header_r, font, rows):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=landscape(A4),
        leftMargin=2 * cm,
        rightMargin=2 * cm,
        topMargin=3 * cm,
        bottomMargin=2.5 * cm
    )

    elements = []
    elements.extend(create_cover(client))
    elements.extend(create_tables(df, rows, font))

    doc.build(
        elements,
        canvasmaker=lambda *a, **k: NumberedCanvas(
            *a,
            header_left=header_l,
            header_right=header_r,
            logo_path=LOGO_PATH,
            **k
        )
    )

    buffer.seek(0)
    return buffer

# =====================================================
# APP
# =====================================================
def main():
    st.title("🐄 Gerador de Relatórios - Acasalamento")

    file = st.file_uploader("Upload do CSV", type="csv")

    if file:
        # FORÇAR ENCODING CORRETO
        df = pd.read_csv(file, encoding="latin1")

        # RENOMEAÇÃO POR POSIÇÃO (GARANTIDO)
        df.columns = [
            "ID animal",
            "Tipo sêmen",
            "Índice",
            "Código pai",
            "NAAB Opção 1",
            "1º Opção",
            "INB %",
            "NAAB Opção 2",
            "2º Opção",
            "INB %",
            "NAAB Opção 3",
            "3º Opção",
            "INB %"
        ]

        st.success("Cabeçalhos corrigidos com sucesso.")
        st.dataframe(df.head())

        client = st.text_input("Cliente", "Fazenda Exemplo")
        header_l = st.text_input("Cabeçalho esquerdo", "Relatório de Acasalamento")
        header_r = st.text_input("Cabeçalho direito", datetime.now().strftime("%d/%m/%Y"))
        font = st.slider("Fonte", 8, 16, 10)
        rows = st.number_input("Linhas por página", 10, calculate_max_rows_per_page(font), 30)

        if st.button("Gerar PDF"):
            pdf = generate_pdf(df, client, header_l, header_r, font, rows)
            st.download_button("Baixar PDF", pdf, file_name="acasalamento.pdf", mime="application/pdf")

if __name__ == "__main__":
    main()
