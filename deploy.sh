# kubectl create namespace debugging
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
kubectl apply -f config/debug-pod.yaml

# echo '_debug_sh_complete() {
#     local cur_word prev_word opts
#     cur_word="${COMP_WORDS[COMP_CWORD]}"
#     prev_word="${COMP_WORDS[COMP_CWORD-1]}"

#     # src/ 디렉토리에서 파일명만 추출
#     opts=$(compgen -f '$(pwd)'/src/ | xargs -n 1 basename)

#     COMPREPLY=($(compgen -W "${opts}" -- "${cur_word}"))
#     return 0
# }

# complete -F _debug_sh_complete '$(pwd)'/debug.sh' >> ~/.bashrc

# source ~/.bashrc
# kubectl delete pod debug-pod