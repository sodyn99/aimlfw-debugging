import requests
import json
from kubernetes import client, config
from kubernetes.client.rest import ApiException

def load_kube_config():
    try:
        config.load_kube_config()
    except:
        config.load_incluster_config()

def test_kserve(namespace, name):
    api = client.CustomObjectsApi()
    try:
        isvc = api.get_namespaced_custom_object(
            group="serving.kserve.io",
            version="v1beta1",
            namespace=namespace,
            plural="inferenceservices",
            name=name
        )
        print(f"KServe InferenceService '{name}' status:")
        print(json.dumps(isvc['status'], indent=2))
        return isvc
    except ApiException as e:
        print(f"Error getting InferenceService: {e}")
        return None

def test_knative(namespace, name):
    api = client.CustomObjectsApi()
    try:
        ksvc = api.get_namespaced_custom_object(
            group="serving.knative.dev",
            version="v1",
            namespace=namespace,
            plural="services",
            name=name
        )
        print(f"Knative Service '{name}' status:")
        print(json.dumps(ksvc['status'], indent=2))
        return ksvc
    except ApiException as e:
        print(f"Error getting Knative Service: {e}")
        return None

def get_node_port():
    v1 = client.CoreV1Api()
    try:
        service = v1.read_namespaced_service(name="istio-ingressgateway", namespace="istio-system")
        for port in service.spec.ports:
            if port.port == 80:
                return port.node_port
    except ApiException as e:
        print(f"Error getting NodePort: {e}")
    return None

def get_node_ip():
    v1 = client.CoreV1Api()
    try:
        nodes = v1.list_node()
        for node in nodes.items:
            for address in node.status.addresses:
                if address.type == "InternalIP":
                    return address.address
    except ApiException as e:
        print(f"Error getting Node IP: {e}")
    return None

def test_istio(node_ip, node_port, model_name, namespace, data):
    url = f"http://{node_ip}:{node_port}/v1/models/{model_name}:predict"
    headers = {
        'Host': f"{model_name}.{namespace}.example.com",
        'Content-Type': 'application/json'
    }
    try:
        print(f"Attempting to connect to: {url}")
        print(f"Headers: {headers}")
        print(f"Data: {json.dumps(data, indent=2)}")
        response = requests.post(url, headers=headers, json=data, timeout=30)
        print(f"Istio Gateway test results:")
        print(f"Status code: {response.status_code}")
        print(f"Response: {response.text}")
        return response
    except requests.exceptions.RequestException as e:
        print(f"Error during Istio Gateway test: {e}")
        return None

def main():
    load_kube_config()

    namespace = "kserve-test"
    isvc_name = "qoe-model"
    ksvc_name = f"{isvc_name}-predictor"

    # Test KServe
    isvc = test_kserve(namespace, isvc_name)

    # Test Knative
    ksvc = test_knative(namespace, ksvc_name)

    # Test Istio
    if isvc and ksvc:
        node_port = get_node_port()
        node_ip = get_node_ip()
        if node_port and node_ip:
            data = {
                "instances": [[[2.56, 2.56] for _ in range(10)]]
            }
            test_istio(node_ip, node_port, isvc_name, namespace, data)
        else:
            print("Failed to get NodePort or Node IP")

if __name__ == "__main__":
    main()