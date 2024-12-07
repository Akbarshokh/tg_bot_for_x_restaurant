from .start import start_router
from .settings import settings_router
from .feedbacks import feedback_router

routers_list = [
    start_router,
    settings_router,
    feedback_router,
]

__all__ = [
    "routers_list",
]