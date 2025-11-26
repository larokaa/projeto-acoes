"""
Backend principal do Sistema de Coleta e Visualização de Dados Históricos de Ações.
"""

from pathlib import Path
from typing import Any, Dict, List

from flask import Flask, jsonify, request, send_from_directory

from db import database
from collector import fetch_data

# Diretórios base
BASE_DIR = Path(__file__).parent
INTERFACE_DIR = BASE_DIR / "interface"

# Flask vai servir TUDO que está na pasta /interface diretamente na raiz (/)
# Ou seja:
#   interface/styles.css  ->  http://127.0.0.1:5000/styles.css
#   interface/script.js   ->  http://127.0.0.1:5000/script.js
app = Flask(
    __name__,
    static_folder="interface",
    static_url_path=""
)


@app.route("/", methods=["GET"])
def index() -> Any:
    """Serve o arquivo index.html da interface."""
    return send_from_directory(INTERFACE_DIR, "index.html")


@app.route("/api/fetch-and-save", methods=["POST"])
def api_fetch_and_save() -> Any:
    """
    Recebe um ticker, coleta dados via yfinance e salva no banco.

    Corpo esperado (JSON):
    {
        "ticker": "AAPL"
    }
    """
    data: Dict[str, Any] = request.get_json(silent=True) or {}
    ticker = (data.get("ticker") or "").strip()

    if not ticker:
        return jsonify({"status": "error", "message": "Ticker é obrigatório."}), 400

    try:
        print(f"[INFO] Coletando dados para ticker: {ticker}")

        # 1) Coleta os dados históricos via yfinance
        prices = fetch_data.fetch_historical_data(ticker)
        print(f"[INFO] {len(prices)} registros retornados pelo coletor")

        # Se não vier dado nenhum, avisa mas não é erro interno
        if not prices:
            return jsonify(
                {
                    "status": "warning",
                    "message": "Nenhum dado encontrado para o ticker.",
                }
            ), 200

        # 2) Garante que o banco existe
        database.init_db()

        # 3) Cria ou obtém o asset
        asset_id = database.get_or_create_asset(ticker.upper())

        # 4) Salva apenas registros com todos os campos necessários
        count_inserted = 0
        count_skipped = 0

        for p in prices:
            o = p.get("open")
            h = p.get("high")
            l = p.get("low")
            c = p.get("close")
            v = p.get("volume")

            # Se algum campo importante for None, ignora esse registro
            if None in (o, h, l, c, v):
                count_skipped += 1
                continue

            database.insert_price(
                asset_id=asset_id,
                date=p["date"],
                open_price=o,
                high_price=h,
                low_price=l,
                close_price=c,
                volume=v,
            )
            count_inserted += 1

        print(
            f"[INFO] {count_inserted} registros inseridos no banco. "
            f"{count_skipped} registros ignorados por dados incompletos."
        )

        return jsonify(
            {
                "status": "success",
                "message": "Dados coletados e salvos com sucesso.",
                "inserted": count_inserted,
                "skipped": count_skipped,
            }
        ), 200

    except Exception as exc:  # noqa: BLE001
        # Aqui ainda tratamos qualquer erro inesperado
        print(f"[ERROR] Erro em /api/fetch-and-save: {exc}")
        return (
            jsonify(
                {
                    "status": "error",
                    "message": "Erro ao coletar ou salvar os dados.",
                    "detail": str(exc),
                }
            ),
            500,
        )


@app.route("/api/prices/<ticker>", methods=["GET"])
def api_get_prices(ticker: str) -> Any:
    """Retorna os preços salvos no banco para o ticker informado."""
    ticker = (ticker or "").strip()

    if not ticker:
        return jsonify({"status": "error", "message": "Ticker é obrigatório."}), 400

    try:
        database.init_db()
        prices: List[Dict[str, Any]] = database.get_prices_by_ticker(ticker.upper())

        return jsonify(
            {
                "status": "success",
                "ticker": ticker.upper(),
                "count": len(prices),
                "prices": prices,
            }
        )
    except Exception as exc:  # noqa: BLE001
        print(f"[ERROR] Erro em /api/prices/{ticker}: {exc}")
        return (
            jsonify(
                {
                    "status": "error",
                    "message": "Erro ao consultar preços no banco.",
                    "detail": str(exc),
                }
            ),
            500,
        )


if __name__ == "__main__":
    print("==============================================")
    print("Sistema de Coleta e Visualização de Dados Históricos de Ações")
    print("==============================================")
    print("[INFO] Inicializando banco de dados...")
    database.init_db()
    print("[INFO] Banco de dados pronto")
    print("[INFO] Iniciando servidor Flask em http://127.0.0.1:5000")
    app.run(debug=True)
