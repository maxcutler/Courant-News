# import general project settings
from courant.default_settings import *

# import settings dependent on the local machine configuration   
from local_settings import *

# import settings dependent on the type of deployment
from platform import node
if DEVELOPMENT_SERVER:
    from development import *
else:
    from production import *