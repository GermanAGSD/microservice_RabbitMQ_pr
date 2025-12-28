from fastapi import FastAPI
from faststream.rabbit.fastapi import RabbitRouter
import uvicorn


app = FastAPI()

router = RabbitRouter("amqp://admin:admin123@172.30.30.19:5672/")

@router.get("/order")
async def make_order(name: str):
    await router.broker.publish(
        f"new order: {name}",
        queue="orders"
    )
    return {"data": "success"}

app.include_router(router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="192.168.3.2", port=8000)