# Moltclawdbot fork app: Google-Sheets-shaped spreadsheet storage.
from datetime import datetime
from typing import ClassVar

from inflection import tableize
from pydantic import EmailStr
from sqlalchemy.future.engine import Engine as SQLEngine
from sqlalchemy.orm import registry

from appworld.apps.model_lib import Database as _Database
from appworld.apps.model_lib import DBChangesTracker, Field
from appworld.apps.model_lib import SQLModel as _SQLModel
from appworld.common.datetime import DateTime


class Database(_Database):
    engine: SQLEngine
    tracker: DBChangesTracker


class SQLModel(_SQLModel, registry=registry()):
    app_name: ClassVar[str] = "sheets"
    db: ClassVar[type[_Database]] = Database


@SQLModel.register("User")
class User(SQLModel, table=True):
    table_name: ClassVar[str] = tableize("User")

    id: int | None = Field(None, primary_key=True)
    first_name: str = Field(..., description="Your first name.", min_length=1)
    last_name: str = Field(..., description="Your last name.", min_length=1)
    email: EmailStr = Field(..., description="Your email address.")
    password: str = Field(..., description="Your password.", min_length=5)
    created_at: datetime = Field(
        datetime=True,
        default_factory=DateTime.now,
        description="The date and time the account was created.",
    )

    unique_by: ClassVar[list[tuple[str, ...]]] = [("email",)]
    has_one: ClassVar[tuple[str, ...]] = ()
    has_many: ClassVar[tuple[str, ...]] = ("spreadsheets",)


@SQLModel.register("Spreadsheet")
class Spreadsheet(SQLModel, table=True):
    table_name: ClassVar[str] = tableize("Spreadsheet")

    id: int | None = Field(None, primary_key=True)
    user_id: int = Field(
        ..., description="ID of the user who owns the spreadsheet.", foreign_key="user.id"
    )
    title: str = Field(..., description="Title of the spreadsheet.", min_length=1)
    created_at: datetime = Field(
        datetime=True,
        default_factory=DateTime.now,
        description="The date and time the spreadsheet was created.",
    )
    updated_at: datetime = Field(
        datetime=True,
        default_factory=DateTime.now,
        description="The date and time the spreadsheet was last updated.",
    )

    unique_by: ClassVar[list[tuple[str, ...]]] = [("user_id", "title")]
    has_one: ClassVar[tuple[str, ...]] = ("user",)
    has_many: ClassVar[tuple[str, ...]] = ("sheets",)


@SQLModel.register("Sheet")
class Sheet(SQLModel, table=True):
    table_name: ClassVar[str] = tableize("Sheet")

    id: int | None = Field(None, primary_key=True)
    spreadsheet_id: int = Field(
        ...,
        description="ID of the spreadsheet this sheet (tab) belongs to.",
        foreign_key="spreadsheet.id",
    )
    title: str = Field(..., description="Title of the sheet (tab).", min_length=1)
    index: int = Field(0, description="Zero-based position of the tab.", ge=0)

    unique_by: ClassVar[list[tuple[str, ...]]] = [("spreadsheet_id", "title")]
    has_one: ClassVar[tuple[str, ...]] = ("spreadsheet",)
    has_many: ClassVar[tuple[str, ...]] = ("cells",)


@SQLModel.register("Cell")
class Cell(SQLModel, table=True):
    table_name: ClassVar[str] = tableize("Cell")

    id: int | None = Field(None, primary_key=True)
    sheet_id: int = Field(
        ..., description="ID of the sheet this cell belongs to.", foreign_key="sheet.id"
    )
    row: int = Field(..., description="One-based row number.", ge=1)
    col: int = Field(..., description="One-based column number.", ge=1)
    value: str = Field("", description="Cell value as entered (string-typed).")

    unique_by: ClassVar[list[tuple[str, ...]]] = [("sheet_id", "row", "col")]
    has_one: ClassVar[tuple[str, ...]] = ("sheet",)
    has_many: ClassVar[tuple[str, ...]] = ()
