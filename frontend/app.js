// frontend/app.js
// Modernized frontend behavior (connected to backend /plan_trip)

const historyList = document.getElementById('history-list');
const newChatBtn = document.getElementById('new-chat-btn');
const sendBtn = document.getElementById('send-btn');
const userInput = document.getElementById('user-input');
const chatContainer = document.getElementById('chat-container');
const themeToggle = document.getElementById('theme-toggle');
const themeIcon = document.getElementById('theme-icon');
const currentTitle = document.getElementById('current-conversation-title');
const clearHistoryBtn = document.getElementById('clear-history');

let conversations = []; // each: { title, date, messages: [{role:'user'|'bot', content: string}] }
let activeConversationIndex = null; // null => a fresh unsaved conversation shown in UI

/* UTIL */
function el(tag, cls, html){
  const e = document.createElement(tag);
  if (cls) e.className = cls;
  if (html) e.innerHTML = html;
  return e;
}
function nowDate(){ return new Date().toLocaleString(); }

/* RENDER: history list */
function renderHistory(){
  if (!historyList) return;
  historyList.innerHTML = '';
  if (conversations.length === 0){
    const p = el('div','history-empty','<div style="color:var(--muted);font-size:13px;padding:12px;text-align:center">Henüz kayıtlı rota yok. Yeni Rota başlatın.</div>');
    historyList.appendChild(p);
    return;
  }
  conversations.slice().reverse().forEach((conv, i)=> {
    const idx = conversations.length - 1 - i;
    const div = el('div','history-item',`<div class="title">${escapeHtml(conv.title)}</div><div class="meta">${conv.date}</div>`);
    if (idx === activeConversationIndex) div.classList.add('active');
    div.addEventListener('click', ()=> loadConversation(idx));
    historyList.appendChild(div);
  });
}

/* ESCAPE */
function escapeHtml(s = ''){
  return String(s).replaceAll('&','&amp;').replaceAll('<','&lt;').replaceAll('>','&gt;');
}

/* load conversation by index */
function loadConversation(idx){
  const conv = conversations[idx];
  if (!conv) return;
  activeConversationIndex = idx;
  currentTitle.innerText = conv.title || 'Rota';
  renderChatFromMessages(conv.messages || []);
  renderHistory();
}

/* render chat container from messages array */
function renderChatFromMessages(messages){
  if (!chatContainer) return;
  chatContainer.innerHTML = '';
  if (!messages || messages.length === 0){
    showZeroState();
    return;
  }
  messages.forEach(m=>{
    if (m.role === 'user') appendUserMessage(m.content, false);
    else appendBotMessage(m.content, false);
  });
  chatContainer.scrollTop = chatContainer.scrollHeight;
}

/* messages append - optionally store to current unsaved conversation */
function appendUserMessage(text, store=true){
  if (!chatContainer) return;
  const m = el('div','message user-message');
  const c = el('div','message-content');
  c.innerText = text;
  m.appendChild(c);
  chatContainer.appendChild(m);
  chatContainer.scrollTop = chatContainer.scrollHeight;
  if (store) pushMessageToConversation('user', text);
}
function appendBotMessage(html, store=true){
  if (!chatContainer) return;
  const m = el('div','message bot-message');
  const c = el('div','message-content');
  c.innerHTML = html;
  m.appendChild(c);
  chatContainer.appendChild(m);
  chatContainer.scrollTop = chatContainer.scrollHeight;
  if (store) pushMessageToConversation('bot', html);
}

/* push message to currently active conversation or to a temp unsaved conversation */
function pushMessageToConversation(role, content){
  if (activeConversationIndex === null){
    const title = content.length > 40 ? content.slice(0,40) + '…' : content;
    const conv = { title: title || 'Yeni Rota', date: nowDate(), messages: [{role, content}] };
    conversations.push(conv);
    activeConversationIndex = conversations.length - 1;
    currentTitle.innerText = conv.title;
    renderHistory();
  } else {
    conversations[activeConversationIndex].messages.push({role, content});
    if (!conversations[activeConversationIndex].title || conversations[activeConversationIndex].title === 'Yeni Rota'){
      const firstUser = conversations[activeConversationIndex].messages.find(m=>m.role==='user');
      if (firstUser) conversations[activeConversationIndex].title = firstUser.content.slice(0,40) + (firstUser.content.length>40?'…':'');
      conversations[activeConversationIndex].date = nowDate();
      renderHistory();
    }
  }
}

/* show zero-state welcome */
function showZeroState(){
  if (!chatContainer) return;
  chatContainer.innerHTML = `
    <div class="zero-state" role="status" aria-live="polite">
      <h2>Hoş geldiniz — Profesyonel Rota Planlayıcınız</h2>
      <p>Yeni bir rota başlatmak için <strong>Yeni Rota</strong> butonuna tıklayın veya planınızı yazıp gönderin. Örnek: <em>2 günlük İstanbul gezisi; tarihi yerler ve kafe önerileri</em></p>
      <div class="zero-cta">
        <button id="quick-sample" class="primary-btn" style="width:auto;padding:10px 14px">Örnek Rota Başlat</button>
        <button id="clear-view" class="tiny-btn" style="align-self:center">Gizli ipuçları göster</button>
      </div>
    </div>
  `;
  const sample = document.getElementById('quick-sample');
  if (sample) sample.addEventListener('click', ()=> {
    userInput.value = '2 günlük İstanbul gezisi; tarihi yerler, uygun oteller ve güzel kafeler öner.';
    userInput.focus();
  });
}

/* ACTIONS */
if (newChatBtn) {
  newChatBtn.addEventListener('click', ()=>{
    activeConversationIndex = null;
    currentTitle.innerText = 'Yeni Rota';
    userInput.value = '';
    showZeroState();
    renderHistory();
    userInput.focus();
  });
}

if (sendBtn) sendBtn.addEventListener('click', sendHandler);

/* Main: sends the user's text to backend /plan_trip and renders response */
async function sendHandler(){
  const text = userInput.value.trim();
  if (!text) return;

  appendUserMessage(text, true);
  userInput.value = '';

  // typing indicator
  const typing = document.createElement('div');
  typing.className = 'typing';
  typing.style.padding = '10px';
  typing.innerHTML = '<div class="typing-dot"></div><div class="typing-dot"></div><div class="typing-dot"></div>';
  chatContainer.appendChild(typing);
  chatContainer.scrollTop = chatContainer.scrollHeight;

  try {
    const resp = await fetch('http://localhost:8000/plan_trip', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text })
    });
    if (!resp.ok) {
      let errText = `API isteği başarısız oldu. Status: ${resp.status}`;
      try { const errJson = await resp.json(); if (errJson.detail) errText += ` — ${errJson.detail}`; } catch(e){}
      throw new Error(errText);
    }
    const data = await resp.json();

    typing.remove();

    // Oteller
    let hotelsHtml = '';
    if (data.hotels && data.hotels.length > 0) {
      hotelsHtml = `<h3>Önerilen Oteller</h3><ul>` +
        data.hotels.map(h => `<li><strong>${escapeHtml(h.name)}</strong>${h.address? ' - ' + escapeHtml(h.address): ''}</li>`).join('') +
        `</ul>`;
    }

    // POI
    let poisHtml = '';
    if (data.pois && data.pois.length > 0) {
      poisHtml = `<h3>Gezilecek Yerler</h3><ul>` +
        data.pois.map(p => `<li><strong>${escapeHtml(p.name)}</strong>${p.address? ' - ' + escapeHtml(p.address): ''}</li>`).join('') +
        `</ul>`;
    }

    // Description (safe-escaped)
    const descriptionHtml = data.description ? `<div class="description">${escapeHtml(data.description).replace(/\n/g,'<br/>')}</div>` : '';

    // Map: backend returns an embed URL (google maps embed). Use iframe when provided, else an <img>.
    let mapEmbedHtml = '';
    if (data.map_url) {
      // if map_url looks like a full embed URL, use iframe
      if (data.map_url.includes("/maps/embed") || data.map_url.includes("embed/v1")) {
        mapEmbedHtml = `<div class="map-embed" role="img" aria-label="Harita önizlemesi">
            <iframe src="${data.map_url}" style="width:100%;height:400px;border:0" allowfullscreen="" loading="lazy"></iframe>
          </div>`;
      } else {
        mapEmbedHtml = `<div class="map-embed"><img src="${data.map_url}" style="width:100%;height:400px;object-fit:cover" alt="map"/></div>`;
      }
    }

    const botHtml = `
      <div><strong>Plan Açıklaması:</strong></div>
      ${descriptionHtml}
      ${mapEmbedHtml}
      ${hotelsHtml}
      ${poisHtml}
      <div style="margin-top:10px;display:flex;gap:10px">
        <button class="primary-btn" onclick="favoritePlan()">⭐ Favorilere Ekle</button>
        <button class="icon-btn" style="background:transparent;border:1px solid rgba(255,255,255,0.06);padding:8px;border-radius:10px" onclick="editPlan()">✏️ Rotayı Düzenle</button>
      </div>
    `;

    appendBotMessage(botHtml, true);

  } catch (err) {
    if (typing && typing.remove) typing.remove();
    appendBotMessage("Bir hata oluştu: " + escapeHtml(err.message || String(err)), true);
    console.error(err);
  }
}

/* small global funcs for inline buttons */
window.favoritePlan = ()=> alert('Favorilere eklendi!');
window.editPlan = ()=> alert('Rota düzenleme modalı (örnek).');

/* history clear */
clearHistoryBtn?.addEventListener('click', ()=>{
  if (!confirm('Tüm geçmiş rotaları silmek istediğinizden emin misiniz?')) return;
  conversations = [];
  activeConversationIndex = null;
  showZeroState();
  renderHistory();
});

/* theme toggle with persistence */
function setTheme(dark){
  if (dark) document.documentElement.classList.add('dark');
  else document.documentElement.classList.remove('dark');
  if (themeIcon) themeIcon.className = dark ? 'fas fa-sun' : 'fas fa-moon';
  try { localStorage.setItem('ta_theme_dark', dark ? '1' : '0'); } catch(e){}
}
if (themeToggle) {
  themeToggle.addEventListener('click', ()=>{
    const isDark = document.documentElement.classList.toggle('dark');
    if (themeIcon) themeIcon.className = isDark ? 'fas fa-sun' : 'fas fa-moon';
    try { localStorage.setItem('ta_theme_dark', isDark ? '1' : '0'); } catch(e){}
  });
}
try {
  const saved = localStorage.getItem('ta_theme_dark');
  if (saved === '1') setTheme(true);
  else setTheme(false);
} catch(e){}

/* textarea: auto-resize & enter handling */
if (userInput) {
  userInput.addEventListener('input', ()=> {
    userInput.style.height = 'auto';
    userInput.style.height = (userInput.scrollHeight) + 'px';
  });
  userInput.addEventListener('keydown', (e)=>{
    if (e.key === 'Enter' && !e.shiftKey){
      e.preventDefault();
      sendHandler();
    }
  });
}

/* helper to render initial zero state on load */
function init(){
  showZeroState();
  renderHistory();
  if (userInput) {
    userInput.style.height = '42px';
    userInput.value = '';
  }
}
init();

/* expose for debugging */
window._TA = {conversations, loadConversation, renderHistory};
