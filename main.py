import json
from typing import List
import os
from dotenv import load_dotenv

from fastapi import FastAPI, HTTPException, Form, Request, UploadFile
from models.models import token_pydantic, token_pydanticIn, Token
from pydantic import BaseModel

# generate rand string
import random
import string

from web3 import Web3, HTTPProvider

from web3._utils.events import get_event_data

from tortoise.contrib.fastapi import register_tortoise


register_tortoise(
    app,
    db_url='sqlite://database.sqlite3',
    modules={'models': ['models.models']},
    generate_schemas=True,
    add_exception_handlers=True
)

app = FastAPI()
#rinkeby
load_dotenv()
w3 = Web3(Web3.HTTPProvider(os.getenv('WEB3_INFURA_PROJECT')))
ABI = os.getenv('ABI')
MintableNFT = w3.eth.contract(address="0x7abbEc0b2Edf56325F6dA1BE71BC2202001b09e2", abi=ABI)


def random_string():
    letters = string.ascii_letters + string.digits
    rand_string = ''.join(random.choice(letters) for i in range(20))
    return rand_string


@app.post('/tokens/create')
async def create_token(token: token_pydanticIn):
    token_info = token.dict()
    token_obj = await Token.create(**token_info)
    new_token = await token_pydantic.from_tortoise_orm(token_obj)
    print(token.dict())
    return {"status": "ok",
            "data":
                f"owner: {new_token.owner} media_url: {new_token.media_url}"
            }


@app.get("/tokens/list", response_model=List[token_pydantic])
async def list_tokens():
    return await token_pydantic.from_queryset(Token.all())


@app.get("/tokens/total_supply")
async def total_supply_token():
    total_supply = MintableNFT.functions.totalSupply().call()
    print("Total supply: ", total_supply)
    return {"result": total_supply}
