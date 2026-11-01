/* --------------------------------------------------------------------------
   The chat box in the bottom corner.

   This file only exists in the page when an AI key has been set up, so if
   you are not using the assistant you can ignore it completely.

   What it does: collect what you type, send it to our own /api/chat
   address, and show whatever comes back. The API key stays on the server.
   -------------------------------------------------------------------------- */

const toggle = document.getElementById("chat-toggle");
const panel = document.getElementById("chat-panel");
const form = document.getElementById("chat-form");
const input = document.getElementById("chat-input");
const messagesBox = document.getElementById("chat-messages");

// Everything said so far, in the shape the AI service expects.
const conversation = [];


// Show or hide the panel when the button is clicked.
toggle.addEventListener("click", () => {
  panel.hidden = !panel.hidden;
  if (!panel.hidden) input.focus();
});


// Put one line of text on screen.
function addLine(who, text) {
  const line = document.createElement("div");
  line.className = "chat-line";

  // textContent, not innerHTML. If a reply contained HTML tags we want the
  // visitor to SEE them, not for the browser to run them. Treating text as
  // text is how you avoid a cross-site scripting bug.
  const name = document.createElement("b");
  name.textContent = who + ": ";
  line.appendChild(name);
  line.appendChild(document.createTextNode(text));

  messagesBox.appendChild(line);
  messagesBox.scrollTop = messagesBox.scrollHeight;
}


form.addEventListener("submit", async (event) => {
  // Stop the browser reloading the page, which is what a form normally does.
  event.preventDefault();

  const question = input.value.trim();
  if (!question) return;

  addLine("You", question);
  conversation.push({ role: "user", content: question });
  input.value = "";
  addLine("Assistant", "thinking...");

  const response = await fetch("/api/chat", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ messages: conversation }),
  });

  const data = await response.json();

  messagesBox.lastChild.remove();          // take away "thinking..."
  addLine("Assistant", data.reply);
  conversation.push({ role: "assistant", content: data.reply });
});
