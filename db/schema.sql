-- =====================================================
-- Schema SQL para o Sistema de Coleta de Dados NASDAQ
-- =====================================================
-- Este arquivo define a estrutura do banco de dados SQLite
-- com as tabelas necessárias para armazenar informações
-- de ativos e seus preços históricos.
-- =====================================================

-- =====================================================
-- Tabela: assets
-- =====================================================
-- Armazena informações básicas dos ativos (ações) da NASDAQ.
-- Cada registro representa um ticker único com seu nome.
-- =====================================================
CREATE TABLE IF NOT EXISTS assets (
    -- Identificador único do ativo (chave primária)
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    
    -- Ticker do ativo (ex: AAPL, MSFT, GOOGL)
    -- ÚNICO: garante que não haverá duplicatas de tickers
    ticker TEXT NOT NULL UNIQUE,
    
    -- Nome completo da empresa/ativo
    name TEXT NOT NULL
);

-- =====================================================
-- Tabela: prices
-- =====================================================
-- Armazena os preços históricos de cada ativo.
-- Cada registro representa os dados de um dia específico
-- para um determinado ativo.
-- =====================================================
CREATE TABLE IF NOT EXISTS prices (
    -- Identificador único do registro de preço (chave primária)
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    
    -- Referência ao ativo na tabela assets (chave estrangeira)
    -- Garante integridade referencial: só podemos ter preços
    -- para ativos que existem na tabela assets
    asset_id INTEGER NOT NULL,
    
    -- Data do registro de preço (formato: YYYY-MM-DD)
    date DATE NOT NULL,
    
    -- Preço de abertura do dia
    open REAL NOT NULL,
    
    -- Maior preço do dia
    high REAL NOT NULL,
    
    -- Menor preço do dia
    low REAL NOT NULL,
    
    -- Preço de fechamento do dia
    close REAL NOT NULL,
    
    -- Volume de negociações do dia
    volume INTEGER NOT NULL,
    
    -- Definição da chave estrangeira
    -- Quando um ativo é deletado, os preços relacionados também são deletados (CASCADE)
    FOREIGN KEY (asset_id) REFERENCES assets(id) ON DELETE CASCADE,
    
    -- Índice composto para otimizar consultas por ativo e data
    -- Evita duplicatas: um ativo não pode ter dois registros para a mesma data
    UNIQUE(asset_id, date)
);

-- =====================================================
-- Índices adicionais para melhorar performance
-- =====================================================

-- Índice na coluna asset_id da tabela prices
-- Acelera consultas que filtram por ativo específico
CREATE INDEX IF NOT EXISTS idx_prices_asset_id ON prices(asset_id);

-- Índice na coluna date da tabela prices
-- Acelera consultas que filtram por intervalo de datas
CREATE INDEX IF NOT EXISTS idx_prices_date ON prices(date);
