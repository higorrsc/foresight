from pydantic import BaseModel, ConfigDict, Field


class Currency(BaseModel):
    """
    Immutable currency metadata.
    """

    code: str = Field(min_length=3, max_length=3)
    name: str
    symbol: str
    numeric_code: str = Field(min_length=3, max_length=3)
    decimal_places: int = Field(ge=0)

    model_config = ConfigDict(frozen=True)
