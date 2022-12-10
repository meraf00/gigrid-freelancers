// Socket Events
CONNECT = "connect";
JOIN = "join";
SEND_MESSAGE = "send_message";
RECEIVE_MESSAGE = "receive_message";
ONLINE_ANN = "online_announcement";

// UI Components

// socket.io

let current_chat = null;

const socket = io.connect("http://localhost:5000");

const user_token = document.getElementById("user_token").value;

socket.on(CONNECT, () => {
  console.log("Connected to server sending join message");
  socket.emit(JOIN, {
    authentication_token: user_token,
  });
});

socket.on(RECEIVE_MESSAGE, (data) => {
  if (current_chat != data.chat_id) return;

  chatPanel.innerHTML += `
  <div>
  ${data.message}<br>
  sender: ${data.from}
  <hr>
  </div>
  `;
});

const selectChat = (component) => {
  current_chat = component.dataset.chatid;
  console.log("Chat ID:", current_chat);
  document.getElementById("log").innerHTML = current_chat;
};

const chatPanel = document.getElementById("messages");
chatPanel.innerHTML = "";

const textPanel = document.getElementById("text");
textPanel.innerHTML = "";

const send = () => {
  const message = textPanel.innerHTML;

  if (message.length == 0) return;

  socket.emit(SEND_MESSAGE, {
    authentication_token: user_token,
    message: message,
    chat_id: current_chat,
  });

  textPanel.innerHTML = "";
};
