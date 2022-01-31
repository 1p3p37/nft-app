import sqlite3
from tortoise.fields import CharField
from tortoise.contrib.pydantic import pydantic_model_creator, pydantic_queryset_creator
from tortoise import Tortoise, fields, run_async
from tortoise.models import Model
from datetime import datetime


class Tokens(Model):
    id = fields.IntField(pk=True, index=True)
    unique_hash = fields.CharField(max_length=20)
    tx_hash = fields.CharField(max_length=100)
    media_url = fields.CharField(max_length=100, null=False, unique=True)
    owner = fields.CharField(max_length=100, null=False, unique=True)


token_pydantic = pydantic_model_creator(Tokens, name="Token")
tokenIn_pydantic = pydantic_model_creator(Tokens, name="TokenIn", exclude_readonly=True)
