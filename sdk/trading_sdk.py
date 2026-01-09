from typing import Any, Dict, List, Optional
import requests


class TradingSDK:
    """Minimal wrapper SDK for the Simple Trading API."""

    def __init__(self, base_url: str = "http://127.0.0.1:8000/api/v1") -> None:
        self.base_url = base_url.rstrip("/")

    def _get(self, path: str) -> Any:
        resp = requests.get(f"{self.base_url}{path}")
        resp.raise_for_status()
        return resp.json()

    def _post(self, path: str, payload: Dict[str, Any]) -> Any:
        resp = requests.post(f"{self.base_url}{path}", json=payload)
        resp.raise_for_status()
        return resp.json()

    def list_instruments(self) -> List[Dict[str, Any]]:
        return self._get("/instruments")

    def place_order(
        self,
        symbol: str,
        side: str,
        order_type: str,
        quantity: int,
        price: Optional[float] = None,
    ) -> Dict[str, Any]:
        payload: Dict[str, Any] = {
            "symbol": symbol,
            "side": side,
            "orderType": order_type,
            "quantity": quantity,
        }
        if price is not None:
            payload["price"] = price
        return self._post("/orders", payload)

    def get_order(self, order_id: int) -> Dict[str, Any]:
        return self._get(f"/orders/{order_id}")

    def list_trades(self) -> List[Dict[str, Any]]:
        return self._get("/trades")

    def get_portfolio(self) -> List[Dict[str, Any]]:
        return self._get("/portfolio")
