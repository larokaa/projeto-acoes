# Sistema de Coleta e Visualização de Dados Históricos de Ações (NASDAQ)
📌 Resumo do Projeto

Este projeto consiste em um sistema completo para coleta, armazenamento e visualização de dados históricos de ações da NASDAQ.
Ele integra Python (Flask + yfinance) no backend, SQLite como banco local e uma interface web moderna construída com HTML, CSS, JavaScript e Chart.js.

##
O objetivo é demonstrar habilidades reais em:

Desenvolvimento backend (APIs, Python, Flask)
Integração com serviços externos (yfinance)
Persistência de dados (SQLite)
Frontend (gráficos, tabelas, UX)
Arquitetura limpa e organizada
Tratamento de erros e fluxo completo de dados

🛠️ Tecnologias Principais
Backend
Python 3
Flask
yfinance (coleta de dados)
SQLite
Frontend
HTML5
CSS3 (tema baseado nas cores STEN)
JavaScript (ES6)
Chart.js

🧱 Arquitetura do Sistema
Usuário → Interface Web → API Flask → yfinance → Banco SQLite

## Fluxo resumido:
Usuário digita um ticker
Backend coleta dados históricos via yfinance
Dados são salvos no banco SQLite
Interface exibe:
📊 Gráfico (preço de fechamento)
📋 Tabela com todos os dados formatados

###
📂 Estrutura do Projeto
projeto-acoes/
├── app.py              # API Flask
├── collector/          
│   └── fetch_data.py   # Coleta via yfinance
├── db/
│   ├── database.py     # Operações no SQLite
│   └── schema.sql      # Schema das tabelas
├── interface/
│   ├── index.html      # Interface
│   ├── script.js       # Lógica de frontend
│   └── styles.css      # Estilo visual
└── stocks.db           # Banco local


###📁 Descrição dos Arquivos

#### collector/fetch_data.py
Módulo responsável por coletar dados históricos usando yfinance.
Função principal: fetch_historical_data(ticker)

Tecnologia utilizada: yfinance (Yahoo Finance API)
Retorn: Lista de dicionários com {date, open, high, low, close, volume}
Tratamento:
Validação de ticker
Conversão de valores (float/int)
Tratamento de valores faltantes e erros

#### db/database.py

Gerencia todas as operações com o banco SQLite.
Funções principais:
init_db() → Inicializa o banco usando o schema SQL
get_or_create_asset(ticker) → Cria ou retorna o ativo
insert_price(...) → Insere preços históricos
get_prices_by_ticker(ticker) → Retorna dados do ativo
Tecnologias usadas:
SQLite (nativo do Python)
Context managers
Type hints
#### db/schema.sql
Define toda a estrutura do banco de dados.
Tabela assets → Informações dos ativos
Tabela prices → Dados históricos
Relacionamento:
prices.asset_id → assets.id
Índices para melhorar busca por asset_id e date

#### app.py
Backend Flask que integra coleta, banco e interface.
Rotas:
GET / → Serve a interface
POST /api/fetch-and-save → Coleta via yfinance e salva no banco

GET /api/prices/<ticker> → Retorna dados armazenados
Tecnologias:
Flask
SQLite
yfinance
Funcionalidades:
Validação
Tratamento de erros
API REST em JSON

#### interface/index.html
Interface principal do sistema.
Tecnologias:
HTML5
Chart.js (via CDN)
Elementos:
Input de ticker
Botão de buscar
Gráfico
Tabela
Logo e layout estilizado

#### interface/script.js

Lógica de frontend e comunicação com o backend.
Funções principais:
handleSearch() → Faz POST para coletar e salvar
loadPrices() → Busca dados no banco
updateUIWithPrices() → Atualiza gráfico e tabela
formatVolume() → Formata volume para milhões (ex.: 14.79 M)
Tecnologias:
JavaScript ES6+
Fetch API
Chart.js

#### interface/styles.css
Estilização completa da interface.
Tecnologias:
CSS3
Características:
Tema inspirado nas cores da STEN
Layout responsivo
Gradientes
Estilo do gráfico e da tabela
Ajustes para desktop, tablet e celular


🚀 Como Executar
python -m venv venv
venv\Scripts\activate  # Windows

pip install flask yfinance

python app.py


Acesse no navegador:

http://127.0.0.1:5000

📈 Funcionalidades
##
✔️ Busca de dados históricos de ações da NASDAQ
✔️ Salvamento local em banco SQLite
✔️ Interface moderna com logo e cores STEN
✔️ Gráfico interativo Chart.js
✔️ Volume exibido automaticamente em milhões
✔️ Tabela formatada com datas e valores
✔️ Mensagens de status (carregando, erro, sucesso)

💡 Pontos Técnicos de Destaque

Integração completa entre backend, banco de dados e frontend
Uso de módulos separados e arquitetura limpa
Tratamento de dados nulos, erros de rede e validação de ticker
Responsividade e experiência do usuário aprimorada
Código organizado com comentários e boas práticas

⭐ Resultado Final
O sistema entrega uma ferramenta profissional capaz de:
Automatizar coleta de dados financeiros
Armazenar de forma persistente
Exibir visualmente de maneira simples e elegante
Ideal para análise, demonstração técnica ou expansão futura.

📞 Sobre o Autor

Projeto desenvolvido como case técnico para fins de estudo e demonstração de habilidades.