import time
import uuid

from fastapi import FastAPI, HTTPException, Request
from loguru import logger

app = FastAPI()


@app.middleware("http")
async def log_request_middleware(request: Request, call_next):
    request_id = str(uuid.uuid4())[:8]

    with logger.contextualize(request_id=request_id):
        logger.info("Incoming request {} {}", request.method, request.url.path)
        try:
            start_time = time.time()

            response = await call_next(request)

            process_time = (start_time - time.time()) * 1000
            logger.info(
                "Request completed in {:.2f}ms with status code {}",
                process_time,
                response.status_code,
            )

            response.headers["X-Request-ID"] = request_id
            return response
        except HTTPException:
            raise
        except Exception:
            logger.exception("Request failed while {} {}", request.method, request.url.path)
            raise
