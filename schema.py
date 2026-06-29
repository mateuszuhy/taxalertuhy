from dataclasses import dataclass


@dataclass
class TaxItem:
    title: str
    what_changed: str
    impact: str
    legal_basis: str
    source: str = ""
    url: str = ""
