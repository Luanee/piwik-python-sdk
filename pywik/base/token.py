import threading
from typing import Any, Protocol

tls = threading.local()


class BaseTokenStorage(Protocol):
    def get_token(self, client_id: str) -> Any: ...

    def add_token(self, client_id: str, token: Any): ...

    def create_token_hash(self, client_id: str): ...


class DefaultTokenStorage(BaseTokenStorage):
    @property
    def storage(self):
        items = getattr(tls, "tokens", None)
        if items is None:
            items = {}
            setattr(tls, "tokens", items)
        return items

    def add_token(self, client_id: str, token: Any):
        name = self.create_token_hash(client_id)
        self.storage[name] = token

    def get_token(self, client_id: str):
        name = self.create_token_hash(client_id)
        return self.storage.get(name)

    def create_token_hash(self, client_id: str):
        return f"{client_id}"

    @classmethod
    def clear_cache(cls):
        items = getattr(tls, "tokens", {})
        items.clear()
