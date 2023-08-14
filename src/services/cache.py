import json
from typing import Any

from redis import Redis

from configs.settings import Settings


class RedisCache:
    def __init__(self) -> None:
        self.instance = Redis.from_url(Settings.REDIS_URI)

    def get(self, key: str) -> Any | None:
        if data := self.instance.get(key):
            return json.loads(data)
        
    def set(self, key: str, data: Any) -> None:
        self.instance.set(key, json.dumps(data), 60)
