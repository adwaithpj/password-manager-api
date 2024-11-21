from fastapi import APIRouter, HTTPException, Response
from fastapi.responses import JSONResponse
from starlette import status
from datetime import datetime, timedelta

RefreshRouter = APIRouter(prefix="/reload", tags=["reload"])

MAX_RETRIES = 3


@RefreshRouter.get("/", status_code=status.HTTP_200_OK)
async def try_refresh(retries=0):
    try:
        return JSONResponse(
            content={"success": True, "message": "Refresh completed"},
            status_code=status.HTTP_200_OK,
        )
    except OperationalError:
        if retries < MAX_RETRIES:
            return await try_refresh(retries + 1)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred: {str(e)}",
        )
