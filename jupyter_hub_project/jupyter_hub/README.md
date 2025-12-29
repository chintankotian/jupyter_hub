# Steps to deploy jupyterhub

## Make sure the namespace are same 



1. Create config.yaml with required information

2. Make sure that name space is create 

3. Add jupyter hub repo to helm 
```bash
helm repo add jupyterhub https://hub.jupyter.org/helm-chart/
helm repo update
```



4. Deploy jupyter hub using helm (Version can be found here https://hub.jupyter.org/helm-chart/)
```bash
helm upgrade --cleanup-on-fail \
  --install jupyter-hub jupyterhub/jupyterhub \
  --namespace enterprise-gateway \
  --create-namespace \
  --timeout 10m0s \
  --wait \
  --version=4.3.2 \
  --values config.yaml
```