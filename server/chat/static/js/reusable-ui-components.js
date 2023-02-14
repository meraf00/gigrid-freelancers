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

const create_contract = (user_id, jobs) => `
<form class="contract-form">
    <div><strong>Create contract</strong></div>
    
    <div class="contract-form">
        <label for="jobs">Job</label>
        <select id="jobs">
            ${
                `<option>`
            }            
        </select>

        <label for="budget">Budget</label>
        <input type="number" step="0.01" id="budget"/>

        <label for="deadline">Deadline</label>
        <input type="date" id="deadline"/>
    </div>
</form>
`;
