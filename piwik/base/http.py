from requests_oauthlib import OAuth2Session
from urllib3 import Retry
from requests.adapters import HTTPAdapter


class RefreshingOAuth2Session(OAuth2Session):
    def refresh_token(self, token_url, **kwargs):
        kwargs.update(self.auto_refresh_kwargs)
        kwargs.pop("grant_type")
        return self.fetch_token(token_url, **kwargs)


class RetryHttpAdapter(HTTPAdapter):
    max_retries_on_connection: int = 3
    max_retries_on_bad_status: int = 3
    force_retries_on_status: list[int] = [502, 503, 504]

    def __init__(self):
        retry = Retry(
            status=self.max_retries_on_bad_status,
            connect=self.max_retries_on_connection,
            status_forcelist=self.force_retries_on_status,
        )
        super().__init__(max_retries=retry)
