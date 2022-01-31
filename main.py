from fastapi import FastAPI, HTTPException
from models.models import token_pydantic, tokenIn_pydantic, Tokens
from pydantic import BaseModel
app = FastAPI()


@app.post("/tokens/create")
async def create_token(name: str):
    name_token = name
    return {"token": f"{name_token}"}


@app.get("/tokens/list")
async def list_tokens():
    return {"list"}


@app.get("/tokens/total_supply")
async def list_tokens():
    return {"result": 10000}
