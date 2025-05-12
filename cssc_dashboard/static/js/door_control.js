var text = document.getElementById("door_status");
var open_button = document.getElementById("door_open");
var close_button = document.getElementById("door_close");

function disable_button(element) {
    element.style.color = "black"
    element.style.cursor = "not-allowed";
    element.style.opacity = "0.5";
    element.style.display = "inline-block";
    element.style.cursor = "pointer";
    element.style.pointerEvents = "none";
    element.style.textDecoration = "none";
}

if (text.innerHTML === "Open") {
    text.style.color="#50C878";
    disable_button(open_button);
}

if (text.innerHTML === "Closed") {
    text.style.color="#FF2C2C";
    disable_button(close_button);

}