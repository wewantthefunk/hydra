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

    const toggleButton = document.getElementById('account-current-password-reveal');
    if (isValueValid(toggleButton)) {
        toggleButton.addEventListener('click', () => {
            togglePasswordReveal(toggleButton, 'account-current-password');
        });
    }

    const toggleButton1 = document.getElementById('account-new-password-reveal');
    if (isValueValid(toggleButton1)) {
        toggleButton1.addEventListener('click', () => {
            togglePasswordReveal(toggleButton1, 'account-new-password');
        });
    }

    const toggleButton2 = document.getElementById('account-confirm-new-password-reveal');
    if (isValueValid(toggleButton2)) {
        toggleButton2.addEventListener('click', () => {
            togglePasswordReveal(toggleButton2, 'account-confirm-new-password');
        });
    }

    const toggleButton3 = document.getElementById('update-account-password-reveal');
    if (isValueValid(toggleButton3)) {
        toggleButton3.addEventListener('click', () => {
            togglePasswordReveal(toggleButton3, 'update-account-password');
        });
    }
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

    return USER_LEVEL_ATTENDEE_NAME;
};

async function confirmSaveAccount() {
    show(document.getElementById('update-account-password-div'));
    document.getElementById('update-account-password').focus();
};

async function cancelSaveAccount() {
    hide(document.getElementById('update-account-password-div'));
    document.getElementById('update-account-password').value = '';
};

async function closePasswordRequirements() {
    hide(document.getElementById('password-requirements-div'));
};

async function showPasswordRequirements() {
    show(document.getElementById('password-requirements-div'));
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
        }, 'invalid');

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
    const cpwd = document.getElementById('account-current-password').value.trim();
    const npwd = document.getElementById('account-new-password').value.trim();
    const cnpwd = document.getElementById('account-confirm-new-password').value.trim();

    if (cpwd == '') {
        showErrMsg('Current Password is Required');
        document.getElementById('account-current-password').focus();
        return;
    }

    if (npwd == '') {
        showErrMsg('New Password is Required');
        document.getElementById('account-new-password').focus();
        return;
    }

    if (cnpwd == '') {
        showErrMsg('New Password Confirmation is Required');
        document.getElementById('account-confirm-new-password').focus();
        return;
    }

    if (cnpwd != npwd) {
        showErrMsg('New Passwords Must Match');
        document.getElementById('account-new-password').focus();
        return;
    }

    if (!checkPasswordStrength(npwd)) {
        showErrMsg("New Password is not strong enough");
        document.getElementById('account-new-password').focus();
        return;
    }

    const token = await encryptWithPublicKey(sessionStorage.getItem('token'));
    const uname = await encryptWithPublicKey(sessionStorage.getItem('uname'));
    const enpwd = await encryptWithPublicKey(npwd);
    const ecpwd = await encryptWithPublicKey(cpwd);

    const result = await postJsonToApi('/changepassword', {
        'field1': token,
        'field2': enpwd,
        'field3': ecpwd,
        'field4': uname,
    }, 'invalid');

    if (result['result'] != 200) {
        showErrMsg(result['message']);
        document.getElementById('account-current-password').focus();
        stopProcessing();
        return;
    }

    showMsg('Password Updated');
    stopProcessing();

    document.getElementById('account-current-password').value = '';
    document.getElementById('account-new-password').value = '';
    document.getElementById('account-confirm-new-password').value = '';
};