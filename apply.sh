# kubectl create namespace debugging
kubectl apply -f secret-reader-role.yaml
kubectl apply -f secret-reader-rolebinding-1.yaml
kubectl create serviceaccount debug-sa -n default
kubectl apply -f secret-reader-rolebinding-2.yaml
kubectl apply -f cluster-secret-reader.yaml
kubectl apply -f debug-pod.yaml
# kubectl delete pod debug-pod