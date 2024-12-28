async function encryptWithPublicKey(data) {
    if (IS_HTTPS === '1')
        return encryptWithRsaPublicKey(data);

    return data;
}

async function encryptWithRsaPublicKey(data) {
    const publicKey = await importPublicKey(publicKeyPem);
    const encryptedData = await window.crypto.subtle.encrypt(
        { name: 'RSA-OAEP' },
        publicKey,
        new TextEncoder().encode(data)
    );
    return arrayBufferToBase64(encryptedData);
};

async function importPublicKey(publicKeyPem) {
    const spki = pemToArrayBuffer(publicKeyPem);
    return await window.crypto.subtle.importKey(
        'spki',
        spki,
        { name: 'RSA-OAEP', hash: { name: 'SHA-256' } },
        true,
        ['encrypt']
    );
};

function pemToArrayBuffer(pem) {
    const base64 = pem.replace(/^-+BEGIN [A-Z-]+-+/, '').replace(/-+END [A-Z-]+-+$/g, '');
    const binaryString = atob(base64);
    const len = binaryString.length;
    const bytes = new Uint8Array(len);
    for (let i = 0; i < len; i++) {
        bytes[i] = binaryString.charCodeAt(i);
    }
    return bytes.buffer;
};

function arrayBufferToBase64(buffer) {
    const uint8Array = new Uint8Array(buffer);
    let binary = '';
    for (let i = 0; i < uint8Array.byteLength; i++) {
        binary += String.fromCharCode(uint8Array[i]);
    }
    return btoa(binary);
};

async function decryptString(ciphertext, password) {
    if (IS_HTTPS === '1')
        return decryptStringSymmetric(ciphertext, password);
    
    return ciphertext;
}

async function decryptStringSymmetric(text, password) {
    ciphertext = base64ToUint8Array(text)
    // Extract the salt, IV, and actual ciphertext from the input byte array
    const salt = new Uint8Array(ciphertext.slice(0, 16));  // Ensure it's a Uint8Array
    const iv = new Uint8Array(ciphertext.slice(16, 32));    // Ensure it's a Uint8Array
    const encryptedData = new Uint8Array(ciphertext.slice(32));  // Ensure it's a Uint8Array

    // Derive the key from the password and salt using PBKDF2 with SHA-256
    const key = await deriveKey(password, salt);

    // Decrypt the ciphertext using AES-CBC with the derived key and IV
    const decryptedData = await decryptAES(key, iv, encryptedData);

    // Convert the decrypted data from a byte array to a string
    const plaintext = decodeText(decryptedData);

    return plaintext;
};

async function deriveKey(password, salt) {
    // Convert password to a Uint8Array (text encoded as bytes)
    const encoder = new TextEncoder();
    const passwordBytes = encoder.encode(password);

    // Use PBKDF2 to derive a 256-bit key from the password and salt
    const keyMaterial = await crypto.subtle.importKey(
        'raw', passwordBytes, { name: 'PBKDF2' }, false, ['deriveKey']
    );

    return crypto.subtle.deriveKey(
        { name: 'PBKDF2', salt: salt, iterations: 100000, hash: 'SHA-256' },
        keyMaterial, { name: 'AES-CBC', length: 256 },
        false, ['decrypt']
    );
};

async function decryptAES(key, iv, ciphertext) {
    // Decrypt the ciphertext using AES-CBC with the provided key and IV
    const decrypted = await crypto.subtle.decrypt(
        { name: 'AES-CBC', iv: iv }, key, ciphertext
    );

    // Return the decrypted data
    return new Uint8Array(decrypted);
};

function decodeText(decryptedData) {
    // Convert the decrypted byte array back to a string
    const decoder = new TextDecoder();
    return decoder.decode(decryptedData);
};
