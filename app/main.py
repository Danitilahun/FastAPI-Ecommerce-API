from fastapi import FastAPI , APIRouter
from app.routers import products, categories, users, auth, accounts , orders

test_router = APIRouter()

@test_router.get("/")
async def test_endpoint():
    return {"message": "Test endpoint works!"}

# --- App Description ---
description = """
    Welcome to the E-commerce API! 🚀

    This API will be used to demo how to use pytest and GitHub Actions for CI/CD.

    Done by Group 8 for a Selected Topic Assignment.
"""

# --- FastAPI App ---
app = FastAPI(
    description=description,
    title="E-commerce API",
    version="1.0.0",
    swagger_ui_parameters={
        "syntaxHighlight.theme": "monokai",
        "layout": "BaseLayout",
        "filter": True,
        "tryItOutEnabled": True,
        "onComplete": "Ok"
    },
)

app.include_router(products.router)
app.include_router(categories.router)
app.include_router(orders.router)
app.include_router(users.router)
app.include_router(accounts.router)
app.include_router(auth.router)
