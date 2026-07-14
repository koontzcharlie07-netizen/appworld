# Moltclawdbot fork app: Strava-shaped activity storage.
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
    app_name: ClassVar[str] = "strava"
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
    has_many: ClassVar[tuple[str, ...]] = ("activities",)


@SQLModel.register("Activity")
class Activity(SQLModel, table=True):
    table_name: ClassVar[str] = tableize("Activity")

    id: int | None = Field(None, primary_key=True)
    user_id: int = Field(
        ..., description="ID of the athlete who recorded the activity.", foreign_key="user.id"
    )
    name: str = Field(..., description="Name of the activity.", min_length=1)
    sport_type: str = Field(..., description="Sport type, e.g. Run or Ride.", min_length=1)
    distance: float = Field(..., description="Distance in meters.", ge=0)
    moving_time: int = Field(..., description="Moving time in seconds.", ge=0)
    elapsed_time: int = Field(..., description="Elapsed time in seconds.", ge=0)
    total_elevation_gain: float = Field(0, description="Elevation gain in meters.", ge=0)
    start_date: datetime = Field(
        datetime=True,
        default_factory=DateTime.now,
        description="Start date and time of the activity.",
    )
    average_speed: float = Field(0, description="Average speed in meters/second.", ge=0)

    unique_by: ClassVar[list[tuple[str, ...]]] = []
    has_one: ClassVar[tuple[str, ...]] = ("user",)
    has_many: ClassVar[tuple[str, ...]] = ()
