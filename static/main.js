async function login() {
    const message = document.getElementById("message");
    message.innerHTML = PLACEHOLDER;
    
    const uname = document.getElementById("uname").value;
    const pwd = document.getElementById("pwd").value;
    const tempPassword = generateRandomString(12);

    const u = await encryptWithPublicKey(uname);
    const p = await encryptWithPublicKey(pwd);
    const tp = await encryptWithPublicKey(tempPassword);

    const result = await postJsonToApi("/login", {"field1":u,"field2": p, "field3": tp}, "Invalid Username and Password");

    message.innerHTML = result['message'];

    if (result['message'] == SUCCESS_LOGIN_MSG) {
        const token = await decryptString(base64ToUint8Array(result['token']), tempPassword);
        sessionStorage.setItem('uname', uname);
        sessionStorage.setItem('token', token);
        sessionStorage.setItem('level', result['level']);
        navigate('home');
    } else {
        if (result['status'].indexOf('401') > -1) {
            message.innerHTML = "Account Not Verified. Click the 'Verify Account' link below."
        }
    }
};

function createAccount() {
    navigate("/newuser");
};

function verifyAccount() {
    navigate("/verify");
}

function finishedLoad() {
    
};