## Running ENterprose Gateway 

### Need kubectl ,  minikube, helm on local


1. Create namespace 
```bash
kubectl create namespace enterprise-gateway
```


3. Create values-full.yaml


2. Install enterprise-gateway
```bash
helm  upgrade --install  enterprise-gateway \
  https://github.com/jupyter-server/enterprise_gateway/releases/download/v3.2.3/jupyter_enterprise_gateway_helm-3.2.3.tar.gz \
   --kube-context minikube \
   --namespace enterprise-gateway \
   -f values-full.yaml

```


3. Port Forward 
```bash
kubectl port-forward -n enterprise-gateway svc/enterprise-gateway 8888:8888 & pf_pid=$!
```

4. Test the JEG 
```bash
curl -v http://localhost:8888/api/kernelspecs
```
<!-- 


## Install & run Enterprise Gateway

1. Install
```bash
pip install jupyter-enterprise-gateway
```

2. Start gateway (listen on all interfaces)
```bash
jupyter enterprisegateway --ip=0.0.0.0 --port=8888
```

3. Verify kernelspecs available
```bash
curl -s http://localhost:8888/api/kernelspecs | jq .
```

4. Basic test: start a kernel and check status
```bash
# create a kernel
curl -X POST -H "Content-Type: application/json" \
    -d '{"name":"python3"}' \
    http://localhost:8888/api/kernels

# list running kernels
curl http://localhost:8888/api/kernels
```

5. Integrate with JupyterHub
- Configure Spawner to use the gateway endpoint or set the KernelManager in your Hub config to target the Enterprise Gateway API.
- Example (Spawner-specific): set the notebook server to connect using the gateway's host:port and available kernelspec names.

Notes:
- For advanced auth, TLS, or multi-node setups consult the Enterprise Gateway docs.
- Replace ports/hosts as needed for your environment. -->