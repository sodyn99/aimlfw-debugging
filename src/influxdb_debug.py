from featurestoresdk.feature_store_sdk import FeatureStoreSdk
from influxdb_client import InfluxDBClient

fs_sdk = FeatureStoreSdk()

print("\n\033[92mFeature Store Configuration:\033[0m")
print("Database Name:", fs_sdk.feature_store_db_name)
print("IP Address:", fs_sdk.feature_store_ip)
print("Port:", fs_sdk.feature_store_port)
print("Username:", fs_sdk.feature_store_username)
print("Password:", fs_sdk.feature_store_password)

def debug_influxdb(fs_sdk):
    try:
        client = InfluxDBClient(url=f"http://my-release-influxdb.default:8086",
                                token='sPEfOtervRYoveYcQiMO',
                                org='primary')

        query_api = client.query_api()

        # 버킷 목록 확인
        buckets_api = client.buckets_api()
        buckets = buckets_api.find_buckets().buckets
        print("Buckets:")
        for bucket in buckets:
            print(bucket.name)

        # 특정 버킷의 데이터 샘플 확인
        bucket_name = "your_bucket_name"  # 실제 버킷 이름으로 변경
        query = f'from(bucket:"{bucket_name}") |> range(start: -1h) |> limit(n:5)'
        result = query_api.query(query=query)

        print(f"\nSample data from {bucket_name}:")
        for table in result:
            for record in table.records:
                print(record)

        client.close()
    except Exception as e:
        print(f"InfluxDB Debug Error: {str(e)}")

debug_influxdb(fs_sdk)