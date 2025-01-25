let CURRENT_EVENT = {};

async function finishedLoad() {
    await universalFinishedLoad();

    startProcessing();

    const event_row = JSON.parse(sessionStorage.getItem("currentEvent"));

    const event = {
        "inviteCode": event_row.inviteCode,
        "name": event_row.name,
        "startDate": event_row.startDate,
        "startTime": event_row.startTime,
        "endDate": event_row.endDate,
        "endTime": event_row.endTime,
        "location": event_row.location,
        "maxAttendees": event_row.maxAttendees,
        "cost": event_row.cost,
        "sku": event_row.sku,
        "id": event_row.id,
        "lastDayToCancel": event_row.lastDayToCancel,
        "stripePriceId": event_row.stripePriceId,
    };

    CURRENT_EVENT = event;

    await showEventInfo(event);

    await showEventAttendees(event.inviteCode);

    const inputBox = document.getElementById("attendee-badge-number");

    inputBox.addEventListener("input", async function () {
        if (inputBox.value.length === 10) {
            await direct_check_in(inputBox.value);
        }
    });

    stopProcessing();
};

async function showEventAttendees(invitecode) {
    const token = sessionStorage.getItem('token');
    const uname = sessionStorage.getItem('uname');

    const t = await encryptWithPublicKey(token);
    const u = await encryptWithPublicKey(uname);

    const i = await encryptWithPublicKey(invitecode);
    const result = await postJsonToApi('/geteventattendees', { 'field1': t, 'field2': u, 'field3': i, 'e': IS_HTTPS });

    if (result.result == RESULT_OK) {
        const attendees = JSON.parse(result.message);

        let rows = 0;

        // Get the table body element where we'll append the rows
        const tableBody = document.getElementById('attendees-body');

        // Clear any existing rows in the table body
        tableBody.innerHTML = '';

        attendees.attendees.forEach(attendee => {
            rows++;
            // Create a new <tr> element for the row
            const row = document.createElement('tr');

            // Create a <td> element for the 'name' column and append it to the row
            const nameCell = document.createElement('td');
            nameCell.textContent = attendee.name;
            row.appendChild(nameCell);

            const emailCell = document.createElement('td');
            emailCell.textContent = attendee.email;
            row.appendChild(emailCell);

            const uniqueIdCell = document.createElement('td');
            uniqueIdCell.textContent = attendee.uniqueId;
            row.appendChild(uniqueIdCell);

            const userTypeIdCell = document.createElement('td');
            userTypeIdCell.textContent = attendee.userType;
            row.appendChild(userTypeIdCell);

            const userTypeCell = document.createElement('td');
            let userType = USER_LEVEL_ATTENDEE_NAME;
            if (attendee.userType == USER_LEVEL_SUPERUSER) {
                userType = USER_LEVEL_SUPERUSER_NAME;
            } else if (attendee.userType == USER_LEVEL_ORGANIZER) {
                userType = USER_LEVEL_ORGANIZER_NAME;
            } else if (attendee.userType == USER_LEVEL_ADMIN) {
                userType = USER_LEVEL_ADMIN_NAME;
            }
            userTypeCell.textContent = userType;
            row.appendChild(userTypeCell);

            const badgeNumberCell = document.createElement('td');
            badgeNumberCell.textContent = attendee.badgeNumber;
            row.appendChild(badgeNumberCell);

            const checkInLink = document.createElement('td');
            const checkIn = document.createElement('img');
            checkIn.src = 'static/check-in.png';
            checkIn.setAttribute("onclick", "direct_check_in('" + attendee.badgeNumber + "');");
            checkIn.setAttribute('title', "Check In Attendee");
            checkIn.className = 'clickable';
            checkInLink.appendChild(checkIn);
            row.appendChild(checkInLink);

            const receipt = document.createElement('td');
            const receiptPaper = document.createElement('img');
            receiptPaper.src = 'static/receipt.png';
            receiptPaper.setAttribute("onclick", "showReceipt('" + attendee.receiptUrl + "');");
            receiptPaper.setAttribute('title', "Show Receipt");
            receiptPaper.className = 'clickable';
            receipt.appendChild(receiptPaper);
            row.appendChild(receipt);

            tableBody.appendChild(row);
        });
    }
};

async function showEventInfo(event) {
    document.getElementById('event-admin-header').innerHTML = event.name;

    const startDate = {
        "date": event.startDate,
        "time": event.startTime
    };

    const endDate = {
        "date": event.endDate,
        "time": event.endTime
    };

    const untilStart = getTimeDifference(startDate);
    const untilEnd = getTimeDifference(endDate);

    let daysPlural = "s";
    let hoursPlural = "s";

    if (untilStart.days == 1) {
        daysPlural = "";
    }

    if (untilStart.hours == 1) {
        hoursPlural = "";
    }

    let msg = String(untilStart.days) + " day" + daysPlural + " " + String(untilStart.hours) + " hour" + hoursPlural + " until the event starts!";

    if (untilStart.days < 0) {
        if (untilEnd.days < 0) {
            msg = "This event is over!";
        } else {
            msg = "This is event is currently running!";
            show(document.getElementById('check-in-div'))
        }
    }

    document.getElementById('event-days-until-start').innerHTML = msg;
};

async function showReceipt(url) {
    // Define the url and size of the window
    var winWidth = RECEIPT_WINDOW_WIDTH;
    var winHeight = RECEIPT_WINDOW_HEIGHT;

    // Create a new browser window with the specified URL and size
    window.open(url, "_blank", `width=${winWidth}, height=${winHeight}`);
};

async function check_in() {
    show(document.getElementById('check-in-modal-div'));
    document.getElementById('attendee-badge-number').focus();
    document.getElementById('attendee-check-in-msg').innerHTML = PLACEHOLDER;
};

async function check_in_confirm() {
    await direct_check_in(document.getElementById('attendee-badge-number').value);
};

async function direct_check_in(badgeNum) {
    startProcessing();
    document.getElementById('attendee-check-in-msg').innerHTML = "Checking attendee in...";

    const token = sessionStorage.getItem('token');
    const uname = sessionStorage.getItem('uname');

    const t = await encryptWithPublicKey(token);
    const u = await encryptWithPublicKey(uname);
    const b = await encryptWithPublicKey(badgeNum);
    const i = await encryptWithPublicKey(CURRENT_EVENT.inviteCode);

    const result = await postJsonToApi('/checkin', {
        'field1': t, 'field2': u, 'field3': i, 'field4': b,'e': IS_HTTPS
    }, "Unable to Check In");

    if (result.result  == RESULT_OK) {
        document.getElementById('attendee-badge-number').value = "";
        document.getElementById('attendee-check-in-msg').innerHTML = "Check In Successful. Check In Someone Else?";
        showMsg("Attendee Checked In");
    } else {
        showErrMsg(result.message);
        document.getElementById('attendee-check-in-msg').innerHTML = result.message;
    }

    stopProcessing();
};