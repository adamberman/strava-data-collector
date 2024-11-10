from typing import List
from lib.strava_client import StravaActivity

class StravaAnalysis():
    def __init__(self, activities: List[StravaActivity]) -> None:
        self.activities = activities
        self.do_analysis()

    def do_analysis(self) -> None:
        self.snow = 0
        self.biking = 0
        self.running = 0
        self.weights = 0
        for activity in self.activities:
            if activity.sport_type == "WeightTraining":
                self.weights += 1
            elif activity.sport_type in ["Snowshoe", "NordicSki"]:
                self.snow += 1
            elif activity.sport_type == "Ride":
                self.biking += 1
            elif activity.sport_type == "Run":
                self.running += 1
