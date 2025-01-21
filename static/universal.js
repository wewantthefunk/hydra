let isUserMenuVisible = false;
let userMenuOpened = false;

const PLACEHOLDER = "&nbsp;";
const SUCCESS_LOGIN_MSG = 'Successful Login';
const USER_LEVEL_ATTENDEE = 99;
const USER_LEVEL_ORGANIZER = 50;
const USER_LEVEL_ADMIN = 1;
const USER_LEVEL_SUPERUSER = 0;

const USER_LEVEL_ATTENDEE_NAME = 'Attendee';
const USER_LEVEL_ORGANIZER_NAME = 'Organizer';
const USER_LEVEL_ADMIN_NAME = 'Administrator';
const USER_LEVEL_SUPERUSER_NAME = 'Super User';

let IS_HTTPS = 0;

const HIDE_PASSWORD_IMAGE = 'static/hide-static.png';
const SHOW_PASSWORD_IMAGE = 'static/reveal-static.png';
const HIDE_PASSWORD_MESSAGE = 'Click to hide password';
const SHOW_PASSWORD_MESSAGE = 'Click to show password';

async function postJsonToApi(url, data, errmsg) {
    if (!isValueValid(data['e'])) {
        data['e'] = IS_HTTPS;
    }
    try {
        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });

        /*if (!response.ok) {
            const r = 
            throw new Error(`HTTP error! Status: ${response.status}`);
        }*/

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

function hide(o) {
    if (o != null && o != 'undefined' && o != 'null') {
        o.style.display = 'none';
    }
};

function show(o) {
    if (o != null && o != 'undefined' && o != 'null') {
        o.style.display = 'block';
    }
};

function show_span(o) {
    if (o != null && o != 'undefined' && o != 'null') {
        o.style.display = 'inline';
    }
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

function generateRandomStringNoSymbols(length) {
    // Define all possible characters that can be used in the random string
    const characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
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

function publicevents() {
    navigate("/publicevents");
};

function navigate(url) {
    startProcessing();
    isUserMenuVisible = false;
    setTimeout(() => {
        stopProcessing();
        window.location.href = url;
    }, 400);
};

function reload() {
    window.location.reload();
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

    const popupmsg = document.getElementById('popup-msg-div');

    popupmsg.style.top = '52px';
    popupmsg.style.left = ((sizes['width'] / 2) - 250) + 'px';

    const popuperrmsg = document.getElementById('popup-error-msg-div');

    popuperrmsg.style.top = '52px';
    popuperrmsg.style.left = ((sizes['width'] / 2) - 250) + 'px';
};

function isUrlHttps(url) {
    if (url.indexOf('localhost') > -1 || url.indexOf("127.0.0.1") > -1)
        return '1';

    const parsedUrl = new URL(url);
    return parsedUrl.protocol === 'https:' ? '1' : '0';
};

async function universalFinishedLoad() {
    const token = sessionStorage.getItem('token');
    if (!isValueValid(token)) {
        navigate("/");
    }

    const uname = sessionStorage.getItem('uname');

    const tp = await encryptWithPublicKey(token);
    const u = await encryptWithPublicKey(uname);

    const result = await postJsonToApi("/check", { 'field1': tp, 'field2': u });

    if (result['message'] != 'success') {
        navigate('/');
        return;
    }

    LEVEL = sessionStorage.getItem('level');

    if (!isValueValid(LEVEL)) {
        navigate("/");
        return;
    }

    const destination = sessionStorage.getItem('destination');

    if (isValueValid(destination)) {
        sessionStorage.setItem('destination', null);
        navigate(destination);
        return;
    }

    if (parseInt(LEVEL) <= USER_LEVEL_ADMIN) {
        const a = document.getElementById('admin');
        if (isValueValid(a)) {
            a.style.display = 'block';
        }
    }

    if (parseInt(LEVEL) > USER_LEVEL_ORGANIZER) {
        const a = document.getElementById('createEvent');
        if (isValueValid(a)) {
            a.style.display = 'none';
        }
    } else {
        const a = document.getElementById('createEvent');
        if (isValueValid(a)) {
            a.style.display = 'block';
        }
    }

    document.getElementById('menu_username').innerHTML = sessionStorage.getItem('uname');
    document.getElementById('mnu-username').innerHTML = sessionStorage.getItem('uname');

    switch (parseInt(LEVEL)) {
        case USER_LEVEL_ADMIN:
            document.getElementById("menu_level").innerHTML = "Admin";
            break;
        case USER_LEVEL_ORGANIZER:
            document.getElementById("menu_level").innerHTML = "Organizer";
            break;
        case USER_LEVEL_ATTENDEE:
            document.getElementById("menu_level").innerHTML = "Attendee";
            break;
        case USER_LEVEL_SUPERUSER:
            document.getElementById("menu_level").innerHTML = "Super User";
            break;
    }

    window.addEventListener('resize', function (event) {
        calcsizes();
    });

    calcsizes();

    IS_HTTPS = isUrlHttps(window.location.href);

    const create_event_invite_code = document.getElementById('invite');

    if (isValueValid(create_event_invite_code)) {
        create_event_invite_code.style.backgroundColor = "#aaa";
    }
};

async function outsideFinishedLoad() {
    IS_HTTPS = isUrlHttps(window.location.href);
};

function togglePasswordReveal(toggleButton, id) {
    if (toggleButton.getAttribute('src') == SHOW_PASSWORD_IMAGE) {
        document.getElementById(id).type = 'text';
        toggleButton.setAttribute('src', HIDE_PASSWORD_IMAGE)
        toggleButton.setAttribute('title', HIDE_PASSWORD_MESSAGE);
    } else {
        document.getElementById(id).type = 'password';
        toggleButton.setAttribute('src', SHOW_PASSWORD_IMAGE);
        toggleButton.setAttribute('title', SHOW_PASSWORD_MESSAGE);
    }
};

function showMsg(text) {
    const m =
        document.getElementById('popup-msg').innerHTML = text;
    document.getElementById('popup-msg-div').style.display = 'block';
    setTimeout(() => {
        document.getElementById('popup-msg-div').style.display = 'none';
    }, 2000);
};

function showErrMsg(text) {
    const m = document.getElementById('popup-error-msg-div');
    document.getElementById('popup-error-msg').innerHTML = text;
    m.style.display = 'block';
    setTimeout(() => {
        m.style.display = 'none';
    }, 2000);
};

function copyToClipboard(textBoxId, prefix) {
    // Get the text field
    var copyText = document.getElementById(textBoxId).value;

    if (isValueValid(copyText)) {
        document.getElementById('text-copy-temp').value = prefix + copyText;
        copyInputText();
    }
};

function copyInputText() {
    // Get the input element
    let inputElement = document.getElementById("text-copy-temp");

    // Select the text in the input box
    inputElement.select();

    // For mobile devices, set the selection range
    inputElement.setSelectionRange(0, 99999);

    // Copy the selected text to the clipboard
    try {
        document.execCommand("copy");
        showMsg("Copied to clipboard");
    } catch (err) {
        showErrMsg("Unable to copy text to clipboard");
    }

    inputElement.blur();
};

function validateNumericInput(inputElement) {
    // Remove any non-numeric characters except for the minus sign (-)
    var cleanedValue = inputElement.value.replace(/[^0-9-\.]/g, '');

    // Limit the number of minus signs to at most one (at the beginning)
    if (cleanedValue.startsWith('-')) {
        cleanedValue = '-' + cleanedValue.slice(1).replace(/-/g, '');
    } else {
        cleanedValue = cleanedValue.replace(/-/g, '');
    }

    // Update the input field with the cleaned value
    inputElement.value = cleanedValue;
};

function validateDateInput(inputElement) {
    // Remove any non-numeric characters except for slashes (/)
    var cleanedValue = inputElement.value.replace(/[^0-9\/]/g, '');

    // Limit the number of slashes to at most two (after the month and day)
    if (cleanedValue.split('/').length > 3) {
        cleanedValue = cleanedValue.slice(0, -1);
    }

    // Update the input field with the cleaned value
    inputElement.value = cleanedValue;
};

function validateDate(dateString) {
    dateString = dateString.replaceAll("-", '/');
    // Split the input string into month, day, and year components
    const parts = dateString.split('/');

    if (parts.length !== 3 || isNaN(Number(parts[0])) || isNaN(Number(parts[1])) || isNaN(Number(parts[2]))) {
        return false; // Invalid format or non-numeric components
    }

    const month = parseInt(parts[0], 10);
    const day = parseInt(parts[1], 10);
    const year = parseInt(parts[2], 10);

    if (isNaN(month) || isNaN(day) || isNaN(year)) {
        return false; // Non-numeric components after conversion to integers
    }

    if (month < 1 || month > 12 || day < 1) {
        return false; // Invalid month or day
    }

    const daysInMonth = new Date(year, month, 0).getDate();

    if (day > daysInMonth) {
        return false; // Too many days for the given month and year
    }

    const currentYear = new Date().getFullYear();

    if (year < currentYear) {
        return false; // Year is less than the current year
    }

    return true; // Valid date
};

function isDate1LessThanOrEqual(dateString1, dateString2) {
    // Parse input dates from string format into Date objects
    const date1 = new Date(dateString1);
    const date2 = new Date(dateString2);

    if (isNaN(date1.getTime()) || isNaN(date2.getTime())) {
        throw new Error('Invalid date format'); // Throw an error for invalid dates
    }

    // Check if date1 is less than or equal to date2 using getTime() method
    return date1 <= date2;
};

function julianDayOfYear(dateString) {
    // Parse input date from string format into Date object
    const date = new Date(dateString);

    if (isNaN(date.getTime())) {
        throw new Error('Invalid date format'); // Throw an error for invalid dates
    }

    const startOfYear = new Date(date.getFullYear(), 0, 1);
    const differenceInMilliseconds = date - startOfYear;
    const millisecondsPerDay = 1000 * 60 * 60 * 24;
    const julianDay = Math.floor(differenceInMilliseconds / millisecondsPerDay) + 1;

    return julianDay;
};

function validateTimeInput(inputElement) {
    // Remove any non-numeric characters except for slashes (/)
    var cleanedValue = inputElement.value.replace(/[^0-9\:]/g, '');

    // Limit the number of slashes to at most two (after the month and day)
    if (cleanedValue.split(':').length > 2) {
        cleanedValue = cleanedValue.slice(0, -1);
    }

    // Update the input field with the cleaned value
    inputElement.value = cleanedValue;
};

function checkRequired(o) {
    if (o.value.trim() == '') {
        o.classList.add("required");
        return true;
    } else {
        o.classList.remove("required");
        return false;
    }
};

function isValueValid(v) {
    if (v == null || v == 'undefined' || v == 'null') {
        return false;
    }

    return true;
};

function isValueNotEmpty(v) {
    const va = isValueValid(v);

    if (va) {
        return v != "";
    }

    return va;
};

function isDateInPast(dateString) {
    // Create a Date object from the input string
    const inputDate = new Date(dateString);

    // Get the current date
    const currentDate = new Date();

    // Compare the dates and return true if the input date is in the past, false otherwise
    return inputDate < currentDate;
};

function calcStripeFees(cost) {    
    const c = parseFloat(cost);
    return c.toFixed(2);
    /*return ((c * 1.029) + .3).toFixed(2);*/
};