function showusers() {
    
};

async function finishedLoad() {
    await universalFinishedLoad();

    let level = sessionStorage.getItem('level');

    if (isValueValid(level))
        level = parseInt(level);
    else
        level = USER_LEVEL_ATTENDEE;

    if (level > USER_LEVEL_ADMIN) {
        home();
    }
};