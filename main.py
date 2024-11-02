from lib.strava_client import StravaClient, StravaConfig
from os import environ

def main():
    config = StravaConfig(
        environ.get("CLIENT_ID"),
        environ.get("CLIENT_SECRET"),
        environ.get("REFRESH_TOKEN")
    )
    client = StravaClient(config)
    client.establish_connection()
    activities = client.get_all_activities()
    print(f"number of activities: {len(activities)}")

if __name__ == "__main__":
    main()