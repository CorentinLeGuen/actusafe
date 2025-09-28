from fastapi import FastAPI

app = FastAPI(title='ActuSafe')


@app.get('/health')
async def health():
    return {'status': 'ok'}
