from typing import Any, List, Optional, Dict
from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

class CustomAppException(Exception):
    def __init__(
        self,
        message: str,
        error_code: str = "BAD_REQUEST",
        status_code: int = status.HTTP_400_BAD_REQUEST,
        errors: Optional[List[Dict[str, Any]]] = None,
        details: Optional[Dict[str, Any]] = None
    ):
        self.message = message
        self.error_code = error_code
        self.status_code = status_code
        self.errors = errors or []
        self.details = details

class EntityInUseException(CustomAppException):
    def __init__(self, message: str, reference_count: int, can_archive: bool = True):
        super().__init__(
            message=message,
            error_code="ENTITY_IN_USE",
            status_code=status.HTTP_400_BAD_REQUEST,
            details={"reference_count": reference_count, "can_archive": can_archive}
        )

async def custom_app_exception_handler(request: Request, exc: CustomAppException):
    content = {
        "success": False,
        "error_code": exc.error_code,
        "message": exc.message,
    }
    if exc.errors:
        content["errors"] = exc.errors
    if exc.details:
        content["details"] = exc.details
    return JSONResponse(status_code=exc.status_code, content=content)

async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    error_code = "UNAUTHORIZED" if exc.status_code == 401 else "FORBIDDEN" if exc.status_code == 403 else "NOT_FOUND" if exc.status_code == 404 else "HTTP_ERROR"
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error_code": error_code,
            "message": str(exc.detail),
            "errors": []
        }
    )

async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = []
    for err in exc.errors():
        field = ".".join(str(x) for x in err.get("loc", []) if x not in ("body", "query", "path"))
        errors.append({
            "field": field or "body",
            "message": err.get("msg", "Validation error")
        })
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "success": False,
            "error_code": "VALIDATION_ERROR",
            "message": "Kiritilgan ma'lumotlarda xatolik mavjud",
            "errors": errors
        }
    )

async def generic_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "success": False,
            "error_code": "INTERNAL_SERVER_ERROR",
            "message": "Kutilmagan server xatoligi yuz berdi",
            "errors": [{"field": "server", "message": str(exc)}]
        }
    )
