"""
Versão Simplificada - Sistema de Acasalamento
Para testes rápidos e debug
"""

import streamlit as st
import pandas as pd
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib.enums import TA_CENTER
from datetime import datetime
import io
import math

st.set_page_config(page_title="Gerador PDF - Acasalamento", page_icon="🐄", layout="wide")

st.title("🐄 Gerador de Relatórios - Acasalamento de Animais")
st.markdown("---")

# Upload do arquivo
uploaded_file = st.file_uploader("📤 Upload do arquivo CSV", type=['csv'])

if uploaded_file:
    try:
        # Ler CSV
        df = pd.read_csv(uploaded_file)
        st.success(f"✅ Arquivo carregado: {len(df)} animais | {len(df.columns)} colunas")
        
        # Configurações básicas
        col1, col2, col3 = st.columns(3)
        
        with col1:
            client_name = st.text_input("Nome da Fazenda:", value="Fazenda Exemplo")
        
        with col2:
            font_size = st.slider("Tamanho da Fonte:", 8, 16, 10)
            max_rows = int((21*cm - 6*cm) / (font_size * 0.5))
            st.info(f"Máx: {max_rows} linhas")
        
        with col3:
            rows_per_page = st.number_input("Linhas por Página:", 10, max_rows, 30)
        
        # Seleção de colunas
        st.markdown("### Selecione as Colunas:")
        columns_to_show = st.multiselect(
            "Colunas:",
            options=df.columns.tolist(),
            default=df.columns.tolist()[:5]
        )
        
        if columns_to_show:
            # Preview
            st.markdown("### Preview:")
            st.dataframe(df[columns_to_show].head(10), use_container_width=True)
            
            # Botão gerar
            if st.button("🚀 Gerar PDF", type="primary"):
                with st.spinner("Gerando PDF..."):
                    # Preparar dados
                    df_filtered = df[columns_to_show].fillna('')
                    
                    # Criar PDF
                    buffer = io.BytesIO()
                    doc = SimpleDocTemplate(
                        buffer,
                        pagesize=landscape(A4),
                        rightMargin=2*cm,
                        leftMargin=2*cm,
                        topMargin=3*cm,
                        bottomMargin=2.5*cm
                    )
                    
                    elements = []
                    
                    # Capa simples
                    styles = getSampleStyleSheet()
                    title_style = ParagraphStyle(
                        'CustomTitle',
                        parent=styles['Title'],
                        fontSize=32,
                        textColor=colors.HexColor('#1f77b4'),
                        alignment=TA_CENTER,
                        fontName='Helvetica-Bold'
                    )
                    
                    elements.append(Spacer(1, 4*cm))
                    elements.append(Paragraph("RELATÓRIO DE ACASALAMENTO", title_style))
                    elements.append(Spacer(1, 2*cm))
                    
                    client_style = ParagraphStyle(
                        'ClientName',
                        parent=styles['Normal'],
                        fontSize=24,
                        alignment=TA_CENTER,
                        fontName='Helvetica-Bold'
                    )
                    elements.append(Paragraph(client_name, client_style))
                    elements.append(Spacer(1, 2*cm))
                    
                    date_style = ParagraphStyle(
                        'DateStyle',
                        parent=styles['Normal'],
                        fontSize=14,
                        alignment=TA_CENTER,
                        fontName='Helvetica'
                    )
                    elements.append(Paragraph(f"Data: {datetime.now().strftime('%d/%m/%Y')}", date_style))
                    elements.append(PageBreak())
                    
                    # Tabelas de dados
                    total_rows = len(df_filtered)
                    num_pages = math.ceil(total_rows / rows_per_page)
                    
                    for page_num in range(num_pages):
                        start_idx = page_num * rows_per_page
                        end_idx = min(start_idx + rows_per_page, total_rows)
                        df_page = df_filtered.iloc[start_idx:end_idx]
                        
                        # Preparar dados
                        data = [df_page.columns.tolist()]
                        data.extend(df_page.values.tolist())
                        
                        # Criar tabela
                        table = Table(data, repeatRows=1)
                        
                        style = TableStyle([
                            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1f77b4')),
                            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                            ('FONTSIZE', (0, 0), (-1, 0), font_size),
                            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                            ('FONTSIZE', (0, 1), (-1, -1), font_size),
                            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f0f0f0')]),
                        ])
                        
                        table.setStyle(style)
                        elements.append(table)
                        
                        if page_num < num_pages - 1:
                            elements.append(PageBreak())
                    
                    # Construir PDF
                    doc.build(elements)
                    buffer.seek(0)
                    
                    st.success("✅ PDF gerado com sucesso!")
                    
                    # Download
                    st.download_button(
                        label="📥 Baixar PDF",
                        data=buffer,
                        file_name=f"acasalamento_{client_name.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf",
                        mime="application/pdf"
                    )
        else:
            st.warning("⚠️ Selecione pelo menos uma coluna")
    
    except Exception as e:
        st.error(f"❌ Erro: {str(e)}")
        import traceback
        st.code(traceback.format_exc())

else:
    st.info("👆 Faça upload de um arquivo CSV para começar")
    st.markdown("""
    ### 📖 Como usar:
    1. Faça upload do CSV de acasalamento
    2. Configure o nome da fazenda
    3. Ajuste o tamanho da fonte (8-16pt)
    4. Defina quantas linhas por página
    5. Selecione as colunas desejadas
    6. Clique em "Gerar PDF"
    """)
