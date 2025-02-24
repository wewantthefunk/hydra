async function verify() {
    startProcessing();

    const message = document.getElementById("message");
    message.innerHTML = PLACEHOLDER;
    
    const email = document.getElementById("email").value.trim();
    const pwd = document.getElementById("pwd").value.trim();
    const code = document.getElementById("code").value.trim();

    const em = await encryptWithPublicKey(email);
    const p = await encryptWithPublicKey(pwd);
    const c = await encryptWithPublicKey(code);

    const result = await postJsonToApi("/verifyaccount", {"field1":em,"field2": p, "field3": c}, "Invalid Verification Information");

    message.innerHTML = result['message'];

    if (result['message'].indexOf('Account Verified') > -1) {
        setTimeout(async () => {
            message.innerHTML = 'Logging In';
            const tempPassword = generateRandomString(12);
            const tp = await encryptWithPublicKey(tempPassword);
            const lresult = await postJsonToApi("/login", {"field1":em,"field2": p, "field3": tp}, "Invalid Username and Password");

            if (lresult['message'] == SUCCESS_LOGIN_MSG) {
                const token = await decryptString(lresult['token'], tempPassword);
                sessionStorage.setItem('uname', lresult['uname']);
                sessionStorage.setItem('token', token);
                sessionStorage.setItem('level', lresult['level']);
                navigate('/home');
            } else {
                navigate("/");
            }
        }, 1000);
    } else 
        stopProcessing();
};

async function generateverify() {
    startProcessing();

    message.innerHTML = PLACEHOLDER;

    const email = document.getElementById("email").value.trim();
    if (email == "") {
        message.innerHTML = "Enter your email address to send your Verification Email";
        return;
    }

    const em = await encryptWithPublicKey(email);

    const result = await postJsonToApi("/generateverify", {"field1":em}, "Invalid Verification Information"); 

    if (String(result['status']).indexOf('406') > -1) {
        message.innerHTML = 'Account Already Verified';
    } else {
        message.innerHTML = result['message'];
    }

    stopProcessing();
};

function goback() {
    navigate("/");
};

async function finishedLoad() {
    await outsideFinishedLoad();

    const toggleButton = document.getElementById('password-view');
    if (toggleButton != null && toggleButton != 'undefined') {
        toggleButton.addEventListener('click', () => {
            togglePasswordReveal(toggleButton, 'pwd');
        });
    }
};