"""DraftBuzz-specific base model with shared validators for HTML-scraped data.

DraftBuzz data comes from HTML scraping, which can produce artifacts like empty
dicts for missing nested objects. This base model provides reusable validators
to handle these common patterns.
"""

from __future__ import annotations

from typing import Any

from pydantic import model_validator

from ...core.types.basemodel import BaseModel


class DraftBuzzBaseModel(BaseModel):
    """Base model for all DraftBuzz entity models.

    Provides a ``before`` model validator that converts empty ``dict``
    values to ``None`` for any ``Optional`` field whose annotation
    includes a model (i.e. nested object) type.  This handles the common
    HTML-scraping artifact where a missing nested object is parsed as
    ``{}`` rather than ``None``.
    """

    @model_validator(mode="before")
    @classmethod
    def _empty_dicts_to_none(cls, data: Any) -> Any:
        """Convert empty dict values to None for optional fields."""
        if not isinstance(data, dict):
            return data

        for field_name, field_info in cls.model_fields.items():
            if field_name not in data:
                continue
            val = data[field_name]
            if isinstance(val, dict) and not val and not field_info.is_required():
                data[field_name] = None

        return data
