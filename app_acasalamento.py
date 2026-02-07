import streamlit as st
import pandas as pd
import math
import io
from datetime import datetime
from fpdf import FPDF

# =========================================================
# STREAMLIT CONFIG
# =========================================================
st.set_page_config(
    page_title="Gerador de Relatórios - Acasalamento",
    page_icon="🐄",
    layout="wide"
)

# =========================================================
# PDF CLASS
# =========================================================
class PDF(FPDF):
    def __init__(self, header_left="", header_right=""):
        super().__init__(orientation="L", unit="mm", format="A4")
        self.header_left = header_left
        self.header_right = header_right

    def header(self):
        if self.page_no() > 1:
            self.set_font("Helvetica", size=9)
            self.cell(0, 8, self.header_left, 0, 0, "L")
            self.cell(0, 8, self.header_right, 0, 1, "R")
            self.line(10, 18, 287, 18)
            self.ln(3)

    def footer(self):
        if self.page_no() > 1:
            self.set_y(-12)
            self.set_font("Helvetica", size=8)
            self.cell(0, 8, f"Página {self.page_no() - 1}", 0, 0, "C")


# =========================================================
# AUX FUNCTIONS
# =========================================================
def max_rows_per_page(font_size):
    usable_height = 180
    row_height = font_size * 0.6 + 2
    return max(10, int(usable_height / row_height))


def generate_pdf(df, cfg):
    pdf = PDF(cfg["header_left"], cfg["header_right"])
    pdf.set_auto_page_break(auto=False)

    # ---------------- CAPA ----------------
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 28)
    pdf.ln(50)
    pdf.cell(0, 15, "RELATÓRIO DE ACASALAMENTO", 0, 1, "C")
    pdf.ln(10)
    pdf.set_font("Helvetica", size=18)
    pdf.cell(0, 12, cfg["client"], 0, 1, "C")
    pdf.ln(10)
    pdf.set_font("Helvetica", size=12)
    pdf.cell(0, 10, datetime.now().strftime("%d/%m/%Y"), 0, 1, "C")

    # ---------------- DADOS ----------------
    columns = cfg["columns"]
    rows_per_page = cfg["rows"]
    font_size = cfg["font"]

    df = df[columns].fillna("")
    total_rows = len(df)
    pages = math.ceil(total_rows / rows_per_page)

    col_width = 277 / len(columns)
    row_height = font_size * 0.6 + 2

    for p in range(pages):
        pdf.add_page()
        pdf.set_font("Helvetica", "B", font_size)

        # Header table
        for col in columns:
            pdf.cell(col_width, row_height + 2, col, 1, 0, "C")
        pdf.ln()

        pdf.set_font("Helvetica", size=font_size)

        start = p * rows_per_page
        end = min(start + rows_per_page, total_rows)

        for _, row in df.iloc[start:end].iterrows():
            for item in row:
                pdf.cell(col_width, row_height, str(item), 1, 0, "C")
            pdf.ln()

    buffer = io.BytesIO()
    pdf.output(buffer)
    buffer.seek(0)
    return buffer


# =========================================================
# APP
# =========================================================
def main():
    st.title("🐄 Gerador de Relatórios de Acasalamento")

    with st.sidebar:
        file = st.file_uploader("Upload CSV", type="csv")

    if not file:
        st.info("Faça o upload do CSV para iniciar.")
        return

    df = pd.read_csv(file)

    col1, col2 = st.columns(2)
    with col1:
        client = st.text_input("Cliente", "Fazenda Exemplo")
        header_left = st.text_input("Cabeçalho esquerdo", "Relatório de Acasalamento")
    with col2:
        header_right = st.text_input(
            "Cabeçalho direito",
            datetime.now().strftime("%d/%m/%Y")
        )

    font = st.slider("Tamanho da fonte", 8, 14, 10)
    max_rows = max_rows_per_page(font)
    rows = st.number_input(
        "Linhas por página",
        10,
        max_rows,
        min(30, max_rows)
    )

    columns = st.multiselect(
        "Colunas",
        df.columns.tolist(),
        default=df.columns.tolist()
    )

    if st.button("Gerar PDF", type="primary"):
        if not columns:
            st.error("Selecione ao menos uma coluna.")
            return

        cfg = {
            "client": client,
            "header_left": header_left,
            "header_right": header_right,
            "columns": columns,
            "rows": rows,
            "font": font,
        }

        with st.spinner("Gerando PDF..."):
            pdf = generate_pdf(df, cfg)

        st.download_button(
            "Baixar PDF",
            pdf,
            file_name="acasalamento.pdf",
            mime="application/pdf"
        )


if __name__ == "__main__":
    main()
