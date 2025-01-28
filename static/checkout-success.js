let RECEIPT_URL = "";
let COUNTDOWN = 4;

async function finishedLoad() {
    await universalFinishedLoad();

    startProcessing();

    show(document.getElementById("attend-wait-msg-div"));
    hide(document.getElementById("attend-event-info-div"));

    document.getElementById('countdown').innerHTML = COUNTDOWN;

    setTimeout(getPaymentInfo, COUNTDOWN * 1000);

    setTimeout(countdown, 1000);
};

async function countdown() {
    COUNTDOWN -= 1;
    if (COUNTDOWN > 0) {
        document.getElementById('countdown').innerHTML = '' + COUNTDOWN;
        setTimeout(countdown, 1000);
    } else {
        stopProcessing();
    }
};

async function getPaymentInfo() {
    const event = JSON.parse(sessionStorage.getItem('currentEvent'));
    navigate("/attend/" + event.inviteCode);
};

async function showPaymentInfo() {
    hide(document.getElementById("attend-wait-msg-div"));
    show(document.getElementById("attend-event-info-div"));
    startProcessing();

    const event = JSON.parse(sessionStorage.getItem('currentEvent'));

    document.getElementById('attend-event-name').innerHTML = event.name;
    document.getElementById('attend-event-start-date').innerHTML = event.startDate;
    document.getElementById('attend-event-start-time').innerHTML = event.startTime;
    document.getElementById('attend-event-end-date').innerHTML = event.endDate;
    document.getElementById('attend-event-end-time').innerHTML = event.endTime;
    document.getElementById('attend-event-location').innerHTML = event.location;
    document.getElementById('attend-event-cost').innerHTML = event.cost;
    document.getElementById('attend-event-sku').innerHTML = event.sku;

    const token = await encryptWithPublicKey(sessionStorage.getItem('token'));
    const uname = await encryptWithPublicKey(sessionStorage.getItem('uname'));
    const sessionId = await encryptWithPublicKey(sessionStorage.getItem('sessionId'));
    const invite = await encryptWithPublicKey(event.inviteCode);

    const result = await postJsonToApi('/p-info', {
        'field1': token,
        'field2': sessionId,
        'field3': uname
    }, 'ERROR');

    RECEIPT_URL = result['receipt_url'];

    let rn = '';

    if (isValueValid(result['message'])) {
        rn = result['message'];
    }

    const receipt_id = await encryptWithPublicKey(result['receipt_id']);
    const receipt_num = await encryptWithPublicKey(rn);
    const receipt_url = await encryptWithPublicKey(RECEIPT_URL);

    document.getElementById('attend-event-receipt-num').innerHTML = rn;

    const attend_result = await postJsonToApi('/mark-attended', {
        'field1': token,
        'field2': invite,
        'field3': uname,
        'field4': receipt_id,
        'field5': receipt_num,
        'field6': receipt_url
    }, "ERROR");

    document.getElementById('attend-event-badge-num').innerHTML = attend_result['badge_number'];

    JsBarcode("#barcode", attend_result['badge_number'], {
        fontSize: 20,
        background: "#fff",
        lineColor: "#000",
        margin: 20,
        marginLeft: 20
    });

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