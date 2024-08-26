#!/bin/bash

# 기본값 설정
DEBUG_FILE="debug.py"

# 옵션 파싱
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

# 파일 복사
kubectl cp src/$DEBUG_FILE debug-pod:/app_run/$DEBUG_FILE

# 파일 실행
kubectl exec -it debug-pod -- python3 /app_run/$DEBUG_FILE