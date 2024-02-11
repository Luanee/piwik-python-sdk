import pytest

from piwik.base.token import DefaultTokenStorage


def test_token_storage():
    token_storage = DefaultTokenStorage()
    TOKEN = "token"

    assert len(token_storage.storage) == 0

    token_storage.add_token("client_id_1", TOKEN)

    assert len(token_storage.storage) == 1

    token = token_storage.get_token("client_id_1")

    assert token == TOKEN

    token_storage.clear_cache()
    print(token_storage.storage)
    assert len(token_storage.storage) == 0
