from fastapi import FastAPI
from pydantic import BaseModel
import tracefix

app = FastAPI()
tracefix.init(api_key="key_03db6224", project_id="proj_086c97b7")

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
        total += item.price * item.quantity
    return {"total": total}