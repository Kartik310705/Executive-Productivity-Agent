
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from agent import InternalServiceAgent, REQUESTS, TICKETS

app=FastAPI(title="Veridian Internal Service Agent")
agent=InternalServiceAgent()

HTML = r"""<!doctype html>
<html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Veridian • Internal Service Agent</title>
<style>
body{font-family:Inter,Arial,sans-serif;margin:0;background:#f4f6fb;color:#182033}
.header{background:#111b36;color:#fff;padding:18px 28px;display:flex;justify-content:space-between;align-items:center}
.brand{font-weight:800;font-size:20px}.badge{font-size:12px;padding:7px 10px;border:1px solid #657092;border-radius:20px}
.wrap{max-width:1180px;margin:24px auto;padding:0 18px}.grid{display:grid;grid-template-columns:1.1fr .9fr;gap:18px}
.card{background:white;border-radius:14px;padding:18px;box-shadow:0 4px 18px #17203b12;margin-bottom:18px}
h2{margin:0 0 12px;font-size:18px}.muted{color:#65708a;font-size:13px}
textarea,input,select{width:100%;box-sizing:border-box;border:1px solid #d8ddeb;border-radius:10px;padding:11px;margin-top:7px;font-size:14px}
button{background:#3157d5;color:#fff;border:0;border-radius:10px;padding:11px 15px;margin-top:10px;font-weight:700;cursor:pointer}
button.alt{background:#eef1ff;color:#2947b0}.row{display:flex;gap:8px;align-items:center}.chips span{display:inline-block;background:#eef1ff;color:#2947b0;padding:5px 8px;border-radius:12px;margin:3px;font-size:12px}
.result{border-left:4px solid #3157d5;padding:12px;background:#f8f9fd;border-radius:8px}.danger{border-left-color:#c0392b}.success{border-left-color:#27844a}.warn{border-left-color:#b27a00}
.kv{display:grid;grid-template-columns:120px 1fr;gap:6px;font-size:13px}.kv b{color:#5d6880}
.source{border:1px solid #e0e4ee;border-radius:8px;padding:9px;margin-top:7px;font-size:12px}.source b{color:#2947b0}
table{width:100%;border-collapse:collapse;font-size:12px}th,td{text-align:left;padding:8px;border-bottom:1px solid #edf0f5;vertical-align:top}th{color:#5c6680}
.smallbtn{padding:6px 8px;font-size:11px;margin:0}.footer{text-align:center;color:#7a8398;font-size:11px;margin:22px}
@media(max-width:850px){.grid{grid-template-columns:1fr}}
</style></head>
<body>
<div class="header"><div class="brand">Veridian Corp — Internal Service Agent</div><div class="badge">Policy-grounded • Audited</div></div>
<div class="wrap">
<div class="grid">
<div>
<div class="card"><h2>Ask the IT Agent</h2><div class="muted">Describe an employee issue. The agent retrieves relevant policy, decides whether to resolve/ask/escalate, and creates a structured ticket when needed.</div>
<textarea id="q" rows="5" placeholder="Example: My VPN stopped working and says my credentials expired."></textarea>
<div class="row"><input id="emp" placeholder="Employee name (optional)" style="flex:1"><button onclick="ask()">Run agent</button></div>
<div class="chips"><span onclick="fill('My VPN stopped working, credentials expired.')">VPN</span><span onclick="fill('I think I got a phishing email asking for my login.')">Phishing</span><span onclick="fill('Can I get Wi-Fi access for a guest tomorrow?')">Guest Wi-Fi</span><span onclick="fill('My laptop won’t turn on at all, it is completely dead.')">Laptop</span><span onclick="fill('hey can you help, its not working')">Ambiguous</span></div></div>
<div class="card"><h2>Agent result</h2><div id="out" class="muted">Run a request to see the decision, source policy, precedent and audit event.</div></div>
</div>
<div>
<div class="card"><h2>Scenario tester</h2><div class="muted">Click any supplied employee request to test the same workflow.</div><table><thead><tr><th>ID</th><th>Employee</th><th>Issue</th><th></th></tr></thead><tbody id="reqs"></tbody></table></div>
<div class="card"><h2>Design principles</h2><div class="kv"><b>Grounding</b><span>Only supplied policy/ticket data</span><b>Risk</b><span>Security and unclear authority are escalated</span><b>Traceability</b><span>Every decision writes an audit event</span><b>Human-in-loop</b><span>Unclear ownership/authority is not invented</span></div></div>
</div></div>
<div class="footer">Assignment 2 • Veridian Corp • Data Pack week: 21–25 Sep 2026</div>
</div>
<script>
const reqs=__REQS__;
document.getElementById('reqs').innerHTML=reqs.map(r=>`<tr><td>${r.id}</td><td>${r.employee}</td><td>${r.request}</td><td><button class="smallbtn alt" onclick="runReq('${r.id}')">Test</button></td></tr>`).join('');
function fill(t){document.getElementById('q').value=t}
async function runReq(id){const x=await fetch('/request/'+id,{method:'POST'});show(await x.json())}
async function ask(){const q=document.getElementById('q').value;if(!q.trim())return;const x=await fetch('/ask',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({text:q,employee:document.getElementById('emp').value})});show(await x.json())}
function show(d){
 let cls=d.risk==='High'?'danger':d.decision==='resolve'?'success':d.decision==='follow_up'?'warn':'';
 let html=`<div class="result ${cls}"><div class="kv"><b>Intent</b><span>${d.intent}</span><b>Decision</b><span><strong>${d.decision}</strong> → ${d.route}</span><b>Risk</b><span>${d.risk} | Priority: ${d.priority}</span></div><hr><div>${d.response}</div>`;
 if(d.ticket) html+=`<hr><b>Structured ticket created</b><div class="source">${d.ticket.ticket_id} • ${d.ticket.route} • ${d.ticket.priority}</div>`;
 if(d.follow_up) html+=`<hr><b>Follow-up required:</b> ${d.follow_up}`;
 html+=`<hr><b>Sources used</b>`;
 (d.sources||[]).forEach(s=>html+=`<div class="source"><b>${s.id} — ${s.title}</b><br>${s.text}<br><span class="muted">retrieval score: ${s.score}</span></div>`);
 if((d.precedents||[]).length){html+=`<hr><b>Ticket precedent</b>`;d.precedents.forEach(t=>html+=`<div class="source">${t.id} — ${t.issue} — ${t.status}</div>`)}
 html+=`</div>`;document.getElementById('out').innerHTML=html
}
</script></body></html>"""

class Ask(BaseModel):
    text:str
    employee:str=""

@app.get("/",response_class=HTMLResponse)
def home():
    return HTML.replace("__REQS__",repr(REQUESTS).replace("'",'"'))

@app.post("/ask")
def ask(body:Ask):
    return agent.handle(body.text,body.employee)

@app.post("/request/{req_id}")
def request(req_id:str):
    result=agent.handle_request_id(req_id)
    return result or {"error":"Unknown request ID"}

@app.get("/health")
def health(): return {"status":"ok","agent":"Veridian Internal Service Agent"}

@app.get("/audit")
def audit(): return agent.audit

@app.get("/tickets")
def tickets(): return TICKETS
