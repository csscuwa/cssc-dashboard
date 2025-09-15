var door_status_update_label = document.getElementById("door_status_update_label");
var door_text_update_label = document.getElementById("door_text_update_label");


var text = document.getElementById("door_status");
var open_button = document.getElementById("door_open");
var close_button = document.getElementById("door_close");
const door_text_form = document.getElementById('door_text_form');


var door_text = document.getElementById("door_text");
var door_text_submit = document.getElementById("door_text_submit");
var door_text_label = document.getElementById("door_text_label");

var door_text_original_value = null

var rpi_status = document.getElementById("rpi_status");
var rpi_ping_label = document.getElementById("rpi_ping_label");
var rpi_ping_time_label = document.getElementById("rpi_ping_time_label");

open_button.addEventListener('click', async function() {
    try {
        await fetch('/api/door/open', {
        method: 'GET',
      }).then(() => {
          updateDoorStatus();
      })
    } catch (error) {
        console.error('Error:', error);
    }
});

close_button.addEventListener('click', async function() {

    try {
        await fetch('/api/door/close', {
        method: 'GET',
      }).then(() => {
          updateDoorStatus();
      })
    } catch (error) {
        console.error('Error:', error);
    }
});

door_text_form.addEventListener('submit', async (event) => {
    event.preventDefault(); // Prevent the default form submission
    door_text_label.innerHTML = "Updating text..."

    const formData = new FormData(door_text_form);

    door_text_submit.disabled = true;
    door_text.disabled = true;


    try {
        const response =await fetch('/api/door/set_text', {
            method: 'POST',
            body: formData,
        })

        if (response.ok) {
        // Handle success (e.g., display a message)
            response.json().then((data) => {
            if (data["status"]) {
                door_text_label.innerHTML = "Submitted!"
                door_text_submit.disabled = false;
                door_text.disabled = false;
                door_text_original_value = null
                updateDoorStatus()
            } else {
                door_text_label.innerHTML = "Something wrong happened?"
            }

        })

        } else {
            // Handle error
            console.error('Form submission failed');
        }
    } catch (error) {
        console.error('Error:', error);
    }
});

//get time ago messages
function timeAgo(dateString) {
    const now = new Date();
    const past = new Date(dateString.replace(" ", "T")); // Convert to ISO format

    const diffMs = now - past;
    const diffSec = Math.floor(diffMs / 1000);
    const diffMin = Math.floor(diffSec / 60);
    const diffHour = Math.floor(diffMin / 60);
    const diffDay = Math.floor(diffHour / 24);

    // If more than 5 mins then set it to red to make it apparent to users that something is wrong
    if (diffMin > 5) {
        rpi_ping_label.style.color = "red";
        rpi_status.style.color = "red"
        rpi_status.innerHTML = "NO-PING"
    } else {
        rpi_ping_label.style.color = "green";
        rpi_status.style.color = "green"
        rpi_status.innerHTML = "O.K."
    }

    if (diffSec < 5) return `just now`;
    if (diffSec < 60) return `${diffSec} seconds ago`;
    if (diffMin < 60) return `${diffMin} minutes ago`;
    if (diffHour < 24) return `${diffHour} hours ago`;
    return `${diffDay} days ago`;
}


async function updateDoorStatus() {
    door_status_update_label.innerHTML = "Updating door status...";
    door_text_update_label.innerHTML = "Updating door text...";

    try {
        // Get API responses
        const response = await fetch("/api/door");
        if (!response.ok) throw new Error("Network response was not ok");

        const log_response = await fetch("/api/door/latest_log");
        if (!log_response.ok) throw new Error("Network response was not ok");

        const data = await response.json();
        const log_data = await log_response.json();

        document.getElementById("door_status").innerHTML = data.door_status;


        // Check to see if the current server value has been set, if not change it
        if (door_text_original_value == null) {
            door_text_original_value = data.door_text;
        }
        
        // Only update the textbox if there hasn't been any altercations to the input as to prevent deletion of user edits.
        if (door_text.value === door_text_original_value) {
            door_text.value = data.door_text
        }

        if (data.door_status === "1") {
            text.innerHTML = "Open";
            text.style.color="#50C878";
            open_button.disabled = true;
            close_button.disabled = false;
        }

        if (data.door_status === "0") {
            text.innerHTML = "Closed"
            text.style.color="#FF2C2C";
            close_button.disabled = true;
            open_button.disabled = false;
        }

        // get door log info
        door_status_update_label.innerHTML = "Last updated by " + log_data.latest_status_log[0] + " at " + log_data.latest_status_log[1];
        door_text_update_label.innerHTML = "Last updated by " + log_data.latest_text_log[0] + " at " + log_data.latest_text_log[1];

        rpi_ping_label.innerHTML = timeAgo(data.door_last_ping);
        // Set exact time for ppl to know
        rpi_ping_time_label.innerHTML = data.door_last_ping;


    } catch (error) {
        console.error("Error fetching door status:", error);
        document.getElementById("door_status").innerHTML = "Error";
        text.style.color="#FF2C2C";
        close_button.disabled = true;
        open_button.disabled = false;
    }
}

// code for updating door
updateDoorStatus();

// Then poll every 5s
setInterval(updateDoorStatus, 5000);