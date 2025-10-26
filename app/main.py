from fastapi import FastAPI
from app.routes import auth_routes, chat_routes

app = FastAPI(title="PDF Chatbot API", version="1.0")

app.include_router(auth_routes.router)
app.include_router(chat_routes.router)


@app.get("/")
def root():
    return {"message": "Welcome to the FastAPI PDF Chatbot!"}
