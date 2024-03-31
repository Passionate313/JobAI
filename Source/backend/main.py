import uvicorn
from fastapi import FastAPI

from pymongo import MongoClient
from fastapi.middleware.cors import CORSMiddleware
from routes.api import router as api_router
from src.config import ATLAS_URI, DB_NAME

# init FastAPI app
app = FastAPI()

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup_db_client():
    """
    Lets app connect to mongodb client server with atlas uri and database name
    ATLAS_URI and DB_NAME is defined in env file
    """
    app.mongodb_client = MongoClient(ATLAS_URI)
    app.database = app.mongodb_client[DB_NAME]
    print("Connected to the MongoDB database!")


@app.on_event("shutdown")
def shutdown_db_client():
    """
    Lets app disconnect from mongodb client when app closes
    """
    app.mongodb_client.close()


app.include_router(api_router)

if __name__ == '__main__':
    uvicorn.run(
        "main:app",
        host='0.0.0.0',
        port=8080,
        log_level="info",
        reload=True
    )
