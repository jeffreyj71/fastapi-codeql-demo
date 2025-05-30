from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
import os
import sqlite3
from secrets import SECRET_KEY

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Welcome to vulnerable FastAPI app!"}

# Command injection
@app.get("/run")
async def run_command(cmd: str):
    return os.popen(cmd).read()

# SQL injection
@app.get("/user")
async def get_user(name: str):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    query = f"SELECT * FROM users WHERE name = '{name}'"
    cursor.execute(query)
    return {"result": cursor.fetchall()}

# XSS
@app.get("/greet", response_class=HTMLResponse)
async def greet(request: Request):
    name = request.query_params.get("name", "stranger")
    return f"<html><body><h1>Hello, {name}</h1></body></html>"

# Path traversal
@app.get("/readfile")
async def read_file(file: str):
    with open(file, 'r') as f:
        return f.read()

# Hardcoded secret exposure
@app.get("/secret")
async def show_secret():
    return {"secret": SECRET_KEY}
