// frontend/app.js
// Revize edilmiş, premium UI uyumlu frontend logic.
// Endpoint: POST http://127.0.0.1:8000/plan_trip
// Beklenen response: { map_url, plan, days, stops_by_day, pois }

const historyList = document.getElementById('history-list');
const newChatBtn = document.getElementById('new-chat-btn');
const sendBtn = document.getElementById('send-btn');
const userInput = document.getElementById('user-input');
const chatContainer = document.getElementById('chat-container');
const themeToggle = document.getElementById('theme-toggle');
const themeIcon = document.getElementById('theme-icon');
const currentTitle = document.getElementById('current-conversation-title');
const clearHistoryBtn = document.getElementById('clear-history');

let conversations = []; // { title, date, messages: [{role, content}] }
let activeConversationIndex = null;

function el(tag, cls, html){
  const e = document.createElement(tag);
  if (cls) e.className = cls;
  if (html !== undefined) e.innerHTML = html;
  return e;
}

function nowDate(){ return new Date().toLocaleString(); }

function escapeHtml(s = ''){
  return String(s)
    .replaceAll('&','&amp;')
    .replaceAll('<','&lt;')
    .replaceAll('>','&gt;');
}

/* ---------- History / UI helpers ---------- */
function renderHistory(){
  if (!historyList) return;
  historyList.innerHTML = '';
  if (!conversations.length){
    const p = el('div','history-empty','<div style="color:var(--muted);font-size:13px;padding:12px;text-align:center">Henüz kayıtlı rota yok. Yeni Rota başlatın.</div>');
    historyList.appendChild(p);
    return;
  }
  conversations.slice().reverse().forEach((conv, i) => {
    const idx = conversations.length - 1 - i;
    const active = (idx === activeConversationIndex) ? ' active' : '';
    const html = `<div class="title">${escapeHtml(conv.title)}</div><div class="meta">${conv.date}</div>`;
    const d = el('div','history-item'+active, html);
    d.addEventListener('click', ()=> loadConversation(idx));
    historyList.appendChild(d);
  });
}

function pushMessageToConversation(role, content){
  if (activeConversationIndex === null){
    const title = role === 'user' ? (content.length > 40 ? content.slice(0,40)+'…' : content) : 'Yeni Rota';
    const conv = { title: title || 'Yeni Rota', date: nowDate(), messages: [{role, content}] };
    conversations.push(conv);
    activeConversationIndex = conversations.length - 1;
  } else {
    conversations[activeConversationIndex].messages.push({role, content});
    // update title if needed
    const conv = conversations[activeConversationIndex];
    if ((!conv.title || conv.title === 'Yeni Rota') && conv.messages.length){
      const firstUser = conv.messages.find(m=>m.role==='user');
      if (firstUser) conv.title = firstUser.content.slice(0,40) + (firstUser.content.length>40?'…':'');
    }
    conv.date = nowDate();
  }
  renderHistory();
}

/* ---------- Chat rendering ---------- */
function showZeroState(){
  if (!chatContainer) return;
  chatContainer.innerHTML = `
    <div class="zero-state" role="status" aria-live="polite">
      <h2>Hoş geldiniz — TripArchitect</h2>
      <p class="muted">Serbest metin girin. Örnek: <em>"Nilüfer'den Mudanya'ya 1 günlük rota, 5 durak, deniz kenarında öğle molası"</em></p>
      <div class="zero-cta">
        <button id="quick-sample" class="primary-btn small">Örnek Rota Başlat</button>
      </div>
    </div>
  `;
  const sample = document.getElementById('quick-sample');
  if (sample) sample.addEventListener('click', ()=> {
    userInput.value = "Nilüfer'den Mudanya'ya 1 günlük rota, 5 durak, deniz kenarında öğle molası istiyorum.";
    userInput.focus();
  });
}

function appendUserMessage(text, store=true){
  if (!chatContainer) return;
  const wrap = el('div','message user-message');
  const bubble = el('div','message-content user-bubble', `<div class="msg-text">${escapeHtml(text)}</div>`);
  wrap.appendChild(bubble);
  chatContainer.appendChild(wrap);
  chatContainer.scrollTop = chatContainer.scrollHeight;
  if (store) pushMessageToConversation('user', text);
}

function appendBotMessage(html, store=true){
  if (!chatContainer) return;
  const wrap = el('div','message bot-message');
  const bubble = el('div','message-content bot-bubble');
  bubble.innerHTML = html;
  wrap.appendChild(bubble);
  chatContainer.appendChild(wrap);
  chatContainer.scrollTop = chatContainer.scrollHeight;
  if (store) pushMessageToConversation('bot', html);
}

/* load a stored conversation */
function loadConversation(idx){
  const conv = conversations[idx];
  if (!conv) return;
  activeConversationIndex = idx;
  currentTitle.innerText = conv.title || 'Rota';
  chatContainer.innerHTML = '';
  conv.messages.forEach(m => {
    if (m.role === 'user') appendUserMessage(m.content, false);
    else appendBotMessage(m.content, false);
  });
  renderHistory();
}

/* ---------- Main send handler (keeps backend API same) ---------- */
if (sendBtn) sendBtn.addEventListener('click', sendHandler);
if (userInput) {
  userInput.addEventListener('keydown', (e)=>{
    if (e.key === 'Enter' && !e.shiftKey){
      e.preventDefault();
      sendHandler();
    }
  });
}

async function sendHandler(){
  const text = (userInput.value || '').trim();
  if (!text) return;
  appendUserMessage(text, true);
  userInput.value = '';

  // typing indicator
  const typing = el('div','typing-indicator','<div class="typing-dot"></div><div class="typing-dot"></div><div class="typing-dot"></div>');
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
      try { const errJson = await resp.json(); if (errJson.detail) errText += ` — ${errJson.detail}`; } catch(e){}
      throw new Error(errText);
    }

    const data = await resp.json();
    typing.remove();

    // BUILD PREMIUM BOT CARD
    let card = '';

    // Header info
    card += `<div class="bot-card">`;
    card += `<div class="bot-card-head"><div class="bot-card-title">Oluşturulan Rota</div>`;
    if (data.days) card += `<div class="bot-card-sub">${escapeHtml(String(data.days))} günlük plan</div>`;
    card += `</div>`;

    // Map
    if (data.map_url) {
      card += `<div class="map-wrap"><iframe class="map-frame" src="${escapeHtml(data.map_url)}" frameborder="0" allowfullscreen="" loading="lazy"></iframe></div>`;
    }

    // Plan text
    if (data.plan) {
      card += `<div class="section"><h4>Plan Özeti</h4><div class="plan-text">${escapeHtml(data.plan).replace(/\n/g,'<br/>')}</div></div>`;
    }

    // Timeline & POIs
    if (Array.isArray(data.stops_by_day) && data.stops_by_day.length){
      card += `<div class="section"><h4>Günlere Göre Rota</h4><div class="timeline">`;
      data.stops_by_day.forEach((day, idx) => {
        card += `<div class="timeline-day"><div class="day-header"><span class="day-index">${idx+1}</span><div class="day-title">${idx+1}. Gün</div></div><ol class="day-list">`;
        day.forEach(place => {
          // find matching poi description
          const poi = (data.pois || []).find(p => p.name === place);
          const desc = poi && poi.description ? poi.description : '';
          card += `<li class="place-line"><div class="place-name">${escapeHtml(place)}</div><div class="place-snippet">${escapeHtml(desc)}</div></li>`;
        });
        card += `</ol></div>`;
      });
      card += `</div></div>`; // timeline + section
    }

    // POI Cards (grid)
    if (Array.isArray(data.pois) && data.pois.length){
      card += `<div class="section"><h4>Mekanlar</h4><div class="poi-grid">`;
      data.pois.forEach(p => {
        const name = escapeHtml(p.name || '');
        const desc = escapeHtml(p.description || '');
        const addr = escapeHtml(p.address || '');
        card += `
          <article class="poi-card">
            <div class="poi-card-head"><div class="poi-name">${name}</div></div>
            <div class="poi-desc">${desc}</div>
            ${addr ? `<div class="poi-addr">${addr}</div>` : ''}
          </article>
        `;
      });
      card += `</div></div>`;
    }

    // Actions
    card += `<div class="card-actions"><button class="primary-btn">⭐ Favorilere Ekle</button><button class="secondary-btn" id="save-route-btn">İndir / Paylaş</button></div>`;

    card += `</div>`; // bot-card

    appendBotMessage(card, true);

    // wire up save button (optional)
    setTimeout(()=> {
      const saveBtn = document.getElementById('save-route-btn');
      if (saveBtn) saveBtn.addEventListener('click', ()=> {
        alert('Rota paylaşma / indirme özelliği yakında eklenecek.');
      });
    }, 200);

  } catch (err) {
    if (typing && typing.remove) typing.remove();
    appendBotMessage(`<div class="error">Bir hata oluştu: ${escapeHtml(err.message || String(err))}</div>`, true);
    console.error(err);
  }
}

/* ---------- Misc ---------- */
clearHistoryBtn?.addEventListener('click', ()=>{
  if (!confirm('Tüm geçmiş rotaları silmek istediğinizden emin misiniz?')) return;
  conversations = [];
  activeConversationIndex = null;
  showZeroState();
  renderHistory();
});

function init(){
  showZeroState();
  renderHistory();
  if (userInput) userInput.value = '';
}
init();

/* expose for debugging */
window._TA = { conversations, loadConversation, renderHistory };