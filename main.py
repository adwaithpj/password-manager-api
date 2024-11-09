from fastapi import Depends, FastAPI
from models.BaseModel import init
from router.v1.authRouter import AuthRouter
from router.v1.UserRouter import UserRouter

app = FastAPI(title="Password Manager API")

app.include_router(AuthRouter)
app.include_router(UserRouter)

# Initialize Data Model Attributes
init()
