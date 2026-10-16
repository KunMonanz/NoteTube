import asyncio
import time

from fastapi import HTTPException, Request, status
from slowapi.util import get_remote_address


class TokenBucketLimiter:
    def __init__(self, tokens: int, fill_rate: float):
        self.capacity = tokens
        self.fill_rate = fill_rate
        self.tokens = tokens
        self.last_check = time.monotonic()
        self.lock = asyncio.Lock()

    async def consume(self, tokens_to_consume: int = 1) -> bool:
        async with self.lock:
            now = time.monotonic()
            elapsed = now - self.last_check
            self.last_check = now

            self.tokens = min(self.capacity, self.tokens + (elapsed * self.fill_rate))

            if self.tokens >= tokens_to_consume:
                self.tokens -= tokens_to_consume
                return True
            return False


USER_BUCKETS: dict[str, TokenBucketLimiter] = {}


async def check_ip_rate_limit(request: Request):
    """Extracts client IP and enforces their personal daily token limit."""
    ip_address = get_remote_address(request)

    if ip_address not in USER_BUCKETS:
        USER_BUCKETS[ip_address] = TokenBucketLimiter(tokens=10, fill_rate=10 / 86400)

    bucket = USER_BUCKETS[ip_address]

    if not await bucket.consume(1):
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Rate limit exceeded. You are limited to 10 transcriptions per day.",
        )
