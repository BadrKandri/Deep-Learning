from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from routers.api import router as api_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)

@app.get("/")
async def home():
    return FileResponse("static/index.html")

if __name__ == "__main__":
    print('Loading Server ...')
    uvicorn.run("main:app", host='localhost', port=8000, reload=True)