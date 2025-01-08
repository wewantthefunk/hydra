async function finishedLoad() {
    await universalFinishedLoad();

    document.getElementById('attend-event-msg').innerHTML = PLACEHOLDER;

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
        document.getElementById('skip').style.display = 'block';
        show(document.getElementById('already-attending-div'));
    }

    const result = await postJsonToApi('/getevent', {
        'field1': token,
        'field2': username,
        'field3': invite,
        'e': IS_HTTPS
    }, 'Invalid');

    const event = JSON.parse(result['message']);

    document.getElementById('attend-event-name').innerHTML = event.name;
    document.getElementById('attend-event-start-date').innerHTML = event.startDate;
    document.getElementById('attend-event-start-time').innerHTML = event.startTime;
    document.getElementById('attend-event-end-date').innerHTML = event.endDate;
    document.getElementById('attend-event-end-time').innerHTML = event.endTime;
    document.getElementById('attend-event-location').innerHTML = event.location;
    document.getElementById('attend-event-cost').innerHTML = event.cost;
    document.getElementById('attend-event-sku').innerHTML = event.sku;

    sessionStorage.setItem('currentEvent',JSON.stringify(event));
};

async function attend() {
    document.getElementById('attend-event-msg').innerHTML = PLACEHOLDER;

    const token = await encryptWithPublicKey(sessionStorage.getItem('token'));
    const username = await encryptWithPublicKey(sessionStorage.getItem('uname'));
    const sku = await encryptWithPublicKey(document.getElementById('attend-event-sku').innerHTML);
    const quantity = await encryptWithPublicKey('1');

    const result = await postJsonToApi('/create-checkout-session',{
        'field1': token,
        'field3': username,
        'field2': sku,
        'field4': quantity,
        'e': IS_HTTPS
    }, 'Invalid');

    navigate(result.message);
};