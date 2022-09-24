from dataclasses import dataclass
from typing import Optional

@dataclass
class News:
    headline: str
    summary: str
    url: str
    date: str
    provider: str
    source: Optional[str]=str
    symbol: Optional[str]=None
    related: Optional[str]=None
    score: Optional[str]=None
    