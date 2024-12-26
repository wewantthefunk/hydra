async function verify() {
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
};

async function generateverify() {
    message.innerHTML = PLACEHOLDER;

    const email = document.getElementById("email").value.trim();
    if (email == "") {
        message.innerHTML = "Enter your email address to send your Verification Email";
        return;
    }

    const em = await encryptWithPublicKey(email);

    const result = await postJsonToApi("/generateverify", {"field1":em}, "Invalid Verification Information"); 

    if (result['status'].indexOf('406') > -1) {
        message.innerHTML = 'Account Already Verified';
        return;
    }
    
    message.innerHTML = result['message'];
};

function goback() {
    navigate("/");
};

function finishedLoad() {

};