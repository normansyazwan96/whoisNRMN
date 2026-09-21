const chatbot = document.getElementById("chatbot");
const closeButton = document.getElementById("chatbot-close");
const form = document.getElementById("chatbot-form");
const input = document.getElementById("chatbot-input");
const sendButton = document.getElementById("chatbot-send");
const messages = document.getElementById("chatbot-messages");
const chatFab = document.querySelector(".chat-fab");
const openButtons = document.querySelectorAll("[data-open-chat]");
const promptButtons = document.querySelectorAll(".prompt-chips button");
const menuToggle = document.querySelector(".menu-toggle");
const navLinks = document.getElementById("nav-links");

const API_URL = "https://api.floweaver.top/chat";
let isSending = false;

function openChat() {
  chatbot.classList.add("open");
  chatbot.setAttribute("aria-hidden", "false");
  chatFab.classList.add("hidden");
  document.body.classList.add("chat-open");
  window.setTimeout(() => input.focus(), 220);
}

function closeChat() {
  chatbot.classList.remove("open");
  chatbot.setAttribute("aria-hidden", "true");
  chatFab.classList.remove("hidden");
  document.body.classList.remove("chat-open");
}

function addMessage(text, role) {
  const message = document.createElement("div");
  message.className = `${role}-message message`;
  message.textContent = text;
  messages.appendChild(message);
  messages.scrollTop = messages.scrollHeight;
  return message;
}

function addTypingIndicator() {
  const indicator = document.createElement("div");
  indicator.className = "bot-message message typing";
  indicator.setAttribute("aria-label", "Norman AI is typing");
  indicator.innerHTML = "<i></i><i></i><i></i>";
  messages.appendChild(indicator);
  messages.scrollTop = messages.scrollHeight;
  return indicator;
}

async function sendMessage(question) {
  const cleanQuestion = question.trim();
  if (!cleanQuestion || isSending) return;

  isSending = true;
  input.value = "";
  input.disabled = true;
  sendButton.disabled = true;
  addMessage(cleanQuestion, "user");
  const typing = addTypingIndicator();

  try {
    const response = await fetch(API_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ question: cleanQuestion })
    });

    if (!response.ok) throw new Error(`Request failed with status ${response.status}`);

    const data = await response.json();
    typing.remove();
    addMessage(data.answer || "I couldn't find an answer for that question.", "bot");
  } catch (error) {
    console.error("Chatbot request failed:", error);
    typing.remove();
    addMessage("I’m temporarily unavailable. Please try again shortly or contact Norman by email.", "bot");
  } finally {
    isSending = false;
    input.disabled = false;
    sendButton.disabled = false;
    input.focus();
  }
}

openButtons.forEach((button) => button.addEventListener("click", openChat));
closeButton.addEventListener("click", closeChat);

form.addEventListener("submit", (event) => {
  event.preventDefault();
  sendMessage(input.value);
});

promptButtons.forEach((button) => {
  button.addEventListener("click", () => {
    openChat();
    sendMessage(button.textContent);
  });
});

document.addEventListener("keydown", (event) => {
  if (event.key === "Escape" && chatbot.classList.contains("open")) closeChat();
});

menuToggle.addEventListener("click", () => {
  const isOpen = menuToggle.getAttribute("aria-expanded") === "true";
  menuToggle.setAttribute("aria-expanded", String(!isOpen));
  navLinks.classList.toggle("open", !isOpen);
});

navLinks.querySelectorAll("a").forEach((link) => {
  link.addEventListener("click", () => {
    menuToggle.setAttribute("aria-expanded", "false");
    navLinks.classList.remove("open");
  });
});

const revealObserver = new IntersectionObserver((entries, observer) => {
  entries.forEach((entry) => {
    if (entry.isIntersecting) {
      entry.target.classList.add("visible");
      observer.unobserve(entry.target);
    }
  });
}, { threshold: 0.12 });

document.querySelectorAll(".reveal").forEach((element) => revealObserver.observe(element));
document.getElementById("current-year").textContent = new Date().getFullYear();
