import streamlit as st
import pandas as pd
import os
from datetime import datetime

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import (
    SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
)
from reportlab.lib import colors
from reportlab.pdfgen import canvas


# ===============================
# Paths
# ===============================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOGO_HEADER_PATH = os.path.join(BASE_DIR, "Logo Alta_com frase.jpg")


# ===============================
# Canvas com cabeçalho, rodapé e marca d’água
# ===============================
class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        self.header_text = kwargs.pop("header_text", "")
        self.header_date = kwargs.pop("header_date", "")
        self.logo_path = kwargs.pop("logo_path", None)
        self.watermark_text = kwargs.pop("watermark_text", "")
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page()
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def draw_page(self):
        page_width, page_height = A4

        # ===== Marca d’água =====
        if self.watermark_text:
            self.saveState()
            self.setFont("Helvetica-Bold", 60)
            self.setFillGray(0.85)
            self.translate(page_width / 2, page_height / 2)
            self.rotate(45)
            self.drawCentredString(0, 0, self.watermark_text)
            self.restoreState()

        # ===== Cabeçalho =====
        text_x = 2 * cm

        if self.logo_path and os.path.exists(self.logo_path):
            try:
                self.drawImage(
                    self.logo_path,
                    2 * cm,
                    page_height - 2.2 * cm,
                    width=3.8 * cm,
                    height=1.2 * cm,
                    preserveAspectRatio=True,
                    mask="auto",
                )
                text_x = 6.5 * cm
            except:
                pass

        self.setFont("Helvetica", 10)
        self.setFillColor(colors.black)
        self.drawString(text_x, page_height - 2 * cm, self.header_text)
        self.drawRightString(
            page_width - 2 * cm,
            page_height - 2 * cm,
            self.header_date,
        )

        # ===== Rodapé =====
        self.setFont("Helvetica", 9)
        self.drawCentredString(
            page_width / 2,
            1.5 * cm,
            f"Página {self._pageNumber}",
        )


# ===============================
# Geração do PDF
# ===============================
def generate_pdf(df, config):
    file_path = "resultado_acasalamento.pdf"

    doc = SimpleDocTemplate(
        file_path,
        pagesize=A4,
        leftMargin=2 * cm,
        rightMargin=2 * cm,
        topMargin=3.5 * cm,
        bottomMargin=2.5 * cm,
    )

    styles = getSampleStyleSheet()
    elements = []

    # ===== Título =====
    elements.append(Paragraph("<b>Resultado de Acasalamento</b>", styles["Title"]))
    elements.append(Spacer(1, 12))

    # ===== Tabela =====
    data = [df.columns.tolist()] + df.values.tolist()

    table = Table(data, repeatRows=1)
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
                ("GRID", (0, 0), (-1, -1), 0.25, colors.grey),
                ("FONT", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("ALIGN", (1, 1), (-1, -1), "CENTER"),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ]
        )
    )

    elements.append(table)

    doc.build(
        elements,
        canvasmaker=lambda *args, **kwargs: NumberedCanvas(
            *args,
            header_text=config["header_name"],
            header_date=config["header_date"],
            logo_path=LOGO_HEADER_PATH,
            watermark_text=config["watermark"],
            **kwargs,
        ),
    )

    return file_path


# ===============================
# Streamlit App
# ===============================
def main():
    st.set_page_config(page_title="Acasalamento Alta", layout="wide")
    st.title("📊 Acasalamento – Geração de PDF")

    uploaded_file = st.file_uploader("Upload do arquivo CSV", type=["csv"])

    if uploaded_file:
        try:
            # ===== Leitura robusta =====
            df = pd.read_csv(uploaded_file, encoding="latin1")

            # ===== Renomear colunas por posição =====
            expected_columns = [
                "ID animal",
                "Tipo sêmen",
                "Índice",
                "Código pai",
                "NAAB Opção 1",
                "1ª Opção",
                "INB %",
                "NAAB Opção 2",
                "2ª Opção",
                "INB %",
                "NAAB Opção 3",
                "3ª Opção",
                "INB %",
            ]

            if len(df.columns) >= len(expected_columns):
                df.columns = expected_columns + list(
                    df.columns[len(expected_columns):]
                )

            st.success("Arquivo carregado com sucesso")
            st.dataframe(df, use_container_width=True)

            # ===== Configurações =====
            st.subheader("Configurações do PDF")

            header_name = st.text_input(
                "Nome no cabeçalho",
                "Plano de Acasalamento – Alta Genetics",
            )

            watermark = st.text_input(
                "Texto da marca d’água",
                "USO INTERNO – ALTA GENETICS",
            )

            header_date = datetime.now().strftime("%d/%m/%Y")

            if st.button("📄 Gerar PDF"):
                config = {
                    "header_name": header_name,
                    "header_date": header_date,
                    "watermark": watermark,
                }

                pdf_path = generate_pdf(df, config)

                with open(pdf_path, "rb") as f:
                    st.download_button(
                        "⬇️ Download do PDF",
                        f,
                        file_name="resultado_acasalamento.pdf",
                        mime="application/pdf",
                    )

        except Exception as e:
            st.error(f"Erro ao processar o arquivo: {e}")


if __name__ == "__main__":
    main()
