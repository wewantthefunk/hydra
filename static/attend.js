async function finishedLoad() {
    await universalFinishedLoad();

    const token = await encryptWithPublicKey(sessionStorage.getItem('token'));
    const username = await encryptWithPublicKey(sessionStorage.getItem('uname'));
    const invite = await encryptWithPublicKey(window.location.pathname.replace("/attend/", ""));

    const r = await postJsonToApi('/checkattendance', {
        'field1': token,
        'field2': invite,
        'field3': username,
        'e': IS_HTTPS
    }, 'Unable to determine attendance');

    if (r['message'] == 'Already Attending') {
        document.getElementById('attend').style.display = 'none';
        show(document.getElementById('already-attending-div'));
    }

    const result = await postJsonToApi('/getevent', {
        'field1': token,
        'field2': username,
        'field3': invite,
        'e': IS_HTTPS
    }, 'Invalid');

    const event = JSON.parse(result['message']);

    console.log(event);
};

async function attend() {
    
};