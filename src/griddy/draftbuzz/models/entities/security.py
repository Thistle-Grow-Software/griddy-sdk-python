"""Security model for DraftBuzz SDK authentication.

Carries bearer-token credentials used by the SDK when making
authenticated requests. DraftBuzz does not currently require auth.
"""

from __future__ import annotations

from typing import Optional

from typing_extensions import Annotated

from ...utils import FieldMetadata, SecurityMetadata
from ..base import DraftBuzzBaseModel


class Security(DraftBuzzBaseModel):
    """Bearer-token authentication model for the DraftBuzz SDK."""

    draftbuzz_auth: Annotated[
        Optional[str],
        FieldMetadata(
            security=SecurityMetadata(
                scheme=True,
                scheme_type="http",
                sub_type="bearer",
                field_name="Authorization",
            )
        ),
    ] = None
