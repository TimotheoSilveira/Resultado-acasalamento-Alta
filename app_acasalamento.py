"""
Sistema de Geração de Relatórios PDF - Acasalamento de Animais
Versão 2.2 - CORRIGIDA

Correções:
- Logo da Alta aparece em TODAS as páginas
- Suporte para .jpg e .png
- Orientação paisagem ou retrato
- Páginas SEMPRE com o número máximo de linhas configurado
- Capa não empurra conteúdo
"""

import streamlit as st
import pandas as pd
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape, portrait
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, PageBreak
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas
from datetime import datetime
import io
import os
import math

# Buscar logo da Alta (PNG ou JPG)
LOGO_ALTA_PATH = None
for filename in ['Logo Alta_com frase.png', 'Logo Alta_com frase.jpg', 
                  'Logo_Alta_com_frase.png', 'Logo_Alta_com_frase.jpg',
                  'logo_alta_com_frase.png', 'logo_alta_com_frase.jpg']:
    test_path = os.path.join(os.path.dirname(__file__) if __file__ else '.', filename)
    if os.path.exists(test_path):
        LOGO_ALTA_PATH = test_path
        break

def rename_csv_columns(df):
    """Renomeia as colunas do CSV para nomes mais amigáveis"""
    df_renamed = df.copy()
    original_cols = df.columns.tolist()
    new_names = []
    
    naab_count = 0
    nome_curto_count = 0
    inb_count = 0
    
    for col in original_cols:
        col_upper = col.upper().strip()
        
        if 'NÚMERO' in col_upper or 'NUMERO' in col_upper:
            new_names.append('ID animal')
        elif col_upper == 'STOC':
            new_names.append('Tipo sêmen')
        elif 'ÍNDICE' in col_upper or 'INDICE' in col_upper:
            new_names.append('Índice')
        elif 'TOURO' in col_upper:
            new_names.append('Código pai')
        elif col_upper == 'NAAB':
            naab_count += 1
            new_names.append(f'NAAB Opção {naab_count}')
        elif 'NOME CURTO' in col_upper or ('NOME' in col_upper and 'CURTO' in col_upper):
            nome_curto_count += 1
            new_names.append(f'{nome_curto_count}º Opção')
        elif 'INB' in col_upper and '%' in col_upper:
            inb_count += 1
            if inb_count == 1:
                new_names.append('INB %')
            else:
                new_names.append(f'INB % ({inb_count})')
        else:
            new_names.append(col)
    
    df_renamed.columns = new_names
    return df_renamed

def calculate_max_rows_per_page(font_size, orientation='landscape'):
    """Calcula o número máximo de linhas por página"""
    if orientation == 'landscape':
        page_height = landscape(A4)[1]
    else:
        page_height = portrait(A4)[1]
    
    top_margin = 3.5 * cm
    bottom_margin = 2.5 * cm
    available_height = page_height - top_margin - bottom_margin
    
    header_row_height = font_size + 12
    row_height = font_size + 6
    
    rows_fit = int((available_height - header_row_height) / row_height)
    return max(10, rows_fit)

# Classe para cabeçalho e rodapé
class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        self.header_text = kwargs.pop('header_text', '')
        self.header_date = kwargs.pop('header_date', '')
        self.orientation = kwargs.pop('orientation', 'landscape')
        canvas.Canvas.__init__(self, *args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_number(num_pages)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def draw_page_number(self, page_count):
        if self.orientation == 'landscape':
            page_width = landscape(A4)[0]
            page_height = landscape(A4)[1]
        else:
            page_width = portrait(A4)[0]
            page_height = portrait(A4)[1]
        
        # Logo da Alta em TODAS as páginas
        if LOGO_ALTA_PATH and os.path.exists(LOGO_ALTA_PATH):
            try:
                self.drawImage(LOGO_ALTA_PATH, 2*cm, page_height - 2.8*cm, 
                             width=2*cm, height=2*cm, 
                             preserveAspectRatio=True, mask='auto')
            except:
                pass
        
        # Cabeçalho e rodapé apenas nas páginas de dados (não na capa)
        if self._pageNumber > 1:
            # Cabeçalho
            self.setFont("Helvetica", 10)
            self.drawString(4.5*cm, page_height - 2*cm, self.header_text)
            self.drawRightString(page_width - 2*cm, page_height - 2*cm, self.header_date)
            
            # Linha abaixo do cabeçalho
            self.setStrokeColor(colors.grey)
            self.setLineWidth(0.5)
            self.line(2*cm, page_height - 3*cm, page_width - 2*cm, page_height - 3*cm)
            
            # Rodapé com numeração
            self.setFont("Helvetica", 9)
            page_text = f"Página {self._pageNumber - 1} de {page_count - 1}"
            self.drawCentredString(page_width / 2, 1.5*cm, page_text)

def create_cover_page(client_name, responsible_name, contact_phone, orientation='landscape'):
    """Cria a capa do relatório - PÁGINA ÚNICA"""
    elements = []
    
    if orientation == 'landscape':
        page_width = landscape(A4)[0]
        page_height = landscape(A4)[1]
    else:
        page_width = portrait(A4)[0]
        page_height = portrait(A4)[1]
    
    # Título
    title_data = [[f"RELATÓRIO DE ACASALAMENTO"]]
    title_table = Table(title_data, colWidths=[page_width - 4*cm])
    title_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 28),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#1f77b4')),
        ('TOPPADDING', (0, 0), (-1, -1), 4*cm),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 1*cm),
    ]))
    elements.append(title_table)
    
    # Informações
    info_data = [
        [f"{client_name}"],
        [""],
        [f"Responsável: {responsible_name}"],
        [f"Telefone: {contact_phone}"],
        [""],
        [f"Data: {datetime.now().strftime('%d/%m/%Y')}"]
    ]
    info_table = Table(info_data, colWidths=[page_width - 4*cm])
    info_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (0, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (0, 0), 22),
        ('FONTNAME', (0, 2), (0, 3), 'Helvetica'),
        ('FONTSIZE', (0, 2), (0, 3), 14),
        ('FONTNAME', (0, 5), (0, 5), 'Helvetica'),
        ('FONTSIZE', (0, 5), (0, 5), 12),
        ('TEXTCOLOR', (0, 5), (0, 5), colors.grey),
    ]))
    elements.append(info_table)
    
    elements.append(PageBreak())
    return elements

def create_data_pages(df, columns_to_show, rows_per_page, font_size, orientation='landscape'):
    """Cria páginas de dados preenchendo SEMPRE com rows_per_page linhas"""
    elements = []
    
    df_filtered = df[columns_to_show].copy()
    df_filtered = df_filtered.fillna('')
    
    total_rows = len(df_filtered)
    num_pages = math.ceil(total_rows / rows_per_page)
    
    if orientation == 'landscape':
        page_width = landscape(A4)[0]
    else:
        page_width = portrait(A4)[0]
    
    # Calcular largura das colunas
    num_cols = len(columns_to_show)
    available_width = page_width - 4*cm
    col_width = available_width / num_cols
    col_widths = [col_width] * num_cols
    
    for page_num in range(num_pages):
        start_idx = page_num * rows_per_page
        end_idx = start_idx + rows_per_page
        
        if end_idx <= total_rows:
            # Página completa
            df_page = df_filtered.iloc[start_idx:end_idx]
        else:
            # Última página - preencher com linhas vazias
            df_page = df_filtered.iloc[start_idx:total_rows]
            rows_needed = rows_per_page - len(df_page)
            empty_rows = pd.DataFrame(
                [[''] * num_cols for _ in range(rows_needed)],
                columns=columns_to_show
            )
            df_page = pd.concat([df_page, empty_rows], ignore_index=True)
        
        # Preparar dados
        data = [columns_to_show]  # Cabeçalho
        data.extend(df_page.values.tolist())
        
        # Criar tabela
        table = Table(data, colWidths=col_widths, repeatRows=1)
        
        # Estilo
        style = TableStyle([
            # Cabeçalho
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1f77b4')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), font_size),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
            ('TOPPADDING', (0, 0), (-1, 0), 8),
            
            # Dados
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), font_size),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f0f0f0')]),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (-1, -1), 3),
            ('RIGHTPADDING', (0, 0), (-1, -1), 3),
            ('TOPPADDING', (0, 1), (-1, -1), 2),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 2),
        ])
        
        table.setStyle(style)
        elements.append(table)
        
        if page_num < num_pages - 1:
            elements.append(PageBreak())
    
    return elements

def generate_pdf(df, config):
    """Gera o PDF completo"""
    buffer = io.BytesIO()
    
    orientation = config.get('orientation', 'landscape')
    if orientation == 'landscape':
        pagesize = landscape(A4)
    else:
        pagesize = portrait(A4)
    
    doc = SimpleDocTemplate(
        buffer,
        pagesize=pagesize,
        rightMargin=2*cm,
        leftMargin=2*cm,
        topMargin=3.5*cm,
        bottomMargin=2.5*cm
    )
    
    elements = []
    
    # Capa
    cover = create_cover_page(
        config['client_name'],
        config['responsible_name'],
        config['contact_phone'],
        orientation
    )
    elements.extend(cover)
    
    # Dados
    data_pages = create_data_pages(
        df,
        config['columns_to_show'],
        config['rows_per_page'],
        config['font_size'],
        orientation
    )
    elements.extend(data_pages)
    
    # Construir PDF
    doc.build(
        elements,
        canvasmaker=lambda *args, **kwargs: NumberedCanvas(
            *args,
            header_text=config['header_name'],
            header_date=config['header_date'],
            orientation=orientation,
            **kwargs
        )
    )
    
    buffer.seek(0)
    return buffer

# Interface Streamlit
st.set_page_config(page_title="Gerador de Relatórios PDF - Acasalamento", layout="wide")

st.title("📊 Gerador de Relatórios PDF - Acasalamento de Animais")

# Info sobre logo
if LOGO_ALTA_PATH:
    st.success(f"✅ Logo da Alta encontrada: {os.path.basename(LOGO_ALTA_PATH)}")
else:
    st.warning("⚠️ Logo da Alta não encontrada. Coloque 'Logo Alta_com frase.png' ou 'Logo Alta_com frase.jpg' no mesmo diretório do app.")

uploaded_file = st.file_uploader("📁 Carregar arquivo CSV", type=['csv'])

if uploaded_file:
    try:
        df = pd.read_csv(uploaded_file)
        df = rename_csv_columns(df)
        
        st.success(f"✅ Arquivo carregado: {len(df)} animais | {len(df.columns)} colunas")
        
        # Configurações
        st.markdown("---")
        col1, col2, col3 = st.columns([1, 1, 1])
        
        with col1:
            st.markdown("### 📝 Informações da Capa")
            client_name = st.text_input("Nome da Fazenda/Cliente:", value="Fazenda Exemplo")
            responsible_name = st.text_input("Responsável pelo Acasalamento:", value="")
            contact_phone = st.text_input("Telefone para Contato:", value="")
        
        with col2:
            st.markdown("### 📌 Cabeçalho das Páginas")
            header_name = st.text_input("Texto Esquerdo:", value="Relatório de Acasalamento")
            header_date = st.text_input("Texto Direito:", value=datetime.now().strftime('%d/%m/%Y'))
        
        with col3:
            st.markdown("### 🔧 Configurações")
            orientation = st.radio(
                "Orientação:",
                options=['landscape', 'portrait'],
                format_func=lambda x: 'Paisagem (Horizontal)' if x == 'landscape' else 'Retrato (Vertical)',
                index=0
            )
            
            font_size = st.slider("Tamanho da Fonte:", min_value=6, max_value=14, value=8, step=1)
            
            max_rows = calculate_max_rows_per_page(font_size, orientation)
            st.info(f"💡 Máximo: **{max_rows} linhas/página**")
            
            rows_per_page = st.number_input(
                "Linhas por Página:",
                min_value=10,
                max_value=max_rows,
                value=min(40, max_rows),
                step=5
            )
        
        # Seleção de colunas
        st.markdown("---")
        st.markdown("### 📋 Selecionar Colunas para o Relatório")
        
        all_columns = df.columns.tolist()
        
        col_select1, col_select2 = st.columns([3, 1])
        
        with col_select1:
            cols = st.columns(4)
            selected_columns = []
            for idx, col in enumerate(all_columns):
                with cols[idx % 4]:
                    if st.checkbox(col, value=True, key=f"col_{idx}"):
                        selected_columns.append(col)
        
        with col_select2:
            st.markdown("**Ações Rápidas:**")
            if st.button("✅ Selecionar Todas"):
                st.rerun()
            if st.button("❌ Desmarcar Todas"):
                st.rerun()
        
        if selected_columns:
            # Preview
            st.markdown("### 👁️ Preview dos Dados")
            st.dataframe(df[selected_columns].head(10), use_container_width=True)
            
            total_pages = math.ceil(len(df) / rows_per_page) + 1  # +1 para capa
            st.info(f"📄 O relatório terá aproximadamente **{total_pages} páginas** ({total_pages-1} de dados + 1 capa)")
            
            # Gerar PDF
            if st.button("🚀 Gerar PDF", type="primary"):
                with st.spinner("⏳ Gerando PDF..."):
                    config = {
                        'client_name': client_name,
                        'responsible_name': responsible_name,
                        'contact_phone': contact_phone,
                        'header_name': header_name,
                        'header_date': header_date,
                        'columns_to_show': selected_columns,
                        'rows_per_page': rows_per_page,
                        'font_size': font_size,
                        'orientation': orientation
                    }
                    
                    pdf_buffer = generate_pdf(df, config)
                    
                    st.success("✅ PDF gerado com sucesso!")
                    
                    filename = f"acasalamento_{client_name.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf"
                    
                    st.download_button(
                        label="📥 Baixar PDF",
                        data=pdf_buffer,
                        file_name=filename,
                        mime="application/pdf"
                    )
        else:
            st.warning("⚠️ Selecione pelo menos uma coluna para gerar o relatório")
            
    except Exception as e:
        st.error(f"❌ Erro ao processar arquivo: {str(e)}")
        st.exception(e)
else:
    st.info("👆 Faça upload de um arquivo CSV para começar")
