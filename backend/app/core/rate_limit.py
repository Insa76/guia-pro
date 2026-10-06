import time
from threading import Lock


class RateLimiter:
    def __init__(
        self,
        max_attempts: int,
        window_seconds: int,
    ):
        self.max_attempts = max_attempts
        self.window_seconds = window_seconds
        self._attempts: dict[str, list[float]] = {}
        self._lock = Lock()

    def is_allowed(self, key: str) -> bool:
        now = time.time()

        with self._lock:
            attempts = self._attempts.get(key, [])

            attempts = [
                timestamp
                for timestamp in attempts
                if now - timestamp < self.window_seconds
            ]

            if len(attempts) >= self.max_attempts:
                self._attempts[key] = attempts
                return False

            attempts.append(now)
            self._attempts[key] = attempts

            return True

    def reset(self, key: str) -> None:
        with self._lock:
            self._attempts.pop(key, None)


admin_login_limiter = RateLimiter(
    max_attempts=5,
    window_seconds=15 * 60,
)


professional_login_limiter = RateLimiter(
    max_attempts=5,
    window_seconds=15 * 60,
)


public_review_limiter = RateLimiter(
    max_attempts=10,
    window_seconds=15 * 60,
)

public_registration_limiter = RateLimiter(
    max_attempts=5,
    window_seconds=15 * 60,
)