# Debugging 내용 작성

# 서버 연결 테스트
import requests

url = "http://my-release-influxdb.default:8086"

try:
    response = requests.get(url)

    if response.status_code == 200:
        print(f"연결 성공! 응답 코드: {response.status_code}")
    else:
        print(f"연결 실패. 응답 코드: {response.status_code}")
except requests.exceptions.RequestException as e:
    print(f"연결 중 오류 발생: {e}")
