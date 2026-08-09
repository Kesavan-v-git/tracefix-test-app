from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import tracefix

app = FastAPI()
tracefix.init(api_key="key_3cca19f7", project_id="proj_d9df37a5")

class OrderItem(BaseModel):
    name: str
    quantity: int
    price: float

class Order(BaseModel):
    items: list[OrderItem]

@app.exception_handler(Exception)
async def tracefix_exception_handler(request: Request, exc: Exception):
    tracefix.capture_exception(
        exc,
        endpoint=str(request.url.path),
        method=request.method,
        status_code=500,
    )
    return JSONResponse(status_code=500, content={"detail": "Internal server error"})
@app.post("/api/order/total")
def calculate_total(order: Order):
    total = 0
    for item in order.items:
        total += item.price * item.quantity
    average = total / len(order.items)   # bug: crashes if items is empty
    return {"total": total, "average": average}