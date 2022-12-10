BASE_URL = "http://localhost:5000";

const openChat = (e) => {
  fetch(`${BASE_URL}/messages`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      authentication_token: document.getElementById("user_token").value,
      chat_id: parseInt(e.dataset.chat_id),
    }),
  })
    .then((response) => {
      console.log(response);
      return response.json();
    })
    .then((data) => {
      const chat_history = document.getElementById("chat-history");
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
    });

  // const x = new Date();
  // x.getUTCHours
};
