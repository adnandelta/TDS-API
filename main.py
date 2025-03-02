from fastapi import FastAPI, Request, HTTPException
import httpx

app = FastAPI()

@app.get("/api")
async def proxy(url: str, request: Request):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            response.raise_for_status()  # Raise error for bad responses
            
        headers = {"Access-Control-Allow-Origin": "*"}
        return response.json() if "application/json" in response.headers.get("content-type", "") else response.text
    except httpx.RequestError as e:
        raise HTTPException(status_code=500, detail=f"Request error: {str(e)}")
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=f"HTTP error: {str(e)}")
