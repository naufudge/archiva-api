from typing import TypedDict, List, Optional
from datetime import datetime


class GLDetail(TypedDict):
    code: int
    fund: str
    amount: float

class Invoice(TypedDict):
    comments: str
    documentNum: Optional[str]
    invoiceNumber: str
    invoiceDate: Optional[str | datetime]
    invoiceTotal: float
    glDetails: List[GLDetail]

class Staff(TypedDict):
    name: Optional[str]
    designation: Optional[str]

class ClearingDoc(TypedDict):
    num: Optional[int]
    date: Optional[datetime]

class PV(TypedDict):
    pvNum: int
    businessArea: str
    agency: str
    vendor: str
    date: datetime | str
    notes: str
    currency: str
    exchangeRate: float | int
    invoiceDetails: List[Invoice]
    preparedBy: Staff
    verifiedBy: Staff
    authorisedByOne: Staff
    authorisedByTwo: Staff

    poNum: Optional[str] = None
    paymentMethod: Optional[str]
    parkedDate: Optional[datetime] = None
    postingDate: Optional[datetime] = None
    clearingDoc: ClearingDoc
    transferNum: Optional[str] = None
