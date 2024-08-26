### 1. Clone

```bash
git clone https://github.com/sodyn99/aimlfw-debugging.git Debugging
```

### 2. yaml 수정

`debug-pod.yaml` 파일 수정

```yaml
  env:
  - name: INFLUXDB_HOST
    value: "my-release-influxdb.default"
  - name: INFLUXDB_PORT
    value: "8086"
  - name: INFLUXDB_TOKEN
    value: "sPEfOtervRYoveYcQiMO" # influxdb token 수정
```

### 3. Debugging 파일 생성

`Debugging/src` 디렉토리에 `~.py` 파일 생성

### 4. 실행

```bash
./apply.sh
```

```bash
./debug.sh -f ~.py
```

![screenshot 1](/assets/screenshot_1.png)
