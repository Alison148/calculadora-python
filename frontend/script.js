// ===== CONFIG =====
const BASE_API = 'http://127.0.0.1:8000';   // se servir o front pelo FastAPI, troque para ''
const CALC_URL = `${BASE_API}/calcular`;
const HIST_URL = `${BASE_API}/historico`;

let modo = 'DEG';
let ultimoResultado = null;
let historico = [];

// ===== HISTÓRICO (API + cache local) =====
async function loadHistoricoAPI() {
  try {
    const res = await fetch(HIST_URL);
    const data = await res.json();
    historico = data.itens || [];
    localStorage.setItem('calc_hist', JSON.stringify(historico));
  } catch {
    // fallback pro cache local
    try { historico = JSON.parse(localStorage.getItem('calc_hist') || '[]'); }
    catch { historico = []; }
  }
}
function updateHistorico() {
  const ul = document.getElementById('historico');
  if (!ul) return;
  ul.innerHTML = '';
  [...historico].slice(-20).reverse().forEach(item => {
    const li = document.createElement('li');
    const when = new Date((item.ts || 0) * 1000).toLocaleString();
    li.textContent = `${item.expressao} = ${item.resultado} (${item.modo}) — ${when}`;
    ul.appendChild(li);
  });
}

function focusTrap() {
  const trap = document.getElementById('trap');
  const disp = document.getElementById('display');
  if (trap) trap.focus();
  if (disp) disp.focus();
}
function append(value) { document.getElementById('display').value += value; }
function backspace() {
  const d = document.getElementById('display');
  d.value = d.value.slice(0, -1);
}
function clearDisplay() { document.getElementById('display').value = ''; }
function toggleMode() {
  modo = modo === 'DEG' ? 'RAD' : 'DEG';
  document.getElementById('mode').innerText = `Modo: ${modo}`;
}
function usarAns() { if (ultimoResultado !== null) append(String(ultimoResultado)); }
function autoClose(expr) {
  const open = (expr.match(/\(/g) || []).length;
  const close = (expr.match(/\)/g) || []).length;
  return expr + ')'.repeat(Math.max(0, open - close));
}

// TECLADO (sem duplicar)
document.addEventListener('keydown', (e) => {
  e.preventDefault();
  const key = e.key;
  if (/^[0-9.+\-*/()^]$/.test(key)) append(key);
  else if (key.toLowerCase() === 's') append('sin(');
  else if (key.toLowerCase() === 'c') append('cos(');
  else if (key.toLowerCase() === 't') append('tan(');
  else if (key.toLowerCase() === 'r') append('sqrt(');
  else if (key === '%') append('%');
  else if (key === 'Backspace') backspace();
  else if (key === 'Escape') clearDisplay();
  else if (key === 'Enter' || key === '=') calcular();
});

// ===== API =====
async function calcular() {
  let expressao = document.getElementById('display').value.trim();
  if (!expressao) return;

  expressao = autoClose(expressao);

  try {
    const res = await fetch(CALC_URL, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ expressao, modo })
    });
    const data = await res.json();
    if (typeof data.resultado !== 'undefined') {
      ultimoResultado = data.resultado;
      document.getElementById('display').value = data.resultado;
      await loadHistoricoAPI(); // recarrega do backend após salvar
      updateHistorico();
    } else {
      document.getElementById('display').value = 'Erro';
      console.error('API error:', data);
    }
  } catch (err) {
    document.getElementById('display').value = 'Erro';
    console.error('Fetch error:', err);
  }
}

async function limparHistorico() {
  try {
    await fetch(HIST_URL, { method: 'DELETE' });
  } catch (e) {
    console.warn('Falha ao limpar no servidor.', e);
  }
  await loadHistoricoAPI();
  updateHistorico();
}

// ===== INIT =====
document.addEventListener('DOMContentLoaded', async () => {
  await loadHistoricoAPI();
  updateHistorico();
  focusTrap();
});
