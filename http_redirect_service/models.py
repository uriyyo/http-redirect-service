from typing import Annotated

from annotated_types import Gt, Len
from pydantic import Field, StringConstraints

Domain = Annotated[
    str,
    # TODO: simplify regex, maybe it's better to find smth better
    StringConstraints(pattern=r"^(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+[a-z0-9][a-z0-9-]{0,61}[a-z0-9]$"),
    Field(examples=["domain-a.xyz", "domain-b.xyz"]),
]
DomainWeight = Annotated[
    int,
    Gt(0),
    Field(examples=[0, 1, 5, 10]),
]
PoolDomains = Annotated[
    dict[Domain, DomainWeight],
    Len(min_length=1),
    Field(examples=[{"domain-a.xyz": 2, "domain-b.xyz": 1}]),
]
PoolID = Annotated[
    str,
    Len(1, 256),
    Field(examples=["pool-1", "pool-2"]),
]

__all__ = [
    "Domain",
    "DomainWeight",
    "PoolDomains",
    "PoolID",
]
