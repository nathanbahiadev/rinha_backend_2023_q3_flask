import json

from redis import Redis

from configs.settings import Settings


class Cache:
    def __init__(self) -> None:
        self.instance = Redis.from_url(Settings.REDIS_URI)

    def get(self, key: str) -> dict | None:
        if data := self.instance.get(key):
            return json.loads(data)
        
    def set(self, key: str, data: dict) -> None:
        self.instance.set(key, json.dumps(data))
