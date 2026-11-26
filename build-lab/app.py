import streamlit as st
from datetime import date

st.set_page_config(page_title="OPSFORGE AI Build Lab", page_icon="⚙️", layout="wide")

st.markdown("""
<style>
:root { --ink:#e8eef9; --muted:#9aa9c2; --panel:#111d31; --line:#243651; --accent:#65d7f2; }
.stApp { background: radial-gradient(ellipse at 15% 0%, #17304d 0%, #0a1220 46%, #080e18 100%); color:var(--ink); }
.block-container { padding-top:2.2rem; max-width:1440px; }
h1,h2,h3 { letter-spacing:-.035em; }
.hero { padding:2rem 2.2rem; border:1px solid #294765; border-radius:22px; background:linear-gradient(120deg,rgba(23,53,82,.94),rgba(14,26,44,.92)); margin-bottom:1.2rem; }
.eyebrow { color:#70d9f2; font-size:.75rem; letter-spacing:.18em; font-weight:800; }
.punch { font-size:clamp(2rem,4vw,3.7rem); line-height:1.03; font-weight:850; margin:.6rem 0; color:#f5f8ff; }
.sub { color:#b5c4d9; font-size:1.05rem; max-width:850px; }
.card { border:1px solid #29405c; border-radius:16px; padding:1rem 1.1rem; background:rgba(17,29,49,.88); min-height:180px; }
.tag { display:inline-block; padding:.2rem .55rem; border-radius:999px; background:#173b52; color:#83e1f5; font-size:.72rem; font-weight:700; margin-bottom:.6rem; }
.small { color:#9eafc7; font-size:.84rem; }
a { color:#7cddf4 !important; }
div[data-testid="stMetric"] { background:#111d31; border:1px solid #29405c; padding:12px 16px; border-radius:14px; }
</style>
""", unsafe_allow_html=True)

PROJECTS = [
 {"name":"OPSFORGE","family":"Governance","stage":"Live platform","problem":"AI agents need bounded tools, human approval and an auditable run history.","proof":"Six registered agents, approval workflow, override reasons and audit trail.","repo":"https://github.com/sghatge/opsforge","demo":"https://sghatge.github.io/opsforge/","punch":"Autonomy without accountability is just automation with a bigger blast radius."},
 {"name":"ACC Agent Gate","family":"Governance","stage":"Live demo","problem":"An AI agent should not be able to trigger a consequential campaign action without policy checks.","proof":"Policy gate, approval boundary and tamper-evident evidence patterns.","repo":"https://github.com/sghatge/acc-agent-gate","demo":"https://sghatge.github.io/acc-agent-gate/","punch":"Put a control plane between the agent and the action."},
 {"name":"AJO Journey Time Machine","family":"Journey intelligence","stage":"Live Streamlit + MCP","problem":"Journey definitions and event streams need deterministic validation before operational use.","proof":"Synthetic scenario simulation, consent gates, risk heuristics and hash-chained audit evidence.","repo":"https://github.com/sghatge/ajo-journey-time-machine","demo":"https://ajo-journey-time-machine.streamlit.app/","punch":"Replay the journey before the customer lives it."},
 {"name":"CampaignPulse AI","family":"Journey intelligence","stage":"Live Streamlit","problem":"Campaign teams need transparent diagnostics from aggregate performance metrics.","proof":"Deterministic KPIs, validation, evidence-labelled findings and exportable reports.","repo":"https://github.com/sghatge/campaignpulse-ai","demo":"https://campaignpulse-ai.streamlit.app/","punch":"From campaign numbers to the next operational decision."},
 {"name":"AI Readiness Calculator","family":"Transformation","stage":"Live web app","problem":"AI adoption needs measurable capability, governance and change-readiness signals.","proof":"31-question assessment, 10 dimensions, what-if simulator and 30-day action plan.","repo":"https://github.com/sghatge/ai-readiness-calculator","demo":"https://sghatge.github.io/ai-readiness-calculator/","punch":"AI adoption is a capability journey—not a licence purchase."},
 {"name":"Email 2030 Showcase","family":"Autonomous engineering","stage":"Five demos","problem":"Email operations are changing as agents, orchestration and AI-readable content converge.","proof":"Prompt-to-journey, governance, pre-flight, AI-readable email and test-loop concepts.","repo":"https://github.com/sghatge/email-2030-showcase","demo":"https://github.com/sghatge/email-2030-showcase","punch":"The inbox is becoming an interface. Is your email ready?"},
 {"name":"Adobe Campaign v8 Governance","family":"Governance","stage":"Portfolio showcase","problem":"Enterprise campaign operations need repeatable governance and evidence.","proof":"Independent governance blueprint, QA patterns and operational controls.","repo":"https://github.com/sghatge/adobe-campaign-v8-governance","demo":"https://sghatge.github.io/adobe-campaign-v8-governance/","punch":"Campaign quality should be engineered—not inspected at the last minute."},
 {"name":"Customer 360 Intelligence","family":"Journey intelligence","stage":"Learning lab","problem":"Customer data, identity, consent and activation must work as one governed lifecycle.","proof":"Synthetic-data learning lab for XDM, identity resolution, consent and audiences.","repo":"https://github.com/sghatge/customer-360-intelligence","demo":"https://sghatge.github.io/adobe-campaign-v8-governance/demos/customer-360.html","punch":"A 360° view is only useful when identity and consent are trustworthy."},
 {"name":"Digital Marketing AI Agents","family":"Autonomous engineering","stage":"Live Streamlit","problem":"Marketing workflows can be decomposed into bounded, reviewable agent tasks.","proof":"Interactive strategy, content, campaign QA and performance-analysis workflows.","repo":"https://github.com/sghatge/digital-marketing-ai-agents","demo":"https://sghatge-digital-marketing-ai-agents-app-5uhltb.streamlit.app/","punch":"Don't add AI to the workflow. Redesign the workflow around outcomes."},
 {"name":"Campaign v8 Pre-flight Agent","family":"Governance","stage":"Prototype","problem":"Campaign release readiness should be checked before deployment windows.","proof":"Deterministic pre-flight controls and explainable verdicts.","repo":"https://github.com/sghatge/campaign-v8-preflight-agent","demo":"https://github.com/sghatge/campaign-v8-preflight-agent","punch":"The safest campaign is the one that fails fast before send time."},
 {"name":"AJO Journey Orchestration Lab","family":"Journey intelligence","stage":"Learning lab","problem":"Teams need a practical environment to reason about orchestration patterns.","proof":"Independent AJO-oriented journey learning and design exercises.","repo":"https://github.com/sghatge/ajo-journey-orchestration-lab","demo":"https://github.com/sghatge/ajo-journey-orchestration-lab","punch":"Orchestration is not a canvas. It is a set of operational decisions."},
 {"name":"Salesforce CRM AI Lab","family":"Transformation","stage":"Learning lab","problem":"CRM intelligence needs structured lifecycle and decision-support patterns.","proof":"Independent CRM AI learning stream.","repo":"https://github.com/sghatge/salesforce-crm-ai-lab","demo":"https://github.com/sghatge/salesforce-crm-ai-lab","punch":"Customer intelligence becomes valuable when it changes the next action."}
]

RESEARCH = [
 {"title":"Introducing Gemini 4 Neon","date":"18 Nov 2026","source":"Google DeepMind","url":"https://blog.google/innovation-and-ai/models-and-research/gemini-models/introducing-gemini-4-neon/","idea":"Frontier models are being positioned for complex software engineering and multi-step knowledge work.","build":"AJO Journey Time Machine · OPSFORGE","question":"Which parts of an enterprise workflow should be delegated, and which must remain deterministic?"},
 {"title":"AgentArch: A Benchmark for Evaluating Agent Architectures in Enterprise Workflows","date":"Nov 2026","source":"ACL 2026 / ServiceNow AI Research","url":"https://aclanthology.org/2026.aacl-long.44.pdf","idea":"18 agent configurations show that orchestration, agent style, memory and thinking tools interact; there is no universal best architecture.","build":"Four Agents, One Campaign · OPSFORGE","question":"Are we evaluating the architecture—or just the model's demo performance?"},
 {"title":"A Capability Framework for Evaluating Agentic AI Platforms in Regulated Enterprises","date":"18 Nov 2026","source":"arXiv","url":"https://arxiv.org/abs/2611.24039","idea":"Enterprise agent platforms should be evaluated across capability, execution reliability, governance and business value.","build":"OPSFORGE Evaluation Lab · ACC Agent Gate","question":"What evidence would justify moving an agent from prototype to production?"},
 {"title":"Governing Agentic AI in Enterprise Workflows","date":"20 Sep 2026","source":"Information journal","url":"https://www.mdpi.com/2078-2489/17/9/923","idea":"Bounded autonomy, delegated authority and controlled execution help separate an agent's proposal from an authorized action.","build":"ACC Agent Gate · Deterministic CRM QA","question":"Can an agent recommend an action without having authority to execute it?"},
 {"title":"READY or Not: Reliable Enterprise Agent Deployment","date":"4 Sep 2026","source":"Scale Labs","url":"https://labs.scale.com/papers/reliable-enterprise-agent-deployment","idea":"Deployment qualification should consider reliability targets, human oversight burden and operating cost—not just autonomous accuracy.","build":"Agent Pre-flight · Evaluation Lab","question":"What is the minimum oversight needed to meet a defined reliability target?"}
]

st.markdown("""
<div class="hero">
 <div class="eyebrow">SANGRAM GHATGE · INDEPENDENT ENGINEERING PORTFOLIO</div>
 <div class="punch">Don't just talk about AI.<br>Build it. Test it. Govern it.</div>
 <div class="sub">OPSFORGE AI Build Lab connects working prototypes, enterprise use cases, evaluation methods and current research—so visitors can inspect the evidence, not just the pitch.</div>
</div>
""", unsafe_allow_html=True)

projects_tab, research_tab, evaluate_tab, publish_tab = st.tabs(["🚀 Build portfolio","🧠 Research radar","🧪 Evaluate a concept","📣 LinkedIn studio"])

with projects_tab:
    c1,c2,c3=st.columns(3)
    c1.metric("Showcased builds",len(PROJECTS))
    c2.metric("Research connections",len(RESEARCH))
    c3.metric("Product families",len(set(p["family"] for p in PROJECTS)))
    family=st.selectbox("Filter by product family",["All"]+sorted(set(p["family"] for p in PROJECTS)))
    query=st.text_input("Search builds",placeholder="Try governance, journey, campaign, readiness…")
    visible=[p for p in PROJECTS if (family=="All" or p["family"]==family) and (query.lower() in (p["name"]+" "+p["problem"]+" "+p["proof"]).lower())]
    for start in range(0,len(visible),2):
        cols=st.columns(2)
        for col,p in zip(cols,visible[start:start+2]):
            with col:
                st.markdown(f'<div class="card"><span class="tag">{p["family"]} · {p["stage"]}</span><h3>{p["name"]}</h3><p>{p["problem"]}</p><p class="small"><b>What you can inspect:</b> {p["proof"]}</p><p><i>“{p["punch"]}”</i></p></div>',unsafe_allow_html=True)
                st.markdown(f'[Open repository ↗]({p["repo"]})　 ·　 [Open demo ↗]({p["demo"]})')
    st.caption("Portfolio inventory is curated from public repositories. A repository link is not a claim that every concept has a hosted interactive demo.")

with research_tab:
    st.markdown("### Research-to-build connections")
    st.info("A research headline is useful only when it changes a design decision. Each item below links a published source to a build and a question worth testing.")
    for r in RESEARCH:
        with st.expander(f'{r["title"]} · {r["date"]}'):
            st.caption(f'{r["source"]} · {r["date"]}')
            st.write(r["idea"])
            st.markdown(f'**Related build:** {r["build"]}')
            st.markdown(f'**Audience question:** {r["question"]}')
            st.link_button("Read original source",r["url"])
    st.caption("Research snapshot curated 26 November 2026. Check original publications for updates, methods and limitations.")

with evaluate_tab:
    st.markdown("### Prototype-to-production evaluation")
    st.write("Score a concept using a transparent, editable rubric. This is a discussion aid—not a certification or production approval.")
    concept=st.selectbox("Concept to evaluate",[p["name"] for p in PROJECTS])
    st.caption("Rate each dimension from 1 (weak / unproven) to 5 (strong evidence).")
    dims=["Business value clarity","Functional completeness","Reliability and repeatability","Governance and security","Observability and auditability","User experience","Deployment readiness","Evidence quality"]
    scores={}
    for i,d in enumerate(dims):
        scores[d]=st.slider(d,1,5,3,key=f"score_{i}")
    total=round(sum(scores.values())/ (len(scores)*5)*100)
    st.metric("Evidence maturity score",f"{total}/100")
    st.progress(total/100)
    if total>=80: st.success("Strong prototype evidence. Validate with representative users and operational controls before production claims.")
    elif total>=60: st.warning("Promising. Close the evidence gaps and repeat the evaluation.")
    else: st.error("Early-stage. Prioritise core functionality, test coverage and clear safety boundaries.")
    st.dataframe([{"Dimension":k,"Score":v,"Max":5} for k,v in scores.items()],use_container_width=True,hide_index=True)
    st.download_button("Download evaluation as CSV","Dimension,Score,Max\n"+"\n".join(f"{k},{v},5" for k,v in scores.items())+f"\nOverall,{total},100",file_name="opsforge_concept_evaluation.csv",mime="text/csv")
    st.caption("Scores are user-entered and not independently verified. Do not interpret this score as a security certification or readiness guarantee.")

with publish_tab:
    st.markdown("### Turn a build into a research-backed LinkedIn post")
    selected=st.selectbox("Choose a build",[p["name"] for p in PROJECTS],key="publish_project")
    p=next(x for x in PROJECTS if x["name"]==selected)
    related=[r for r in RESEARCH if any(term in (r["build"]+" "+r["title"]).lower() for term in selected.lower().split()[:2])]
    st.text_input("Opening punch line",value=p["punch"],key="punchline")
    audience=st.selectbox("Audience",["CRM and MarTech leaders","Enterprise architects","AI engineers","Marketing operations leaders","Business transformation leaders"])
    angle=st.selectbox("Post angle",["Build in public","Research to implementation","Architecture deep dive","Business problem and measurable value"])
    draft=f"""The next AI breakthrough isn't another impressive demo. It's a system we can inspect, test and govern.

{p["punch"]}

I built {p["name"]} to explore this enterprise problem:
{p["problem"]}

What the prototype demonstrates:
• {p["proof"]}
• A practical way to evaluate the design, not just describe it.
• A clear boundary between prototype evidence and production claims.

Why it matters to {audience.lower()}:
The conversation needs to move from AI capability to reliable business outcomes.

Build: {p["repo"]}
Demo / project: {p["demo"]}

What would you test before trusting this in a real enterprise workflow?

#EnterpriseAI #AgenticAI #MarTech #CRM #AIGovernance #BuildInPublic"""
    st.text_area("Editable LinkedIn draft",draft,height=360)
    st.download_button("Download LinkedIn draft",draft,file_name="linkedin_build_post.txt",mime="text/plain")
    st.caption("Edit the draft to reflect what you personally tested. Add screenshots or a short demo recording before publishing.")

st.divider()
st.markdown("**OPSFORGE AI BUILD LAB** · Independent prototypes. Synthetic-data-first demonstrations. Evidence before claims.")
st.markdown("[GitHub profile](https://github.com/sghatge) · [Portfolio](https://sghatge.github.io/adobe-campaign-v8-governance/) · [OPSFORGE](https://github.com/sghatge/opsforge)")
