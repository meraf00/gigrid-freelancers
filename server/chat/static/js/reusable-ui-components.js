const user = (avater, username, text) => `
<div class="chat-item" onclick="openChat(this)">
    <div class="avater">
        <img src="${avater}" alt="" />
    </div>

    <div class="group">
        <h1 class="username">${username}</h1>
        <p class="${text}">Online</p>
    </div>
</div>`;

const textMessageComponent = (content, time, sent = "") => `
<div class="${"text-message " + sent}">
    <p class="content">${content}</p>
    <div class="time">${time}</div>
</div>`;

const fileMessageComponent = (fileName, fileLink, time, sent = "") => `
<div class="${"file-message " + sent}">
    <a class="content" href=${fileLink}>${fileName}</a>
    <div class="time">${time}</div>
</div>`;
