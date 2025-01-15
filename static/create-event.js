function copylink() {
    copyToClipboard('invite');
};

function createNewEvent() {
    document.getElementById('createEventDiv').style.display = 'block';
    document.getElementById('invite').value = generateRandomStringNoSymbols(16);
    document.getElementById('eventName').value = "";
    document.getElementById('startDate').value = "";
    document.getElementById('startTime').value = "";
    document.getElementById('endDate').value = "";
    document.getElementById('endTime').value = "";
    document.getElementById('last-cancel').value = "";
    document.getElementById('location').value = "";
    document.getElementById('max').value = "";
    document.getElementById('sku').value = "";
    document.getElementById('cost').value = "";
    document.getElementById("createNewEventMessage").innerHTML = PLACEHOLDER;
    document.getElementById("createNewEventMessage2").innerHTML = PLACEHOLDER;
    document.getElementById('create-event-header').innerHTML = 'Create New Event';
    document.getElementById('createEventButton').value = 'Create';
    document.getElementById('new-or-update-event').innerHTML = 'new';
    document.getElementById('event-id').innerHTML = '-1';
    document.getElementById('eventType').value = '0';
    document.getElementById('paymentType').value = '0';

    document.getElementById('max').focus();
    document.getElementById('startDate').focus();
    document.getElementById('endDate').focus();
    document.getElementById('startTime').focus();
    document.getElementById('endTime').focus();
    document.getElementById('location').focus();
    document.getElementById('last-cancel').focus();
    document.getElementById('eventName').focus();
};

function updateEvent(event_row) {
    document.getElementById('createEventDiv').style.display = 'block';
    document.getElementById('invite').value = event_row.children[15].children[0].value;
    document.getElementById('eventName').value = event_row.children[0].innerHTML;
    document.getElementById('startDate').value = event_row.children[5].innerHTML;
    document.getElementById('startTime').value = event_row.children[6].innerHTML;
    document.getElementById('endDate').value = event_row.children[7].innerHTML;
    document.getElementById('endTime').value = event_row.children[8].innerHTML;
    document.getElementById('location').value = event_row.children[4].innerHTML;
    document.getElementById('max').value = event_row.children[9].innerHTML;
    document.getElementById('cost').value = event_row.children[11].innerHTML;
    document.getElementById('sku').value = event_row.children[12].innerHTML;
    document.getElementById("createNewEventMessage").innerHTML = PLACEHOLDER;
    document.getElementById("createNewEventMessage2").innerHTML = PLACEHOLDER;
    document.getElementById('create-event-header').innerHTML = 'Update Event';
    document.getElementById('createEventButton').value = 'Update';
    document.getElementById('new-or-update-event').innerHTML = 'update';
    document.getElementById('event-id').innerHTML = event_row.children[1].innerHTML;
    document.getElementById('last-cancel').value = event_row.children[18].innerHTML;

    if (event_row.children[2].innerHTML == '1') {
        document.getElementById('allow-anonymous-signup').setAttribute('checked', 'checked');
    }

    if (event_row.children[3].innerHTML == '1') {
        document.getElementById('require-signin').setAttribute('checked', 'checked');
    }


    if (parseInt(event_row.children[16].innerHTML) >= 0) {
        document.getElementById('eventType').value = event_row.children[16].innerHTML;
    }

    if (parseInt(event_row.children[17].innerHTML) >= 0) {
        document.getElementById('paymentType').value = event_row.children[17].innerHTML;
    }

    document.getElementById('max').focus();
    document.getElementById('startDate').focus();
    document.getElementById('endDate').focus();
    document.getElementById('startTime').focus();
    document.getElementById('endTime').focus();
    document.getElementById('location').focus();
    document.getElementById('sku').focus();
    document.getElementById('cost').focus();
    document.getElementById('last-cancel').focus();
    document.getElementById('eventName').focus();
};

function closeCreateEvent() {
    document.getElementById('createEventDiv').style.display = 'none';
};

async function saveNewEvent() {
    document.getElementById('createNewEventMessage').innerHTML = PLACEHOLDER;
    document.getElementById('createNewEventMessage2').innerHTML = PLACEHOLDER;
    const eventName = document.getElementById('eventName').value.trim();
    const startDate = document.getElementById('startDate').value.trim();
    const endDate = document.getElementById('endDate').value.trim();
    const lastCancel = document.getElementById('last-cancel').value.trim()
    const startTime = document.getElementById('startTime').value.trim();
    const endTime = document.getElementById('endTime').value.trim();
    const location = document.getElementById('location').value.trim();
    const max = document.getElementById('max').value.trim();
    const sku = document.getElementById('sku').value.trim();
    const cost = document.getElementById('cost').value.trim();

    if (eventName == '') {
        document.getElementById('eventName').focus();
        document.getElementById('createNewEventMessage').innerHTML = "Fill Out All Required Fields";
        return;
    }

    if (startDate == '') {
        document.getElementById('startDate').focus();
        document.getElementById('createNewEventMessage').innerHTML = "Fill Out All Required Fields";
        return;
    }

    if (endDate == '') {
        document.getElementById('endDate').focus();
        document.getElementById('createNewEventMessage').innerHTML = "Fill Out All Required Fields";
        return;
    }

    if (startTime == '') {
        document.getElementById('startTime').focus();
        document.getElementById('createNewEventMessage').innerHTML = "Fill Out All Required Fields";
        return;
    }

    if (endTime == '') {
        document.getElementById('endTime').focus();
        document.getElementById('createNewEventMessage').innerHTML = "Fill Out All Required Fields";
        return;
    }

    if (location == '') {
        document.getElementById('location').focus();
        document.getElementById('createNewEventMessage').innerHTML = "Fill Out All Required Fields";
        return;
    }

    if (max == '') {
        document.getElementById('max').focus();
        document.getElementById('createNewEventMessage').innerHTML = "Fill Out All Required Fields";
        return;
    }

    if (sku == '') {
        document.getElementById('sku').focus();
        document.getElementById('createNewEventMessage').innerHTML = "Fill Out All Required Fields";
        return;
    }

    if (cost == '') {
        document.getElementById('cost').focus();
        document.getElementById('createNewEventMessage').innerHTML = "Fill Out All Required Fields";
        return;
    }

    let parts = startDate.split("-");
    const sd = parts[1] + "/" + parts[2] + '/' + parts[0];
    if (!validateDate(sd)) {
        document.getElementById('startDate').focus();
        document.getElementById('createNewEventMessage').innerHTML = "Enter a valid date in";
        document.getElementById('createNewEventMessage2').innerHTML = "MM/DD/YYYY format";
        return;
    }

    parts = endDate.split("-");
    const ed = parts[1] + "/" + parts[2] + '/' + parts[0];
    if (!validateDate(ed)) {
        document.getElementById('endDate').focus();
        document.getElementById('createNewEventMessage').innerHTML = "Enter a valid date in";
        document.getElementById('createNewEventMessage2').innerHTML = "MM/DD/YYYY format";
        return;
    }

    parts = lastCancel.split("-");
    const ld = parts[1] + "/" + parts[2] + '/' + parts[0];
    if (!validateDate(ld)) {
        document.getElementById('last-cancel').focus();
        document.getElementById('createNewEventMessage').innerHTML = "Enter a valid date in";
        document.getElementById('createNewEventMessage2').innerHTML = "MM/DD/YYYY format";
        return;
    }

    if (!isDate1LessThanOrEqual(startDate, endDate)) {
        document.getElementById('startDate').focus();
        document.getElementById('createNewEventMessage').innerHTML = "Start Date cannot be";
        document.getElementById('createNewEventMessage2').innerHTML = "Greater than End Date";
        return;
    }

    if (startDate == endDate) {
        const st = parseInt(startTime.replace(":", ""));
        const et = parseInt(endTime.replace(":", ""));

        if (st > et) {
            document.getElementById('startTime').focus();
            document.getElementById('createNewEventMessage').innerHTML = "Start Time cannot be";
            document.getElementById('createNewEventMessage2').innerHTML = "Greater than End Time";
            return;
        }
    }

    const etype = document.getElementById('eventType').value;

    if (parseInt(etype) < 0) {
        document.getElementById('eventType').focus();
        document.getElementById('createNewEventMessage').innerHTML = "Select Event Type";
        return;
    }

    const paymentType = document.getElementById('paymentType').value;

    if (parseInt(paymentType) < 0) {
        document.getElementById('paymentType').focus();
        document.getElementById('createNewEventMessage').innerHTML = "Select Payment Type";
        return;
    }

    const aas = document.getElementById('allow-anonymous-signup').checked ? '1' : '0';

    const rsi = document.getElementById('require-signin').checked ? '1' : '0';

    startProcessing();

    const result = await postJsonToApi('/createevent', {
        'field1': await encryptWithPublicKey(sessionStorage.getItem('token')),
        'field2': await encryptWithPublicKey(eventName),
        'field3': await encryptWithPublicKey(startDate),
        'field4': await encryptWithPublicKey(endDate),
        'field5': await encryptWithPublicKey(location),
        'field6': await encryptWithPublicKey(max),
        'field7': await encryptWithPublicKey(etype),
        'field8': await encryptWithPublicKey(document.getElementById('invite').value),
        'field9': await encryptWithPublicKey(sessionStorage.getItem('uname')),
        'field10': await encryptWithPublicKey(startTime),
        'field11': await encryptWithPublicKey(endTime),
        'field12': await encryptWithPublicKey(aas),
        'field13': await encryptWithPublicKey(document.getElementById('new-or-update-event').innerHTML),
        'field14': await encryptWithPublicKey(document.getElementById('event-id').innerHTML),
        'field15': await encryptWithPublicKey(rsi),
        'field16': await encryptWithPublicKey(paymentType),
        'field17': await encryptWithPublicKey(cost),
        'field18': await encryptWithPublicKey(sku),
        'field19': await encryptWithPublicKey(lastCancel)
    });

    document.getElementById('createNewEventMessage').innerHTML = result['message']

    if (result['message'] == 'Event Created' || result['message'] == 'Event Updated') {
        setTimeout(() => {
            navigate(window.location.href);
        }, 1000);
    } else {
        stopProcessing();
    }
};