// DOM Elements
const historyList = document.getElementById('history-list');
const newChatBtn = document.getElementById('new-chat-btn');
const sendBtn = document.getElementById('send-btn');
const userInput = document.getElementById('user-input');
const chatContainer = document.getElementById('chat-container');
const themeToggle = document.getElementById('theme-toggle');
const themeIcon = document.getElementById('theme-icon');
const currentTitle = document.getElementById('current-conversation-title');
const clearHistoryBtn = document.getElementById('clear-history');
const settingsBtn = document.getElementById('settings-btn');

// State
let conversations = JSON.parse(localStorage.getItem('conversations')) || [];
let activeConversationIndex = parseInt(localStorage.getItem('activeConversationIndex')) || null;

// Helper Functions
function el(tag, cls, html) {
  const e = document.createElement(tag);
  if (cls) e.className = cls;
  if (html !== undefined) e.innerHTML = html;
  return e;
}

function nowDate() {
  return new Date().toLocaleString('tr-TR', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  });
}

function escapeHtml(s = '') {
  return String(s)
    .replaceAll('&', '&amp;')
    .replaceAll('<', '&lt;')
    .replaceAll('>', '&gt;')
    .replaceAll('"', '&quot;')
    .replaceAll("'", '&#039;');
}

function saveState() {
  localStorage.setItem('conversations', JSON.stringify(conversations));
  localStorage.setItem('activeConversationIndex', activeConversationIndex);
}

// History Management
function renderHistory() {
  if (!historyList) return;
  historyList.innerHTML = '';

  if (!conversations.length) {
    const emptyState = el('div', 'history-empty', `
      <div style="color:var(--muted);font-size:13px;padding:12px;text-align:center">
        <i class="fas fa-compass" style="font-size:24px;margin-bottom:8px;opacity:0.5"></i>
        <div>Henüz kayıtlı rota yok</div>
      </div>
    `);
    historyList.appendChild(emptyState);
    return;
  }

  conversations.slice().reverse().forEach((conv, i) => {
    const idx = conversations.length - 1 - i;
    const active = idx === activeConversationIndex ? ' active' : '';
    const html = `
      <div class="title">${escapeHtml(conv.title)}</div>
      <div class="meta">${conv.date}</div>
    `;
    const item = el('div', 'history-item' + active, html);
    item.addEventListener('click', () => loadConversation(idx));
    historyList.appendChild(item);
  });
}

function pushMessageToConversation(role, content) {
  if (activeConversationIndex === null) {
    const title = role === 'user'
      ? (content.length > 40 ? content.slice(0, 40) + '…' : content)
      : 'Yeni Rota';
    const conv = {
      title: title || 'Yeni Rota',
      date: nowDate(),
      messages: [{ role, content }]
    };
    conversations.push(conv);
    activeConversationIndex = conversations.length - 1;
  } else {
    conversations[activeConversationIndex].messages.push({ role, content });
    const conv = conversations[activeConversationIndex];

    if ((!conv.title || conv.title === 'Yeni Rota') && conv.messages.length) {
      const firstUser = conv.messages.find(m => m.role === 'user');
      if (firstUser) {
        conv.title = firstUser.content.slice(0, 40) +
                    (firstUser.content.length > 40 ? '…' : '');
      }
    }
    conv.date = nowDate();
  }
  saveState();
  renderHistory();
}

// Chat Rendering
function showZeroState() {
  if (!chatContainer) return;
  chatContainer.innerHTML = `
    <div class="zero-state" role="status" aria-live="polite">
      <div style="font-size:48px;margin-bottom:16px;color:var(--primary);opacity:0.8">
        <i class="fas fa-route"></i>
      </div>
      <h2>TripArchitect'e Hoş Geldiniz</h2>
      <p class="muted">Seyahat planlarınızı anlatın, AI asistanımız sizin için mükemmel rotayı oluştursun.<br>
        Örnek: <em>"Eşimle 2 günlük romantik İstanbul gezisi, boğaz manzaralı restoranlar ile"</em></p>
      <div class="zero-cta">
        <button id="quick-sample" class="primary-btn small">
          <i class="fas fa-lightbulb"></i> Örnek Rota Göster
        </button>
      </div>
    </div>
  `;

  const sampleBtn = document.getElementById('quick-sample');
  if (sampleBtn) {
    sampleBtn.addEventListener('click', () => {
      userInput.value = "Eşimle 2 günlük romantik İstanbul gezisi, boğaz manzaralı restoranlar ile";
      userInput.focus();
    });
  }
}

function appendUserMessage(text, store = true) {
  if (!chatContainer) return;

  const wrap = el('div', 'message user-message');
  const bubble = el('div', 'message-content user-bubble', `
    <div class="msg-text">${escapeHtml(text)}</div>
  `);

  wrap.appendChild(bubble);
  chatContainer.appendChild(wrap);
  chatContainer.scrollTop = chatContainer.scrollHeight;

  if (store) pushMessageToConversation('user', text);
}

function appendBotMessage(html, store = true) {
  if (!chatContainer) return;

  const wrap = el('div', 'message bot-message');
  const bubble = el('div', 'message-content bot-bubble');
  bubble.innerHTML = html;

  wrap.appendChild(bubble);
  chatContainer.appendChild(wrap);
  chatContainer.scrollTop = chatContainer.scrollHeight;

  if (store) pushMessageToConversation('bot', bubble.innerHTML);
}

function loadConversation(idx) {
  const conv = conversations[idx];
  if (!conv) return;

  activeConversationIndex = idx;
  currentTitle.textContent = conv.title || 'Rota';
  chatContainer.innerHTML = '';

  conv.messages.forEach(m => {
    if (m.role === 'user') {
      appendUserMessage(m.content, false);
    } else {
      const msg = el('div', 'message-content bot-bubble');
      msg.innerHTML = m.content;
      appendBotMessage(msg.innerHTML, false);
    }
  });

  saveState();
  renderHistory();
}

// Message Sending
async function sendHandler() {
  const text = (userInput.value || '').trim();
  if (!text) return;

  appendUserMessage(text, true);
  userInput.value = '';

  // Typing indicator
  const typing = el('div', 'typing-indicator', `
    <div class="typing-dot"></div>
    <div class="typing-dot"></div>
    <div class="typing-dot"></div>
  `);
  chatContainer.appendChild(typing);
  chatContainer.scrollTop = chatContainer.scrollHeight;

  try {
    const resp = await fetch('http://127.0.0.1:8000/plan_trip', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text })
    });

    if (!resp.ok) {
      let errText = `API isteği başarısız. Status: ${resp.status}`;
      try {
        const errJson = await resp.json();
        if (errJson.detail) errText += ` — ${errJson.detail}`;
      } catch (e) {}
      throw new Error(errText);
    }

    const data = await resp.json();
    typing.remove();

    // Build bot response card
    let card = `
      <div class="bot-card">
        <div class="bot-card-head">
          <div class="bot-card-title">Oluşturulan Rota</div>
          ${data.days ? `<div class="bot-card-sub">${escapeHtml(String(data.days))} günlük plan</div>` : ''}
        </div>
    `;

    // Map
    if (data.map_url) {
      card += `
        <div class="map-wrap">
          <iframe class="map-frame" src="${escapeHtml(data.map_url)}" frameborder="0" allowfullscreen loading="lazy"></iframe>
          <div class="map-controls">
            <button class="map-btn" title="Yol tarifi al"><i class="fas fa-route"></i></button>
            <button class="map-btn" title="Uydu görünümü"><i class="fas fa-satellite-dish"></i></button>
            <button class="map-btn" title="Yakınlaştır"><i class="fas fa-search-plus"></i></button>
          </div>
        </div>
      `;
    }

    // Plan text
    if (data.plan) {
      card += `
        <div class="section">
          <h4>Plan Özeti</h4>
          <div class="plan-text">${escapeHtml(data.plan).replace(/\n/g, '<br/>')}</div>
        </div>
      `;
    }

    // Timeline
    if (Array.isArray(data.stops_by_day) && data.stops_by_day.length) {
      card += `
        <div class="section">
          <h4>Günlere Göre Rota</h4>
          <div class="timeline">
      `;

      data.stops_by_day.forEach((day, idx) => {
        card += `
          <div class="timeline-day">
            <div class="day-header">
              <span class="day-index">${idx + 1}</span>
              <div class="day-title">${idx + 1}. Gün</div>
            </div>
            <ol class="day-list">
        `;

        day.forEach(place => {
          const poi = (data.pois || []).find(p => p.name === place);
          const desc = poi && poi.description ? poi.description : '';
          card += `
            <li class="place-line">
              <div class="place-name">${escapeHtml(place)}</div>
              <div class="place-snippet">${escapeHtml(desc)}</div>
            </li>
          `;
        });

        card += `
            </ol>
          </div>
        `;
      });

      card += `
          </div>
        </div>
      `;
    }

    // POIs
    if (Array.isArray(data.pois) && data.pois.length) {
      card += `
        <div class="section">
          <h4>Mekanlar</h4>
          <div class="poi-grid">
      `;

      data.pois.forEach(p => {
        const name = escapeHtml(p.name || '');
        const desc = escapeHtml(p.description || '');
        const addr = escapeHtml(p.address || '');

        card += `
          <article class="poi-card">
            <div class="poi-card-head">
              <div class="poi-name">${name}</div>
            </div>
            <div class="poi-desc">${desc}</div>
            ${addr ? `
              <div class="poi-addr">
                <i class="fas fa-map-marker-alt"></i> ${addr}
              </div>
            ` : ''}
          </article>
        `;
      });

      card += `
          </div>
        </div>
      `;
    }

    // Actions
    card += `
      <div class="card-actions">
        <button class="primary-btn" id="save-pdf-btn">
          <i class="fas fa-file-pdf"></i> PDF Olarak Kaydet
        </button>
        <button class="secondary-btn" id="share-route-btn">
          <i class="fas fa-share-alt"></i> Paylaş
        </button>
      </div>
    `;

    card += `</div>`; // Close bot-card
    appendBotMessage(card, true);

    // Add event listeners to new buttons
    setTimeout(() => {
      const pdfBtn = document.getElementById('save-pdf-btn');
      const shareBtn = document.getElementById('share-route-btn');

      if (pdfBtn) {
        pdfBtn.addEventListener('click', () => {
          alert('PDF kaydetme özelliği yakında eklenecek.');
        });
      }

      if (shareBtn) {
        shareBtn.addEventListener('click', () => {
          alert('Paylaşma özelliği yakında eklenecek.');
        });
      }
    }, 200);

  } catch (err) {
    if (typing && typing.remove) typing.remove();
    appendBotMessage(`
      <div class="error">
        <i class="fas fa-exclamation-circle"></i> Bir hata oluştu: ${escapeHtml(err.message || String(err))}
      </div>
    `, true);
    console.error(err);
  }
}

// Event Listeners
if (sendBtn) sendBtn.addEventListener('click', sendHandler);

if (userInput) {
  userInput.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendHandler();
    }
  });

  // Auto-resize textarea
  userInput.addEventListener('input', () => {
    userInput.style.height = 'auto';
    userInput.style.height = Math.min(userInput.scrollHeight, 180) + 'px';
  });
}

newChatBtn?.addEventListener('click', () => {
  activeConversationIndex = null;
  currentTitle.textContent = 'Yeni Rota';
  showZeroState();
  saveState();
});

clearHistoryBtn?.addEventListener('click', () => {
  if (!confirm('Tüm geçmiş rotaları silmek istediğinizden emin misiniz?')) return;
  conversations = [];
  activeConversationIndex = null;
  showZeroState();
  saveState();
  renderHistory();
});

settingsBtn?.addEventListener('click', () => {
  alert('Ayarlar menüsü yakında eklenecek.');
});

// Theme Toggle
themeToggle?.addEventListener('click', () => {
  document.documentElement.classList.toggle('dark');
  const isDark = document.documentElement.classList.contains('dark');
  themeIcon.className = isDark ? 'fas fa-sun' : 'fas fa-moon';
  localStorage.setItem('theme', isDark ? 'dark' : 'light');
});

// Initialize
function init() {
  // Load theme preference
  if (localStorage.getItem('theme') === 'dark' ||
      (window.matchMedia('(prefers-color-scheme: dark)').matches && !localStorage.getItem('theme'))) {
    document.documentElement.classList.add('dark');
    themeIcon.className = 'fas fa-sun';
  }

  // Load conversation if exists
  if (activeConversationIndex !== null && conversations[activeConversationIndex]) {
    loadConversation(activeConversationIndex);
  } else {
    showZeroState();
  }

  renderHistory();
}

init();

// For debugging
window._TA = {
  conversations,
  loadConversation,
  renderHistory,
  clearHistory: () => {
    conversations = [];
    activeConversationIndex = null;
    saveState();
    renderHistory();
    showZeroState();
  }
};