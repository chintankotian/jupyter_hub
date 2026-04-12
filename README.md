# JupyterHub with Enterprise Gateway on Kubernetes

A complete setup for running JupyterHub with Jupyter Enterprise Gateway on Kubernetes, enabling distributed kernel execution and scalable data science workloads.

## 🏗️ Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   JupyterHub    │───▶│ Enterprise       │───▶│ Remote Kernels  │
│   (Web UI)      │    │ Gateway          │    │ (Python, Spark, │
│                 │    │ (Kernel Mgmt)    │    │  R, Scala)      │
└─────────────────┘    └──────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│ User Notebooks  │    │ Kubernetes       │    │ Kernel Pods     │
│ (Lab/Classic)   │    │ Cluster          │    │ (Distributed)   │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

## ✨ Features

- **Multi-user JupyterHub** with authentication and user isolation
- **Remote kernel execution** via Jupyter Enterprise Gateway
- **Scalable compute** - kernels run as separate Kubernetes pods
- **Multiple environments** - Python, R, Scala, and Spark kernels
- **Resource management** - CPU/memory limits per kernel
- **Network isolation** - Secure pod-to-pod communication
- **Custom images** - Support for specialized data science stacks

## 🚀 Quick Start

### Prerequisites

- Kubernetes cluster (minikube, kind, or cloud provider)
- `kubectl` configured for your cluster
- `helm` v3.x installed
- Docker (for building custom images)

### 1. Clone and Setup

```bash
git clone <your-repo-url>
cd jupyter_hub
```

### 2. Deploy Enterprise Gateway

```bash
# Create namespace
kubectl create namespace enterprise-gateway

# Deploy Enterprise Gateway
helm upgrade --install enterprise-gateway \
  https://github.com/jupyter-server/enterprise_gateway/releases/download/v3.2.3/jupyter_enterprise_gateway_helm-3.2.3.tar.gz \
  --namespace enterprise-gateway \
  -f ./jupyter_hub_project/enterprise_gateway/values-full.yaml
```

### 3. Deploy JupyterHub

```bash
# Add JupyterHub Helm repo
helm repo add jupyterhub https://hub.jupyter.org/helm-chart/
helm repo update

# Deploy JupyterHub
helm upgrade --cleanup-on-fail \
  --install jupyterhub jupyterhub/jupyterhub \
  --namespace enterprise-gateway \
  --timeout 10m0s \
  --wait \
  --version=4.3.2 \
  --values ./jupyter_hub_project/jupyter_hub/config.yaml
```

### 4. Access JupyterHub

```bash
# Port-forward to access locally
kubectl port-forward -n enterprise-gateway service/proxy-public 8080:http

# Open browser to http://localhost:8080
```

## 📁 Project Structure

```
jupyter_hub/
├── README.md                           # This file
├── jupyter_hub_project/
│   ├── enterprise_gateway/
│   │   ├── values-full.yaml           # EG Helm configuration
│   │   └── readme.md                  # EG deployment guide
│   ├── jupyter_hub/
│   │   ├── config.yaml                # JupyterHub Helm configuration
│   │   └── README.md                  # JH deployment guide
│   └── jupyterlab_image/
│       └── dockerfile                 # Custom image with gateway client
├── scripts/
│   └── delete-ns-pods-and-services.sh # Cleanup utility
└── not_required/                      # Legacy Docker Compose files
```

## ⚙️ Configuration

### JupyterHub Configuration

Key settings in `jupyter_hub_project/jupyter_hub/config.yaml`:

```yaml
singleuser:
  # Gateway client installation via init container
  initContainers:
    - name: install-gateway
      image: jupyter/minimal-notebook:latest
      command: ["pip", "install", "jupyter-server-gateway"]
  
  # Environment variables for gateway connection
  extraEnv:
    JUPYTER_GATEWAY_URL: "http://enterprise-gateway:8888"
    JUPYTER_GATEWAY_CONNECT_TIMEOUT: "120"
    JUPYTER_GATEWAY_REQUEST_TIMEOUT: "120"
  
  # Network policy to allow gateway communication
  networkPolicy:
    egressAllowRules:
      privateIPs: true
```

### Enterprise Gateway Configuration

Key settings in `jupyter_hub_project/enterprise_gateway/values-full.yaml`:

```yaml
# Service configuration
service:
  type: "NodePort"
  ports:
    - name: "http"
      port: 8888
      targetPort: 8888

# Kernel configuration
kernel:
  allowedKernels: 
    - "python3"
    - "ir"
    - "scala"
    - "spark_python_kubernetes"
    - "spark_r_kubernetes"
    - "spark_scala_kubernetes"

# Resource limits
deployment:
  resources:
    limits:
      cpu: 2
      memory: 10Gi
    requests:
      cpu: 1
      memory: 2Gi
```

## 🔧 Management Commands

### View Logs

```bash
# JupyterHub hub logs
kubectl logs -f deployment/hub -n enterprise-gateway

# Enterprise Gateway logs
kubectl logs -f deployment/enterprise-gateway -n enterprise-gateway

# User server logs
kubectl logs -f <jupyter-username-pod> -n enterprise-gateway
```

### Scaling

```bash
# Scale Enterprise Gateway
kubectl scale deployment enterprise-gateway --replicas=3 -n enterprise-gateway

# Scale JupyterHub user schedulers
kubectl scale deployment user-scheduler --replicas=2 -n enterprise-gateway
```

### Cleanup

```bash
# Clean up all pods and services in namespace
./scripts/delete-ns-pods-and-services.sh enterprise-gateway

# Or clean up everything
helm uninstall jupyterhub -n enterprise-gateway
helm uninstall enterprise-gateway -n enterprise-gateway
kubectl delete namespace enterprise-gateway
```

## 🐛 Troubleshooting

### Common Issues

**1. User pods stuck in `PodInitializing`**
```bash
# Check init container logs
kubectl logs <pod-name> -c install-gateway -n enterprise-gateway

# Common fix: ensure correct package name in initContainer
```

**2. Kernels not connecting to gateway**
```bash
# Verify environment variables in user pod
kubectl exec <user-pod> -n enterprise-gateway -- env | grep JUPYTER_GATEWAY

# Check network connectivity
kubectl exec <user-pod> -n enterprise-gateway -- curl http://enterprise-gateway:8888/api/kernelspecs
```

**3. Gateway authentication errors**
```bash
# Check gateway logs for auth issues
kubectl logs deployment/enterprise-gateway -n enterprise-gateway

# Verify service endpoints
kubectl get endpoints enterprise-gateway -n enterprise-gateway
```

### Debugging Steps

1. **Check pod status**: `kubectl get pods -n enterprise-gateway`
2. **Describe problematic pods**: `kubectl describe pod <pod-name> -n enterprise-gateway`
3. **Check services**: `kubectl get svc -n enterprise-gateway`
4. **Verify network policies**: `kubectl get networkpolicy -n enterprise-gateway`
5. **Test connectivity**: Use `kubectl exec` to test connections between pods

## 🔒 Security Considerations

### Network Policies

The setup includes NetworkPolicies to control traffic:
- User pods can communicate with Enterprise Gateway
- Hub can communicate with user pods
- Gateway can spawn kernel pods

### Resource Limits

Configure appropriate resource limits:
```yaml
singleuser:
  memory:
    limit: 2G
    guarantee: 1G
  cpu:
    limit: 2
    guarantee: 0.1
```

### Authentication

- Default uses DummyAuthenticator (development only)
- For production, configure proper authenticators (LDAP, OAuth, etc.)
- Set up RBAC for Kubernetes resources

## 🚀 Advanced Usage

### Custom Images

Build custom images with pre-installed packages:

```dockerfile
FROM jupyter/minimal-notebook:latest
RUN pip install jupyter-server-gateway pandas scikit-learn
# Add your packages here
```

### Spark Integration

For Spark kernels, ensure:
1. Spark operator is installed in cluster
2. Appropriate RBAC permissions for kernel pods
3. Spark configuration in Enterprise Gateway

### Multi-tenant Setup

For production multi-tenancy:
1. Use separate namespaces per team/project
2. Configure resource quotas
3. Set up proper RBAC policies
4. Use network policies for isolation

## 📚 References

- [Zero to JupyterHub Documentation](https://z2jh.jupyter.org/)
- [Jupyter Enterprise Gateway Documentation](https://jupyter-enterprise-gateway.readthedocs.io/)
- [Kubernetes Documentation](https://kubernetes.io/docs/)
- [Helm Documentation](https://helm.sh/docs/)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

- Create an issue for bugs or feature requests
- Check existing issues for known problems
- Refer to troubleshooting section above
- Consult official documentation for components

---

**Happy Data Science! 🎉**