let isUserMenuVisible = false;
let userMenuOpened = false;

const PLACEHOLDER = "&nbsp;";
const SUCCESS_LOGIN_MSG = 'Successful Login';
const USER_LEVEL = 99;

let IS_HTTPS = false;

async function postJsonToApi(url, data, errmsg) {
    try {
        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });

        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }

        const jsonResponse = await response.json();
        return jsonResponse;
    } catch (error) {
        return { "message": errmsg, "status": error.message };
    }
};

async function getApi(url) {
    try {
        const response = await fetch(url, {
            method: 'GET',
            headers: {}
        });

        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }

        const jsonResponse = await response.json();
        return jsonResponse;
    } catch (error) {
        return { "message": "Invalid Name and Password!", "status": error.message };
    }
};

function validElement(e) {
    if (e != null && e != 'undefined')
        return true;

    return false;
};

function validateEmail(email) {
    const regex = /^[\w-]+(\.[\w-]+)*@([\w-]+\.)+[a-zA-Z]{2,7}$/;
    return regex.test(email);
};

function checkPasswordStrength(password) {
    // Check length
    if (password.length < 12 || password.length > 25) {
        return false;
    }

    // Check for at least two uppercase letters, lowercase letters, numbers and special characters
    const upperCaseRegex = /[A-Z].*[A-Z]/;
    const lowerCaseRegex = /[a-z].*[a-z]/;
    const numberRegex = /\d.*\d/;
    const specialCharRegex = /[!@#$%^&*].*[!@#$%^&*]/;

    if (!upperCaseRegex.test(password) || !lowerCaseRegex.test(password) || !numberRegex.test(password) || !specialCharRegex.test(password)) {
        return false;
    }

    // Check for repeating characters of 3 or more
    const repeatRegex = /(.)\1\1/;
    if (repeatRegex.test(password)) {
        return false;
    }

    // Check for common patterns
    const commonPatterns = ['123', 'abc', 'qwe', 'password'];
    for (let pattern of commonPatterns) {
        if (password.toLowerCase().includes(pattern)) {
            return false;
        }
    }

    // Pass all checks
    return true;
};

function generateRandomString(length) {
    // Define all possible characters that can be used in the random string
    const characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!#@$%^&*';
    let result = '';

    // Generate a random string of the specified length
    for (let i = 0; i < length; i++) {
        // Get a random index from the characters string
        const randomIndex = Math.floor(Math.random() * characters.length);
        // Add the character at the random index to the result string
        result += characters[randomIndex];
    }

    return result;
};

function base64ToUint8Array(base64) {
    const binaryString = atob(base64); // Decode Base64 to binary string
    const length = binaryString.length;
    const bytes = new Uint8Array(length);
    for (let i = 0; i < length; i++) {
        bytes[i] = binaryString.charCodeAt(i);
    }
    return bytes;
};

function exit() {
    sessionStorage.setItem("token", null);
    sessionStorage.setItem("level", "9999");
    sessionStorage.setItem("uname", null);
    isUserMenuVisible = true;
    toggleUserMenu();
    navigate("/");
};

function account() {
    navigate("/account");
};

function home() {
    navigate("/home");
};

function admin() {
    navigate("/admin");
};

function navigate(url) {
    startProcessing();
    stopProcessing();
    isUserMenuVisible = false;
    setTimeout(() => {
        window.location.href = url;
    }, 400);
};

function toggleUserMenu() {
    isUserMenuVisible = !isUserMenuVisible;

    if (!isUserMenuVisible) {
        document.getElementById("userMenu").style.display = 'none';
    } else {
        document.getElementById('userMenu').style.display = 'block';
        userMenuOpened = true;
    }
};

function closeAllModals() {
    isUserMenuVisible = true;
    toggleUserMenu();
};

function startProcessing() {
    const processing = document.getElementById("processing");
    if (processing != null && processing != 'undefined') {
        processing.style.display = 'block';
    }
    const overlay = document.getElementById("overlay");
    if (overlay != null && overlay != 'undefined') {
        overlay.style.display = 'block';
    }
};

function stopProcessing() {
    const processing = document.getElementById("processing");
    if (processing != null && processing != 'undefined') {
        processing.style.display = 'none';
    }
    const overlay = document.getElementById("overlay");
    if (overlay != null && overlay != 'undefined') {
        overlay.style.display = 'none';
    }
};

function getWindowSize() {
    var width = window.innerWidth || document.documentElement.clientWidth || document.body.clientWidth;
    var height = window.innerHeight || document.documentElement.clientHeight || document.body.clientHeight;
    return { width: width, height: height };
};

function getElementHeight(element) {
    var styles = window.getComputedStyle(element);
    var margin = parseFloat(styles['marginTop']) + parseFloat(styles['marginBottom']);
    return element.offsetHeight + margin;
};

function getElementWidth(element) {
    var styles = window.getComputedStyle(element);
    var margin = parseFloat(styles['marginRight']) + parseFloat(styles['marginLeft']);
    return element.offsetWidth + margin;
};

function calcsizes() {
    const maindiv = document.getElementById('maindiv');
    const leftmenu = document.getElementById('leftmenu');

    const sizes = getWindowSize();

    const heading = document.getElementById('heading');

    let headingOffset = 0;

    if (heading != null && heading != 'undefined') {
        headingOffset = getElementHeight(heading);
    }

    if (maindiv != null && maindiv != 'undefined') {
        maindiv.style.height = (sizes['height'] - headingOffset) + 'px';
    }

    if (leftmenu != null && leftmenu != 'undefined') {
        leftmenu.style.height = (sizes['height'] - headingOffset) + 'px';

        if (maindiv != null && maindiv != 'undefined') {
            maindiv.style.width = (sizes['width'] - getElementWidth(leftmenu) - 45) + 'px';
        }
    }
};

function isUrlHttps(url) {
    const parsedUrl = new URL(url);
    return parsedUrl.protocol === 'https:';
};

async function universalFinishedLoad() {
    const token = sessionStorage.getItem('token');
    if (token == 'undefined' || token == null) {
        navigate("/");
    }

    const uname = sessionStorage.getItem('uname');

    const tp = await encryptWithPublicKey(token);
    const u = await encryptWithPublicKey(uname);

    const result = await postJsonToApi("/check", { 'field1': tp, 'field2': u });

    if (result['message'] != 'success') {
        navigate('/');
    }

    LEVEL = sessionStorage.getItem('level');

    if (LEVEL == 'undefined' || LEVEL == null) {
        navigate("/");
    }

    if (parseInt(LEVEL) > 1) {
        document.getElementById("createEvent").style.display = 'none';
    }

    if (sessionStorage.getItem('level') == '0') {
        const a = document.getElementById('admin');
        if (a != null && a != 'undefined') {
            a.style.display = 'block';
        }
    }

    window.addEventListener('resize', function (event) {
        calcsizes();
    });

    calcsizes();

    IS_HTTPS = isUrlHttps(window.location.href);

    const use_encrypt = IS_HTTPS ? 'True' : '';

    await postJsonToApi("/setencryption", {'field1': use_encrypt}, '');
};

async function outsideFinishedLoad() {
    IS_HTTPS = isUrlHttps(window.location.href);

    const use_encrypt = IS_HTTPS ? 'True' : '';

    await postJsonToApi("/setencryption", {'field1': use_encrypt}, '');
};