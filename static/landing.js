async function finishedLoad() {
    await universalFinishedLoad();

    startProcessing();
    const token = sessionStorage.getItem('token');
    const uname = sessionStorage.getItem('uname');

    const t = await encryptWithPublicKey(token);
    const u = await encryptWithPublicKey(uname);

    const result = await postJsonToApi('/myevents', { 'field1': t, 'field2': u, 'e': IS_HTTPS });

    displayEventsTable(JSON.parse(result.message)['events'], 'event-list', 'event-list-body', 0, 'event-org-header');

    displayAttendeeTable(JSON.parse(result.message)['events'], 'attendee-list', 'attendee-list-body', 2);
    stopProcessing();
};

async function displayEventsTable(events, table, tbody, level, header) {
    // Get the table body element where we'll append the rows
    const tableBody = document.getElementById(tbody);

    // Clear any existing rows in the table body
    tableBody.innerHTML = '';

    let rows = 0;
    // Loop through each event object and create a new row for it
    events.forEach(event => {
        if (event.relationship == level) {
            rows++;
            // Create a new <tr> element for the row
            const row = document.createElement('tr');

            // Create a <td> element for the 'name' column and append it to the row
            const nameCell = document.createElement('td');
            nameCell.textContent = event.name;
            row.appendChild(nameCell);

            // Create a <td> element for the 'id' column and append it to the row
            const idCell = document.createElement('td');
            idCell.textContent = event.id;
            row.appendChild(idCell);

            const aaCell = document.createElement('td');
            aaCell.textContent = event.allowAnonymousAttendees;
            row.appendChild(aaCell);

            const rsiCell = document.createElement('td');
            rsiCell.textContent = event.requireSignIn;
            row.appendChild(rsiCell);

            const locationCell = document.createElement('td');
            locationCell.textContent = event.location;
            row.appendChild(locationCell);

            const startDateCell = document.createElement('td');
            startDateCell.textContent = event.startDate;
            row.appendChild(startDateCell);

            const startTimeeCell = document.createElement('td');
            startTimeeCell.textContent = event.startTime;
            row.appendChild(startTimeeCell);

            const endDateCell = document.createElement('td');
            endDateCell.textContent = event.endDate;
            row.appendChild(endDateCell);

            const endTimeeCell = document.createElement('td');
            endTimeeCell.textContent = event.endTime;
            row.appendChild(endTimeeCell);

            const max = document.createElement('td');
            max.textContent = event.maxAttendees;
            row.appendChild(max);

            const current = document.createElement('td');
            const spotsLeft = parseInt(event.maxAttendees) - parseInt(event.currentAttendees);
            current.textContent = String(spotsLeft);
            row.appendChild(current);

            const cost = document.createElement('td');
            cost.textContent = event.cost;
            row.appendChild(cost);

            const sku = document.createElement('td');
            sku.textContent = event.sku;
            row.appendChild(sku);

            const ed = document.createElement('td');
            const cal = document.createElement('img');
            cal.src = 'static/edit.png';
            cal.setAttribute("onclick", "updateEvent(this.parentElement.parentElement);");
            cal.setAttribute('title', "Edit");
            cal.className = 'clickable';
            ed.appendChild(cal);
            row.appendChild(ed);

            const del = document.createElement('td');
            const deli = document.createElement('img');
            deli.src = 'static/delete.png';
            deli.setAttribute("onclick", "delete_event(this.parentElement.parentElement);");
            deli.setAttribute('title', "Delete");
            deli.className = 'clickable';
            del.appendChild(deli);
            row.appendChild(del);

            const link = document.createElement('td');
            const code = document.createElement('input');
            code.setAttribute('type', 'text');
            code.setAttribute('readonly', 'readonly');
            code.setAttribute('value', event.inviteCode);
            code.setAttribute('id', 'i-' + event.inviteCode);
            code.classList.add('hidden');
            const copy = document.createElement('img');
            copy.src = 'static/copy.png';
            copy.setAttribute("onclick", "copyToClipboard('i-" + event.inviteCode + "');");
            copy.setAttribute('title', "Copy Event Link");
            copy.className = 'clickable';
            link.appendChild(code);
            link.appendChild(copy);

            row.appendChild(link);

            const eventType = document.createElement('td');
            eventType.textContent = event.inviteType;
            row.appendChild(eventType);

            const paymentType = document.createElement('td');
            paymentType.textContent = event.paymentType;
            row.appendChild(paymentType);

            const goto = document.createElement('td');
            const gotoi = document.createElement('img');
            gotoi.src = 'static/start.png';
            gotoi.setAttribute("onclick", "gotoEvent('" + event.id + "');");
            gotoi.setAttribute('title', "Go To Event");
            gotoi.className = 'clickable';
            goto.appendChild(gotoi);

            row.appendChild(goto);

            // Append the new row to the table body
            tableBody.appendChild(row);
        }
    });

    if (rows > 0) {
        document.getElementById(table).style.display = 'block';
        document.getElementById(header).style.display = 'block';
    }
};

async function displayAttendeeTable(events, table, tbody, level) {
    // Get the table body element where we'll append the rows
    const tableBody = document.getElementById(tbody);

    // Clear any existing rows in the table body
    tableBody.innerHTML = '';

    let rows = 0;
    // Loop through each event object and create a new row for it
    events.forEach(event => {
        if (event.relationship == level) {
            rows++;
        }
    });

    if (rows > 0) {
        document.getElementById(table).style.display = 'block';
    }
};

async function delete_event(event_row) {
    const confirmCode = generateRandomStringNoSymbols(6);
    document.getElementById("delete-confirm-code").innerHTML = confirmCode;
    document.getElementById("confirm-delete").setAttribute('placeholder', confirmCode);
    document.getElementById('delete-event-name').innerHTML = event_row.childNodes[0].innerHTML;
    document.getElementById('delete-event-id').innerHTML = event_row.childNodes[1].innerHTML;
    document.getElementById('delete-event-div').style.display = 'block';
};

async function cancelDelete() {
    document.getElementById('delete-event-div').style.display = 'none';
};

async function confirmDelete() {
    const typed = document.getElementById('confirm-delete').value;
    const code = document.getElementById("delete-confirm-code").innerHTML;

    if (typed != code) {
        showErrMsg("Confirm Delete Code Incorrect");
        return;
    }

    startProcessing();

    const u = await encryptWithPublicKey(sessionStorage.getItem('uname'));
    const t = await encryptWithPublicKey(sessionStorage.getItem('token'));
    const eid = await encryptWithPublicKey(document.getElementById('delete-event-id').innerHTML);

    const result = await postJsonToApi('/deleteevent', { 'field1': eid, 'field2': t, 'field3': u, 'e': IS_HTTPS });

    if (result['message'] == 'Event Deleted') {
        navigate('/home');
        return;
    }

    showErrMsg(result['message']);

    stopProcessing();
};