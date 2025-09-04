var text = document.getElementById("door_status");
var open_button = document.getElementById("door_open");
var close_button = document.getElementById("door_close");
const door_text_form = document.getElementById('door_text_form');


var door_text = document.getElementById("door_text");
var door_text_submit = document.getElementById("door_text_submit");
var door_text_label = document.getElementById("door_text_label");


open_button.addEventListener('click', async function() {
    try {
        await fetch('/api/door/open', {
        method: 'GET',
      }).then(() => {
          window.location.reload();
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
          window.location.reload();
      })
    } catch (error) {
        console.error('Error:', error);
    }
});


if (text.innerHTML === "Open") {
    text.style.color="#50C878";
    open_button.disabled = true;
}

if (text.innerHTML === "Closed") {
    text.style.color="#FF2C2C";
    close_button.disabled = true;

}

door_text_form.addEventListener('submit', async (event) => {
    event.preventDefault(); // Prevent the default form submission
    door_text_submit.disabled = true;
    door_text.disabled = true;

    door_text_label.innerHTML = "Updating text..."


    const formData = new FormData(form);

    try {
        await fetch('/api/door/set_text', {
            method: 'POST',
            body: formData,
        })

        if (response.ok) {
        // Handle success (e.g., display a message)
            response.json().then((data) => {
            if (data["logged_in"]) {
                success.innerHTML = "<b><i>Logged in. Redirecting...</i></b>";
                window.location.replace("/home");
            } else {
                success.innerHTML = "Error: not logged in";
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

open_button.addEventListener('click', async function() {
    try {
        await fetch('/api/door/open', {
        method: 'GET',
      }).then(() => {
          window.location.reload();
      })
    } catch (error) {
        console.error('Error:', error);
    }
});