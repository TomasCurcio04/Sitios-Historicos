"""Schemas para el endpoint de sites"""

from marshmallow import Schema, fields, validate


class SiteQuerySchema(Schema):
    """Schema para validar parámetros de query del endpoint sites"""
    
    name = fields.Str(load_default=None)
    description = fields.Str(load_default=None)
    city = fields.Str(load_default=None)
    province = fields.Str(load_default=None)
    tags = fields.Str(load_default=None)
    conservation_state = fields.Str(load_default=None)
    search = fields.Str(load_default=None)
    
    order_by = fields.Str(
        load_default=None,
        validate=validate.OneOf(['rating-5-1', 'rating-1-5', 'latest', 'oldest', 'name-asc', 'name-desc'])
    )
    
    lat = fields.Float(load_default=None, validate=validate.Range(min=-90, max=90))
    long = fields.Float(load_default=None, validate=validate.Range(min=-180, max=180))
    radius = fields.Float(load_default=None, validate=validate.Range(min=0))
    
    page = fields.Int(load_default=1, validate=validate.Range(min=1))
    per_page = fields.Int(load_default=20, validate=validate.Range(min=1, max=100))


class SiteResponseSchema(Schema):
    """Schema para la respuesta del endpoint sites"""
    
    id = fields.Int()
    name = fields.Str()
    short_description = fields.Str()
    description = fields.Str()
    city = fields.Str()
    province = fields.Str()
    country = fields.Str()
    lat = fields.Float(allow_none=True)
    long = fields.Float(allow_none=True)
    tags = fields.List(fields.Str())
    state_of_conservation = fields.Str(allow_none=True)
    cover_image = fields.Str(allow_none=True)
    images = fields.List(fields.Dict(), allow_none=True)
    average_rating = fields.Float(allow_none=True)
    review_count = fields.Int()
    inserted_at = fields.Str(allow_none=True)
    updated_at = fields.Str(allow_none=True)


class SitesListResponseSchema(Schema):
    """Schema para la respuesta completa del listado de sites"""
    
    data = fields.List(fields.Nested(SiteResponseSchema))
    meta = fields.Dict(keys=fields.Str(), values=fields.Raw())