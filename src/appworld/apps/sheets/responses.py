# Moltclawdbot fork app: response models for the sheets app.
from datetime import datetime

from pydantic import EmailStr, constr

from appworld.apps.response_lib import ResponseModel as _ResponseModel


class ResponseModel(_ResponseModel):
    pass


@ResponseModel.register("User:default")
class UserResponse(ResponseModel):
    first_name: constr(min_length=1)
    last_name: constr(min_length=1)
    email: EmailStr
    registered_at: datetime
    last_logged_in: datetime
    verified: bool


@ResponseModel.register("User:shortened")
class ShortenedUserResponse(ResponseModel):
    first_name: constr(min_length=1)
    last_name: constr(min_length=1)
    email: EmailStr
    registered_at: datetime


@ResponseModel.register("Spreadsheet:shortened")
class SpreadsheetShortenedResponse(ResponseModel):
    spreadsheet_id: int
    title: constr(min_length=1)
    num_sheets: int
    created_at: datetime
    updated_at: datetime


@ResponseModel.register("Spreadsheet:default")
class SpreadsheetResponse(ResponseModel):
    spreadsheet_id: int
    title: constr(min_length=1)
    created_at: datetime
    updated_at: datetime
    sheets: list[dict]


@ResponseModel.register("Sheet:default")
class SheetResponse(ResponseModel):
    sheet_id: int
    spreadsheet_id: int
    title: constr(min_length=1)
    index: int
    num_rows: int
    num_cols: int
    cells: list[dict]
    grid: list[list[str]]


@ResponseModel.register("message-spreadsheet_id")
class MessageSpreadsheetIdResponse(ResponseModel):
    message: str
    spreadsheet_id: int
    sheet_ids: list[int]


@ResponseModel.register("message-sheet_id")
class MessageSheetIdResponse(ResponseModel):
    message: str
    sheet_id: int


@ResponseModel.register("message-row")
class MessageRowResponse(ResponseModel):
    message: str
    row: int
