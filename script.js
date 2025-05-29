const chat = document.getElementById('chat');
const input = document.getElementById('messageInput');

const username = prompt("Enter your username:");
const socket = new WebSocket("ws://localhost:6789");

socket.onopen = () => {
  socket.send(username);
};

socket.onmessage = (event) => {
  const msg = document.createElement("div");
  msg.textContent = event.data;

  // If it's the user's own message, style it
  if (event.data.startsWith(`${username}:`)) {
    msg.classList.add("own-message");
  }

  chat.appendChild(msg);
  chat.scrollTop = chat.scrollHeight;
};

function sendMessage() {
  const message = input.value.trim();
  if (message !== "") {
    socket.send(message);
    input.value = "";
  } else {
    alert("Please enter a message.");
  }
}

input.addEventListener("keydown", (e) => {
  if (e.key === "Enter") {
    sendMessage();
  }
});
