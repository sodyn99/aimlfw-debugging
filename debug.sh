#!/bin/bash

DEBUG_FILE="debug.py"

while getopts ":f:" opt; do
  case $opt in
    f)
      DEBUG_FILE="$OPTARG"
      ;;
    \?)
      echo "Invalid option: -$OPTARG" >&2
      exit 1
      ;;
    :)
      echo "Option -$OPTARG requires an argument." >&2
      exit 1
      ;;
  esac
done

kubectl exec -it debug-pod -- /bin/bash -c "source /opt/conda/etc/profile.d/conda.sh && conda run -n aimlfw python3 /app_run/src/$DEBUG_FILE"
