c = get_config()

# PAM Authentication with only one user allowed
c.JupyterHub.authenticator_class = 'jupyterhub.auth.PAMAuthenticator'
c.Authenticator.allowed_users = {'ckotian'}

# Use JupyterLab as default
c.Spawner.default_url = '/lab'

# Point to Jupyter Enterprise Gateway
from jupyter_client.kernelspec import RemoteKernelSpecManager
c.NotebookApp.kernel_spec_manager_class = RemoteKernelSpecManager
c.EnterpriseGatewayKernelSpecManager.gateway_url = 'http://enterprise-gateway:8888'
c.EnterpriseGatewayKernelSpecManager.validate_kernelspecs = False