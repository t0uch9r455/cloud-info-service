import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from prometheus_fastapi_instrumentator import Instrumentator
from database import get_db, init_db

app = FastAPI(title="Cloud Info Service")
Instrumentator().instrument(app).expose(app)  # Creates /metrics automatically

class Item(BaseModel):
    name: str
    value: str

@app.on_event("startup")
def startup():
    init_db()

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/info")
def info():
    return {
        "version": os.getenv("APP_VERSION", "1.0.0"),
        "commit": os.getenv("GIT_COMMIT", "unknown"),
        "build_time": os.getenv("BUILD_TIME", "unknown"),
        "environment": os.getenv("ENVIRONMENT", "dev"),
    }

@app.post("/items", status_code=201)
def create_item(item: Item):
    try:
        db = get_db()
        try:
            cursor = db.cursor()
            cursor.execute("INSERT INTO items (name, value) VALUES (?, ?)", 
                         (item.name, item.value))
            db.commit()
            return {"status": "created", "name": item.name}
        finally:
            db.close()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/items")
def list_items():
    try:
        db = get_db()
        try:
            rows = db.execute("SELECT * FROM items").fetchall()
            return [dict(r) for r in rows]
        finally:
            db.close()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
