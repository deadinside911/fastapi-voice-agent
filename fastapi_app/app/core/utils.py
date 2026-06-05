import time

from fastapi import Request

from core.database import async_session_factory
from core.models import PerformanceAnalyticsRecord


async def logging_data_middleware(request: Request, call_next):
    """
    """
    
    start_time = time.perf_counter()
    x_forwarded_for = request.headers.get("x-forwarded-for")

    client_ip = ""
    if x_forwarded_for:
       client_ip = x_forwarded_for.split(",")[0].strip()
    else:
        if request.client:
            client_ip = request.client.host
        else:
            client_ip = "Unknown" 

    response = await call_next(request)

    process_time = time.perf_counter() - start_time

    performance_log = PerformanceAnalyticsRecord(client_ip=client_ip, processing_time=process_time)
    
    async with async_session_factory() as session:
        try:
            session.add(performance_log)
            await session.commit()
            print("logged")
        except Exception as e:
            print(f"Exception {e}, failed to log")
            await session.rollback()

    return response
