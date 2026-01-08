from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional, Dict
from datetime import datetime

app = FastAPI(title="Simple Trading API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- In-memory storage ---
INSTRUMENTS = [
    {
        "symbol": "AAPL",
        "exchange": "NASDAQ",
        "instrumentType": "EQUITY",
        "lastTradedPrice": 190.25,
    },
    {
        "symbol": "MSFT",
        "exchange": "NASDAQ",
        "instrumentType": "EQUITY",
        "lastTradedPrice": 420.10,
    },
    {
        "symbol": "TSLA",
        "exchange": "NASDAQ",
        "instrumentType": "EQUITY",
        "lastTradedPrice": 245.80,
    },
]

orders: Dict[int, dict] = {}
trades: List[dict] = []
portfolio: Dict[str, dict] = {}
order_seq = 1


class OrderRequest(BaseModel):
    symbol: str
    side: str = Field(..., pattern="^(BUY|SELL)$")
    orderType: str = Field(..., pattern="^(MARKET|LIMIT)$")
    quantity: int
    price: Optional[float] = None


class OrderResponse(BaseModel):
    orderId: int
    status: str


@app.get("/api/v1/instruments")
def list_instruments():
    return INSTRUMENTS


def find_instrument(symbol: str) -> dict:
    for inst in INSTRUMENTS:
        if inst["symbol"] == symbol:
            return inst
    return {}


def execute_order(order: dict) -> None:
    symbol = order["symbol"]
    side = order["side"]
    qty = order["quantity"]
    price = order["executedPrice"]

    trade = {
        "tradeId": len(trades) + 1,
        "orderId": order["orderId"],
        "symbol": symbol,
        "side": side,
        "quantity": qty,
        "price": price,
        "timestamp": datetime.utcnow().isoformat() + "Z",
    }
    trades.append(trade)

    holding = portfolio.get(symbol, {"symbol": symbol, "quantity": 0, "averagePrice": 0.0})

    if side == "BUY":
        total_cost = holding["averagePrice"] * holding["quantity"] + price * qty
        new_qty = holding["quantity"] + qty
        avg_price = total_cost / new_qty if new_qty else 0.0
        holding["quantity"] = new_qty
        holding["averagePrice"] = round(avg_price, 2)
    else:
        holding["quantity"] = holding["quantity"] - qty
        if holding["quantity"] <= 0:
            holding["quantity"] = 0
            holding["averagePrice"] = 0.0

    portfolio[symbol] = holding


@app.post("/api/v1/orders", response_model=OrderResponse)
def place_order(req: OrderRequest):
    global order_seq

    if req.quantity <= 0:
        raise HTTPException(status_code=400, detail="Quantity must be greater than 0")

    instrument = find_instrument(req.symbol)
    if not instrument:
        raise HTTPException(status_code=404, detail="Instrument not found")

    if req.orderType == "LIMIT" and (req.price is None or req.price <= 0):
        raise HTTPException(status_code=400, detail="Price is required for LIMIT orders")

    if req.side == "SELL":
        holding = portfolio.get(req.symbol, {"quantity": 0})
        if holding["quantity"] < req.quantity:
            raise HTTPException(status_code=400, detail="Insufficient holdings to sell")

    executed_price = req.price if req.orderType == "LIMIT" else instrument["lastTradedPrice"]

    order = {
        "orderId": order_seq,
        "symbol": req.symbol,
        "side": req.side,
        "orderType": req.orderType,
        "quantity": req.quantity,
        "price": req.price,
        "status": "PLACED",
        "executedPrice": executed_price,
        "timestamp": datetime.utcnow().isoformat() + "Z",
    }

    orders[order_seq] = order
    order_seq += 1

    # Simple execution simulation: execute immediately
    order["status"] = "EXECUTED"
    execute_order(order)

    return {"orderId": order["orderId"], "status": order["status"]}


@app.get("/api/v1/orders/{order_id}")
def get_order(order_id: int):
    order = orders.get(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


@app.get("/api/v1/trades")
def list_trades():
    return trades


@app.get("/api/v1/portfolio")
def get_portfolio():
    results = []
    for symbol, holding in portfolio.items():
        instrument = find_instrument(symbol)
        ltp = instrument.get("lastTradedPrice", 0.0)
        current_value = round(holding["quantity"] * ltp, 2)
        results.append(
            {
                "symbol": symbol,
                "quantity": holding["quantity"],
                "averagePrice": holding["averagePrice"],
                "currentValue": current_value,
            }
        )
    return results
