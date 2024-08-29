from piwik.schemas.product_custom_dimensions import ProductCustomDimensionCreateDraft, ProductCustomDimensionUpdateDraft

RESPONSE_DATA_PRODUCT_CUSTOM_DIMENSION = {
    "data": {
        "type": "ProductCustomDimension",
        "id": "id",
        "attributes": {
            "website_id": "website_id",
            "name": "Product package height in mm",
            "slot": 1,
            "updated_at": "2017-07-14T08:33:53.215948Z",
            "created_at": "2017-07-14T08:33:53.215948Z",
        },
    }
}

PRODUCT_CUSTOM_DIMENSION_CREATE_DRAFT = ProductCustomDimensionCreateDraft(
    name="Product package height in mm",
    website_id="website_id",
    slot=1,
)


PRODUCT_CUSTOM_DIMENSION_UPDATE_DRAFT = ProductCustomDimensionUpdateDraft(
    id="id",
    name="Product package height in mm",
    website_id="website_id",
    slot=1,
)
