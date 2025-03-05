from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from database import Base, engine
import models  # ✅ Import models to ensure table creation
from routes import router  # ✅ Import API routes
from fastapi.middleware.cors import CORSMiddleware

# ✅ Initialize FastAPI app
app = FastAPI(
    title="Decentralized Identity API",
    description="API for authentication and decentralized identity management",
    version="1.0",
    openapi_tags=[
        {"name": "Authentication", "description": "User authentication and JWT management"},
    ]
)

# ✅ Add CORS middleware to allow frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Update with frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Custom OpenAPI Schema for Bearer Token Authentication
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Decentralized Identity API",
        version="1.0",
        description="API for authentication and decentralized identity management",
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
            "description": "Enter 'Bearer <your_token>' to authenticate"
        }
    }
    # ✅ Apply BearerAuth to all paths
    for path in openapi_schema["paths"].values():
        for method in path:
            path[method]["security"] = [{"BearerAuth": []}]

    app.openapi_schema = openapi_schema
    return app.openapi_schema

# ✅ Assign the custom OpenAPI schema
app.openapi = custom_openapi

# ✅ Create database tables if they don't exist
Base.metadata.create_all(bind=engine)

# ✅ Include authentication and identity routes
app.include_router(router)

# ✅ Root endpoint
@app.get("/")
def read_root():
    return {"message": "Decentralized Identity System is running!"}
