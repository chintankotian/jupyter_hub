from dockerspawner import DockerSpawner

c.JupyterHub.spawner_class = DockerSpawner
c.DockerSpawner.image = 'user-jupyterlab'
c.DockerSpawner.remove = True
c.DockerSpawner.network_name = 'jupyterhub-net'

# Mount volumes for persistence
c.DockerSpawner.volumes = {'jupyterhub-user-{username}': '/home/jovyan/work'}

# Spawn JupyterLab directly
c.Spawner.default_url = '/lab'

# Authentication — simple dummy (for example)
from jupyterhub.auth import DummyAuthenticator
c.JupyterHub.authenticator_class = DummyAuthenticator
c.DummyAuthenticator.allow_any_password = True
c.DummyAuthenticator.user = {'ckotian'}