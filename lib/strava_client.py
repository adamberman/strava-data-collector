from __future__ import annotations
from typing import List
import requests

class StravaConfig():
    def __init__(self, client_id, client_secret, refresh_token) -> None:
        self.client_id = client_id
        self.client_secret = client_secret
        self.refresh_token = refresh_token

class StravaActivity():
    def from_json(json_blob) -> StravaActivity:
        return StravaActivity(
            json_blob["name"],
            json_blob["distance"],
            json_blob["moving_time"],
            json_blob["elapsed_time"],
            json_blob["total_elevation_gain"],
            json_blob["sport_type"],
            json_blob["id"],
            json_blob["start_date"],
            json_blob["start_date_local"],
            json_blob["utc_offset"],
            json_blob["average_speed"],
            json_blob["max_speed"],
            json_blob["has_heartrate"],
            json_blob["average_heartrate"],
            json_blob["max_heartrate"],
            json_blob["suffer_score"],
        )

    def __init__(self,
        name: str,
        distance: float,
        moving_time: int,
        elapsed_time: int,
        total_elevation_gain: float,
        sport_type: str,
        id: int,
        start_date: str,
        start_date_local: str,
        utc_offset: str,
        average_speed: float,
        max_speed: float,
        has_heartrate: bool,
        average_heartrate: float,
        max_heartrate: float,
        suffer_score: float,
    ) -> None:
        self.name = name
        self.distance = str(distance)
        self.moving_time = str(moving_time)
        self.elapsed_time = str(elapsed_time)
        self.total_elevation_gain = str(total_elevation_gain)
        self.sport_type = sport_type
        self.id = id
        self.start_date = start_date
        self.start_date_local = start_date_local
        self.utc_offset = utc_offset
        self.average_speed = str(average_speed)
        self.max_speed = str(max_speed)
        self.has_heartrate = has_heartrate
        self.average_heartrate = str(average_heartrate)
        self.max_heartrate = str(max_heartrate)
        self.suffer_score = str(suffer_score)

    def to_dict(self) -> dict:
        return self.__dict__

class StravaClient():
    def __init__(self, config: StravaConfig) -> None:
        self.config = config

    def establish_connection(self) -> None:
        response = requests.post(
            "https://www.strava.com/api/v3/oauth/token",
            data = {
                "client_id": self.config.client_id,
                "refresh_token": self.config.refresh_token,
                "client_secret": self.config.client_secret,
                "scope": "activity:read_all",
                "grant_type": "refresh_token",
                "f": "json",
            }
        )
        self.access_token = response.json()["access_token"]

    def get_all_activities(self) -> List[StravaActivity]:
        current = []
        page = 1
        next_activities = self.get_activities(page)
        while len(next_activities) > 0:
            current += next_activities
            page += 1
            next_activities = self.get_activities(page)
        return current

    def get_activities(self, page: int) -> List[StravaActivity]:
        if not self.access_token:
            return []
        response = requests.get(
            "https://www.strava.com/api/v3/athlete/activities",
            headers={
                "Authorization": f"Bearer {self.access_token}",
            },
            params={
                "per_page": "100",
                "after": 1727740800,
                "page": page,
            }
        )
        return [StravaActivity.from_json(i) for i in response.json()]