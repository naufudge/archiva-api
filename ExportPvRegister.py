import traceback
from io import BytesIO
from typing import List
from datetime import datetime
from DB.models import PV

# Optional dependency: pandas
try:
    import pandas as pd
except Exception:
    pd = None


# def convert_to_datetime(date_str: str) -> datetime:
#     """Convert an ISO 8601 UTC date string to a datetime object."""
#     return datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S.%fZ").replace(tzinfo=timezone.utc)

def convert_to_datetime(date_str: str) -> datetime:
    """Convert an ISO 8601 UTC date string to DD.MM.YYYY format."""
    dt = datetime.fromisoformat(date_str)  # Parse the input string
    return dt.strftime("%d.%m.%Y")  # Format as DD.MM.YYYY

class ExportPvRegister:
    def __init__(self, pv_no_delimiter: str = "/"):
        self.pv_no_delimiter = pv_no_delimiter

        # Define column name mappings
        self.COLUMN_MAPPING = {
            "pvNum": "Voucher No",
            "vendor": "Vendor",
            "date": "Date",
            "details": "Details",
            "documentNum": "Document No",
            "invoiceNumber": "Invoice / Ref No",
            "code": "GL Code",
            "total": "Total",
            "poNum": "Po No",
            "paymentMethod": "Payment Method C/FT/LT",
            "parkedDate": "Parked Date",
            "postingDate": "Posting Date",
            "clearingDocNum": "Clearing Document No",
            "clearingDocDate": "Clearing Document Date",
            "transferNum": "Local Transfer No / Cheque No",
        }

        # Define column order for the final output
        self.COLUMN_ORDER = ["Date", "Voucher No", "Document No", "Po No", "Invoice / Ref No", "Vendor", "Details", "GL Code", "Total", "Parked Date", "Posting Date", "Payment Method C/FT/LT", "Clearing Document Date", "Clearing Document No", "Local Transfer No / Cheque No"]

    def export_to_excel(self, pvs: List[PV]):
        """Export PVs data into an excel file."""
        final: List[List[PV]] = []
        for pv in pvs:
            date = pv["date"]
            parkedDate = pv["parkedDate"]
            postingDate = pv["postingDate"]
            clearingDocDate = pv["clearingDoc"]["date"]

            if isinstance(date, str):
                date = convert_to_datetime(date)
            if isinstance(parkedDate, str):
                parkedDate = convert_to_datetime(parkedDate)
            if isinstance(postingDate, str):
                postingDate = convert_to_datetime(postingDate)
            if isinstance(clearingDocDate, str):
                clearingDocDate = convert_to_datetime(clearingDocDate)

            invoices = pv["invoiceDetails"]
            for invoice in invoices:
                # Convert invoice number to integer if possible
                try:
                    invoiceNumber = str(invoice["invoiceNumber"])
                except:
                    invoiceNumber = invoice["invoiceNumber"] if invoice["invoiceNumber"] else ""
                
                # Convert Document number to integer if possible
                try:
                    documentNum = str(invoice["documentNum"])
                except:
                    documentNum = invoice["documentNum"] if invoice["documentNum"] else ""

                glDetails = invoice["glDetails"]
                for gl in glDetails:
                    try:
                        result = {
                            "date": date,
                            "pvNum": f"1506{self.pv_no_delimiter}{pv['pvNum'].replace('-', self.pv_no_delimiter)}",
                            "documentNum": documentNum,
                            "poNum": pv["poNum"],
                            "invoiceNumber": invoiceNumber,
                            "vendor": pv["vendor"],
                            "details": invoice["comments"],
                            "code": gl["code"],
                            "total": gl["amount"],
                            "parkedDate": parkedDate if parkedDate else "",
                            "postingDate": postingDate if postingDate else "",
                            "paymentMethod": pv["paymentMethod"],
                            "clearingDocDate": clearingDocDate if clearingDocDate else "",
                            "clearingDocNum": pv["clearingDoc"]["num"],
                            "transferNum": pv["transferNum"]
                        }
                        final.append(result)
                    except KeyError:
                        print(traceback.print_exc())
                        print(pv["pvNum"])
        
        if pd is None:
            # If pandas is not available, return a small empty excel to avoid crashing
            output = BytesIO()
            output.write(b"")
            output.seek(0)
            return output

        df = pd.DataFrame(final)
        if not df.empty:
            df.rename(columns=self.COLUMN_MAPPING, inplace=True)
            df = df[self.COLUMN_ORDER]

        output = BytesIO()
        with pd.ExcelWriter(output, engine="openpyxl") as writer:
            df.to_excel(writer, index=False, sheet_name="PV Register")
        
        output.seek(0)

        return output

