# Moltclawdbot fork app: response models for the strava app.
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


@ResponseModel.register("Activity:shortened")
class ActivityShortenedResponse(ResponseModel):
    activity_id: int
    name: constr(min_length=1)
    sport_type: constr(min_length=1)
    distance: float
    moving_time: int
    start_date: datetime


@ResponseModel.register("Activity:default")
class ActivityResponse(ResponseModel):
    activity_id: int
    name: constr(min_length=1)
    sport_type: constr(min_length=1)
    distance: float
    moving_time: int
    elapsed_time: int
    total_elevation_gain: float
    start_date: datetime
    average_speed: float


@ResponseModel.register("message-activity_id")
class MessageActivityIdResponse(ResponseModel):
    message: str
    activity_id: int
