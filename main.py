import os
from contextlib import asynccontextmanager
from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from core.config import settings
from core.exceptions import (
    CustomAppException,
    custom_app_exception_handler,
    http_exception_handler,
    validation_exception_handler,
    generic_exception_handler,
)
from db.init_db import init_db

# Import Domain App Routers
from apps.accounts.urls import router as accounts_router
from apps.dashboard.urls import router as dashboard_router
from apps.products.urls import router as products_router
from apps.master_data.urls import router as master_data_router
from apps.warehouse.urls import router as warehouse_router
from apps.purchasing.urls import router as purchasing_router
from apps.production.urls import router as production_router
from apps.sales.urls import router as sales_router
from apps.finance.urls import router as finance_router
from apps.audit.urls import router as audit_router
from apps.files.urls import router as files_router
from apps.dashboard.reports import router as reports_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    yield

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global Exception Handlers
app.add_exception_handler(CustomAppException, custom_app_exception_handler)
app.add_exception_handler(StarletteHTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, generic_exception_handler)

# Aggregate Domain App Routers into /api/v1
api_router = APIRouter()
api_router.include_router(accounts_router, prefix="/auth", tags=["Accounts & Auth"])
api_router.include_router(dashboard_router, prefix="/dashboard", tags=["Dashboard"])
api_router.include_router(products_router, prefix="/products", tags=["Products Catalog"])
api_router.include_router(master_data_router, prefix="/master-data", tags=["Master Data"])
api_router.include_router(warehouse_router, prefix="/warehouse", tags=["Warehouse & Inventory"])
api_router.include_router(purchasing_router, prefix="/purchasing", tags=["Purchasing"])
api_router.include_router(production_router, prefix="/production", tags=["Production Batches"])
api_router.include_router(sales_router, prefix="/sales", tags=["Sales Invoices"])
api_router.include_router(finance_router, prefix="/finance", tags=["Finance & Transactions"])
api_router.include_router(audit_router, prefix="/audit-logs", tags=["Audit Logs"])
api_router.include_router(files_router, prefix="/files", tags=["Files Upload"])
api_router.include_router(reports_router, prefix="/reports", tags=["Reports"])

app.include_router(api_router, prefix=settings.API_V1_STR)

# Serve Uploaded Files
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
app.mount("/uploads", StaticFiles(directory=settings.UPLOAD_DIR), name="uploads")

@app.get("/health", tags=["Health Check"])
async def health_check():
    return {
        "status": "online",
        "app": settings.PROJECT_NAME,
        "environment": settings.ENVIRONMENT
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
