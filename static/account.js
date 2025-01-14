async function finishedLoad() {
    await universalFinishedLoad();

    const result = await postJsonToApi('/getme', {
        'field1': await encryptWithPublicKey(sessionStorage.getItem('token')),
        'field2': await encryptWithPublicKey(sessionStorage.getItem('uname'))
    }, 'error');

    if (result['message'] != 'user info') {
        debugger;
        navigate("/home");
        return;
    }

    document.getElementById('account-email').value = result['email'];
    document.getElementById('account-username').value = result['username'];
    document.getElementById('account-type').innerHTML = convertUserType(result['type']);
};

function convertUserType(t) {
    if (t == USER_LEVEL_ORGANIZER) {
        return USER_LEVEL_ORGANIZER_NAME;
    }

    if (t == USER_LEVEL_ADMIN) {
        return USER_LEVEL_ADMIN_NAME;
    }

    if (t == USER_LEVEL_SUPERUSER) {
        return USER_LEVEL_SUPERUSER_NAME;
    }

    return USER_LEVEL_ADMIN_NAME;
};

async function saveAccount() {

};

async function savePassword() {

};