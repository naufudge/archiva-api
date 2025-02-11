from pydantic import BaseModel
from typing import Optional, List, Dict
from datetime import datetime


class Dhuvas(BaseModel):
    id: Optional[str] = None
    day: Optional[int] = None
    month: Optional[int] = None
    year: Optional[int] = None
    detail: Optional[str] = None
    source: Optional[str] = None


class PaymentVoucher(BaseModel):
    pvNum: str
    businessArea: int
    agency: str
    vendor: str
    date: datetime | str
    notes: str
    currency: str
    exchangeRate: float | int
    invoiceDetails: List[Dict[str, str | int | datetime | float | List[Dict[str, float | str]] | None]]
    preparedBy: Dict[str, str]
    verifiedBy: Dict[str, Optional[str]]
    authorisedByOne: Dict[str, Optional[str]]
    authorisedByTwo: Dict[str, Optional[str]]

    poNum: Optional[str] = None
    paymentMethod: str
    parkedDate: Optional[datetime] = None
    postingDate: Optional[datetime] = None
    clearingDoc: Dict[str, str | datetime | None]
    transferNum: Optional[str] = None


class Staff(BaseModel):
    _id: Optional[str] = None
    name: str
    designation: str