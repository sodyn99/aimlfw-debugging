from featurestoresdk.feature_store_sdk import FeatureStoreSdk
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider

def debug_cassandra(fs_sdk):
    try:
        auth_provider = PlainTextAuthProvider(username=fs_sdk.feature_store_username, password=fs_sdk.feature_store_password)
        cluster = Cluster([fs_sdk.feature_store_ip], port=fs_sdk.feature_store_port, auth_provider=auth_provider)
        session = cluster.connect(fs_sdk.feature_store_db_name)

        rows = session.execute("SELECT table_name FROM system_schema.tables WHERE keyspace_name = %s", [fs_sdk.feature_store_db_name])
        print("Tables in keyspace:")
        for row in rows:
            print(row.table_name)

        table_name = "kt_train"  # Please replace with the table name you want to debug
        rows = session.execute(f"SELECT * FROM {table_name} LIMIT 5")
        print(f"\nSample data from {table_name}:")
        for row in rows:
            print(row)

        cluster.shutdown()
    except Exception as e:
        print(f"Cassandra Debug Error: {str(e)}")

# FeatureStoreSdk 인스턴스 생성
fs_sdk = FeatureStoreSdk()

# debug_cassandra 함수 호출
debug_cassandra(fs_sdk)