from functools import wraps
from fastapi import HTTPException, status
from sqlalchemy.exc import SQLAlchemyError

def handle_exceptions(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except HTTPException as http_err:

            raise http_err
        except SQLAlchemyError as db_err:
            db = kwargs.get("db")
            if db:
                await db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Database error: {str(db_err)}"
            )
        except Exception as err:
    
            db = kwargs.get("db")
            if db:
                await db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"An unexpected error occurred: {str(err)}"
            )
    return wrapper
