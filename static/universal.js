let isUserMenuVisible = false;
let userMenuOpened = false;

async function postJsonToApi(url, data, tempPassword) {
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
        return { "message": "Invalid Name and Password!" };
    }
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
    isUserMenuVisible = true;
    toggleUserMenu();
    navigate("/");
};

function navigate(url) {
    isUserMenuVisible = false;
    setTimeout(() => {
        window.location.href = url;
    }, 150);
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

async function universalFinishedLoad() {
    const token = sessionStorage.getItem('token');
    if (token == 'undefined' || token == null) {
        navigate("/");
    }

    const uname = sessionStorage.getItem('uname');

    const tp = await encryptWithPublicKey(token);
    const u = await encryptWithPublicKey(uname);

    const result = await postJsonToApi("/check", {'field1': tp, 'field2': u});

    if (result['message'] != 'success') {
        navigate('/');
    }
};