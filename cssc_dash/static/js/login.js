const form = document.getElementById('login_form');
success = document.getElementById('password_success');


form.addEventListener('submit', async (event) => {
  event.preventDefault(); // Prevent the default form submission

  const formData = new FormData(form);

  try {
    const response = await fetch('/api/auth', {
      method: 'POST',
      body: formData,
    });

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