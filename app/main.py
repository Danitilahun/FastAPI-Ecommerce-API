from fastapi import FastAPI , APIRouter

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

app.include_router(test_router)