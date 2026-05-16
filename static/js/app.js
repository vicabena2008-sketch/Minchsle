const API = {
  respond: '/api/respond',
  newSession: '/api/new_session',
  clear: '/api/clear',
};

let sessionId = localStorage.getItem('ca_ai_session') || null;
let isAutoScroll = true;

async function ensureSession() {
  if (sessionId) return sessionId;
  const res = await fetch(API.newSession, { method: 'POST' });
  const j = await res.json();
  sessionId = j.session_id;
  localStorage.setItem('ca_ai_session', sessionId);
  return sessionId;
}

const chatEl = document.getElementById('chat');
const heroEl = document.getElementById('hero');
const messageInp = document.getElementById('message');
const sendBtn = document.getElementById('sendBtn');
const clearBtn = document.getElementById('clearBtn');

function addMessage(text, role, imageUrl = null) {
  heroEl.style.display = 'none';
  chatEl.style.display = 'flex';

  const row = document.createElement('div');
  row.className = 'message-row';
  
  const msg = document.createElement('div');
  msg.className = `message ${role}`;

  if (role === 'bot') {
    const textDiv = document.createElement('div');
    textDiv.className = 'bot-text';
    msg.appendChild(textDiv);
    
    if (imageUrl) {
      const card = document.createElement('div');
      card.className = 'product-card';
      const img = document.createElement('img');
      img.src = imageUrl;
      img.className = 'product-image';
      const info = document.createElement('div');
      info.className = 'product-info';
      info.innerHTML = '<strong>In Stock</strong><p>Verified Christian Agyapong Sales Item</p>';
      card.appendChild(img);
      card.appendChild(info);
      msg.insertBefore(card, textDiv);
    }
  } else {
    msg.textContent = text;
  }

  row.appendChild(msg);
  chatEl.appendChild(row);
  chatScroll();
  return msg;
}

function showTyping() {
  const row = document.createElement('div');
  row.className = 'message-row typing-row';
  row.innerHTML = `
    <div class="message bot">
      <div class="typing">
        <div class="dot"></div>
        <div class="dot"></div>
        <div class="dot"></div>
      </div>
    </div>
  `;
  chatEl.appendChild(row);
  chatScroll();
}

function hideTyping() {
  const row = document.querySelector('.typing-row');
  if (row) row.remove();
}

async function typeMessage(container, text) {
  const textDiv = container.querySelector('.bot-text');
  let i = 0;
  const speed = 20; 
  
  return new Promise((resolve) => {
    function next() {
      if (i < text.length) {
        const chunk = text.slice(i, i + 3);
        textDiv.textContent += chunk;
        i += 3;
        if (isAutoScroll) window.scrollTo({ top: document.body.scrollHeight, behavior: 'auto' });
        setTimeout(next, speed);
      } else {
        resolve();
      }
    }
    next();
  });
}

async function handleSend() {
  const text = messageInp.value.trim();
  if (!text) return;

  const sid = await ensureSession();
  messageInp.value = '';
  messageInp.style.height = 'auto';

  addMessage(text, 'user');
  showTyping();

  try {
    const res = await fetch(API.respond, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message: text, session_id: sid })
    });
    const j = await res.json();
    
    hideTyping();
    const botMsg = addMessage('', 'bot', j.image_url);
    await typeMessage(botMsg, j.reply);
  } catch (e) {
    hideTyping();
    addMessage("I'm sorry, I encountered an error. Please try again.", 'bot');
  }
}

function chatScroll() {
  const threshold = 150;
  const position = window.innerHeight + window.scrollY;
  const height = document.body.scrollHeight;
  isAutoScroll = (height - position) < threshold;
  
  if (isAutoScroll) {
    window.scrollTo({ top: height, behavior: 'smooth' });
  }
}

sendBtn.onclick = handleSend;
messageInp.onkeydown = (e) => {
  if (e.key === 'Enter' && !e.shiftKey) {
    e.preventDefault();
    handleSend();
  }
};

clearBtn.onclick = async () => {
  if (!sessionId) return;
  await fetch(API.clear, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ session_id: sessionId })
  });
  chatEl.innerHTML = '';
  chatEl.style.display = 'none';
  heroEl.style.display = 'flex';
};

// Textarea auto-resize
messageInp.oninput = () => {
  messageInp.style.height = 'auto';
  messageInp.style.height = messageInp.scrollHeight + 'px';
};

lucide.createIcons();
