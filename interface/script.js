// script.js
// Frontend simples: busca dados, salva no banco e carrega para gráfico + tabela.

let priceChart = null;

// Utilitário para mostrar mensagens de status
function setStatus(type, message) {
    const el = document.getElementById("status-message");
    if (!el) return;

    el.textContent = message || "";

    el.classList.remove("success", "error", "warning", "loading");

    if (!message) {
        el.style.display = "none";
        return;
    }

    el.style.display = "block";

    switch (type) {
        case "success":
            el.classList.add("success");
            break;
        case "error":
            el.classList.add("error");
            break;
        case "warning":
            el.classList.add("warning");
            break;
        case "loading":
            el.classList.add("loading");
            break;
    }
}

// Converte número para string formatada (2 casas decimais)
function formatNumber(value) {
    if (value === null || value === undefined) return "-";
    const n = Number(value);
    if (Number.isNaN(n)) return "-";
    return n.toFixed(2);
}

// Converte volume para milhões (ex.: 14.79 M)
function formatVolume(value) {
    if (value === null || value === undefined) return "-";

    const n = Number(value);
    if (Number.isNaN(n)) return "-";

    // converte para milhões
    const millions = n / 1_000_000;

    // retorna com duas casas decimais + letra M
    return millions.toFixed(2) + " M";
}


// Atualiza gráfico e tabela com os dados retornados do backend
function updateUIWithPrices(response) {
    const dataSection = document.getElementById("data-section");
    const tickerTitle = document.getElementById("ticker-title");
    const dataCount = document.getElementById("data-count");
    const tableBody = document.getElementById("table-body");

    if (!dataSection || !tickerTitle || !dataCount || !tableBody) {
        console.error("Elementos de UI não encontrados.");
        return;
    }

    const prices = response.prices || [];
    const ticker = response.ticker || "";

    // Mostra seção de dados
    dataSection.style.display = prices.length > 0 ? "block" : "none";

    // Atualiza textos
    tickerTitle.textContent = ticker || "TICKER";
    dataCount.textContent = `${prices.length} registros encontrados`;

    // Prepara dados para o gráfico
    const labels = prices.map((p) => p.date);
    const closeData = prices.map((p) => p.close);

    // Atualiza gráfico
    const ctx = document.getElementById("price-chart");
    if (ctx) {
        if (priceChart) {
            priceChart.destroy();
        }

        priceChart = new Chart(ctx, {
            type: "line",
            data: {
                labels,
                datasets: [
                    {
                        label: "Preço de Fechamento (USD)",
                        data: closeData,
                        tension: 0.2,
                        fill: true,
                    },
                ],
            },
            options: {
                responsive: true,
                scales: {
                    x: {
                        ticks: {
                            maxTicksLimit: 12,
                        },
                    },
                    y: {
                        beginAtZero: false,
                    },
                },
            },
        });
    }

    // Atualiza tabela
    tableBody.innerHTML = "";

    for (const p of prices) {
        const tr = document.createElement("tr");
        tr.innerHTML = `
            <td>${p.date}</td>
            <td>${formatNumber(p.open)}</td>
            <td>${formatNumber(p.high)}</td>
            <td>${formatNumber(p.low)}</td>
            <td>${formatNumber(p.close)}</td>
            <td>${formatVolume(p.volume)}</td>
        `;
        tableBody.appendChild(tr);
    }
}

// Faz POST /api/fetch-and-save para coletar e salvar dados
async function fetchAndSaveTicker(ticker) {
    const response = await fetch("/api/fetch-and-save", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ ticker }),
    });

    if (!response.ok) {
        throw new Error(`Erro HTTP ${response.status}`);
    }

    const data = await response.json();
    return data;
}

// Faz GET /api/prices/<ticker> para carregar dados salvos
async function getPricesFromDb(ticker) {
    const response = await fetch(`/api/prices/${encodeURIComponent(ticker)}`);
    if (!response.ok) {
        throw new Error(`Erro HTTP ${response.status}`);
    }
    const data = await response.json();
    return data;
}

// Inicialização
document.addEventListener("DOMContentLoaded", () => {
    const input = document.getElementById("ticker-input");
    const button = document.getElementById("fetch-button");

    if (!input || !button) {
        console.error("Input ou botão não encontrados.");
        return;
    }

    async function handleSearch() {
        const raw = input.value || "";
        const ticker = raw.trim().toUpperCase();

        if (!ticker) {
            setStatus("warning", "Por favor, digite um ticker.");
            return;
        }

        try {
            setStatus("loading", "Coletando dados na NASDAQ e salvando no banco...");

            // 1) Coleta e salva no backend
            const saveResult = await fetchAndSaveTicker(ticker);
            if (saveResult.status === "error") {
                setStatus("error", saveResult.message || "Erro ao coletar dados.");
                return;
            }

            if (saveResult.status === "warning") {
                setStatus("warning", saveResult.message || "Nenhum dado encontrado.");
            } else {
                setStatus("success", saveResult.message || "Dados coletados com sucesso.");
            }

            // 2) Carrega do banco para exibir
            const pricesResult = await getPricesFromDb(ticker);

            if (pricesResult.status !== "success") {
                setStatus("error", pricesResult.message || "Erro ao carregar dados do banco.");
                return;
            }

            updateUIWithPrices(pricesResult);
        } catch (err) {
            console.error(err);
            setStatus("error", `Erro ao carregar dados: ${(err && err.message) || err}`);
        }
    }

    button.addEventListener("click", handleSearch);

    // Enter no input também dispara a busca
    input.addEventListener("keyup", (ev) => {
        if (ev.key === "Enter") {
            handleSearch();
        }
    });
});
