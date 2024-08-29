#!/bin/bash
CURRENT_DIR=$(pwd)

# sudo sysctl -w fs.inotify.max_user_watches=1048576
# sudo sysctl -w fs.inotify.max_user_instances=1048576
# sudo sysctl -w fs.inotify.max_queued_events=1048576

function display_logs() {
    echo "Waiting for pod to be ready..."
    kubectl wait --for=condition=Ready pod/debug-pod -n default --timeout=90s
    if [[ $? -ne 0 ]]; then
        echo -e "\e[31mPod failed to start.\e[0m"
        exit 1
    fi
    pod_name='debug-pod'
    echo "Displaying logs for pod $pod_name..."
    kubectl logs -f $pod_name -n default
}

if [[ "$1" == "-p" ]]; then
    sed "s|<HOST_PATH>|$CURRENT_DIR|g" config/debug-pod-template.yaml > config/debug-pod-deployment.yaml
    kubectl apply -f config/debug-pod-deployment.yaml
    display_logs
    if [[ $? -eq 0 ]]; then
        echo -e "\e[32mDeployment complete.\e[0m"
    fi
    exit 0
fi

kubectl apply -f config/secret-reader-role.yaml
kubectl apply -f config/secret-reader-rolebinding-1.yaml
kubectl create serviceaccount debug-sa -n default
kubectl apply -f config/secret-reader-rolebinding-2.yaml
kubectl apply -f config/cluster-secret-reader.yaml
kubectl apply -f config/kserve-rbac-config.yaml
kubectl apply -f config/pod-reader-rbac.yaml
kubectl apply -f config/istio-virtualservice-rbac.yaml
kubectl apply -f config/service-list-role.yaml
kubectl apply -f config/knative-role.yaml
kubectl apply -f config/istio-role.yaml

sed "s|<HOST_PATH>|$CURRENT_DIR|g" config/debug-pod-template.yaml > config/debug-pod-deployment.yaml
kubectl apply -f config/debug-pod-deployment.yaml

display_logs
if [[ $? -eq 0 ]]; then
    echo -e "\e[32mDeployment complete.\e[0m"
fi