from dataclasses import dataclass
from dataclasses_json import dataclass_json

@dataclass_json
@dataclass
class BaseApiResponse:
    """Base Api Response class represent root api response

    Attributes
    ----------
    ok : bool
        response status ok
    data: any
        data payload api response
    message: str
        api response message
    """
    ok: bool
    data: any
    message: str
