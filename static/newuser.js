async function createAccount() {
    startProcessing();
    const username = document.getElementById("uname").value.trim();
    const email = document.getElementById("email").value.trim();
    const password = document.getElementById('pwd').value.trim();
    const cpassword = document.getElementById('cpwd').value.trim();

    if (username == '' || email == '' || password == '' || cpassword == '') {
        document.getElementById('message').innerHTML = "All Fields Must Be Filled Out!"
        stopProcessing();
        return;
    }

    if (!validateEmail(email)) {
        document.getElementById('message').innerHTML = "Email must follow the pattern of 'name@domain.ext'";
        stopProcessing();
        return;
    }

    if (username.length < 8 || username.length > 16) {
        document.getElementById('message').innerHTML = "Username must be between 8 and 16 characters";stopProcessing();
        stopProcessing();
        return;
    }

    if (password != cpassword) {
        document.getElementById('message').innerHTML = "Passwords MUST match";
        stopProcessing();
        return;
    }

    if (!checkPasswordStrength(password)) {
        document.getElementById('message').innerHTML = "Password is not strong enough";
        stopProcessing();
        return;
    }

    document.getElementById('message').innerHTML = PLACEHOLDER;

    const u = await encryptWithPublicKey(username);
    const p = await encryptWithPublicKey(password);
    const e = await encryptWithPublicKey(email);

    const dm = "Unable to Create Account";

    const result = await postJsonToApi("/createaccount", {"field3":u,"field2": p, "field1": e}, dm);

    message.innerHTML = result['message'];

    if (result['message'] != dm) {
        document.getElementById('verify').style.display = 'block';
    }

    stopProcessing();
};

function goback() {
    navigate("/");
};

function verify() {
    navigate('/verify');
}

async function finishedLoad() {
    await outsideFinishedLoad();

    const toggleButton = document.getElementById('password-view');
    if (toggleButton != null && toggleButton != 'undefined') {
        toggleButton.addEventListener('click', () => {
            togglePasswordReveal(toggleButton, 'pwd');
        });
    }

    const toggleButton1 = document.getElementById('cpassword-view');
    if (toggleButton1 != null && toggleButton1 != 'undefined') {
        toggleButton1.addEventListener('click', () => {
            togglePasswordReveal(toggleButton1, 'cpwd');
        });
    }
};