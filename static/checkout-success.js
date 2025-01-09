let RECEIPT_URL = "";

async function finishedLoad() {
    await universalFinishedLoad();

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

    const result = await postJsonToApi('/get-payment-info', {
        'field1': token,
        'field2': sessionId,
        'field3': uname
    }, 'ERROR');

    RECEIPT_URL = result['receipt_url'];

    const receipt_id = await encryptWithPublicKey(result['receipt_id']);

    document.getElementById('attend-event-receipt-num').innerHTML = result['message'];

    const attend_result = await postJsonToApi('/mark-attended', {
        'field1': token,
        'field2': invite,
        'field3': uname,
        'field4': receipt_id
    }, "ERROR");

    document.getElementById('attend-event-badge-num').innerHTML = attend_result['badge_number'];

    JsBarcode("#barcode", attend_result['badge_number'], {
        fontSize: 20,
        background: "royalblue",
        lineColor: "#ffffff",
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
    var newWin = window.open(url, "_blank", `width=${winWidth}, height=${winHeight}`);
};