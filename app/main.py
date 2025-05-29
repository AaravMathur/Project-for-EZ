from fastapi import FastAPI
from app.routers import ops, client

app = FastAPI(
    title="Secure File Sharing System",
    description="A secure file-sharing API with two user roles: Ops and Client",
    version="1.0.0"
)

app.include_router(ops.router, prefix="/ops", tags=["Ops User"])
app.include_router(client.router, prefix="/client", tags=["Client User"])