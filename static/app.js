const chat = document.getElementById('chat');
const micBtn = document.getElementById('mic-btn');
const sendBtn = document.getElementById('send-btn');
const soundBtn = document.getElementById('sound-btn');
const clearBtn = document.getElementById('clear-btn');
const textInput = document.getElementById('text-input');
const hint = document.getElementById('hint');
const statusPill = document.getElementById('status-pill');
const statusText = document.getElementById('status-text');

const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
let voiceEnabled = true;

addMessage(
  'Hello, I am Loki, your personal assistant. Ask me for the time, news, a song, or to open a website.',
  'welcome'
);

function setStatus(state, label) {
  statusPill.classList.remove('listening', 'thinking', 'offline');
  if (state) statusPill.classList.add(state);
  statusText.textContent = label;
}

function setHint(text, busy) {
  hint.textContent = text;
  hint.classList.toggle('busy', !!busy);
}

function buildAvatar() {
  const img = document.createElement('img');
  img.src = '/static/mascot.png';
  img.alt = 'Loki';
  img.classList.add('mascot', 'avatar');
  return img;
}

function addMessage(text, sender, delay = 0) {
  const row = document.createElement('div');
  row.className = `message ${sender}`;
  row.style.animationDelay = `${delay}ms`;

  if (sender === 'assistant' || sender === 'welcome') {
    row.appendChild(buildAvatar());
  }

  const bubble = document.createElement('div');
  bubble.className = 'bubble';
  bubble.textContent = text;
  row.appendChild(bubble);

  chat.appendChild(row);
  chat.scrollTop = chat.scrollHeight;
  return row;
}

function showTyping() {
  const row = document.createElement('div');
  row.className = 'message assistant typing';
  row.appendChild(buildAvatar());
  const bubble = document.createElement('div');
  bubble.className = 'bubble';
  for (let i = 0; i < 3; i++) {
    const dot = document.createElement('span');
    dot.className = 'dot';
    bubble.appendChild(dot);
  }
  row.appendChild(bubble);
  chat.appendChild(row);
  chat.scrollTop = chat.scrollHeight;
  return row;
}

function pickVoice() {
  const voices = window.speechSynthesis.getVoices();
  return (
    voices.find(v => /google us english/i.test(v.name)) ||
    voices.find(v => v.lang === 'en-US') ||
    voices[0]
  );
}

function speak(text) {
  if (!voiceEnabled || !('speechSynthesis' in window) || !text) return;
  window.speechSynthesis.cancel();
  const utterance = new SpeechSynthesisUtterance(text);
  const voice = pickVoice();
  if (voice) utterance.voice = voice;
  utterance.rate = 1;
  utterance.pitch = 1;
  utterance.onstart = () => document.body.classList.add('talking');
  utterance.onend = () => document.body.classList.remove('talking');
  window.speechSynthesis.speak(utterance);
}

async function sendCommand(command) {
  command = command.trim();
  if (!command) return;

  addMessage(command, 'user');
  setHint('Loki is thinking...', true);
  setStatus('thinking', 'Thinking');
  document.body.classList.add('thinking');

  const typing = showTyping();

  try {
    const res = await fetch('/api/command', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ command })
    });
    const data = await res.json();
    const responses = data.responses || ['Sorry, no response from the assistant.'];

    typing.remove();
    document.body.classList.remove('thinking');
    responses.forEach((text, i) => addMessage(text, 'assistant', i * 90));
    speak(responses.join('. '));

    if (data.url) {
      setTimeout(() => window.open(data.url, '_blank', 'noopener'), 300);
    }

    setHint('Press the mic and speak, or type a command');
    setStatus(null, 'Idle');
  } catch (err) {
    typing.remove();
    document.body.classList.remove('thinking');
    addMessage('I could not reach the assistant server. Is it running?', 'assistant');
    setHint('Connection error');
    setStatus('offline', 'Offline');
  }
}

function startListening() {
  if (micBtn.classList.contains('listening')) return;
  micBtn.classList.remove('error');

  if (!SpeechRecognition) {
    setHint('Speech recognition is not supported in this browser. Please type your command.');
    micBtn.classList.add('error');
    return;
  }

  const recognition = new SpeechRecognition();
  recognition.lang = 'en-US';
  recognition.interimResults = false;
  recognition.maxAlternatives = 1;

  recognition.onstart = () => {
    micBtn.classList.add('listening');
    document.body.classList.add('listening');
    setHint('Listening... speak your command');
    setStatus('listening', 'Listening');
  };

  recognition.onresult = (event) => {
    sendCommand(event.results[0][0].transcript);
  };

  recognition.onerror = (event) => {
    micBtn.classList.remove('listening');
    document.body.classList.remove('listening');
    setStatus(null, 'Idle');
    if (event.error === 'not-allowed') {
      setHint('Microphone access denied. Allow it in your browser settings.');
      micBtn.classList.add('error');
    } else if (event.error === 'no-speech') {
      setHint('I did not hear anything. Try again.');
    } else {
      setHint(`Could not hear you (${event.error}). Please try again.`);
    }
  };

  recognition.onend = () => {
    micBtn.classList.remove('listening');
    document.body.classList.remove('listening');
    if (!statusPill.classList.contains('thinking')) {
      setStatus(null, 'Idle');
    }
  };

  recognition.start();
}

micBtn.addEventListener('click', startListening);

function submitText() {
  const value = textInput.value.trim();
  if (!value) return;
  sendCommand(value);
  textInput.value = '';
}

sendBtn.addEventListener('click', submitText);
textInput.addEventListener('keydown', (e) => {
  if (e.key === 'Enter') submitText();
});

document.getElementById('chips').addEventListener('click', (e) => {
  const chip = e.target.closest('.chip');
  if (chip) sendCommand(chip.dataset.command);
});

soundBtn.addEventListener('click', () => {
  voiceEnabled = !voiceEnabled;
  soundBtn.classList.toggle('muted', !voiceEnabled);
  soundBtn.setAttribute('aria-pressed', String(voiceEnabled));
  if (!voiceEnabled) window.speechSynthesis.cancel();
  setHint(voiceEnabled ? 'Voice replies on' : 'Voice replies off');
});

clearBtn.addEventListener('click', () => {
  chat.innerHTML = '';
  addMessage('Chat cleared. What can I do for you?', 'welcome');
});

if ('speechSynthesis' in window) {
  window.speechSynthesis.getVoices();
  window.speechSynthesis.onvoiceschanged = () => {};
}
