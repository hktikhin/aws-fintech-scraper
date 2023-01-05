from dataclasses import dataclass
from typing import Optional, Union 
from datetime import datetime

@dataclass
class News:
    headline: str
    url: str
    date: Union[str, datetime]
    provider: str
    summary: Optional[str]=None
    source: Optional[str]=None
    symbol: Optional[str]=None
    related: Optional[str]=None
    score: Optional[str]=None
    created_at: Optional[datetime]=None
    