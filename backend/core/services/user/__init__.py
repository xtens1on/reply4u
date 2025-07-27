import warnings

from core.config import USER_STORAGE_TYPE

if USER_STORAGE_TYPE == 'sql':
    from .sql import UserServiceSQL as UserService
elif USER_STORAGE_TYPE == 'json':
    from .json import UserServiceJSON as UserService
else:
    warnings.warn('WARNING: Wrong USER_STORAGE_TYPE value in .env, using JSON mode as default')
    from .json import UserServiceJSON as UserService
