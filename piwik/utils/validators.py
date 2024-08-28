import requests


def validate_response(response: requests.Response) -> None:
    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError as exc:
        error = response.json()
        if response.status_code == 400:
            raise ValueError(f"Bad Request for url: {response.url}", error) from exc
        raise exc
