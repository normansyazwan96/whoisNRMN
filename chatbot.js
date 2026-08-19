const chatbot = document.getElementById("chatbot");
const toggle = document.getElementById("chatbot-toggle");
const close = document.getElementById("chatbot-close");
const input = document.getElementById("chatbot-input");
const send = document.getElementById("chatbot-send");
const messages = document.getElementById("chatbot-messages");

toggle.addEventListener("click", () => {
    chatbot.style.display = "flex";
});

close.addEventListener("click", () => {
    chatbot.style.display = "none";
});

send.addEventListener("click", sendMessage);

input.addEventListener("keypress", (e) => {
    if (e.key === "Enter") {
        sendMessage();
    }
});

async function sendMessage() {
    const question = input.value.trim();

    if (!question) return;

    messages.innerHTML += `
        <div class="user-message">
            ${question}
        </div>
    `;

    input.value = "";

    try {
        const response = await fetch("https://api.floweaver.top/chat", {
    method: "POST",
    headers: {
        "Content-Type": "application/json"
    },
    body: JSON.stringify({
        question: question
    })
});

        const data = await response.json();

        messages.innerHTML += `
            <div class="bot-message">
                ${data.answer}
            </div>
        `;

        messages.scrollTop = messages.scrollHeight;

    } catch (error) {
    console.error("CHATBOT ERROR:", error);

    messages.innerHTML += `
        <div class="bot-message">
            Sorry, I couldn't connect to the chatbot.
        </div>
    `;
    }
}
