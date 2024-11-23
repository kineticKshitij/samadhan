const chatWindow = document.getElementById("chat-window");
const userInput = document.getElementById("user-input");

function addMessage(message, isUser = false) {
  const messageDiv = document.createElement("div");
  messageDiv.classList.add("message");
  messageDiv.classList.add(isUser ? "user-message" : "bot-message");
  messageDiv.textContent = message;
  chatWindow.appendChild(messageDiv);
  chatWindow.scrollTop = chatWindow.scrollHeight; 
}

function handleSendMessage() {
  const userMessage = userInput.value.trim();
  if (userMessage) {
    addMessage(userMessage, true); 
    fetch('/chatbot/respond/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCookie('csrftoken')
      },
      body: JSON.stringify({ message: userMessage })
    })
    .then(response => response.json())
    .then(data => {
      const botResponse = data.response;
      addMessage(botResponse);
    })
    .catch(error => console.error('Error:', error));
    userInput.value = ""; 
  }
}

function handleEnterKey(event) {
  if (event.key === "Enter") {
    handleSendMessage();
  }
}

function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}
