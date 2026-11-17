
from fastapi import FastAPI

from routers.auth import router as auth_router
from routers.tasks import router as tasks_router

app = FastAPI(
    title="task manager api",
    description="task manager with authentication",
    version="1.0.0"
)

@app.get("/")
def home():
    return {
        "message": "task manager api is running"
    }

app.include_router(auth_router)
app.include_router(tasks_router)

# print("REGISTERED ROUTES:")

# for route in app.routes:
#     if hasattr(route, "path"):
#         print(route.path)
