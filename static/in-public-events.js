async function finishedLoad() {
    await universalFinishedLoad();
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
        nameCell.className = "secondarybackgroundcolor primarytextcolor";
        row.appendChild(nameCell);

        // Create a <td> element for the 'id' column and append it to the row
        const idCell = document.createElement('td');
        idCell.textContent = event.id;
        idCell.className = "secondarybackgroundcolor primarytextcolor";
        row.appendChild(idCell);

        const locationCell = document.createElement('td');
        locationCell.textContent = event.location;
        locationCell.className = "secondarybackgroundcolor primarytextcolor";
        row.appendChild(locationCell);

        const startDateCell = document.createElement('td');
        startDateCell.textContent = event.startDate;
        startDateCell.className = "secondarybackgroundcolor primarytextcolor";
        row.appendChild(startDateCell);

        const startTimeeCell = document.createElement('td');
        startTimeeCell.textContent = event.startTime;
        startTimeeCell.className = "secondarybackgroundcolor primarytextcolor";
        row.appendChild(startTimeeCell);

        const endDateCell = document.createElement('td');
        endDateCell.textContent = event.endDate;
        endDateCell.className = "secondarybackgroundcolor primarytextcolor";
        row.appendChild(endDateCell);

        const endTimeeCell = document.createElement('td');
        endTimeeCell.textContent = event.endTime;
        endTimeeCell.className = "secondarybackgroundcolor primarytextcolor";
        row.appendChild(endTimeeCell);

        const max = document.createElement('td');
        max.textContent = event.maxAttendees;
        max.className = "primarytextcolor";
        row.appendChild(max);

        const current = document.createElement('td');
        const spotsLeft = parseInt(event.maxAttendees) - parseInt(event.currentAttendees);
        current.textContent = String(spotsLeft);
        current.className = "secondarybackgroundcolor primarytextcolor";
        row.appendChild(current);

        const cost = document.createElement('td');
        cost.textContent = String(event.cost);
        cost.className = "secondarybackgroundcolor primarytextcolor";
        row.appendChild(cost);

        const attend = document.createElement('td');
        if (spotsLeft > 0) {
            const cal = document.createElement('img');
            cal.src = 'static/calendar.png';
            cal.setAttribute("onclick", "attend('" + event.inviteCode + "');");
            cal.setAttribute('title', "Attend");
            cal.className = 'clickable';
            attend.appendChild(cal);
        }
        attend.className = "secondarybackgroundcolor primarytextcolor";
        row.appendChild(attend);

        const link = document.createElement('td');
        link.className = "primarytextcolor";
        const code = document.createElement('input');
        code.setAttribute('type', 'text');
        code.setAttribute('readonly', 'readonly');
        code.setAttribute('value', event.inviteCode);
        code.setAttribute('id', 'i-' + event.inviteCode);
        code.classList.add('readonly');
        code.classList.add('hidden');
        code.style.backgroundColor = 'rgb(170, 170, 170)';
        const copy = document.createElement('img');
        copy.src = 'static/copy.png';
        copy.setAttribute("onclick", "copyToClipboard('i-" + event.inviteCode + "', window.location.origin + '/attend/');");
        copy.setAttribute('title', "Copy Event Link");
        copy.className = 'clickable secondarybackgroundcolor primarytextcolor';
        //copy.style.position = "fixed";
        link.appendChild(code);
        link.appendChild(copy);

        row.appendChild(link);

        // Append the new row to the table body
        tableBody.appendChild(row);
    });
};

async function attend(code) {
    navigate('/attend/' + code);
};