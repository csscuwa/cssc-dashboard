const form = document.getElementById('setup_form');
success = document.getElementById('success');


form.addEventListener('submit', async (event) => {
    event.preventDefault(); // Prevent the default form submission
    document.getElementById('submit_button').disabled = true;

    const formData = new FormData(form);

  try {
    const response = await fetch('/setup/submit', {
      method: 'POST',
      body: formData,
    });

    if (response.ok) {
      // Handle success (e.g., display a message)
        response.json().then((data) => {
            if (data["account_created"]) {
                success.innerHTML = "<b><i>Account created. Redirecting...</i></b>";
                window.location.replace("/login");
            } else {
                success.innerHTML = "Error: account not created";
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