const user = (avater, username, text) => `
<div class="chat-item" onclick="openChat(this)">
    <div class="avatar">
        <img src="${BASE_URL}/messages/static/icons/avatar.png" alt="" />
    </div>

    <div class="group">
        <h1 class="username">${username}</h1>
        <p class="${text}">Online</p>
    </div>
</div>`;

const textMessageComponent = (content, time, sent = "") => `
<div class="${"text-message " + sent}">
    <div class="content">${content}</div>
    <div class="time">${time}</div>
</div>`;

const fileMessageComponent = (fileName, fileLink, time, sent = "") => `
<div class="${"file-message " + sent}">
    <a class="content" href=${fileLink}>${fileName}</a>
    <div class="time">${time}</div>
</div>`;

const user_detail = (username, user_type) => `
<div class="chat-item">
    <div class="avatar">
        <img src="${BASE_URL}/messages/static/icons/avatar.png" alt="" />
    </div>

    <div class="group">
        <h1 class="username">${username}</h1>    
        <p class="small">${user_type}</p> 
    </div>
</div>
`;
