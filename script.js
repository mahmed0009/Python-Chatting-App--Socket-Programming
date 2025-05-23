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
  chat.appendChild(msg);
  chat.scrollTop = chat.scrollHeight;
};

function sendMessage() {
  const message = input.value;
  if (message.trim() !== "") {
    socket.send(message);
    input.value = "";
  }else{
    alert("Please enter a message.");
  }
}
