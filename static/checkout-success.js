async function finishedLoad() {
    await universalFinishedLoad();

    const event = JSON.parse(sessionStorage.getItem('currentEvent'));

    document.getElementById('attend-event-name').innerHTML = event.name;
    document.getElementById('attend-event-start-date').innerHTML = event.startDate;
    document.getElementById('attend-event-start-time').innerHTML = event.startTime;
    document.getElementById('attend-event-end-date').innerHTML = event.endDate;
    document.getElementById('attend-event-end-time').innerHTML = event.endTime;
    document.getElementById('attend-event-location').innerHTML = event.location;
    document.getElementById('attend-event-cost').innerHTML = event.cost;
    document.getElementById('attend-event-sku').innerHTML = event.sku;

    //sessionStorage.setItem('currentEvent', null);
};