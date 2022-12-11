BASE_URL = "http://localhost:5000";

// Socket Events
CONNECT = "connect";
JOIN = "join";
SEND_MESSAGE = "send_message";
RECEIVE_MESSAGE = "receive_message";
ONLINE_ANN = "online_announcement";

const chat_history = document.getElementById("chat-history");
const text_field = document.getElementById("text-input");
const send_btn = document.getElementById("send-message-btn");

const user_token = document.getElementById("user_token").value;
let current_chat = null;

const loadChatHistory = async (chat_id, token) => {
  const response = await fetch(`${BASE_URL}/messages`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      authentication_token: token,
      chat_id: chat_id,
    }),
  });
  const data = await response.json();
  return data;
};

const updateChatHistoryUI = (data) => {
  chat_history.innerHTML = "";

  data.forEach((message) => {
    chat_history.innerHTML += messageComponent(
      message.content,
      new Date(message.timestamp).toLocaleTimeString(navigator.language, {
        hour: "2-digit",
        minute: "2-digit",
      }),
      message.sent ? "sent" : ""
    );
  });
};

const updateChatDetailUI = () => {};

const openChat = (e) => {
  current_chat = parseInt(e.dataset.chat_id);
  loadChatHistory(current_chat, user_token).then((data) =>
    updateChatHistoryUI(data)
  );
};

// Socket Event Handling
const socket = io.connect("http://localhost:5000");

socket.on(CONNECT, () => {
  console.log("Connected to server sending join message");
  socket.emit(JOIN, {
    authentication_token: user_token,
  });
});

socket.on(RECEIVE_MESSAGE, () => {
  loadChatHistory(current_chat, user_token).then((data) =>
    updateChatHistoryUI(data)
  );
});

const sendMessage = () => {
  const message = text_field.innerHTML;

  if (message.length == 0 || current_chat === null) return;

  socket.emit(SEND_MESSAGE, {
    authentication_token: user_token,
    message: message,
    chat_id: current_chat,
  });

  text_field.innerHTML = "";
};

// UI Event listening
send_btn.addEventListener("click", sendMessage);
