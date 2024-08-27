from featurestoresdk.feature_store_sdk import FeatureStoreSdk
import pandas as pd

#--------------------------------------------------------------------------
#----------------------------- Config -------------------------------------
#--------------------------------------------------------------------------
TRAINING_JOB_NAME = "dltrain"
FEATURES = ['Coex_Throughput_DL', 'Gangnam_Throughput_DL', 'GimpoAirport_Throughput_DL', 'Gwanghwamun_Throughput_DL', 'IncheonAirport_Throughput_DL']
# FEATURES = ['x', 'y', 'z']

#--------------------------------------------------------------------------
#----------------------------- Main ---------------------------------------
#--------------------------------------------------------------------------

fs_sdk = FeatureStoreSdk()

#--------------------------------------------------------------------------
#----------------------------- Get Features --------------------------------
#--------------------------------------------------------------------------
# print("\n\033[92mFeature Store Configuration:\033[0m")
# print("Database Name:", fs_sdk.feature_store_db_name)
# print("IP Address:", fs_sdk.feature_store_ip)
# print("Port:", fs_sdk.feature_store_port)
# print("Username:", fs_sdk.feature_store_username)
# print("Password:", fs_sdk.feature_store_password)

try:
    df = fs_sdk.get_features(TRAINING_JOB_NAME, [i for i in FEATURES])
    for i in FEATURES:
        df[i] = pd.to_numeric(df[i], errors='coerce')
    print(f"\033[92mData:\033[0m")
    print(df[(df[FEATURES] != 0).any(axis=1)])
    print(f"\033[92mData types:\033[0m\n{df.dtypes}\n")
except Exception as e:
    print(f"\033[91mError accessing data: {str(e)}\033[0m")
