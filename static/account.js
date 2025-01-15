let EMAIL = '';

async function finishedLoad() {
    await universalFinishedLoad();

    const result = await postJsonToApi('/getme', {
        'field1': await encryptWithPublicKey(sessionStorage.getItem('token')),
        'field2': await encryptWithPublicKey(sessionStorage.getItem('uname'))
    }, 'error');

    if (result['message'] != 'user info') {
        navigate("/home");
        return;
    }

    document.getElementById('account-email').value = result['email'];
    document.getElementById('account-username').value = result['username'];
    document.getElementById('account-type').innerHTML = convertUserType(result['type']);

    EMAIL = result['email'];
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

async function confirmSaveAccount() {
    show(document.getElementById('update-account-password-div'));
    document.getElementById('update-account-password').focus();
};

async function cancelSaveAccount() {
    hide(document.getElementById('update-account-password-div'));
    document.getElementById('update-account-password').value = '';
};

async function saveAccount() {
    const un = document.getElementById('account-username');
    if (checkRequired(un)) {
        showErrMsg("Username is a required field");
        un.focus();
        return;
    }

    const em = document.getElementById('account-email');

    if (checkRequired(em)) {
        showErrMsg("Email is a required field");
        em.focus();
        return;
    }

    const pw = document.getElementById('update-account-password');

    if (checkRequired(pw)) {
        showErrMsg("Password is required!");
        pw.focus();
        return;
    }

    startProcessing();
    const token = await encryptWithPublicKey(sessionStorage.getItem('token'));
    const uname = await encryptWithPublicKey(sessionStorage.getItem('uname'));
    const nuname = await encryptWithPublicKey(un.value.trim());
    const p = await encryptWithPublicKey(pw.value.trim());
    const ne = await encryptWithPublicKey(em.value.trim());
    const e = await encryptWithPublicKey(EMAIL);

    if (un.value.trim() != sessionStorage.getItem('uname')) {
        const result = await postJsonToApi('/changeusername', {
            'field1': token,
            'field2': uname,
            'field3': nuname,
            'field4': p
        }, 'invalid')

        if (result['result'] != 200) {
            showErrMsg(result['message']);
            un.value = sessionStorage.getItem('uname');
            un.focus();
            stopProcessing();
            return;
        }

        sessionStorage.setItem('uname', un.value.trim());
    }

    if (em.value.trim() != EMAIL) {
        const result = await postJsonToApi('/changeemail', {
            'field1': token,
            'field5': uname,
            'field2': e,
            'field3': ne,
            'field4': p
        }, 'invalid')

        if (result['result'] != 200) {
            showErrMsg(result['message']);
            em.value = EMAIL;
            em.focus();
            stopProcessing();
            return;
        }

        EMAIL = em.value.trim();
    }

    showMsg("Account Updated");

    await cancelSaveAccount();

    stopProcessing();
};

async function savePassword() {

};