"""Schemas para el endpoint de reviews"""

from marshmallow import Schema, fields, validate


class ReviewQuerySchema(Schema):
    """Schema para validar parámetros de query del endpoint reviews"""

    page = fields.Int(load_default=1, validate=validate.Range(min=1))
    per_page = fields.Int(load_default=10, validate=validate.Range(min=1, max=100))


class ReviewResponseSchema(Schema):
    """Schema para la respuesta de una reseña"""

    id = fields.Int()
    site_id = fields.Int()
    public_user_id = fields.Int()
    rating = fields.Int()
    comment = fields.Str()
    inserted_at = fields.Str()
    updated_at = fields.Str()


class ReviewCreateSchema(Schema):
    """Schema para crear una nueva reseña"""

    rating = fields.Int(required=True, validate=validate.OneOf([1, 2, 3, 4, 5]))
    site_id = fields.Int(load_default=None)  # Opcional, se ignora (viene de URL)
    comment = fields.Str(
        load_default="", validate=validate.Length(min=0)
    )  # Opcional según schema


class ReviewsListResponseSchema(Schema):
    """Schema para la respuesta completa del listado de reseñas"""

    data = fields.List(fields.Nested(ReviewResponseSchema))
    meta = fields.Dict(keys=fields.Str(), values=fields.Raw())
