var url = "http://127.0.0.1:5000"
let events = []


function get_event_json() {
    fetch(url + "/api/get_events")
    .then(res => res.json())
    .then((out) => {
        console.log(out);
        Array.from(out).forEach(b => events.push(b));

    }).catch(err => console.error(err));

    // console.log(events);
}
