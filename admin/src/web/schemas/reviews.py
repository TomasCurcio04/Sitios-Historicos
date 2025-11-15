"""Schemas para el endpoint de reviews"""

from marshmallow import Schema, fields, validate


class ReviewQuerySchema(Schema):
    """Schema para validar parámetros de query del endpoint reviews"""
    
    page = fields.Int(load_default=1, validate=validate.Range(min=1))
    per_page = fields.Int(load_default=25, validate=validate.Range(min=1, max=100))


class ReviewResponseSchema(Schema):
    """Schema para la respuesta de una reseña"""
    
    id = fields.Int()
    user_alias = fields.Str()
    rating = fields.Int()
    comment = fields.Str()
    created_at = fields.Str()


class ReviewsListResponseSchema(Schema):
    """Schema para la respuesta completa del listado de reseñas"""
    
    data = fields.List(fields.Nested(ReviewResponseSchema))
    meta = fields.Dict(keys=fields.Str(), values=fields.Raw())