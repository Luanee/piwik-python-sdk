from pydantic import BaseModel

from piwik.schemas.tags.base import TagCreateDraft, TagUpdateDraft


class EcommerceRemoveFromCart(BaseModel):
    pass


class EcommerceRemoveFromCartCreateDraft(TagCreateDraft):
    pass


class EcommerceRemoveFromCartUpdateDraft(TagUpdateDraft):
    pass


class EcommerceProductDetailView(BaseModel):
    pass


class EcommerceProductDetailViewCreateDraft(TagCreateDraft):
    pass


class EcommerceProductDetailViewUpdateDraft(TagUpdateDraft):
    pass


class EcommerceOrder(BaseModel):
    pass


class EcommerceOrderCreateDraft(TagCreateDraft):
    pass


class EcommerceOrderUpdateDraft(TagUpdateDraft):
    pass


class EcommerceCartUpdate(BaseModel):
    pass


class EcommerceCartUpdateCreateDraft(TagCreateDraft):
    pass


class EcommerceCartUpdateUpdateDraft(TagUpdateDraft):
    pass


class EcommerceAddToCart(BaseModel):
    pass


class EcommerceAddToCartCreateDraft(TagCreateDraft):
    pass


class EcommerceAddToCartUpdateDraft(TagUpdateDraft):
    pass
