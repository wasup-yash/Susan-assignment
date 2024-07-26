from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from models import *

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/add_to_cart")
async def add_to_cart(order: Order):
    try:
        return add_to_cart(order)
    except BaseException as e:
        raise e

    
@app.get("/fetch_orders")
async def fetch_orders():
    try:
        return fetch_orders_from_db()
    except BaseException as e:
        raise e

@app.post("/remove")
async def remove_product_from_cart(order: Order):
    try:
        return remove_product()
    except BaseException as e:
        raise e