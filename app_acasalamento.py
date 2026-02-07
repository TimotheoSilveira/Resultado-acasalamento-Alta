"""
Sistema de Geração de Relatórios PDF - Acasalamento de Animais

NOTA SOBRE FONTES:
Este sistema utiliza a fonte Helvetica, que é a fonte padrão do ReportLab e 
é praticamente idêntica à Arial. O ReportLab não inclui Arial por padrão, 
mas Helvetica oferece a mesma aparência e legibilidade.

Fontes disponíveis no ReportLab:
- Helvetica (equivalente a Arial)
- Helvetica-Bold
- Times-Roman
- Courier
"""

import streamlit as st
import pandas as pd
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.pdfgen import canvas
from datetime import datetime
import io
import os
import math

# Mapeamento de nomes de colunas
COLUMN_MAPPING = {
    'NÚMERO DE VACAS': 'ID animal',
    'STOC': 'Tipo sêmen',
    'ÍNDICE': 'Índice',
    'TOURO NAAB': 'Código pai',
    'NAAB': 'NAAB Opção 1',  # Primeira ocorrência
    'NOME CURTO': '1º Opção',  # Primeira ocorrência
    'INB %': 'INB %',  # Primeira ocorrência
}

# Logo da Alta (buscar no mesmo diretório do script)
LOGO_ALTA_PATH = os.path.join(os.path.dirname(__file__), 'Logo Alta_com frase.png')
if not os.path.exists(LOGO_ALTA_PATH):
    # Tentar outras variações de nome
    for filename in ['Logo Alta_com frase.png', 'logo_alta_com_frase.png', 'Logo_Alta_com_frase.png']:
        test_path = os.path.join(os.path.dirname(__file__), filename)
        if os.path.exists(test_path):
            LOGO_ALTA_PATH = test_path
            break

# Configuração da página
st.set_page_config(
    page_title="Gerador de Relatórios - Acasalamento de Animais",
    page_icon="🐄",
    layout="wide"
)

# Estilos CSS customizados
st.markdown("""
    <style>
    .main-title {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .section-title {
        font-size: 1.5rem;
        font-weight: bold;
        color: #2c3e50;
        margin-top: 1.5rem;
        margin-bottom: 1rem;
    }
    .info-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #e8f4f8;
        border-left: 4px solid #1f77b4;
        margin: 1rem 0;
    }
    </style>
""", unsafe_allow_html=True)

def calculate_max_rows_per_page(font_size):
    """
    Calcula o número máximo de linhas que cabem em uma página A4 paisagem
    baseado no tamanho da fonte
    """
    # Dimensões da página A4 em paisagem
    page_height = landscape(A4)[1]  # ~21cm = 595.27 pontos
    
    # Área disponível para a tabela (descontando margens e cabeçalhos)
    top_margin = 3 * cm  # Margem superior + cabeçalho
    bottom_margin = 2.5 * cm  # Margem inferior + rodapé
    available_height = page_height - top_margin - bottom_margin
    
    # Altura da linha do cabeçalho da tabela
    header_row_height = font_size + 12  # Cabeçalho com padding
    
    # Altura de cada linha de dados
    row_height = font_size + 6  # Fonte + padding
    
    # Calcular quantas linhas cabem
    rows_fit = int((available_height - header_row_height) / row_height)
    
    return max(10, rows_fit)  # Mínimo de 10 linhas por página

def rename_csv_columns(df):
    """
    Renomeia as colunas do CSV para nomes mais amigáveis
    
    Mapeamento:
    - NÚMERO DE VACAS -> ID animal
    - STOC -> Tipo sêmen
    - ÍNDICE -> Índice
    - TOURO NAAB -> Código pai
    - NAAB (1ª) -> NAAB Opção 1
    - NOME CURTO (1ª) -> 1º Opção
    - INB % (1ª) -> INB %
    - NAAB (2ª) -> NAAB Opção 2
    - NOME CURTO (2ª) -> 2º Opção
    - INB % (2ª) -> INB %
    - NAAB (3ª) -> NAAB Opção 3
    - NOME CURTO (3ª) -> 3º Opção
    - INB % (3ª) -> INB %
    """
    # Criar cópia do dataframe
    df_renamed = df.copy()
    
    # Lista de colunas originais
    original_cols = df.columns.tolist()
    
    # Novos nomes
    new_names = []
    
    # Contadores para colunas repetidas
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
            if naab_count == 1:
                new_names.append('NAAB Opção 1')
            elif naab_count == 2:
                new_names.append('NAAB Opção 2')
            elif naab_count == 3:
                new_names.append('NAAB Opção 3')
            else:
                new_names.append(f'NAAB {naab_count}')
        elif 'NOME CURTO' in col_upper or 'NOME' in col_upper and 'CURTO' in col_upper:
            nome_curto_count += 1
            if nome_curto_count == 1:
                new_names.append('1º Opção')
            elif nome_curto_count == 2:
                new_names.append('2º Opção')
            elif nome_curto_count == 3:
                new_names.append('3º Opção')
            else:
                new_names.append(f'{nome_curto_count}º Opção')
        elif 'INB' in col_upper and '%' in col_upper:
            inb_count += 1
            if inb_count == 1:
                new_names.append('INB %')
            elif inb_count == 2:
                new_names.append('INB % (2)')
            elif inb_count == 3:
                new_names.append('INB % (3)')
            else:
                new_names.append(f'INB % ({inb_count})')
        else:
            # Manter nome original se não for mapeado
            new_names.append(col)
    
    # Renomear colunas
    df_renamed.columns = new_names
    
    return df_renamed

def get_font_size_limits():
    """Retorna os limites de tamanho de fonte e linhas recomendadas"""
    return {
        8: calculate_max_rows_per_page(8),
        9: calculate_max_rows_per_page(9),
        10: calculate_max_rows_per_page(10),
        11: calculate_max_rows_per_page(11),
        12: calculate_max_rows_per_page(12),
        13: calculate_max_rows_per_page(13),
        14: calculate_max_rows_per_page(14),
        15: calculate_max_rows_per_page(15),
        16: calculate_max_rows_per_page(16),
    }

# Classe para cabeçalho e rodapé
class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        self.header_text = kwargs.pop('header_text', '')
        self.header_date = kwargs.pop('header_date', '')
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
        page_width = landscape(A4)[0]
        page_height = landscape(A4)[1]
        
        # Logo da Alta em TODAS as páginas (incluindo capa)
        if os.path.exists(LOGO_ALTA_PATH):
            try:
                # Logo pequeno no cabeçalho (1.5cm x 1.5cm)
                self.drawImage(LOGO_ALTA_PATH, 2*cm, page_height - 2.5*cm, 
                             width=1.5*cm, height=1.5*cm, 
                             preserveAspectRatio=True, mask='auto')
            except:
                pass  # Se houver erro ao carregar logo, continua sem ela
        
        # Pular cabeçalho e rodapé apenas na primeira página (capa)
        if self._pageNumber > 1:
            # Cabeçalho (ajustado para dar espaço ao logo)
            self.setFont("Helvetica", 10)
            self.drawString(4*cm, page_height - 2*cm, self.header_text)
            self.drawRightString(page_width - 2*cm, page_height - 2*cm, self.header_date)
            
            # Linha abaixo do cabeçalho
            self.setStrokeColor(colors.grey)
            self.setLineWidth(0.5)
            self.line(2*cm, page_height - 2.7*cm, page_width - 2*cm, page_height - 2.7*cm)
            
            # Rodapé com numeração
            self.setFont("Helvetica", 9)
            page_text = f"Página {self._pageNumber - 1} de {page_count - 1}"
            self.drawCentredString(page_width / 2, 1.5*cm, page_text)

def create_cover_page(template, client_name, responsible_name, contact_phone, logo_path=None):
    """Cria a capa do relatório"""
    elements = []
    styles = getSampleStyleSheet()
    
    # Espaço inicial (considerando logo da Alta no topo)
    elements.append(Spacer(1, 3*cm))
    
    # Logo (se fornecido)
    if logo_path and os.path.exists(logo_path):
        try:
            img = Image(logo_path, width=8*cm, height=8*cm, kind='proportional')
            img.hAlign = 'CENTER'
            elements.append(img)
            elements.append(Spacer(1, 2*cm))
        except:
            pass
    
    # Título baseado no template
    if template == "Empresarial":
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Title'],
            fontSize=36,
            textColor=colors.HexColor('#1f77b4'),
            spaceAfter=30,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        )
        title = Paragraph("RELATÓRIO DE ACASALAMENTO", title_style)
        
    elif template == "Técnico":
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Title'],
            fontSize=32,
            textColor=colors.HexColor('#2c3e50'),
            spaceAfter=30,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        )
        title = Paragraph("RELATÓRIO TÉCNICO<br/>ACASALAMENTO DE ANIMAIS", title_style)
        
    elif template == "Executivo":
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Title'],
            fontSize=34,
            textColor=colors.HexColor('#27ae60'),
            spaceAfter=30,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        )
        title = Paragraph("RELATÓRIO EXECUTIVO<br/>ACASALAMENTO", title_style)
    
    elements.append(title)
    elements.append(Spacer(1, 1.5*cm))
    
    # Nome do cliente
    client_style = ParagraphStyle(
        'ClientName',
        parent=styles['Normal'],
        fontSize=26,
        textColor=colors.HexColor('#34495e'),
        alignment=TA_CENTER,
        fontName='Helvetica-Bold',
        spaceAfter=20
    )
    client = Paragraph(f"{client_name}", client_style)
    elements.append(client)
    elements.append(Spacer(1, 1*cm))
    
    # Informações do responsável
    info_style = ParagraphStyle(
        'InfoStyle',
        parent=styles['Normal'],
        fontSize=14,
        textColor=colors.HexColor('#2c3e50'),
        alignment=TA_CENTER,
        fontName='Helvetica',
        spaceAfter=10
    )
    
    # Nome do responsável
    responsible = Paragraph(f"<b>Responsável pelo Acasalamento:</b> {responsible_name}", info_style)
    elements.append(responsible)
    
    # Telefone
    phone = Paragraph(f"<b>Telefone para Contato:</b> {contact_phone}", info_style)
    elements.append(phone)
    
    # Data
    date_style = ParagraphStyle(
        'DateStyle',
        parent=styles['Normal'],
        fontSize=16,
        textColor=colors.grey,
        alignment=TA_CENTER,
        fontName='Helvetica'
    )
    date_text = Paragraph(f"Data: {datetime.now().strftime('%d/%m/%Y')}", date_style)
    elements.append(Spacer(1, 1.5*cm))
    elements.append(date_text)
    
    elements.append(PageBreak())
    return elements

def create_data_tables(df, columns_to_show, rows_per_page, font_size):
    """Cria tabelas com os dados do CSV, divididas por número de linhas.
    Sempre preenche a página completamente com exatamente rows_per_page linhas."""
    elements = []
    
    # Filtrar apenas as colunas selecionadas
    df_filtered = df[columns_to_show].copy()
    
    # Converter valores NaN para string vazia
    df_filtered = df_filtered.fillna('')
    
    # Calcular número de páginas necessárias
    total_rows = len(df_filtered)
    num_pages = math.ceil(total_rows / rows_per_page)
    
    for page_num in range(num_pages):
        # Determinar início e fim do slice
        start_idx = page_num * rows_per_page
        end_idx = start_idx + rows_per_page  # SEMPRE pegar rows_per_page linhas
        
        # Obter dados para esta página
        if end_idx <= total_rows:
            # Página completa com dados reais
            df_page = df_filtered.iloc[start_idx:end_idx]
        else:
            # Última página - preencher com dados reais + linhas vazias
            df_page = df_filtered.iloc[start_idx:total_rows]
            
            # Calcular quantas linhas vazias precisamos adicionar
            rows_needed = rows_per_page - len(df_page)
            
            # Criar linhas vazias
            empty_rows = pd.DataFrame(
                [[''] * len(columns_to_show) for _ in range(rows_needed)],
                columns=columns_to_show
            )
            
            # Adicionar linhas vazias ao dataframe da página
            df_page = pd.concat([df_page, empty_rows], ignore_index=True)
        
        # Preparar dados para a tabela
        data = [df_page.columns.tolist()]  # Cabeçalho
        data.extend(df_page.values.tolist())  # Dados
        
        # Criar tabela
        table = Table(data, repeatRows=1)
        
        # Estilo da tabela
        style = TableStyle([
            # Cabeçalho
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1f77b4')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), font_size),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('TOPPADDING', (0, 0), (-1, 0), 12),
            
            # Dados
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), font_size),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f0f0f0')]),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (-1, -1), 4),
            ('RIGHTPADDING', (0, 0), (-1, -1), 4),
            ('TOPPADDING', (0, 1), (-1, -1), 3),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 3),
        ])
        
        table.setStyle(style)
        elements.append(table)
        
        # Adicionar quebra de página, exceto na última página
        if page_num < num_pages - 1:
            elements.append(PageBreak())
    
    return elements

def generate_pdf(df, config):
    """Gera o PDF completo em formato paisagem"""
    buffer = io.BytesIO()
    
    # Criar documento com orientação paisagem
    doc = SimpleDocTemplate(
        buffer,
        pagesize=landscape(A4),
        rightMargin=2*cm,
        leftMargin=2*cm,
        topMargin=3*cm,
        bottomMargin=2.5*cm
    )
    
    elements = []
    
    # Adicionar capa
    cover_elements = create_cover_page(
        config['template'],
        config['client_name'],
        config['responsible_name'],
        config['contact_phone'],
        config.get('logo_path')
    )
    elements.extend(cover_elements)
    
    # Adicionar tabelas de dados
    data_tables = create_data_tables(
        df,
        config['columns_to_show'],
        config['rows_per_page'],
        config['font_size']
    )
    elements.extend(data_tables)
    
    # Construir PDF com cabeçalho e rodapé
    doc.build(
        elements,
        canvasmaker=lambda *args, **kwargs: NumberedCanvas(
            *args,
            header_text=config['header_name'],
            header_date=config['header_date'],
            **kwargs
        )
    )
    
    buffer.seek(0)
    return buffer

# Interface Streamlit
def main():
    st.markdown('<p class="main-title">🐄 Gerador de Relatórios - Acasalamento de Animais</p>', unsafe_allow_html=True)
    
    # Sidebar para upload e configurações principais
    with st.sidebar:
        st.header("⚙️ Configurações")
        
        # Upload do CSV
        uploaded_file = st.file_uploader("📤 Upload do arquivo CSV", type=['csv'])
        
        if uploaded_file:
            # Upload de logo (opcional)
            logo_file = st.file_uploader("🖼️ Logo para a capa (opcional)", type=['png', 'jpg', 'jpeg'])
            
            st.markdown("---")
            st.subheader("📋 Template da Capa")
            template = st.selectbox(
                "Escolha o template:",
                ["Empresarial", "Técnico", "Executivo"]
            )
    
    # Área principal
    if uploaded_file:
        # Salvar logo temporariamente se fornecido
        logo_path = None
        if logo_file:
            logo_path = "/tmp/logo_temp.png"
            with open(logo_path, "wb") as f:
                f.write(logo_file.getbuffer())
        
        # Ler CSV
        try:
            df = pd.read_csv(uploaded_file)
            
            # Renomear colunas para nomes mais amigáveis
            df = rename_csv_columns(df)
            
            st.success(f"✅ Arquivo carregado: {len(df)} animais | {len(df.columns)} colunas")
            
            # Criar colunas para configurações
            st.markdown("---")
            col1, col2, col3 = st.columns([1, 1, 1])
            
            with col1:
                st.markdown('<p class="section-title">📝 Informações da Capa</p>', unsafe_allow_html=True)
                client_name = st.text_input(
                    "Nome da Fazenda/Cliente:",
                    value="Fazenda Exemplo",
                    help="Nome que aparecerá na capa do relatório"
                )
                responsible_name = st.text_input(
                    "Responsável pelo Acasalamento:",
                    value="",
                    help="Nome do responsável técnico"
                )
                contact_phone = st.text_input(
                    "Telefone para Contato:",
                    value="",
                    help="Telefone do responsável"
                )
            
            with col2:
                st.markdown('<p class="section-title">📌 Cabeçalho das Páginas</p>', unsafe_allow_html=True)
                header_name = st.text_input(
                    "Texto Esquerdo:",
                    value="Relatório de Acasalamento",
                    help="Texto que aparecerá no canto esquerdo do cabeçalho"
                )
                header_date = st.text_input(
                    "Texto Direito:",
                    value=datetime.now().strftime('%d/%m/%Y'),
                    help="Texto que aparecerá no canto direito do cabeçalho"
                )
            
            with col3:
                st.markdown('<p class="section-title">📊 Dados Técnicos</p>', unsafe_allow_html=True)
                st.info("ℹ️ Informações adicionais serão exibidas na capa do relatório")
            
            # Configurações de formatação
            st.markdown("---")
            st.markdown('<p class="section-title">⚙️ Configurações de Formatação</p>', unsafe_allow_html=True)
            
            col_format1, col_format2 = st.columns([1, 1])
            
            with col_format1:
                # Tamanho da fonte
                font_size = st.slider(
                    "Tamanho da Fonte:",
                    min_value=8,
                    max_value=16,
                    value=10,
                    step=1,
                    help="Tamanho da fonte para a tabela (mínimo 8, máximo 16)"
                )
                
                # Calcular máximo de linhas para o tamanho de fonte escolhido
                max_rows_possible = calculate_max_rows_per_page(font_size)
                
                st.info(f"💡 Com fonte {font_size}pt, cabem até **{max_rows_possible} linhas** por página")
            
            with col_format2:
                # Linhas por página
                rows_per_page = st.number_input(
                    "Linhas por Página:",
                    min_value=10,
                    max_value=max_rows_possible,
                    value=min(30, max_rows_possible),
                    step=1,
                    help=f"Quantidade de animais por página (máximo {max_rows_possible} para fonte {font_size}pt)"
                )
                
                # Calcular número de páginas
                total_pages = math.ceil(len(df) / rows_per_page)
                st.info(f"📄 Serão geradas **{total_pages} páginas** de dados (+ capa)")
            
            # Seleção de colunas
            st.markdown("---")
            st.markdown('<p class="section-title">📊 Seleção de Colunas</p>', unsafe_allow_html=True)
            
            st.write("Selecione as colunas que deseja exibir no relatório:")
            
            # Criar checkboxes para cada coluna
            col_select1, col_select2, col_select3, col_select4 = st.columns(4)
            
            columns_to_show = []
            all_columns = df.columns.tolist()
            
            # Distribuir colunas em 4 colunas
            cols_per_column = math.ceil(len(all_columns) / 4)
            
            for idx, col_name in enumerate(all_columns):
                col_position = idx % 4
                
                if col_position == 0:
                    with col_select1:
                        if st.checkbox(col_name, value=True, key=f"col_{idx}"):
                            columns_to_show.append(col_name)
                elif col_position == 1:
                    with col_select2:
                        if st.checkbox(col_name, value=True, key=f"col_{idx}"):
                            columns_to_show.append(col_name)
                elif col_position == 2:
                    with col_select3:
                        if st.checkbox(col_name, value=True, key=f"col_{idx}"):
                            columns_to_show.append(col_name)
                else:
                    with col_select4:
                        if st.checkbox(col_name, value=True, key=f"col_{idx}"):
                            columns_to_show.append(col_name)
            
            # Botões de seleção rápida
            st.markdown("---")
            col_btn1, col_btn2, col_btn3, col_btn4 = st.columns(4)
            
            with col_btn1:
                if st.button("✅ Selecionar Todas", use_container_width=True):
                    st.rerun()
            
            with col_btn2:
                if st.button("❌ Limpar Seleção", use_container_width=True):
                    st.rerun()
            
            # Preview dos dados
            if columns_to_show:
                st.markdown("---")
                st.markdown('<p class="section-title">👁️ Preview dos Dados</p>', unsafe_allow_html=True)
                
                st.dataframe(
                    df[columns_to_show].head(rows_per_page),
                    use_container_width=True,
                    height=400
                )
                
                st.info(f"📊 Total de animais: {len(df)} | Colunas selecionadas: {len(columns_to_show)} | Páginas: {total_pages}")
            
            # Botão de gerar PDF
            st.markdown("---")
            col_generate1, col_generate2, col_generate3 = st.columns([1, 1, 1])
            
            with col_generate2:
                if st.button("🚀 Gerar PDF", type="primary", use_container_width=True):
                    if not columns_to_show:
                        st.error("❌ Selecione pelo menos uma coluna!")
                    else:
                        with st.spinner("⏳ Gerando PDF... Isso pode levar alguns segundos para arquivos grandes."):
                            config = {
                                'template': template,
                                'client_name': client_name,
                                'responsible_name': responsible_name,
                                'contact_phone': contact_phone,
                                'header_name': header_name,
                                'header_date': header_date,
                                'columns_to_show': columns_to_show,
                                'rows_per_page': rows_per_page,
                                'font_size': font_size,
                                'logo_path': logo_path
                            }
                            
                            pdf_buffer = generate_pdf(df, config)
                            
                            st.success("✅ PDF gerado com sucesso!")
                            
                            # Download
                            st.download_button(
                                label="📥 Baixar PDF",
                                data=pdf_buffer,
                                file_name=f"acasalamento_{client_name.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf",
                                mime="application/pdf",
                                use_container_width=True
                            )
        
        except Exception as e:
            st.error(f"❌ Erro ao processar arquivo: {str(e)}")
            st.info("💡 Verifique se o arquivo CSV está formatado corretamente")
            import traceback
            st.code(traceback.format_exc())
    
    else:
        # Tela inicial
        st.info("👆 Faça upload do arquivo CSV de acasalamento na barra lateral para começar")
        
        st.markdown("### 📖 Como usar:")
        st.markdown("""
        1. **Upload do CSV**: Carregue o arquivo de acasalamento de animais
        2. **Logo (opcional)**: Adicione uma imagem para a capa
        3. **Template**: Escolha o estilo da capa (Empresarial, Técnico ou Executivo)
        4. **Informações**: Preencha o nome da fazenda/cliente
        5. **Cabeçalho**: Configure os textos do cabeçalho
        6. **Formatação**: 
           - Escolha o tamanho da fonte (8-16pt)
           - Defina quantas linhas por página (10 até o máximo calculado)
        7. **Colunas**: Selecione quais colunas exibir
        8. **Gerar**: Clique em "Gerar PDF" e baixe
        """)
        
        st.markdown("### ✨ Funcionalidades:")
        col_feat1, col_feat2 = st.columns(2)
        
        with col_feat1:
            st.markdown("""
            - ✅ **Formato Paisagem** (A4 horizontal)
            - ✅ **Fonte Helvetica** (similar a Arial)
            - ✅ **Tamanho de fonte**: 8pt a 16pt
            - ✅ **Linhas por página**: ajustável
            - ✅ **Cálculo automático** de linhas máximas
            - ✅ **Capa personalizável**
            """)
        
        with col_feat2:
            st.markdown("""
            - ✅ **Múltiplos templates** de capa
            - ✅ **Logo customizável**
            - ✅ **Cabeçalho editável**
            - ✅ **Rodapé com numeração**
            - ✅ **Seleção livre de colunas**
            - ✅ **Preview antes de gerar**
            """)
        
        # Mostrar cálculo de linhas
        st.markdown("---")
        st.markdown("### 📏 Tabela de Referência: Linhas por Página")
        
        font_limits = get_font_size_limits()
        
        ref_data = {
            "Tamanho da Fonte": list(font_limits.keys()),
            "Máximo de Linhas": list(font_limits.values())
        }
        
        st.table(pd.DataFrame(ref_data))
        
        st.info("💡 **Nota**: Estes valores são calculados automaticamente com base nas margens, cabeçalhos e espaçamento da tabela.")

if __name__ == "__main__":
    main()
