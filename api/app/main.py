from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import Response, JSONResponse

from db import get_stored_articles

app = FastAPI(title='ActuSafe')


app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:5173', 'http://127.0.0.1:5173'],
    allow_methods=['GET'],
)

@app.get('/health')
async def health():
    return {'status': 'ok'}

@app.get('/articles')
async def get_articles() -> Response:
    articles = get_stored_articles()

    return JSONResponse(
        content=jsonable_encoder(articles),
        media_type="application/json",
        status_code=200
    )

