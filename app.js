const API_BASE = "http://127.0.0.1:8000";
let selectedTask = "auto";
document.querySelectorAll(".task").forEach(btn => btn.addEventListener("click", () => {
  document.querySelectorAll(".task").forEach(x => x.classList.remove("selected"));
  btn.classList.add("selected"); selectedTask = btn.dataset.task;
}));
const result = document.getElementById("result");
const statusEl = document.getElementById("result-status");
const submit = document.getElementById("submit-btn");
async function checkHealth(){
  try{
    const r=await fetch(`${API_BASE}/api/health`); const d=await r.json();
    document.getElementById("mode-label").textContent=d.mode==="demo"?"DEMO MODE":"STRANDS + BEDROCK";
  }catch(e){document.getElementById("mode-label").textContent="API OFFLINE";}
}
function escapeHtml(s){return s.replace(/[&<>"']/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));}
function basicMarkdown(s){
  return escapeHtml(s).replace(/^### (.*)$/gm,"<h3>$1</h3>").replace(/^## (.*)$/gm,"<h2>$1</h2>")
    .replace(/\*\*(.*?)\*\*/g,"<strong>$1</strong>").replace(/\n\n/g,"</p><p>").replace(/\n/g,"<br>");
}
submit.addEventListener("click",async()=>{
  const question=document.getElementById("question").value.trim();
  if(question.length<3){alert("Please enter a question or topic first.");return;}
  submit.disabled=true; submit.textContent="Your agents are working...";
  statusEl.textContent="WORKING";
  result.className="result-content";
  result.innerHTML='<div class="empty-art"><div class="empty-ring">✦</div></div><h3>Coordinating your AI team...</h3><p>Finding the best way to help you learn.</p>';
  try{
    const response=await fetch(`${API_BASE}/api/learn`,{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({
      question,subject:document.getElementById("subject").value,
      level:document.getElementById("level").value,language:"English",task:selectedTask
    })});
    const data=await response.json();
    if(!response.ok) throw new Error(data.detail||"Request failed");
    result.className="result-content has-answer";
    result.innerHTML=`<p>${basicMarkdown(data.answer)}</p>`;
    statusEl.textContent=data.mode==="demo"?"DEMO RESULT":"AGENTS COMPLETE";
    document.querySelectorAll(".activity-row small").forEach(x=>x.textContent=data.mode==="demo"?"SIMULATED":"ACTIVE");
  }catch(err){
    result.className="result-content";result.innerHTML=`<h3>We couldn't connect</h3><p>${escapeHtml(err.message)}<br>Start the FastAPI backend and try again.</p>`;
    statusEl.textContent="CONNECTION ERROR";
  }finally{submit.disabled=false;submit.innerHTML='Build my learning session <span>→</span>';}
});
document.getElementById("lang-btn").addEventListener("click",()=>alert("Arabic UI localization is a planned next step. The learning API already accepts Arabic as the response language."));
checkHealth();