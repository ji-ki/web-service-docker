from fastapi import FastAPI
from app.routers import notes
from app.database import engine
from app.models import Base
from prometheus_client import Counter, generate_latest
from app import database
from starlette.responses import Response

app = FastAPI(title="Notes Service", description="Сервис для управления заметками")

REQUEST_COUNT = Counter("request_count", "Total request count", ["method", "endpoint"])

docs_visit_count = Counter("docs_visit_count", "Total visits to /docs endpoint")

@app.middleware("http")
async def metrics_middleware(request, call_next):
    if request.url.path == "/docs":
        docs_visit_count.inc()
    response = await call_next(request)
    return response

@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type="text/plain")

@app.get("/docs")
async def docs():
    return {"message": "This is the docs page!"}

@app.middleware("http")
async def metrics_middleware(request, call_next):
    response = await call_next(request)
    REQUEST_COUNT.labels(request.method, request.url.path).inc()
    return response

@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type="text/plain")

Base.metadata.create_all(bind=engine)

database.init_db()
app.include_router(notes.router, prefix="/notes", tags=["Notes"])



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)


