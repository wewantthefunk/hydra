function copylink() {
    copyToClipboard('invite');
};

function createNewEvent() {
    document.getElementById('createEventDiv').style.display = 'block';
    document.getElementById('invite').value = generateRandomStringNoSymbols(16);
    document.getElementById("createNewEventMessage").innerHTML = PLACEHOLDER;
    document.getElementById("createNewEventMessage2").innerHTML = PLACEHOLDER;
};

function closeCreateEvent() {
    document.getElementById('createEventDiv').style.display = 'none';
};

async function saveNewEvent() {
    startProcessing();
    document.getElementById('createNewEventMessage').innerHTML = PLACEHOLDER;
    document.getElementById('createNewEventMessage2').innerHTML = PLACEHOLDER;
    const eventName = document.getElementById('eventName').value.trim();
    const startDate = document.getElementById('startDate').value.trim();
    const endDate = document.getElementById('endDate').value.trim();
    const startTime = document.getElementById('startTime').value.trim();
    const endTime = document.getElementById('endTime').value.trim();
    const location = document.getElementById('location').value.trim();
    const max = document.getElementById('max').value.trim();

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

    const result = await postJsonToApi('/createevent', {
        'field1': await encryptWithPublicKey(sessionStorage.getItem('token')),
        'field2': await encryptWithPublicKey(eventName),
        'field3': await encryptWithPublicKey(startDate),
        'field4': await encryptWithPublicKey(endDate),
        'field5': await encryptWithPublicKey(location),
        'field6': await encryptWithPublicKey(max),
        'field7': await encryptWithPublicKey(document.getElementById('inviteOnly').checked),
        'field8': await encryptWithPublicKey(document.getElementById('invite').value),
        'field9': await encryptWithPublicKey(sessionStorage.getItem('uname')),
        'field10': await encryptWithPublicKey(startTime),
        'field11': await encryptWithPublicKey(endTime)
    });

    document.getElementById('createNewEventMessage').innerHTML = result['message']

    stopProcessing();
};