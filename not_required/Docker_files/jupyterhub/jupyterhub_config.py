from dockerspawner import DockerSpawner

c.JupyterHub.spawner_class = DockerSpawner
# c.JupyterHub.bind_url = 'jupyterhub'

c.DockerSpawner.image = 'jupyter_user'
c.DockerSpawner.remove = True
c.DockerSpawner.network_name = 'jupyterhub-net-test'

c.JupyterHub.hub_ip = 'jupyterhub'
c.JupyterHub.hub_connect_ip = 'jupyterhub'
# Mount volumes for persistence
c.DockerSpawner.volumes = {'jupyterhub-user-{username}': '/home/jovyan/work'}

# Spawn JupyterLab directly
c.Spawner.default_url = '/lab'

# Authentication — simple dummy (for example)
from jupyterhub.auth import DummyAuthenticator
c.JupyterHub.authenticator_class = DummyAuthenticator
c.DummyAuthenticator.allow_any_password = True
c.DummyAuthenticator.user = {'ckotian'}