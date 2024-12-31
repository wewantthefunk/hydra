function showusers() {
    
};

async function finishedLoad() {
    await universalFinishedLoad();

    const level = sessionStorage.getItem('level');

    if (validElement(level))
        level = parseInt(level);
    else
        level = USER_LEVEL_ATTENDEE;

    if (level > USER_LEVEL_ADMIN) {
        home();
    }
};