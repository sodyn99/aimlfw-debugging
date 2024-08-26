from featurestoresdk.feature_store_sdk import FeatureStoreSdk
from influxdb_client import InfluxDBClient

def debug_influxdb(fs_sdk):
    try:
        client = InfluxDBClient(url=f"http://{fs_sdk.feature_store_ip}:{fs_sdk.feature_store_port}",
                                token=fs_sdk.feature_store_password,
                                org=fs_sdk.feature_store_username)

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

fs_sdk = FeatureStoreSdk()

debug_influxdb(fs_sdk)