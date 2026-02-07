# 🚀 GUIA RÁPIDO - Sistema de Acasalamento

## ⚡ Início Rápido (3 Passos)

### 1️⃣ Instalar
```bash
pip install -r requirements.txt
```

### 2️⃣ Executar
```bash
streamlit run app_acasalamento.py
```

### 3️⃣ Acessar
Abra o navegador em: `http://localhost:8501`

---

## 📋 Fluxo de Trabalho

```
1. Upload CSV → 2. Configurar → 3. Selecionar Colunas → 4. Gerar PDF
```

---

## ⚙️ Configurações Principais

### 🎨 Template da Capa
- **Empresarial**: Azul corporativo
- **Técnico**: Cinza profissional  
- **Executivo**: Verde elegante

### 📏 Tamanho da Fonte
| Fonte | Linhas/Página |
|-------|---------------|
| 8pt   | até 60        |
| 10pt  | até 48        |
| 12pt  | até 40        |
| 14pt  | até 34        |
| 16pt  | até 30        |

### 📄 Configuração Recomendada
```
Fonte: 10pt
Linhas por página: 30-35
Formato: Paisagem (A4)
Fonte: Arial
```

---

## 🎯 Configurações Por Cenário

### 📊 Relatório Executivo
```yaml
Template: Executivo
Fonte: 14pt
Linhas/página: 25
Colunas: 5-7 principais
Logo: Sim
```
**Quando usar**: Apresentações para diretoria

### 📋 Relatório Completo
```yaml
Template: Técnico
Fonte: 8-9pt
Linhas/página: 45-50
Colunas: Todas ou quase todas
Logo: Opcional
```
**Quando usar**: Documentação técnica detalhada

### 📝 Relatório Padrão
```yaml
Template: Empresarial
Fonte: 10-11pt
Linhas/página: 30-35
Colunas: 8-10 essenciais
Logo: Sim
```
**Quando usar**: Uso diário, relatórios mensais

---

## 📊 Seleção de Colunas

### Colunas Sempre Incluir
- ✅ NÚMERO DE VACAS
- ✅ STOC
- ✅ ÍNDICE

### Colunas Opcionais (conforme necessidade)
- TOURO NAAB
- NAAB (1º, 2º, 3º)
- NOME CURTO (1º, 2º, 3º)
- INB % (1º, 2º, 3º)

### Dica de Seleção
```
Menos colunas = Fonte maior = Mais legível
Mais colunas = Precisa fonte menor
```

---

## ⚡ Atalhos e Truques

### Seleção Rápida de Colunas
1. **Selecionar Todas**: Marca todas as colunas
2. **Limpar Seleção**: Desmarca todas
3. Depois ajuste individualmente

### Preview Antes de Gerar
- Sempre verifique o preview
- Confira se as colunas estão corretas
- Note o número de páginas que serão geradas

### Otimizar Tamanho do PDF
1. Menos colunas = Arquivo menor
2. Mais linhas/página = Menos páginas
3. Fonte menor = Mais linhas cabem

---

## 🔧 Configuração Passo a Passo

### 1. Capa
```
Campo: Nome da Fazenda/Cliente
Exemplo: "Fazenda Boa Vista"
Dica: Seja conciso e claro
```

### 2. Cabeçalho
```
Texto Esquerdo: "Relatório de Acasalamento"
Texto Direito: "Janeiro/2026"
Dica: Use datas ou períodos no lado direito
```

### 3. Formatação
```
Passo 1: Escolha o tamanho da fonte (10pt recomendado)
Passo 2: Sistema mostra máximo de linhas possível
Passo 3: Defina linhas por página (30 recomendado)
Passo 4: Veja quantas páginas serão geradas
```

### 4. Colunas
```
Passo 1: Marque as colunas essenciais
Passo 2: Desmarque as desnecessárias
Passo 3: Verifique o preview
```

---

## 💡 Casos de Uso Comuns

### Caso 1: Relatório Mensal
```
Fazenda: [Nome da Fazenda]
Cabeçalho: "Relatório Mensal de Acasalamento"
Data: Janeiro/2026
Fonte: 10pt
Linhas: 30
Colunas: 8 principais
```

### Caso 2: Apresentação Gerencial
```
Fazenda: [Nome da Fazenda]
Cabeçalho: "Resultados de Acasalamento"
Data: 1º Trimestre 2026
Fonte: 14pt
Linhas: 25
Colunas: 5-6 resumo
```

### Caso 3: Arquivo Técnico
```
Fazenda: [Nome da Fazenda]
Cabeçalho: "Base Completa de Dados"
Data: Atualizado em DD/MM/AAAA
Fonte: 8pt
Linhas: 50
Colunas: Todas
```

---

## ❓ Problemas Comuns - Solução Rápida

### ❌ "Colunas muito largas"
**Solução**: Reduza o número de colunas selecionadas

### ❌ "Texto muito pequeno"
**Solução**: Aumente a fonte (mínimo 10pt para boa leitura)

### ❌ "Muitas páginas"
**Solução**: Aumente linhas/página ou use fonte menor

### ❌ "CSV não carrega"
**Solução**: 
1. Abra no Excel
2. Salvar Como → CSV UTF-8
3. Tente novamente

### ❌ "Logo não aparece"
**Solução**: Use PNG/JPG, máx 5MB, mín 300x300px

---

## 📏 Tabela de Referência Completa

| Fonte | Máx Linhas | Uso Recomendado |
|-------|-----------|-----------------|
| 8pt   | ~60       | Máximo de dados |
| 9pt   | ~53       | Muitos dados    |
| 10pt  | ~48       | **Padrão**      |
| 11pt  | ~43       | Boa leitura     |
| 12pt  | ~40       | Confortável     |
| 13pt  | ~37       | Apresentação    |
| 14pt  | ~34       | Executivo       |
| 15pt  | ~32       | Extra grande    |
| 16pt  | ~30       | Máxima legibilidade |

---

## 🎯 Metas de Performance

### Tempo de Geração
- 100 animais: ~2 segundos
- 500 animais: ~5 segundos
- 1000 animais: ~10 segundos

### Qualidade do PDF
- Resolução: 300 DPI
- Fonte: Arial (sempre)
- Cor: RGB

---

## 🔄 Workflow Eficiente

### Para Uso Diário
1. Mantenha logo salvo
2. Use sempre o mesmo template
3. Configure tamanho de fonte padrão
4. Salve lista de colunas favoritas (anote)

### Para Diferentes Públicos
- **Técnicos**: Mais colunas, fonte menor
- **Gestores**: Menos colunas, fonte maior
- **Clientes**: Template executivo, dados essenciais

---

## 📌 Checklist de Qualidade

Antes de gerar o PDF, verifique:
- [ ] Nome da fazenda/cliente correto
- [ ] Data no cabeçalho atualizada
- [ ] Tamanho de fonte apropriado
- [ ] Número de linhas configurado
- [ ] Colunas essenciais selecionadas
- [ ] Preview conferido
- [ ] Logo carregado (se necessário)

---

## 💾 Organização de Arquivos

### Estrutura Sugerida
```
relatorios/
├── 2026/
│   ├── janeiro/
│   │   └── acasalamento_fazenda_20260131.pdf
│   ├── fevereiro/
│   └── marco/
└── templates/
    └── logo_fazenda.png
```

### Nomenclatura Recomendada
```
acasalamento_[fazenda]_[AAAAMMDD].pdf

Exemplos:
- acasalamento_boavista_20260207.pdf
- acasalamento_saojose_20260131.pdf
```

---

## 🎓 Próximos Passos

Após dominar o básico:
1. Experimente diferentes templates
2. Teste vários tamanhos de fonte
3. Crie padrões para diferentes relatórios
4. Otimize seleção de colunas por tipo de uso
5. Configure atalhos no seu sistema

---

## 📞 Comandos Úteis do Terminal

### Ver versão do Streamlit
```bash
streamlit --version
```

### Limpar cache
```bash
streamlit cache clear
```

### Executar em background
```bash
nohup streamlit run app_acasalamento.py &
```

---

## ✅ Conclusão

Com este sistema você pode:
- ✅ Gerar relatórios profissionais em minutos
- ✅ Personalizar para cada necessidade
- ✅ Controlar exatamente o que aparece
- ✅ Manter padrão de qualidade

**Dica Final**: Comece com as configurações padrão e ajuste conforme necessário!

---

**Precisa de mais detalhes?** Consulte o README_ACASALAMENTO.md completo!
