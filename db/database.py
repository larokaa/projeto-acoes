"""
Módulo para gerenciar conexão e operações com o banco de dados SQLite.

- Cria e inicializa o banco (usando schema.sql)
- Gerencia ativos (tabela assets)
- Gerencia preços históricos (tabela prices)
"""

from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Any, Dict, List, Optional

# Caminhos dos arquivos
DB_PATH = Path(__file__).parent / "stocks.db"
SCHEMA_PATH = Path(__file__).parent / "schema.sql"


# ============================================================================
# Conexão com o banco
# ============================================================================

def create_connection() -> sqlite3.Connection:
    """
    Cria e retorna uma conexão com o banco SQLite.
    Configura row_factory para acessar colunas por nome.
    """
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    """
    Garante que o banco de dados e o schema existem.
    Executa o arquivo schema.sql.
    """
    if not DB_PATH.exists():
        print("[INFO] Criando arquivo de banco de dados...")

    with create_connection() as conn:
        with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
            schema_sql = f.read()
        conn.executescript(schema_sql)

    print("[INFO] Banco de dados pronto.")


# ============================================================================
# Operações em assets (tabela de ativos)
# ============================================================================

def get_or_create_asset(ticker: str, name: Optional[str] = None) -> int:
    """
    Retorna o id do ativo para o ticker informado.
    Se não existir, cria um novo registro.
    """
    with create_connection() as conn:
        cur = conn.cursor()

        # Tenta buscar o ativo
        cur.execute("SELECT id FROM assets WHERE ticker = ?", (ticker,))
        row = cur.fetchone()
        if row:
            asset_id = int(row["id"])
            cur.close()
            return asset_id

        # Não existe: cria
        cur.execute(
            "INSERT INTO assets (ticker, name) VALUES (?, ?)",
            (ticker, name or ticker),
        )
        asset_id = cur.lastrowid
        conn.commit()
        cur.close()
        return int(asset_id)


# ============================================================================
# Operações em prices (tabela de preços)
# ============================================================================

def insert_price(
    asset_id: int,
    date: str,
    open_price: Optional[float],
    high_price: Optional[float],
    low_price: Optional[float],
    close_price: Optional[float],
    volume: Optional[int],
) -> None:
    """
    Insere (ou atualiza) um preço histórico para o ativo.

    A tabela prices deve ter UNIQUE(asset_id, date), permitindo
    usar INSERT OR REPLACE.
    """
    with create_connection() as conn:
        cur = conn.cursor()
        cur.execute(
            """
            INSERT OR REPLACE INTO prices
                (asset_id, date, open, high, low, close, volume)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                asset_id,
                date,
                open_price,
                high_price,
                low_price,
                close_price,
                volume,
            ),
        )
        conn.commit()
        cur.close()


def get_prices_by_ticker(ticker: str) -> List[Dict[str, Any]]:
    """
    Retorna os preços históricos de um ticker, em ordem de data.
    """
    with create_connection() as conn:
        cur = conn.cursor()
        cur.execute(
            """
            SELECT
                p.date,
                p.open,
                p.high,
                p.low,
                p.close,
                p.volume
            FROM prices p
            JOIN assets a ON a.id = p.asset_id
            WHERE a.ticker = ?
            ORDER BY p.date
            """,
            (ticker,),
        )
        rows = cur.fetchall()
        cur.close()

    # Converte sqlite3.Row -> dict
    return [dict(row) for row in rows]


