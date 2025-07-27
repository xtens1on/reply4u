API_BASE_URL = 'http://localhost:8000/';

API_USER_LIST = API_BASE_URL + 'telegram/list';
API_USER_DETAILS = API_BASE_URL + 'user/';
API_MY_ACCOUNT = API_BASE_URL + 'telegram/me/';
API_SETTINGS = API_BASE_URL + 'settings/';
API_MODELS_LIST = API_BASE_URL + 'models/';

function getUserDetailURL(telegram_id) {
    return API_USER_DETAILS + `${telegram_id}/`;
}

function getDeleteUserHistoryURL(telegram_id) {
    return getUserDetailURL(telegram_id) + 'history/';
}
