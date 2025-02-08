async function finishedLoad() {
    startProcessing();
    const result = await getApi('/getpublicevents');
    displayEventsTable(JSON.parse(result.message)['events']);

    const toggleButton = document.getElementById('password-view');
    if (isValueValid(toggleButton)) {
        toggleButton.addEventListener('click', () => {
            togglePasswordReveal(toggleButton, 'password');
        });
    }

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
        max.className = "secondarybackgroundcolor primarytextcolor";
        row.appendChild(max);

        const current = document.createElement('td');
        current.textContent = String(parseInt(event.maxAttendees) - parseInt(event.currentAttendees));
        current.className = "secondarybackgroundcolor primarytextcolor";
        row.appendChild(current);

        const allowAnonymous = document.createElement('td');
        allowAnonymous.textContent = event.allowAnonymousAttendees;
        allowAnonymous.className = "primarytextcolor";
        row.appendChild(allowAnonymous);

        const attend = document.createElement('td');
        attend.className = "secondarybackgroundcolor primarytextcolor";
        const cal = document.createElement('img');
        cal.src = 'static/calendar.png';
        cal.setAttribute("onclick", "attend('" + event.inviteCode + "','" + event.name + "'," + event.allowAnonymousAttendees + ");");
        cal.setAttribute('title', "Attend");
        cal.className = 'clickable';
        attend.appendChild(cal);
        row.appendChild(attend);

        // Append the new row to the table body
        tableBody.appendChild(row);
    });
};

async function attend(inviteCode, name, allowAnonymous) {
    sessionStorage.setItem('destination', null);
    if (allowAnonymous < 1) {
        attend_login(inviteCode, name);
        return;
    }

    document.getElementById('a-event-name').innerHTML = name;
    document.getElementById('a-invite-code').innerHTML = inviteCode;
    document.getElementById('anonymousSignupDiv').style.display = 'block';
};

function signupAnonymous() {

};

function attend_login(inviteCode, name) {
    startProcessing();
    dest = "/attend/" + inviteCode;
    const token = sessionStorage.getItem('token');
    if (!isValueValid(token)) {
        stopProcessing();
        document.getElementById('event-name').innerHTML = name;
        document.getElementById("loggedOutMsgDiv").style.display = 'block';

        sessionStorage.setItem('destination', dest);

        return;
    }

    navigate(dest);
};

function goback() {
    navigate('/');
};

function hideWindow() {
    hide(document.getElementById('loggedOutMsgDiv'));
    hide(document.getElementById('anonymousSignupDiv'));
};

async function login() {
    startProcessing();
    const message = document.getElementById("login-message");
    message.innerHTML = PLACEHOLDER;

    const uname = document.getElementById("uname").value;
    const pwd = document.getElementById("password").value;
    const tempPassword = generateRandomString(12);

    const u = await encryptWithPublicKey(uname);
    const p = await encryptWithPublicKey(pwd);
    const tp = await encryptWithPublicKey(tempPassword);

    const result = await postJsonToApi("/login", { "field1": u, "field2": p, "field3": tp }, "Invalid Username and Password");

    message.innerHTML = result['message'];

    stopProcessing();

    if (result['message'] == SUCCESS_LOGIN_MSG) {
        const token = await decryptString(result['token'], tempPassword);
        sessionStorage.setItem('uname', result['uname']);
        sessionStorage.setItem('token', token);
        sessionStorage.setItem('level', result['level']);
        navigate('/home');
    } else {
        if (result['status'].indexOf('401') > -1) {
            message.innerHTML = "Account Not Verified. Click the 'Verify Account' link below."
        }
    }
};