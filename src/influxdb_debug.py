from featurestoresdk.feature_store_sdk import FeatureStoreSdk
from influxdb_client import InfluxDBClient
import os

INFLUXDB_HOST = os.getenv('INFLUXDB_HOST')
INFLUXDB_PORT = os.getenv('INFLUXDB_PORT')

INFLUXDB_TOKEN = os.getenv('INFLUXDB_TOKEN')
INFLUXDB_ORG = os.getenv('INFLUXDB_ORG', 'primary')

fs_sdk = FeatureStoreSdk()

def debug_influxdb(fs_sdk):
    try:
        client = InfluxDBClient(url=f"http://{INFLUXDB_HOST}:{INFLUXDB_PORT}",
                                token=INFLUXDB_TOKEN,
                                org=INFLUXDB_ORG)

        query_api = client.query_api()

        buckets_api = client.buckets_api()
        buckets = buckets_api.find_buckets().buckets
        print("Buckets:")
        for bucket in buckets:
            print(bucket.name)

        bucket_name = "UAVData" # Please replace with the bucket name you want to debug
        query = f'from(bucket:"{bucket_name}") |> range(start: -48h, stop: now()) |> filter(fn: (r) => r._measurement == "liveCell") |> pivot(rowKey:["_time"], columnKey: ["_field"], valueColumn: "_value")'
        result = query_api.query(query=query)

        print(f"\nSample data from {bucket_name}:")

        if not result:
            print("\033[91mNo data found.\033[0m")
        else:
            for table in result:
                for record in table.records:
                    print(record)

        client.close()
    except Exception as e:
        print(f"\033[91mInfluxDB Debug Error: {str(e)}\033[0m")

debug_influxdb(fs_sdk)