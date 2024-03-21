from fastapi import APIRouter

from apis.v1 import router_user, route_blog

api_router = APIRouter()
api_router.include_router(router_user.router, prefix="", tags=["user"])
api_router.include_router(route_blog.router, prefix="", tags=["blog"])
