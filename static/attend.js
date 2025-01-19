let RECEIPT_URL = '';

async function finishedLoad() {
    await universalFinishedLoad();

    RECEIPT_URL = '';
    hide(document.getElementById('receipt_num_row'));
    hide(document.getElementById('receipt-div'));
    hide(document.getElementById('receipt_num_cell_1'));
    hide(document.getElementById('receipt_num_cell_2'));

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
        if (r['reason'] != 2)
            document.getElementById('skip').style.display = 'block';
        else
            document.getElementById('already-attending-msg').innerHTML = 'Your Event';
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

    sessionStorage.setItem('currentEvent', JSON.stringify(event));

    const attend_info = await postJsonToApi('/get-attendance', {
        'field1': token,
        'field2': invite,
        'field3': username,
        'e': IS_HTTPS
    }, 'not attending');

    if (isValueNotEmpty(attend_info['badge_number'])) {
        JsBarcode("#barcode", attend_info['badge_number'], {
            fontSize: 20,
            background: "royalblue",
            lineColor: "#ffffff",
            margin: 20,
            marginLeft: 20
        });

        document.getElementById('attend-event-receipt-num').innerHTML = attend_info['receipt_num'];
        RECEIPT_URL = attend_info['receipt_url'];

        show(document.getElementById('receipt-div'));
        show(document.getElementById('receipt_num_cell_1'));
        show_span(document.getElementById('receipt_num_cell_2'));
    }

    if (sessionStorage.getItem("refund") == '1') {
        sessionStorage.setItem('refund', null);
        showMsg("Refund Issued");
    } else if (sessionStorage.getItem("refund") == "0") {
        sessionStorage.setItem("refund", null);
        showMsg("Canceled Attendance");
    }
};

async function attend() {
    document.getElementById('attend-event-msg').innerHTML = PLACEHOLDER;

    const token = await encryptWithPublicKey(sessionStorage.getItem('token'));
    const username = await encryptWithPublicKey(sessionStorage.getItem('uname'));
    const sku = await encryptWithPublicKey(document.getElementById('attend-event-sku').innerHTML);
    const quantity = await encryptWithPublicKey('1');

    const result = await postJsonToApi('/create-checkout-session', {
        'field1': token,
        'field3': username,
        'field2': sku,
        'field4': quantity,
        'e': IS_HTTPS
    }, 'Invalid');

    sessionStorage.setItem('sessionId', result.sessionId);
    navigate(result.url);
};

async function unattend() {
    show(document.getElementById('skip-event-div'));
    document.getElementById('skip-event-name').innerHTML = JSON.parse(sessionStorage.getItem('currentEvent'))['name'];
    const c = generateRandomStringNoSymbols(6);
    document.getElementById('skip-confirm-code').innerHTML = c;
    document.getElementById('confirm-skip').setAttribute('placeholder', c);
};

async function cancelSkip() {
    hide(document.getElementById('skip-event-div'));
};

async function confirmSkip() {
    startProcessing();
    const token = await encryptWithPublicKey(sessionStorage.getItem('token'));
    const username = await encryptWithPublicKey(sessionStorage.getItem('uname'));
    const i = JSON.parse(sessionStorage.getItem('currentEvent'))['inviteCode'];

    const invite = await encryptWithPublicKey(i);

    const result = await postJsonToApi('/mark-skipped',{
        'field1': token,
        'field3': username,
        'field2': invite,
        'e': IS_HTTPS
    }, 'Unable to Skip');

    if (result['result'] == 200) {
        if (parseFloat(document.getElementById('attend-event-cost').innerHTML) > 0.0) {
            sessionStorage.setItem("refund", "1");
        } else {
            sessionStorage.setItem("refund", "0");
        }

        reload();
    }

    stopProcessing();
};

function showReceipt() {
    // Define the url and size of the window
    var url = RECEIPT_URL;
    var winWidth = 650;
    var winHeight = 950;

    // Create a new browser window with the specified URL and size
    window.open(url, "_blank", `width=${winWidth}, height=${winHeight}`);
};