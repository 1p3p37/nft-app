from typing import List

from fastapi import FastAPI, HTTPException
from models.models import token_pydantic, tokenIn_pydantic, Tokens
from pydantic import BaseModel

# generate rand string
import random
import string

app = FastAPI()


def random_string():
    letters = string.ascii_letters + string.digits
    rand_string = ''.join(random.choice(letters) for i in range(20))
    return rand_string


@app.post("/tokens/create", response_model=token_pydantic)
async def create_token(token: token_pydantic):
    unique_hash = random_string()
    #media_url =
    #owner =
    token_obj = await Tokens.create(**token.dict(exclude_unset=True))
    return await token_pydantic.from_tortoise_orm(token_obj)


@app.get("/tokens/list", response_model=List[token_pydantic])
async def list_tokens():
    return await token_pydantic.from_queryset(Tokens.all())


@app.get("/tokens/total_supply")
async def total_supply_token():
    return {"result": 10000}
