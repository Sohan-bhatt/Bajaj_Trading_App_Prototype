const API_BASE = "http://127.0.0.1:8000/api/v1";

const instrumentsEl = document.getElementById("instruments");
const orderResultEl = document.getElementById("order-result");
const orderStatusEl = document.getElementById("order-status");
const tradesEl = document.getElementById("trades");
const portfolioEl = document.getElementById("portfolio");

function pretty(data) {
  return JSON.stringify(data, null, 2);
}

async function loadInstruments() {
  instrumentsEl.textContent = "Loading...";
  const res = await fetch(`${API_BASE}/instruments`);
  const data = await res.json();
  instrumentsEl.innerHTML = "";
  data.forEach((inst) => {
    const div = document.createElement("div");
    div.textContent = `${inst.symbol} | ${inst.exchange} | ${inst.instrumentType} | LTP: ${inst.lastTradedPrice}`;
    instrumentsEl.appendChild(div);
  });
}

async function submitOrder(evt) {
  evt.preventDefault();
  const form = evt.target;
  const payload = {
    symbol: form.symbol.value.trim(),
    side: form.side.value,
    orderType: form.orderType.value,
    quantity: Number(form.quantity.value),
  };
  if (form.price.value) {
    payload.price = Number(form.price.value);
  }

  orderResultEl.textContent = "Submitting...";
  const res = await fetch(`${API_BASE}/orders`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  const data = await res.json();
  if (!res.ok) {
    orderResultEl.textContent = pretty(data);
    return;
  }
  orderResultEl.textContent = pretty(data);
  form.reset();
}

async function checkOrder() {
  const id = document.getElementById("order-id").value;
  if (!id) {
    orderStatusEl.textContent = "Enter an order ID.";
    return;
  }
  orderStatusEl.textContent = "Loading...";
  const res = await fetch(`${API_BASE}/orders/${id}`);
  const data = await res.json();
  orderStatusEl.textContent = pretty(data);
}

async function loadTrades() {
  tradesEl.textContent = "Loading...";
  const res = await fetch(`${API_BASE}/trades`);
  const data = await res.json();
  tradesEl.textContent = pretty(data);
}

async function loadPortfolio() {
  portfolioEl.textContent = "Loading...";
  const res = await fetch(`${API_BASE}/portfolio`);
  const data = await res.json();
  portfolioEl.textContent = pretty(data);
}

document.getElementById("load-instruments").addEventListener("click", loadInstruments);
document.getElementById("order-form").addEventListener("submit", submitOrder);
document.getElementById("check-order").addEventListener("click", checkOrder);
document.getElementById("load-trades").addEventListener("click", loadTrades);
document.getElementById("load-portfolio").addEventListener("click", loadPortfolio);
