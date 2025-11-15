"""Schemas para el endpoint de sites"""

from marshmallow import Schema, fields, validate


class SiteQuerySchema(Schema):
    """Schema para validar parámetros de query del endpoint sites"""
    
    name = fields.Str(missing=None)
    description = fields.Str(missing=None)
    city = fields.Str(missing=None)
    province = fields.Str(missing=None)
    tags = fields.Str(missing=None)
    conservation_state = fields.Str(missing=None)
    search = fields.Str(missing=None)
    
    order_by = fields.Str(
        missing=None,
        validate=validate.OneOf(['rating-5-1', 'rating-1-5', 'latest', 'oldest', 'name-asc', 'name-desc'])
    )
    
    lat = fields.Float(missing=None, validate=validate.Range(min=-90, max=90))
    long = fields.Float(missing=None, validate=validate.Range(min=-180, max=180))
    radius = fields.Float(missing=None, validate=validate.Range(min=0))
    
    page = fields.Int(missing=1, validate=validate.Range(min=1))
    per_page = fields.Int(missing=20, validate=validate.Range(min=1, max=100))


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
    inserted_at = fields.Str(allow_none=True)
    updated_at = fields.Str(allow_none=True)


class SitesListResponseSchema(Schema):
    """Schema para la respuesta completa del listado de sites"""
    
    data = fields.List(fields.Nested(SiteResponseSchema))
    meta = fields.Dict(keys=fields.Str(), values=fields.Raw())