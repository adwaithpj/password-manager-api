from fastapi import Depends, FastAPI
from models.BaseModel import init
from router.v1.authRouter import AuthRouter
from router.v1.UserRouter import UserRouter
from router.v1.PasswordRouter import PasswordRouter
from router.v1.RefreshRouter import RefreshRouter

app = FastAPI(title="Password Manager API")

app.include_router(AuthRouter)
app.include_router(UserRouter)
app.include_router(PasswordRouter)
app.include_router(RefreshRouter)

# Initialize Data Model Attributes
init()
