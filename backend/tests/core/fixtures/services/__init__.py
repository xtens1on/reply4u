import warnings

from core.config import USER_STORAGE_TYPE

from .settings import settings_service

from .users_json import user_service_json

try:
    from .users_sql import user_service_sql
except ModuleNotFoundError:
    pass


if USER_STORAGE_TYPE == 'sql':
    from .users_sql import user_service_sql as user_service
elif USER_STORAGE_TYPE == 'json':
    from .users_json import user_service_json as user_service
else:
    warnings.warn('WARNING: Wrong USER_STORAGE_TYPE value in .env, using JSON fixture as default')
    from .users_json import user_service_json as user_service
