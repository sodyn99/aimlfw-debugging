#!/bin/bash
CURRENT_DIR=$(pwd)

function display_logs() {
    pod_name='debug-pod'
    kubectl logs -f $pod_name -n default
}

function wait_for_pod_ready() {
    echo "Waiting for pod to be ready..."
    kubectl wait --for=condition=Ready pod/debug-pod -n default --timeout=90s
    if [[ $? -ne 0 ]]; then
        echo "Pod failed to become ready within the timeout period."
        display_logs
        exit 1
    fi
}

function show_progress() {
    local spinner='|/-\'
    local i=0

    while true; do
        if kubectl exec debug-pod -n default -- test -f /tmp/init_complete 2>/dev/null; then
            break
        fi

        status=$(kubectl exec debug-pod -n default -- cat /tmp/progress_state 2>/dev/null || echo "Initializing...")
        i=$(( (i+1) %4 ))
        printf "\r%s %s" "${spinner:$i:1}" "$status"

        sleep 0.1
    done
}

function wait_for_initialization() {
    echo "Waiting for initialization to complete..."
    start_time=$(date +%s)
    timeout=600  # 10 minutes timeout

    show_progress &

    while true; do
        if kubectl exec debug-pod -n default -- test -f /tmp/init_complete 2>/dev/null; then
            echo -e "\n\e[32mInitialization complete!\e[0m"
            return 0
        fi

        current_time=$(date +%s)
        elapsed=$((current_time - start_time))

        if [ $elapsed -ge $timeout ]; then
            echo -e "\n\e[31mInitialization timed out after $timeout seconds\e[0m"
            display_logs
            return 1
        fi

        sleep 10
    done
}

function deploy_pod() {
    sed "s|<HOST_PATH>|$CURRENT_DIR|g" config/debug-pod-template.yaml > config/debug-pod-deployment.yaml
    kubectl apply -f config/debug-pod-deployment.yaml
    wait_for_pod_ready
    wait_for_initialization

    if [[ $? -eq 0 ]]; then
        echo -e "\e[32mDeployment complete!\e[0m"
    else
        echo -e "\e[31mDeployment failed.\e[0m"
        exit 1
    fi
}

function apply_rbac_configs() {
    kubectl apply -f config/secret-reader-role.yaml
    kubectl apply -f config/secret-reader-rolebinding-1.yaml
    kubectl create serviceaccount debug-sa -n default --dry-run=client -o yaml | kubectl apply -f -
    kubectl apply -f config/secret-reader-rolebinding-2.yaml
    kubectl apply -f config/cluster-secret-reader.yaml
    kubectl apply -f config/kserve-rbac-config.yaml
    kubectl apply -f config/pod-reader-rbac.yaml
    kubectl apply -f config/istio-virtualservice-rbac.yaml
    kubectl apply -f config/service-list-role.yaml
    kubectl apply -f config/knative-role.yaml
    kubectl apply -f config/istio-role.yaml
}

if [[ "$1" == "-p" ]]; then
    deploy_pod
else
    apply_rbac_configs
    deploy_pod
fi
