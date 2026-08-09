from fastapi import FastAPI
from pydantic import BaseModel
import tracefix

app = FastAPI()
tracefix.init(api_key="YOUR_API_KEY", project_id="YOUR_PROJECT_ID")

class OrderItem(BaseModel):
    name: str
    quantity: int
    price: float

class Order(BaseModel):
    items: list[OrderItem]

@app.post("/api/order/total")
def calculate_total(order: Order):
    total = 0
    for item in order.items:
        total += item.price * item.quanity  # bug: should be quantity
    return {"total": total}