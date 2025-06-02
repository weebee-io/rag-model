# model-service/app/middleware/logging_middleware.py

import time
import json
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
from app.core.logger import qa_logger, news_logger, hint_logger, general_logger

class RequestResponseLoggerMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        path = request.url.path

        if path.startswith("/api/qa"):
            current_logger = qa_logger
        elif path.startswith("/api/news"):
            current_logger = news_logger
        elif path.startswith("/api/hint"):
            current_logger = hint_logger
        else:
            current_logger = general_logger

        client_ip = request.client.host if request.client else "unknown"
        try:
            body_bytes = await request.body()
            body_str = body_bytes.decode("utf-8") if body_bytes else ""
        except Exception:
            body_str = "<failed to read request body>"
        query_params = dict(request.query_params)

        current_logger.info(
            json.dumps(
                {
                    "type": "request",
                    "path": path,
                    "method": request.method,
                    "client_ip": client_ip,
                    "query_params": query_params,
                    "body": body_str,
                },
                ensure_ascii=False,
            )
        )

        response: Response = await call_next(request)

        resp_body_bytes = b""
        async for chunk in response.body_iterator:
            resp_body_bytes += chunk
        try:
            resp_text = resp_body_bytes.decode("utf-8")
        except Exception:
            resp_text = "<binary or non-utf8 response>"

        process_time = round(time.time() - start_time, 4)

        current_logger.info(
            json.dumps(
                {
                    "type": "response",
                    "path": path,
                    "method": request.method,
                    "status_code": response.status_code,
                    "process_time_sec": process_time,
                    "response_body": resp_text,
                },
                ensure_ascii=False,
            )
        )

        return Response(
            content=resp_body_bytes,
            status_code=response.status_code,
            headers=dict(response.headers),
            media_type=response.media_type,
        )
