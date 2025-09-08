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

async function updateDoorStatus() {
    door_status_update_label.innerHTML = "Updating door status...";
    door_text_update_label.innerHTML = "Updating door text...";

    try {
        const response = await fetch("/api/door");
        if (!response.ok) throw new Error("Network response was not ok");

        const log_response = await fetch("/api/door/latest_log");
        if (!log_response.ok) throw new Error("Network response was not ok");

        const data = await response.json();
        const log_data = await log_response.json();

        document.getElementById("door_status").innerHTML = data.door_status;

        if (door_text_original_value == null) {
            door_text_original_value = data.door_text;
        }

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