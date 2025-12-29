from fastapi import FastAPI
from faststream.rabbit.fastapi import RabbitRouter
import uvicorn
import random

app = FastAPI()

router = RabbitRouter("amqp://admin:admin123@172.30.30.19:5672/")

@router.get("/order")
async def make_order(name: str, event: str):

    data_json = {
        "id": random.randint(1, 1_000_000),
        "event": event,
        "message": name
    }
    await router.broker.publish(
        data_json,
        queue="orders"
    )

    return {"data": "success"}

@router.get("/product")
async def new_product(name: str, event: str):
    data_json = {
        "id": random.randint(1, 1_000_000),
        "event": event,
        "message": name
    }
    await router.broker.publish(
        data_json,
        queue="product"
    )
    return {"data": "success"}


app.include_router(router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="192.168.3.2", port=8000)