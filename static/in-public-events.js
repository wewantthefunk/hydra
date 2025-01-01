async function finishedLoad() {
    universalFinishedLoad();
    startProcessing();
    const result = await getApi('/getpublicevents');
    displayEventsTable(JSON.parse(result.message)['events']);
    stopProcessing();
};

function displayEventsTable(events) {
    // Get the table body element where we'll append the rows
    const tableBody = document.getElementById('event-list-body');

    // Clear any existing rows in the table body
    tableBody.innerHTML = '';

    // Loop through each event object and create a new row for it
    events.forEach(event => {
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

        const attend = document.createElement('td');
        if (spotsLeft > 0) {
            const cal = document.createElement('img');
            cal.src = 'static/calendar.png';
            cal.setAttribute("onclick", "attend('" + event.inviteCode + "');");
            cal.setAttribute('title', "Attend");
            cal.className = 'clickable';
            attend.appendChild(cal);
        }
        row.appendChild(attend);

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

        // Append the new row to the table body
        tableBody.appendChild(row);
    });
};

async function attend() {

};