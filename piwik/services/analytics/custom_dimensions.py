import warnings

from piwik.base import BaseService
from piwik.schemas.dimensions import (
    CustomDimension,
    CustomDimensionCreateDraft,
    CustomDimensionSlots,
    CustomDimensionUpdateDraft,
)
from piwik.schemas.page import Page


class CustomDimensionsService(BaseService):
    _endpoint: str = "/api/analytics/v1/manage/custom-dimensions"

    def list(
        self,
        website_id: str,
        page: int = 0,
        size: int = 10,
    ):
        params = {
            "website_id": website_id,
            "limit": size,
            "offset": page * size,
        }

        response = self._client._get(
            self._endpoint,
            params=params,
        )

        if response.status_code == 200:
            return Page[CustomDimension].deserialize(
                response.json(), page=page, size=size
            )
        if response.status_code in (400, 401, 403, 500, 502, 503):
            raise ValueError(f"{str(response.json())}")
            # obj = ErrorResponse.deserialize(response.json())
            # raise self._client._create_exception(obj, response)
        if response.status_code != 404:
            warnings.warn(f"Unhandled status code: {response.status_code}")

        return Page[CustomDimension].deserialize(page=page, size=size)

    def get(self, id: str, website_id: str):
        response = self._client._get(
            f"{self._endpoint}/{id}",
            params={"website_id": website_id},
        )

        if response.status_code == 200:
            return CustomDimension.deserialize(response.json())
        elif response.status_code in (400, 401, 403, 500, 502, 503):
            raise ValueError(response.json())
        elif response.status_code == 404:
            raise ValueError(f"CustomDimension with id: {id} could not be found.")
        else:
            warnings.warn(f"Unhandled status code: {response.status_code}")

    def get_slots(self, website_id: str):
        response = self._client._get(
            f"{self._endpoint}/slots",
            params={"website_id": website_id},
        )

        if response.status_code == 200:
            return CustomDimensionSlots.deserialize(response.json())
        elif response.status_code in (400, 401, 403, 500, 502, 503):
            raise ValueError(response.json())
        elif response.status_code == 404:
            raise ValueError(
                f"CustomDimensionSlots for website with id: {website_id} could not be found."
            )
        else:
            warnings.warn(f"Unhandled status code: {response.status_code}")

    def create(self, draft: CustomDimensionCreateDraft):
        response = self._client._post(
            f"{self._endpoint}",
            json=draft.serialize(),
        )
        if response.status_code == 201:
            return CustomDimension.deserialize(response.json())
        if response.status_code in (400, 401, 403, 500, 502, 503):
            raise ValueError(response.json())

        warnings.warn(f"Unhandled status code: {response.status_code}")

    def delete(self, id: str, website_id: str):
        response = self._client._delete(
            f"{self._endpoint}/{id}",
            params={"website_id": website_id},
        )

        if response.status_code == 204:
            return None
        if response.status_code in (400, 401, 403, 500, 502, 503):
            raise ValueError(response.json())
        if response.status_code == 404:
            raise ValueError(f"CustomDimension with id: {id} could not be found.")

        warnings.warn(f"Unhandled status code: {response.status_code}")

    def update(self, draft: CustomDimensionUpdateDraft):
        response = self._client._patch(
            f"{self._endpoint}/{draft.id}",
            json=draft.serialize(),
        )

        if response.status_code == 204:
            return None
        if response.status_code in (400, 401, 403, 500, 502, 503):
            raise ValueError(response.json())
        if response.status_code == 404:
            raise ValueError(f"CustomDimension with id: {draft.id} could not be found.")

        warnings.warn(f"Unhandled status code: {response.status_code}")
