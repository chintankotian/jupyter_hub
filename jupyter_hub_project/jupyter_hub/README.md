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

Use one **release name** for the life of the install (official examples use `jupyterhub`). If you previously installed with `jupyterhub`, do not switch to `jupyter-hub`—Helm will refuse to adopt existing resources (e.g. NetworkPolicy `hub`) because `meta.helm.sh/release-name` must match.

```bash
helm upgrade --cleanup-on-fail \
  --install jupyterhub jupyterhub/jupyterhub \
  --namespace enterprise-gateway \
  --create-namespace \
  --timeout 10m0s \
  --wait \
  --version=4.3.2 \
  --values ./jupyter_hub_project/jupyter_hub/config.yaml
```

To **start fresh** under a new release name instead, uninstall the old release first: `helm uninstall jupyterhub -n enterprise-gateway` (removes chart-owned resources; confirm nothing else depends on them).