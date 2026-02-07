import streamlit as st
import pandas as pd
from fpdf import FPDF
import math
import io
from datetime import datetime

st.set_page_config(
    page_title="CSV para PDF",
    page_icon="📄",
    layout="wide"
)

st.title("📄 Conversor de CSV para PDF")

class TablePDF(FPDF):
    def __init__(self, header_left, header_right):
        super().__init__(orientation="L", unit="mm", format="A4")
        self.header_left = header_left
        self.header_right = header_right

    def header(self):
        self.set_font("Helvetica", size=9)
        self.cell(0, 8, self.header_left, 0, 0, "L")
        self.cell(0, 8, self.header_right, 0, 1, "R")
        self.line(10, 18, 287, 18)
        self.ln(3)

    def footer(self):
        self.set_y(-12)
        self.set_font("Helvetica", size=8)
        self.cell(0, 8, f"Página {self.page_no()}", 0, 0, "C")

def generate_pdf(df, rows_per_page=30):
    pdf = TablePDF(
        header_left="Relatório de Acasalamento",
        header_right=datetime.now().strftime("%d/%m/%Y")
    )

    pdf.set_auto_page_break(auto=False)
    pdf.set_font("Helvetica", size=9)

    columns = df.columns.tolist()
    total_rows = len(df)
    pages = math.ceil(total_rows / rows_per_page)

    usable_width = 277
    col_width = usable_width / len(columns)
    row_height = 6

    for p in range(pages):
        pdf.add_page()

        pdf.set_font("Helvetica", "B", 9)
        for col in columns:
            pdf.cell(col_width, row_height + 2, str(col), 1, 0, "C")
        pdf.ln()

        pdf.set_font("Helvetica", size=9)
        start = p * rows_per_page
        end = min(start + rows_per_page, total_rows)

        for _, row in df.iloc[start:end].iterrows():
            for value in row:
                pdf.cell(col_width, row_height, str(value), 1, 0, "C")
            pdf.ln()

    buffer = io.BytesIO()
    pdf.output(buffer)
    buffer.seek(0)
    return buffer

file = st.file_uploader("📤 Envie o arquivo CSV", type="csv")

if file:
    df = pd.read_csv(file)
    st.success(f"Arquivo carregado: {df.shape[0]} linhas × {df.shape[1]} colunas")
    st.dataframe(df.head(20), use_container_width=True)

    rows = st.slider(
        "Linhas por página no PDF",
        min_value=10,
        max_value=50,
        value=30,
        step=5
    )

    if st.button("📄 Gerar PDF", type="primary"):
        with st.spinner("Gerando PDF..."):
            pdf_buffer = generate_pdf(df, rows)

        st.download_button(
            "📥 Baixar PDF",
            pdf_buffer,
            file_name="csv_para_pdf.pdf",
            mime="application/pdf"
        )
else:
    st.info("Faça upload de um arquivo CSV para começar.")
