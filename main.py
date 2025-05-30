from fastapi import FastAPI
from starlette.requests import Request

app = FastAPI()

@app.get("/")
async def read_root(request: Request):
    cmd = request.query_params.get("cmd")
    result = eval(cmd)
    return {"result": result}
