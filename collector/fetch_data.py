"""
Coletor de dados usando yfinance.
"""

import re
import math
from datetime import datetime
from typing import List, Dict, Any

import yfinance as yf

# -----------------------------
# Validação de ticker
# -----------------------------

_TICKER_REGEX = re.compile(r"^[A-Za-z0-9\.\-]{1,10}$")

def validate_ticker(ticker: str) -> str:
    if not ticker:
        raise ValueError("Ticker não pode ser vazio.")

    normalized = ticker.strip().upper()

    if not _TICKER_REGEX.match(normalized):
        raise ValueError("Ticker inválido.")

    return normalized

# -----------------------------
# Funções auxiliares
# -----------------------------

def _safe_float(value) -> float | None:
    if value is None:
        return None
    try:
        f = float(value)
        if math.isnan(f):
            return None
        return f
    except:
        return None


def _safe_int(value) -> int | None:
    if value is None:
        return None
    try:
        return int(value)
    except:
        return None

# -----------------------------
# Coleta via yfinance
# -----------------------------

def fetch_historical_data(ticker: str) -> List[Dict[str, Any]]:
    try:
        ticker = validate_ticker(ticker)
        print(f"[INFO] Coletando dados históricos via yfinance para: {ticker}")

        df = yf.download(
            ticker,
            period="5y",
            interval="1d",
            auto_adjust=False,
            progress=False,
        )

        if df is None or df.empty:
            print(f"[WARN] Nenhum dado encontrado para '{ticker}'.")
            return []

        historical_data: List[Dict[str, Any]] = []

        for index, row in df.iterrows():

            if isinstance(index, datetime):
                date_str = index.strftime("%Y-%m-%d")
            else:
                try:
                    date_str = index.date().isoformat()
                except:
                    date_str = str(index)

            record = {
                "date": date_str,
                "open": _safe_float(row.get("Open")),
                "high": _safe_float(row.get("High")),
                "low": _safe_float(row.get("Low")),
                "close": _safe_float(row.get("Close")),
                "volume": _safe_int(row.get("Volume")),
            }

            historical_data.append(record)

        print(f"[INFO] {len(historical_data)} registros obtidos.")
        return historical_data

    except Exception as e:
        print(f"[ERROR] Erro interno no fetch_historical_data: {e}")
        return []
