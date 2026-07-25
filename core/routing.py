from typing import Callable, List, Optional
from fastapi import APIRouter

class RouteConfig:
    def __init__(
        self,
        path: str,
        endpoint: Callable,
        methods: Optional[List[str]] = None,
        status_code: int = 200,
        summary: Optional[str] = None
    ):
        self.path = path
        self.endpoint = endpoint
        self.methods = methods or ["GET"]
        self.status_code = status_code
        self.summary = summary

def path(
    route_path: str,
    view_func: Callable,
    methods: Optional[List[str]] = None,
    status_code: int = 200,
    summary: Optional[str] = None
) -> RouteConfig:
    return RouteConfig(
        path=route_path,
        endpoint=view_func,
        methods=methods or ["GET"],
        status_code=status_code,
        summary=summary
    )

def create_router(urlpatterns: List[RouteConfig]) -> APIRouter:
    router = APIRouter()
    for route in urlpatterns:
        router.add_api_route(
            path=route.path,
            endpoint=route.endpoint,
            methods=route.methods,
            status_code=route.status_code,
            summary=route.summary
        )
    return router
