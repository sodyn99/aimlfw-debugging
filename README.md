### 1. Clone the Repository

```bash
git clone https://github.com/sodyn99/aimlfw-debugging.git Debugging
```

### 2. Modify the YAML File

Edit the `config/debug-pod-template.yaml` file:

```yaml
  env:
  - name: INFLUXDB_HOST
    value: "my-release-influxdb.default"
  - name: INFLUXDB_PORT
    value: "8086"
  - name: INFLUXDB_TOKEN
    value: "sPEfOtervRYoveYcQiMO" # Update the InfluxDB token / Leave it as is for adaptive use
```

### 3. Create a Debugging File

Create a `~.py` file in the `Debugging/src` directory.

### 4. Execute

```bash
./deploy.sh  # Use the -p flag to deploy only the debug pod
```

```bash
./debug.sh -f ~.py
```

\* Run `auto_completion.sh` to enable auto-completion for the `./debug.sh` script.

![screenshot 1](/assets/screenshot_1.png)
