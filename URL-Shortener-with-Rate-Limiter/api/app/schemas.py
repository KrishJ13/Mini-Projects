"""
Schemas.py file exists to define the shape of data entering and leaving an API. 
In this file, we use pydantic for the validation
"""

from pydantic import BaseModel, HttpUrl

# Validate the request for shortening a url
class ShortenRequest(BaseModel):
    url : HttpUrl

# Validate the response for shortening a url
class ShortenResponse(BaseModel):
    short_code : str
