from pydantic import BaseModel, ConfigDict


class Schema(BaseModel):
    """Base for every schema in the app.

    - extra="forbid": typos in field names fail loudly instead of being dropped
    - frozen=True:    results are immutable once built (safe to share/cache)
    - str_strip_whitespace: trims every incoming string
    """

    model_config = ConfigDict(
        extra="forbid",
        frozen=True,
        str_strip_whitespace=True,
    )
