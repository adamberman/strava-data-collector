from lib.strava_client import StravaClient, StravaConfig
from os import environ
import boto3
import json

def main():
    config = StravaConfig(
        environ.get("CLIENT_ID"),
        environ.get("CLIENT_SECRET"),
        environ.get("REFRESH_TOKEN")
    )
    client = StravaClient(config)
    print("connecting to strava")
    client.establish_connection()
    print("getting activities")
    activities = client.get_all_activities()
    print("sending to aws")
    client = boto3.client(
        "lambda",
        region_name='us-east-2',
    )
    client.invoke(
        FunctionName="arn:aws:lambda:us-east-2:651706778051:function:strava-database-insert",
        Payload=json.dumps([a.to_dict for a in activities])
    )
    print("done")

if __name__ == "__main__":
    main()