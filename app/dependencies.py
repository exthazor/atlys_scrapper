from fastapi import Header, HTTPException
import os
from dotenv import load_dotenv

load_dotenv()

def valid_api_key(api_key: str = Header(..., alias="Authorization")):
    expected_api_key = os.getenv("API_KEY")
    if api_key != expected_api_key:
        raise HTTPException(status_code=403, detail="Invalid or missing API Token")
    return api_key
