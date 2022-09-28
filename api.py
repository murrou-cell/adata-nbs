from fastapi import FastAPI
from ql3 import litewrapper
from pydantic import BaseModel


class article(BaseModel):
    title: str
    date: str
    url: str
    labels: list
    links: list
    body: str


def converter(data):
    for item in data:
        item['labels'] = eval(item['labels'])
        item['links'] = eval(item['links'])
    return data

app = FastAPI()

sql = litewrapper()

@app.get("/")
async def root():
    return {"message": "nbs article api"}

@app.get("/articles/")
async def atricles(label:str = None, date:str = None):
    if not label and not date:
        response = sql.query_all('nbs')
    if label:
        response = sql.query_many('nbs', 'labels', label)
    if date:
        response = sql.query_many('nbs', 'date', date)
    return converter(response)

@app.get("/article/{article_id}")
async def get_single_article(article_id):
    resp = sql.query_by_id('nbs', 'item_id', article_id)
    return converter(resp)

@app.delete("/article/{article_id}")
async def articles_delete(article_id):
    resp = sql.delete_one('nbs', 'item_id', article_id)
    return resp

@app.put("/article/{article_id}")
async def articles_put(article_id: str, article: article):
    resp = sql.update_one(article_id,article)
    return resp