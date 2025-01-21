async function login() {
    startProcessing();
    const message = document.getElementById("message");
    message.innerHTML = PLACEHOLDER;

    const uname = document.getElementById("uname").value;
    const pwd = document.getElementById("pwd").value;
    const tempPassword = generateRandomString(12);

    const u = await encryptWithPublicKey(uname);
    const p = await encryptWithPublicKey(pwd);
    const tp = await encryptWithPublicKey(tempPassword);

    const result = await postJsonToApi("/login", { "field1": u, "field2": p, "field3": tp }, "Invalid Username and Password");

    message.innerHTML = result['message'];

    stopProcessing();

    if (result['message'] == SUCCESS_LOGIN_MSG) {
        const token = await decryptString(result['token'], tempPassword);
        sessionStorage.setItem('uname', result['uname']);
        sessionStorage.setItem('token', token);
        sessionStorage.setItem('level', result['level']);
        navigate('/home');
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

async function finishedLoad() {
    await outsideFinishedLoad();

    const toggleButton = document.getElementById('password-view');
    if (isValueValid(toggleButton)) {
        toggleButton.addEventListener('click', () => {
            togglePasswordReveal(toggleButton, 'pwd');
        });
    }

    // Call the function initially to set the position of the target element
    setElementPosition();

    // Add an event listener to update the position of the target element if the window is resized
    window.addEventListener("resize", setElementPosition);
};

function setElementPosition() {

    // Select the elements
    const referenceElement = document.getElementById("pwd");
    const targetElement = document.getElementById("pass-hint");
    // Get the dimensions and position of the reference element
    const referenceRect = referenceElement.getBoundingClientRect();

    // Set the top of the target element to be equal to the top of the reference element
    targetElement.style.top = `${referenceRect.top}px`;

    // Set the left of the target element to be 45 pixels to the right of the width of the reference element
    targetElement.style.left = `${referenceRect.right}px`;
}