# Bajaj Trading App Prototype

A minimal trading simulator with a FastAPI backend and a static HTML/CSS/JS frontend.

## Project Structure
```python
Bajaj_Trading_App_Prototype/
├── README.md
├── .gitignore
├── backend/
│   ├── Dockerfile
│   ├── main.py
│   └── requirements.txt
└── frontend/
    ├── index.html
    ├── style.css
    └── app.js

```


## Backend

### Features

- List instruments
- Place buy/sell orders (market/limit)
- Check order status
- View executed trades
- View portfolio holdings

### Requirements

- Python 3.9+
-`cd backened'
- `pip install -r requirements.txt`

Install dependencies:

```python
git clone https://github.com/Sohan-bhatt/Bajaj_Trading_App_Prototype.git
cd Bajaj_Trading_App_Prototype/bajaj/backend
python -m venv venv              // Create a virtual Environment
source venv/bin/activate         // Activate the virtual environment
pip install -r requirements.txt
```

### Run the API

```bash
cd Bajaj_Trading_App_Prototype/bajaj/backend
uvicorn main:app --reload
```

API base URL:

```
http://127.0.0.1:8000/api/v1
```

### Endpoints

- `GET /api/v1/instruments`
- `POST /api/v1/orders`
- `GET /api/v1/orders/{orderId}`
- `GET /api/v1/trades`
- `GET /api/v1/portfolio`

## Frontend

Open the file directly in a browser:

```python
Bajaj_Trading_App_Prototype/bajaj/frontend/index.html
```
- ## For live server install in VS Code
```python
  Ctrl+Shift+X
  Install "Live Server"
```
#### `Bottom right you will see the "live" option click on it.`

### Sections

- **Place Order**: Enter symbol, side, order type, quantity, and optional price. Submits a new order.
- **Order Status**: Enter an order ID to fetch its current status and details.
- **Trades**: Shows executed trades returned by the API.
- **Portfolio**: Shows current holdings with quantity, average price, and current value.

## Notes

- Data is stored in memory and resets on server restart.
- Market orders execute immediately at the instrument LTP.
- Limit orders execute immediately at the provided price.

## Implementation Notes (Feature-by-Feature)

- **Instruments**: A fixed in-memory list in `main.py` exposes symbol, exchange, type, and last traded price via `GET /api/v1/instruments`.
- **Order Placement**: Validates quantity > 0, limit price presence, symbol existence, and SELL holdings. Orders are stored in-memory with an auto-increment ID.
- **Order Status**: `GET /api/v1/orders/{orderId}` returns the stored order, including status and execution price.
- **Trade Execution**: Orders are executed immediately; a trade record is generated and appended to the trade list.
- **Trades**: `GET /api/v1/trades` returns all executed trades in memory.
- **Portfolio**: Holdings are updated on execution; average price is recalculated for buys and quantities reduced for sells. `GET /api/v1/portfolio` calculates current value using LTP.
