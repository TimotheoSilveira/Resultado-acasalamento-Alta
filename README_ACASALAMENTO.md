# 🐄 Sistema de Relatórios - Acasalamento de Animais

Sistema web especializado para gerar relatórios PDF profissionais a partir de planilhas CSV de acasalamento de animais, com controle total sobre formatação e apresentação.

## 🎯 Características Principais

### 📄 Formato e Layout
- **Orientação**: Paisagem (A4 horizontal)
- **Fonte**: Arial em todos os elementos
- **Tamanho de fonte**: Ajustável de 8pt a 16pt
- **Linhas por página**: Configurável (mínimo 10, máximo calculado automaticamente)

### ⚙️ Funcionalidades

#### 1. Controle de Paginação Inteligente
- **Cálculo automático** do número máximo de linhas baseado no tamanho da fonte
- Sistema garante que a fonte nunca seja menor que 8pt ou maior que 16pt
- Tabela de referência mostrando linhas possíveis para cada tamanho de fonte

#### 2. Capa Personalizável
- Nome da fazenda/cliente editável
- 3 templates profissionais (Empresarial, Técnico, Executivo)
- Upload de logo opcional
- Data gerada automaticamente

#### 3. Cabeçalho e Rodapé
- **Cabeçalho**: Texto personalizável à esquerda e direita
- **Rodapé**: Numeração automática "Página X de Y"
- Linha decorativa separando cabeçalho do conteúdo

#### 4. Seleção de Colunas
- Interface visual com checkboxes para cada coluna
- Distribuição em 4 colunas para fácil visualização
- Botões de seleção rápida (Selecionar Todas / Limpar)
- Preview dos dados antes de gerar o PDF

## 📋 Requisitos

- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)

## 🔧 Instalação

### 1. Instale as dependências

```bash
pip install -r requirements.txt
```

### 2. Execute a aplicação

```bash
streamlit run app_acasalamento.py
```

### 3. Acesse no navegador

O sistema abrirá automaticamente em: `http://localhost:8501`

## 📖 Guia de Uso Completo

### Passo 1: Upload do Arquivo
1. Clique em **"Browse files"** na barra lateral
2. Selecione seu arquivo CSV de acasalamento
3. O sistema carregará e mostrará: número de animais e colunas

### Passo 2: Logo (Opcional)
1. Clique em **"Logo para a capa"**
2. Selecione uma imagem PNG ou JPG
3. Recomendado: mínimo 300x300px, máximo 5MB

### Passo 3: Escolher Template
Selecione um dos templates disponíveis:
- **Empresarial**: Azul corporativo (#1f77b4)
- **Técnico**: Cinza profissional (#2c3e50)
- **Executivo**: Verde elegante (#27ae60)

### Passo 4: Informações da Capa
- Digite o nome da fazenda ou cliente
- Este nome aparecerá em destaque na capa

### Passo 5: Configurar Cabeçalho
- **Texto Esquerdo**: Ex: "Relatório de Acasalamento"
- **Texto Direito**: Ex: Data atual ou período

### Passo 6: Formatação da Tabela

#### Tamanho da Fonte
- Use o **slider** para escolher entre 8pt e 16pt
- O sistema mostra automaticamente quantas linhas cabem

#### Linhas por Página
- Digite o número desejado de animais por página
- Mínimo: 10 linhas
- Máximo: calculado automaticamente baseado na fonte
- O sistema mostra quantas páginas serão geradas

**Tabela de Referência:**
| Fonte | Máx. Linhas |
|-------|-------------|
| 8pt   | ~60 linhas  |
| 10pt  | ~48 linhas  |
| 12pt  | ~40 linhas  |
| 14pt  | ~34 linhas  |
| 16pt  | ~30 linhas  |

### Passo 7: Selecionar Colunas
1. Marque/desmarque as colunas desejadas
2. Use os botões rápidos se necessário:
   - ✅ **Selecionar Todas**: marca todas as colunas
   - ❌ **Limpar Seleção**: desmarca todas

### Passo 8: Preview
- Visualize os dados que serão incluídos
- Verifique se as colunas estão corretas
- Confirme o número total de páginas

### Passo 9: Gerar PDF
1. Clique em **"🚀 Gerar PDF"**
2. Aguarde o processamento (pode levar alguns segundos)
3. Clique em **"📥 Baixar PDF"**
4. O arquivo será salvo com nome: `acasalamento_[nome]_[data].pdf`

## 📊 Estrutura do CSV

O sistema espera um CSV com as seguintes colunas padrão:

```csv
NÚMERO DE VACAS,STOC,ÍNDICE,TOURO NAAB,NAAB,NOME CURTO,INB %,NAAB,NOME CURTO,INB %,NAAB,NOME CURTO,INB %
199,CN,-296,799HO00004,011HO17733,AltaFANZONE,0.05,011HO17399,AltaINSPIRE 4,0.00,011HO17721,AltaYOSHI,0.05
...
```

**Importante:**
- Primeira linha deve conter os cabeçalhos
- Separador: vírgula (,)
- Encoding: UTF-8
- Células vazias são permitidas

## 🎨 Exemplos de Configuração

### Exemplo 1: Relatório Resumido
```
Fazenda: Fazenda Boa Vista
Template: Empresarial
Fonte: 12pt
Linhas/página: 30
Colunas: NÚMERO DE VACAS, STOC, ÍNDICE, TOURO NAAB, NAAB (1º), NOME CURTO (1º)
```

### Exemplo 2: Relatório Completo
```
Fazenda: Agropecuária São José
Template: Técnico
Fonte: 8pt
Linhas/página: 50
Colunas: Todas as colunas
```

### Exemplo 3: Relatório Executivo
```
Fazenda: Grupo Pecuário Elite
Template: Executivo
Fonte: 14pt
Linhas/página: 25
Colunas: NÚMERO DE VACAS, ÍNDICE, NOME CURTO (1º, 2º e 3º)
```

## 🔍 Detalhes Técnicos

### Cálculo de Linhas Máximas
O sistema calcula automaticamente baseado em:
- Altura da página: 21cm (A4 paisagem)
- Margem superior: 3cm (inclui cabeçalho)
- Margem inferior: 2.5cm (inclui rodapé)
- Altura do cabeçalho da tabela: fonte + 12pt padding
- Altura de cada linha: fonte + 6pt padding

**Fórmula:**
```
linhas_máximas = (altura_disponível - altura_cabeçalho) / altura_linha
```

### Fonte Arial
- **Cabeçalho da tabela**: Arial Bold
- **Dados da tabela**: Arial Regular
- **Cabeçalho da página**: Arial
- **Rodapé**: Arial
- **Capa**: Helvetica (títulos) e Arial (informações)

### Cores Padrão
- **Cabeçalho da tabela**: Azul (#1f77b4) com texto branco
- **Linhas alternadas**: Branco e cinza claro (#f0f0f0)
- **Bordas**: Cinza (0.5pt)

## 🛠️ Personalização Avançada

### Adicionar Novo Template de Capa

Edite a função `create_cover_page()` em `app_acasalamento.py`:

```python
elif template == "Seu Template":
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Title'],
        fontSize=34,
        textColor=colors.HexColor('#SUACOR'),
        spaceAfter=30,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    title = Paragraph("SEU TÍTULO", title_style)
```

### Modificar Cores da Tabela

Edite a função `create_data_tables()`:

```python
# Mudar cor do cabeçalho
('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#SUACOR')),

# Mudar cores das linhas alternadas
('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#SUACOR')]),
```

### Ajustar Margens

No método `generate_pdf()`:

```python
doc = SimpleDocTemplate(
    buffer,
    pagesize=landscape(A4),
    rightMargin=2*cm,   # Margem direita
    leftMargin=2*cm,    # Margem esquerda
    topMargin=3*cm,     # Margem superior
    bottomMargin=2.5*cm # Margem inferior
)
```

## 📐 Dimensões da Página

- **Largura**: 29.7cm (A4 paisagem)
- **Altura**: 21cm
- **Área útil para tabela**: ~24.7cm x 15.5cm
- **Máximo de colunas recomendado**: depende da largura de cada coluna

## ❓ Solução de Problemas

### CSV não carrega corretamente
**Problema**: Caracteres estranhos ou colunas erradas  
**Solução**:
1. Abra o CSV no Excel
2. Salvar Como → CSV UTF-8 (Delimitado por Vírgula)
3. Tente fazer upload novamente

### Tabela muito larga
**Problema**: Colunas cortadas ou texto muito pequeno  
**Solução**:
1. Reduza o número de colunas selecionadas
2. Use abreviações nos nomes das colunas
3. Diminua o tamanho da fonte

### PDF com muitas páginas
**Problema**: Arquivo muito grande  
**Solução**:
1. Aumente o número de linhas por página
2. Diminua o tamanho da fonte (mínimo 8pt)
3. Reduza o número de colunas

### Fonte muito pequena
**Problema**: Difícil de ler  
**Solução**:
1. Aumente o tamanho da fonte (máximo 16pt)
2. Reduza linhas por página
3. Selecione menos colunas

### Logo não aparece
**Problema**: Imagem não carrega na capa  
**Solução**:
1. Use PNG ou JPG
2. Tamanho máximo: 5MB
3. Formato recomendado: quadrado (300x300px ou maior)

## 💡 Dicas e Boas Práticas

### ✅ Recomendações

1. **Para leitura fácil**: Use fonte 10-12pt com 30-35 linhas
2. **Para mais dados**: Use fonte 8-9pt com 45-50 linhas
3. **Para apresentação**: Use fonte 12-14pt com 25-30 linhas
4. **Colunas essenciais**: Selecione apenas as mais importantes
5. **Nome curto**: Use nomes de fazenda/cliente concisos
6. **Preview**: Sempre verifique o preview antes de gerar

### ❌ Evite

1. Fontes menores que 8pt (ilegível)
2. Mais de 10 colunas (tabela muito larga)
3. Nomes de colunas muito longos
4. Logos de baixa qualidade
5. CSVs com erros de formatação

## 📊 Benchmarks de Performance

| Animais | Colunas | Fonte | Linhas/pág | Tempo Aprox. |
|---------|---------|-------|------------|--------------|
| 100     | 5       | 10pt  | 30         | ~2s          |
| 500     | 8       | 10pt  | 30         | ~5s          |
| 1000    | 10      | 8pt   | 50         | ~10s         |
| 2000    | 12      | 8pt   | 50         | ~20s         |

*Tempos medidos em computador padrão (i5, 8GB RAM)*

## 🔄 Atualizações Futuras

Recursos planejados:
- [ ] Exportar configurações para reutilizar
- [ ] Salvar templates customizados
- [ ] Gráficos e estatísticas na capa
- [ ] Filtros por índice ou categoria
- [ ] Múltiplos logos (capa e cabeçalho)
- [ ] Marca d'água personalizada

## 📞 Comandos Úteis

### Executar em porta diferente
```bash
streamlit run app_acasalamento.py --server.port 8502
```

### Desabilitar auto-reload
```bash
streamlit run app_acasalamento.py --server.runOnSave false
```

### Modo headless (sem navegador)
```bash
streamlit run app_acasalamento.py --server.headless true
```

## 📄 Arquivos do Projeto

```
projeto/
├── app_acasalamento.py           # Aplicação principal
├── requirements.txt               # Dependências
├── README.md                      # Esta documentação
├── GUIA_RAPIDO_ACASALAMENTO.md   # Guia rápido
└── exemplo_acasalamento.csv      # Arquivo de exemplo
```

## 📝 Licença

Este projeto é de uso livre para fins comerciais e educacionais.

---

**Desenvolvido especialmente para gestão de acasalamento bovino** 🐄

Para suporte, consulte a documentação ou entre em contato com o desenvolvedor.
