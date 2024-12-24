async function login() {
    const message = document.getElementById("message");
    message.innerHTML = '';
    
    const uname = document.getElementById("uname").value;
    const pwd = document.getElementById("pwd").value;
    const tempPassword = generateRandomString(12);

    const u = await encryptWithPublicKey(uname);
    const p = await encryptWithPublicKey(pwd);
    const tp = await encryptWithPublicKey(tempPassword);

    const result = await postJsonToApi("/login", {"field1":u,"field2": p, "field3": tp}, tp);

    message.innerHTML = result['message'];

    if (result['message'] == 'success') {
        const token = await decryptString(base64ToUint8Array(result['token']), tempPassword);
        sessionStorage.setItem('uname', uname);
        sessionStorage.setItem('token', token);
        navigate('landing');
    }
};

function finishedLoad() {
    document.getElementById("uname").value = "admin";
    document.getElementById("pwd").value = "FnM0g@#2mihCrurFcv0SuCxsK";
    console.log("finshed load");
};