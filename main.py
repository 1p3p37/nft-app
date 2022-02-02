import json
from typing import List
import os
from dotenv import load_dotenv

from fastapi import FastAPI, HTTPException, Form, Request, UploadFile
from models.models import token_pydantic, token_pydanticIn, Token
from tortoise.contrib.fastapi import register_tortoise

# generate rand string
import random
import string

from web3 import Web3, HTTPProvider
from web3.middleware import geth_poa_middleware

app = FastAPI()
# rinkeby
load_dotenv()
w3 = Web3(Web3.HTTPProvider(os.getenv('WEB3_INFURA_PROJECT')))
w3.middleware_onion.inject(geth_poa_middleware, layer=0)
ABI = os.getenv('ABI')
MintableNFT = w3.eth.contract(address="0x92e098deF0CA9577BD50ca61B90b9A46EC1F2040", abi=ABI)

register_tortoise(
    app,
    db_url='sqlite://database.sqlite3',
    modules={'models': ['models.models']},
    generate_schemas=True,
    add_exception_handlers=True
)


def random_string():
    letters = string.ascii_letters + string.digits
    rand_string = ''.join(random.choice(letters) for i in range(20))
    return rand_string


@app.post('/tokens/create')
async def create_token(Media_url: str = Form(...), Owner: str = Form(...)):
    token_obj = await Token.create(owner=Owner, unique_hash=random_string(), media_url=Media_url, tx_hash="None")
    new_token = await token_pydantic.from_tortoise_orm(token_obj)
    Mint = MintableNFT.functions.mint(
        new_token.owner,
        new_token.unique_hash,
        new_token.media_url
    ).buildTransaction()
    Mint.update({'gas': 500000})
    Mint.update({'maxFeePerGas': w3.eth.gasPrice * 2})
    Mint.update({'maxPriorityFeePerGas': w3.eth.gasPrice})
    Mint.update({'nonce': w3.eth.get_transaction_count(os.getenv('ADDRESS'))})
    signed_tx = w3.eth.account.sign_transaction(Mint, os.getenv('PRIVATE_KEY'))
    # send the transaction
    txn_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
    txn_receipt = w3.eth.wait_for_transaction_receipt(txn_hash)
    print(txn_receipt, "\n")
    print(w3.toHex(w3.keccak(signed_tx.rawTransaction)))

    await Token.filter(id=new_token.id).update(tx_hash=w3.toHex(w3.keccak(signed_tx.rawTransaction)))

    # print(token_pydantic.dict())
    return {"status": "ok",
            "data":
                f"owner: {new_token.owner} media_url: {new_token.media_url}\nToken successfully created "
            }


@app.get("/tokens/list", response_model=List[token_pydantic])
async def list_tokens():
    return await token_pydantic.from_queryset(Token.all())


@app.get("/tokens/total_supply")
async def total_supply_token():
    total_supply = MintableNFT.functions.totalSupply().call()
    print("Total supply: ", total_supply)
    return {"result": total_supply}
