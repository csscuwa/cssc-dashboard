var text = document.getElementById("door_status");

if (text.innerHTML === "Open") {
    text.style.color="#50C878";
}

if (text.innerHTML === "Closed") {
    text.style.color="#FF2C2C";
}