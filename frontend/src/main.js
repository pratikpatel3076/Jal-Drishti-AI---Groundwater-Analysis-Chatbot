const form = document.getElementById('input-form');
const input = document.getElementById('query-input');
const messages = document.getElementById('messages');
const voiceBtn = document.getElementById('voice-btn');
const chips = document.querySelectorAll('.chip');

let isListening = false;
let recognition = null;

if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
  const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
  recognition = new SpeechRecognition();
  recognition.lang = 'en-IN';
  recognition.interimResults = false;
  recognition.maxAlternatives = 1;

  recognition.onresult = (e) => {
    input.value = e.results[0][0].transcript;
    isListening = false;
    voiceBtn.classList.remove('listening');
    voiceBtn.textContent = '🎤';
    form.dispatchEvent(new Event('submit'));
  };

  recognition.onerror = () => {
    isListening = false;
    voiceBtn.classList.remove('listening');
    voiceBtn.textContent = '🎤';
  };

  recognition.onend = () => {
    isListening = false;
    voiceBtn.classList.remove('listening');
    voiceBtn.textContent = '🎤';
  };
}

voiceBtn.addEventListener('click', () => {
  if (!recognition) {
    addMessage('bot', 'Voice input is not supported in this browser. Please use Chrome or Edge.');
    return;
  }
  if (isListening) {
    recognition.stop();
    return;
  }
  isListening = true;
  voiceBtn.classList.add('listening');
  voiceBtn.textContent = '⏺';
  recognition.start();
});

chips.forEach(chip => {
  chip.addEventListener('click', () => {
    input.value = chip.dataset.query;
    form.dispatchEvent(new Event('submit'));
  });
});

input.addEventListener('keydown', (e) => {
  if (e.key === 'Enter' && !e.shiftKey) {
    e.preventDefault();
    form.dispatchEvent(new Event('submit'));
  }
});

form.addEventListener('submit', async (e) => {
  e.preventDefault();
  const query = input.value.trim();
  if (!query) return;

  addMessage('user', query);
  input.value = '';
  showTyping();

  try {
    const res = await fetch('/api/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ query, language: 'EN' }),
    });
    const data = await res.json();
    removeTyping();

    let html = data.answer.replace(/\n/g, '<br>');

    if (data.chart_url) {
      html += `<br><img src="${data.chart_url}" alt="Trend chart">`;
    }

    if (data.ai_insights) {
      html += `<div class="ai-tag">✨ AI-powered insight</div>`;
    }

    addMessage('bot', html);

    if (data.suggestions && data.suggestions.length > 0) {
      updateSuggestions(data.suggestions);
    }
  } catch (err) {
    removeTyping();
    addMessage('bot', 'Sorry, I could not reach the backend. Make sure the server is running on port 5000.');
  }
});

function addMessage(role, html) {
  const div = document.createElement('div');
  div.className = `message ${role}`;
  div.innerHTML = `
    <div class="avatar">${role === 'user' ? '👤' : '🤖'}</div>
    <div class="bubble">${html}</div>
  `;
  messages.appendChild(div);
  scrollToBottom();
}

function showTyping() {
  const div = document.createElement('div');
  div.className = 'message bot';
  div.id = 'typing-indicator';
  div.innerHTML = `
    <div class="avatar">🤖</div>
    <div class="bubble">
      <div class="typing"><span></span><span></span><span></span></div>
    </div>
  `;
  messages.appendChild(div);
  scrollToBottom();
}

function removeTyping() {
  const el = document.getElementById('typing-indicator');
  if (el) el.remove();
}

function updateSuggestions(suggestions) {
  const container = document.getElementById('suggestions');
  container.innerHTML = suggestions.slice(0, 4).map(s =>
    `<button class="chip" data-query="${s.replace(/"/g, '&quot;')}">${s}</button>`
  ).join('');
  container.querySelectorAll('.chip').forEach(chip => {
    chip.addEventListener('click', () => {
      input.value = chip.dataset.query;
      form.dispatchEvent(new Event('submit'));
    });
  });
}

function scrollToBottom() {
  const container = document.getElementById('chat-container');
  container.scrollTop = container.scrollHeight;
}
