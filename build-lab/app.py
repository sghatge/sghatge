import streamlit as st
from datetime import date
from pathlib import Path
import base64
import csv
import io
import re

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
.card { border:1px solid #31516f; border-radius:18px; padding:1.2rem 1.25rem; background:linear-gradient(145deg,rgba(20,39,64,.97),rgba(10,19,34,.98)); min-height:190px; box-shadow:0 10px 28px rgba(0,0,0,.18); }
.card h3 { color:#f5f8ff; font-size:1.35rem; margin:.3rem 0 .65rem; }
.card p { color:#d2deee; line-height:1.55; }
.tag { display:inline-block; padding:.2rem .55rem; border-radius:999px; background:#173b52; color:#83e1f5; font-size:.72rem; font-weight:700; margin-bottom:.6rem; }
.small { color:#9eafc7; font-size:.84rem; }
.project-visual { overflow:hidden; border-radius:14px; margin:0 0 .7rem; border:1px solid #294765; background:#071326; }
.project-card { border:1px solid #294765; border-radius:18px; padding:1.05rem 1.1rem 1rem; background:linear-gradient(145deg,rgba(18,35,58,.98),rgba(8,17,31,.98)); box-shadow:0 12px 28px rgba(0,0,0,.2); position:relative; overflow:hidden; }
.project-card:before { content:""; position:absolute; width:150px; height:150px; right:-65px; top:-75px; border-radius:50%; background:var(--glow); filter:blur(36px); opacity:.18; pointer-events:none; }
.project-card-head { display:flex; align-items:center; gap:.75rem; margin-bottom:.8rem; position:relative; }
.project-icon { width:48px; height:48px; min-width:48px; display:grid; place-items:center; border-radius:14px; font-size:1.45rem; background:var(--icon-bg); border:1px solid var(--icon-border); box-shadow:inset 0 0 18px rgba(255,255,255,.035); }
.project-name { color:#f4f8ff; font-size:1.2rem; font-weight:850; line-height:1.2; letter-spacing:-.025em; }
.project-meta { color:#a9bdd5; font-size:.72rem; font-weight:750; letter-spacing:.035em; text-transform:uppercase; margin-top:.28rem; }
.project-card p { color:#d0dced; line-height:1.48; font-size:.91rem; margin:.55rem 0; position:relative; }
.project-proof { color:#b9cce1 !important; border-left:2px solid var(--accent); padding-left:.65rem; }
.project-punch { color:#85e6f8 !important; font-weight:700; font-size:.88rem !important; }
.project-links { display:flex; gap:1rem; margin:.8rem 0 0; font-size:.83rem; font-weight:750; }
.project-links a { text-decoration:none; border-bottom:1px solid rgba(124,221,244,.35); padding-bottom:2px; }
.concept-card { border:1px solid #31516f; border-radius:16px; padding:.85rem; background:linear-gradient(145deg,rgba(22,43,70,.98),rgba(8,17,31,.98)); min-height:100%; box-shadow:0 9px 22px rgba(0,0,0,.18); }
.concept-title { color:#ffffff; font-size:1.22rem; font-weight:850; margin:.35rem 0 .65rem; letter-spacing:-.02em; }
.concept-copy { color:#d0dced; font-size:.96rem; line-height:1.6; }
.concept-hook { color:#83e8ff; font-weight:800; font-size:1rem; line-height:1.45; margin:.85rem 0 .2rem; }
/* High-contrast bespoke sidebar and multipage navigation */
[data-testid="stSidebar"], [data-testid="stSidebar"] > div:first-child {
  background:linear-gradient(180deg,#101f34 0%,#0b1423 100%) !important;
  border-right:1px solid #294765 !important;
}
[data-testid="stSidebar"] * { color:#e8f1ff !important; }
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p,
[data-testid="stSidebar"] [data-testid="stCaptionContainer"] p { color:#b9cbe0 !important; }
[data-testid="stSidebarNav"] a,
[data-testid="stSidebarNav"] span,
[data-testid="stSidebarNav"] p { color:#e5efff !important; opacity:1 !important; }
[data-testid="stSidebarNav"] a[aria-current="page"] {
  background:linear-gradient(90deg,rgba(101,215,242,.2),rgba(101,215,242,.07)) !important;
  border-left:3px solid #65d7f2 !important;
  border-radius:8px !important;
}
[data-testid="stSidebar"] a { color:#7fe5ff !important; }
[data-testid="stSidebar"] hr { border-color:#294765 !important; }
[data-testid="stSidebar"] button { color:#f4f8ff !important; }
.project-visual img { display:block; width:100%; height:auto; max-height:190px; object-fit:contain; border-radius:12px; }
@media (max-width: 760px) {
  .block-container { padding-left:1rem; padding-right:1rem; }
  .project-card { min-height:0; }
}
a { color:#7cddf4 !important; }
.stApp, .stApp p, .stApp label, .stApp span, .stApp li, .stApp small { color:#e5edf8; }
.stTabs [data-baseweb="tab"] { color:#d7e5f5 !important; font-weight:700; }
.stTabs [aria-selected="true"] { color:#ff5578 !important; }
.stMarkdown p, .stCaption, [data-testid="stCaptionContainer"] { color:#c4d2e5 !important; }
div[data-testid="stMetric"] { background:#14233a; border:1px solid #35516f; padding:16px 18px; border-radius:14px; }
div[data-testid="stMetricLabel"] p { color:#b9cbe0 !important; font-size:.95rem !important; }
div[data-testid="stMetricValue"] { color:#f4f8ff !important; font-size:2.3rem !important; }
div[data-testid="stSelectbox"] label, div[data-testid="stTextInput"] label { color:#eaf2ff !important; font-weight:700; }
.stSelectbox div[data-baseweb="select"] > div { border-radius:12px; }
.stButton button, .stDownloadButton button { border-radius:12px; font-weight:750; }

</style>
""", unsafe_allow_html=True)


@st.cache_data(show_spinner=False)
def image_html(filename, alt="OPSFORGE AI concept artwork"):
    """Load a repository-owned SVG safely and return a compact responsive image."""
    asset_path = Path(__file__).parent / "assets" / filename
    try:
        svg = asset_path.read_text(encoding="utf-8")
        encoded = base64.b64encode(svg.encode("utf-8")).decode("ascii")
        return f'<div class="project-visual"><img src="data:image/svg+xml;base64,{encoded}" alt="{alt}" loading="lazy"></div>'
    except (FileNotFoundError, OSError, UnicodeDecodeError) as exc:
        st.warning(f"Artwork unavailable for {alt}: {filename}")
        return f'<div class="project-visual project-visual-fallback" role="img" aria-label="{alt} artwork unavailable"><span>◇</span><small>{alt}</small></div>'

PROJECTS = [
 {"name":"OPSFORGE","research_ids":["gemini-4-neon","agentic-platform-evaluation","bounded-autonomy-enterprise"],"image":"opsforge-architecture.svg","family":"Governance","stage":"Live platform + Streamlit showcase","problem":"AI agents need bounded tools, human approval and an auditable run history.","proof":"Governed agent workspace, approval and override controls, run ledger, Signal → Execution pipeline and Resilience Command Centre.","repo":"https://github.com/sghatge/opsforge","demo":"https://sghatge.streamlit.app/","punch":"Autonomy without accountability is just automation with a bigger blast radius."},
 {"name":"Signal → Execution","research_ids":["agentic-platform-evaluation","bounded-autonomy-enterprise"],"image":"opsforge-architecture.svg","family":"Governance","stage":"Integrated Streamlit workspace","problem":"Operational teams need a traceable path from external signals to governed decisions.","proof":"RSS intake, relevance scoring, specialist routing, Autonomous / Notify / Approve classification and reviewer decision ledger. External actions remain disabled.","repo":"https://github.com/sghatge/opsforge","demo":"https://sghatge.streamlit.app/","punch":"Turn signals into decisions—not uncontrolled actions."},
 {"name":"Resilience Command Centre","research_ids":["agentic-platform-evaluation","bounded-autonomy-enterprise"],"image":"opsforge-architecture.svg","family":"Governance","stage":"Integrated OPSFORGE module","problem":"Operational resilience needs a dedicated workspace for structured assessment and response.","proof":"A dedicated resilience module integrated into the OPSFORGE Streamlit navigation.","repo":"https://github.com/sghatge/opsforge/tree/main/products/resilience-command-centre","demo":"https://sghatge.streamlit.app/","punch":"Resilience is designed before the incident, not during it."},
 {"name":"ACC Agent Gate","research_ids":["agentic-platform-evaluation","bounded-autonomy-enterprise"],"image":"agent-governance.svg","family":"Governance","stage":"Live demo","problem":"An AI agent should not be able to trigger a consequential campaign action without policy checks.","proof":"Policy gate, approval boundary and tamper-evident evidence patterns.","repo":"https://github.com/sghatge/acc-agent-gate","demo":"https://sghatge.github.io/acc-agent-gate/","punch":"Put a control plane between the agent and the action."},
 {"name":"AJO Journey Time Machine","research_ids":["agentarch-2026","gemini-4-neon"],"image":"ajo-journey-time-machine.svg","family":"Journey intelligence","stage":"Live Streamlit + MCP","problem":"Journey definitions and event streams need deterministic validation before operational use.","proof":"Synthetic scenario simulation, consent gates, risk heuristics and hash-chained audit evidence.","repo":"https://github.com/sghatge/ajo-journey-time-machine","demo":"https://ajo-journey-time-machine.streamlit.app/","punch":"Replay the journey before the customer lives it."},
 {"name":"CampaignPulse AI","research_ids":[],"image":"campaign-intelligence.svg","family":"Journey intelligence","stage":"Live Streamlit","problem":"Campaign teams need transparent diagnostics from aggregate performance metrics.","proof":"Deterministic KPIs, validation, evidence-labelled findings and exportable reports.","repo":"https://github.com/sghatge/campaignpulse-ai","demo":"https://campaignpulse-ai.streamlit.app/","punch":"From campaign numbers to the next operational decision."},
 {"name":"AI Readiness Calculator","research_ids":["agentic-platform-evaluation"],"image":"ai-readiness-calculator.svg","family":"Transformation","stage":"Live web app","problem":"AI adoption needs measurable capability, governance and change-readiness signals.","proof":"31-question assessment, 10 dimensions, what-if simulator and 30-day action plan.","repo":"https://github.com/sghatge/ai-readiness-calculator","demo":"https://sghatge.github.io/ai-readiness-calculator/","punch":"AI adoption is a capability journey—not a licence purchase."},
 {"name":"Email 2030 Showcase","research_ids":["gemini-4-neon","agentarch-2026"],"image":"ai-readable-email.svg","family":"Autonomous engineering","stage":"Five demos","problem":"Email operations are changing as agents, orchestration and AI-readable content converge.","proof":"Prompt-to-journey, governance, pre-flight, AI-readable email and test-loop concepts.","repo":"https://github.com/sghatge/email-2030-showcase","demo":"https://github.com/sghatge/email-2030-showcase","punch":"The inbox is becoming an interface. Is your email ready?"},
 {"name":"Adobe Campaign v8 Governance","research_ids":["bounded-autonomy-enterprise"],"image":"adobe-campaign-v8-governance.svg","family":"Governance","stage":"Portfolio showcase","problem":"Enterprise campaign operations need repeatable governance and evidence.","proof":"Independent governance blueprint, QA patterns and operational controls.","repo":"https://github.com/sghatge/adobe-campaign-v8-governance","demo":"https://sghatge.github.io/adobe-campaign-v8-governance/","punch":"Campaign quality should be engineered—not inspected at the last minute."},
 {"name":"Customer 360 Intelligence","research_ids":[],"image":"deterministic-crm-qa.svg","family":"Journey intelligence","stage":"Learning lab","problem":"Customer data, identity, consent and activation must work as one governed lifecycle.","proof":"Synthetic-data learning lab for XDM, identity resolution, consent and audiences.","repo":"https://github.com/sghatge/customer-360-intelligence","demo":"https://sghatge.github.io/adobe-campaign-v8-governance/demos/customer-360.html","punch":"A 360° view is only useful when identity and consent are trustworthy."},
 {"name":"Digital Marketing AI Agents","research_ids":["agentarch-2026"],"image":"four-agents-one-campaign.svg","family":"Autonomous engineering","stage":"Live Streamlit","problem":"Marketing workflows can be decomposed into bounded, reviewable agent tasks.","proof":"Interactive strategy, content, campaign QA and performance-analysis workflows.","repo":"https://github.com/sghatge/digital-marketing-ai-agents","demo":"https://sghatge-digital-marketing-ai-agents-app-5uhltb.streamlit.app/","punch":"Don't add AI to the workflow. Redesign the workflow around outcomes."},
 {"name":"Campaign v8 Pre-flight Agent","research_ids":["ready-enterprise-agents"],"image":"preflight-agent.svg","family":"Governance","stage":"Prototype","problem":"Campaign release readiness should be checked before deployment windows.","proof":"Deterministic pre-flight controls and explainable verdicts.","repo":"https://github.com/sghatge/campaign-v8-preflight-agent","demo":"https://github.com/sghatge/campaign-v8-preflight-agent","punch":"The safest campaign is the one that fails fast before send time."},
 {"name":"AJO Journey Orchestration Lab","research_ids":["agentarch-2026"],"image":"prompt-to-journey.svg","family":"Journey intelligence","stage":"Learning lab","problem":"Teams need a practical environment to reason about orchestration patterns.","proof":"Independent AJO-oriented journey learning and design exercises.","repo":"https://github.com/sghatge/ajo-journey-orchestration-lab","demo":"https://github.com/sghatge/ajo-journey-orchestration-lab","punch":"Orchestration is not a canvas. It is a set of operational decisions."},
 {"name":"Salesforce CRM AI Lab","research_ids":[],"image":"salesforce-crm-lifecycle.svg","family":"Transformation","stage":"Learning lab","problem":"CRM intelligence needs structured lifecycle and decision-support patterns.","proof":"Independent CRM AI learning stream.","repo":"https://github.com/sghatge/salesforce-crm-ai-lab","demo":"https://github.com/sghatge/salesforce-crm-ai-lab","punch":"Customer intelligence becomes valuable when it changes the next action."}
]


CONCEPTS = [
 {"name":"Email 2030 — Agent Governance","family":"Enterprise AI Governance","image":"agent-governance.svg","problem":"Place explicit policy and human approval between autonomous agents and campaign-impacting actions.","hook":"Your AI agent is only as trustworthy as the controls around it.","repo":"https://github.com/sghatge/email-2030-showcase","demo":"https://github.com/sghatge/acc-agent-gate"},
 {"name":"Campaign Pre-flight Agent","family":"Release Assurance","image":"preflight-agent.svg","problem":"Run deterministic readiness checks before a campaign enters a deployment window.","hook":"The safest campaign is the one that fails fast before send time.","repo":"https://github.com/sghatge/campaign-v8-preflight-agent","demo":"https://github.com/sghatge/campaign-v8-preflight-agent"},
 {"name":"Prompt to Journey","family":"Journey Intelligence","image":"prompt-to-journey.svg","problem":"Translate a marketing brief into a structured, reviewable customer journey blueprint.","hook":"From a sentence to a journey blueprint—with humans still in control.","repo":"https://github.com/sghatge/email-2030-showcase/tree/main/01-prompt-to-journey","demo":"https://github.com/sghatge/email-2030-showcase"},
 {"name":"AI-readable Email","family":"Future of Email","image":"ai-readable-email.svg","problem":"Explore how structured, semantically clear email content can be easier for AI-assisted experiences to interpret.","hook":"The inbox is becoming an interface. Is your email ready for AI?","repo":"https://github.com/sghatge/email-2030-showcase/tree/main/04-ai-readable-email","demo":"https://github.com/sghatge/email-2030-showcase"},
 {"name":"Self-Optimizing Test Loop","family":"Autonomous Engineering","image":"self-optimizing-test-loop.svg","problem":"Demonstrate a closed-loop test workflow that measures, learns and proposes the next experiment.","hook":"Stop guessing what works. Build a loop that learns from evidence.","repo":"https://github.com/sghatge/email-2030-showcase/tree/main/05-test-loop","demo":"https://github.com/sghatge/email-2030-showcase"},
 {"name":"AJO Journey Time Machine","family":"Journey Intelligence","image":"ajo-journey-time-machine.svg","problem":"Replay synthetic journey events, validate consent gates and inspect deterministic risk evidence.","hook":"Replay the journey before the customer lives it.","repo":"https://github.com/sghatge/ajo-journey-time-machine","demo":"https://ajo-journey-time-machine.streamlit.app/"},
 {"name":"OPSFORGE Architecture","family":"Enterprise AI Operating Model","image":"opsforge-architecture.svg","problem":"Coordinate bounded agents, named approvals, run ledgers and auditable operational workflows.","hook":"Autonomy without accountability is just automation with a bigger blast radius.","repo":"https://github.com/sghatge/opsforge","demo":"https://sghatge.github.io/opsforge/"},
 {"name":"Deterministic CRM QA Engine","family":"CRM Governance","image":"deterministic-crm-qa.svg","problem":"Turn operational QA rules into repeatable checks with explainable pass, warning and fail outcomes.","hook":"Campaign quality should be engineered—not inspected at the last minute.","repo":"https://github.com/sghatge/adobe-campaign-v8-governance","demo":"https://sghatge.github.io/adobe-campaign-v8-governance/"},
 {"name":"Four Agents, One Campaign","family":"Multi-Agent Systems","image":"four-agents-one-campaign.svg","problem":"Explore specialist agents collaborating across planning, content, QA and performance analysis.","hook":"One campaign. Four specialist agents. One governed workflow.","repo":"https://github.com/sghatge/digital-marketing-ai-agents","demo":"https://sghatge-digital-marketing-ai-agents-app-5uhltb.streamlit.app/"},
 {"name":"Adobe Campaign v8 Governance","family":"MarTech Architecture","image":"adobe-campaign-v8-governance.svg","problem":"Showcase campaign governance patterns, QA evidence and operational control points.","hook":"Enterprise campaign operations deserve engineering-grade governance.","repo":"https://github.com/sghatge/adobe-campaign-v8-governance","demo":"https://sghatge.github.io/adobe-campaign-v8-governance/"},
 {"name":"Campaign Intelligence Agent","family":"Marketing Analytics","image":"campaign-intelligence.svg","problem":"Convert aggregate campaign metrics into transparent KPIs, diagnostic findings and next checks.","hook":"From campaign numbers to the next operational decision.","repo":"https://github.com/sghatge/campaignpulse-ai","demo":"https://campaignpulse-ai.streamlit.app/"},
 {"name":"AI Readiness Calculator","family":"Enterprise Transformation","image":"ai-readiness-calculator.svg","problem":"Assess adoption capability across skills, governance, use-case fit and organizational readiness.","hook":"AI adoption is a capability journey—not a licence purchase.","repo":"https://github.com/sghatge/ai-readiness-calculator","demo":"https://sghatge.github.io/ai-readiness-calculator/"}
]

RESEARCH = [
 {"id":"gemini-4-neon","title":"Introducing Gemini 4 Neon","date":"18 Nov 2026","source":"Google DeepMind","url":"https://blog.google/innovation-and-ai/models-and-research/gemini-models/introducing-gemini-4-neon/","idea":"Frontier models are being positioned for complex software engineering and multi-step knowledge work.","build":"AJO Journey Time Machine · OPSFORGE","question":"Which parts of an enterprise workflow should be delegated, and which must remain deterministic?"},
 {"id":"agentarch-2026","title":"AgentArch: A Benchmark for Evaluating Agent Architectures in Enterprise Workflows","date":"Nov 2026","source":"ACL 2026 / ServiceNow AI Research","url":"https://aclanthology.org/2026.aacl-long.44/","idea":"18 agent configurations show that orchestration, agent style, memory and thinking tools interact; there is no universal best architecture.","build":"Four Agents, One Campaign · OPSFORGE","question":"Are we evaluating the architecture—or just the model's demo performance?"},
 {"id":"agentic-platform-evaluation","title":"A Capability Framework for Evaluating Agentic AI Platforms in Regulated Enterprises","date":"18 Nov 2026","source":"arXiv","url":"https://arxiv.org/abs/2611.24039","idea":"Enterprise agent platforms should be evaluated across capability, execution reliability, governance and business value.","build":"OPSFORGE Evaluation Lab · ACC Agent Gate","question":"What evidence would justify moving an agent from prototype to production?"},
 {"id":"bounded-autonomy-enterprise","title":"Governing Agentic AI in Enterprise Workflows","date":"20 Sep 2026","source":"Information journal","url":"https://www.mdpi.com/2078-2489/17/9/923","idea":"Bounded autonomy, delegated authority and controlled execution help separate an agent's proposal from an authorized action.","build":"ACC Agent Gate · Deterministic CRM QA","question":"Can an agent recommend an action without having authority to execute it?"},
 {"id":"ready-enterprise-agents","title":"READY or Not: Reliable Enterprise Agent Deployment","date":"4 Sep 2026","source":"Scale Labs","url":"https://labs.scale.com/papers/reliable-enterprise-agent-deployment","idea":"Deployment qualification should consider reliability targets, human oversight burden and operating cost—not just autonomous accuracy.","build":"Agent Pre-flight · Evaluation Lab","question":"What is the minimum oversight needed to meet a defined reliability target?"}
]

st.markdown("""
<div class="hero">
 <div class="eyebrow">SANGRAM GHATGE · INDEPENDENT ENGINEERING PORTFOLIO</div>
 <div class="punch">Don't just talk about AI.<br>Build it. Test it. Govern it.</div>
 <div class="sub">OPSFORGE AI Build Lab connects working prototypes, enterprise use cases, evaluation methods and current research—so visitors can inspect the evidence, not just the pitch.</div>
</div>
""", unsafe_allow_html=True)

def render_portfolio():
    c1,c2,c3=st.columns(3)
    c1.metric("Showcased builds",len(PROJECTS))
    c2.metric("Research connections",len(RESEARCH))
    c3.metric("Product families",len(set(p["family"] for p in PROJECTS)))
    with st.form("portfolio_filter_form"):
        family=st.selectbox("Filter by product family",["All"]+sorted(set(p["family"] for p in PROJECTS)))
        query=st.text_input("Search builds",placeholder="Try governance, journey, campaign, readiness…")
        apply_filters=st.form_submit_button("Apply filters")
    visible=[p for p in PROJECTS if (family=="All" or p["family"]==family) and (query.lower() in (p["name"]+" "+p["problem"]+" "+p["proof"]).lower())]
    PROJECT_ICON_STYLE = {
        "OPSFORGE": ("⚙️","#53d9f4"),
        "ACC Agent Gate": ("🛡️","#9b8cff"),
        "AJO Journey Time Machine": ("🧭","#42d9c5"),
        "CampaignPulse AI": ("📈","#ffb454"),
        "AI Readiness Calculator": ("🎯","#8ddc86"),
        "Email 2030 Showcase": ("✉️","#63b7ff"),
        "Adobe Campaign v8 Governance": ("🧩","#ff8caa"),
        "Customer 360 Intelligence": ("🌐","#4fd7e8"),
        "Digital Marketing AI Agents": ("🤖","#b18cff"),
        "Campaign v8 Pre-flight Agent": ("🚦","#ffc45e"),
        "AJO Journey Orchestration Lab": ("🕸️","#52d6b5"),
        "Salesforce CRM AI Lab": ("☁️","#72a7ff"),
    }
    for start in range(0,len(visible),2):
        cols=st.columns(2, gap="medium")
        for col,p in zip(cols,visible[start:start+2]):
            with col:
                glyph,accent=PROJECT_ICON_STYLE.get(p["name"],("✦","#63d8f2"))
                card_html = f'''
                <div class="project-card" style="--accent:{accent};--glow:{accent};--icon-bg:{accent}18;--icon-border:{accent}66">
                  <div class="project-card-head">
                    <div class="project-icon">{glyph}</div>
                    <div><div class="project-name">{p["name"]}</div><div class="project-meta">{p["family"]} · {p["stage"]}</div></div>
                  </div>
                  <p>{p["problem"]}</p>
                  <p class="project-proof"><b>What you can inspect</b><br>{p["proof"]}</p>
                  <p class="project-punch">“{p["punch"]}”</p>
                  <div class="project-links"><a href="{p["repo"]}" target="_blank" rel="noopener noreferrer">↗ Repository</a><a href="{p["demo"]}" target="_blank" rel="noopener noreferrer">↗ Live demo / project</a></div>
                </div>'''
                st.markdown(card_html,unsafe_allow_html=True)
    st.caption("Portfolio inventory is curated from public repositories. A repository link is not a claim that every concept has a hosted interactive demo.")


def render_concepts():
    st.markdown("### The 12-concept visual showcase")
    st.write("Each concept has its own original OPSFORGE artwork, a clear enterprise problem, a memorable point of view and a direct path to its repository or demonstration.")
    family_filter = st.selectbox("Filter concepts", ["All"] + sorted({x["family"] for x in CONCEPTS}), key="concept_family")
    selected_concepts = [x for x in CONCEPTS if family_filter == "All" or x["family"] == family_filter]
    for start in range(0, len(selected_concepts), 3):
        cols = st.columns(3)
        for col, item in zip(cols, selected_concepts[start:start+3]):
            with col:
                st.markdown(image_html(item["image"], item["name"]), unsafe_allow_html=True)
                st.markdown(f'<div class="concept-card"><span class="tag">{item["family"]}</span><div class="concept-title">{item["name"]}</div><div class="concept-copy">{item["problem"]}</div><div class="concept-hook">“{item["hook"]}”</div></div>', unsafe_allow_html=True)
                st.markdown(f'[Source ↗]({item["repo"]})　 ·　 [Demo ↗]({item["demo"]})')
    st.caption("Artwork is original, concept-specific vector illustration. Project maturity and demo availability are stated per repository; visual polish does not imply production readiness.")


def render_research():
    st.markdown("### Research-to-build connections")
    st.info("A research headline is useful only when it changes a design decision. Each item below links a published source to a build and a question worth testing.")
    for r in RESEARCH:
        with st.expander(f'{r["title"]} · {r["date"]}'):
            st.caption(f'{r["source"]} · {r["date"]}')
            st.write(r["idea"])
            st.markdown(f'**Related build:** {r["build"]}')
            st.markdown(f'**Audience question:** {r["question"]}')
            st.link_button("Read original source",r["url"])
    st.caption(f"Research snapshot curated {date.today().strftime('%d %B %Y')}. Check original publications for updates, methods and limitations.")


def render_evaluate():
    st.markdown("### Prototype-to-production evaluation")
    st.write("Score a concept using a transparent, editable rubric. This is a discussion aid—not a certification or production approval.")
    dims=["Business value clarity","Functional completeness","Reliability and repeatability","Governance and security","Observability and auditability","User experience","Deployment readiness","Evidence quality"]
    with st.form("evaluation_form"):
        concept=st.selectbox("Concept to evaluate",[p["name"] for p in PROJECTS])
        st.caption("Rate each dimension from 1 (weak / unproven) to 5 (strong evidence).")
        scores={}
        for i,d in enumerate(dims):
            scores[d]=st.slider(d,1,5,3,key=f"score_{i}")
        submitted=st.form_submit_button("Calculate evidence score")
    if submitted:
        total=round(sum(scores.values())/(len(scores)*5)*100)
        st.metric("Evidence maturity score",f"{total}/100")
        st.progress(total/100)
        if total>=80: st.success("Strong prototype evidence. Validate with representative users and operational controls before production claims.")
        elif total>=60: st.warning("Promising. Close the evidence gaps and repeat the evaluation.")
        else: st.error("Early-stage. Prioritise core functionality, test coverage and clear safety boundaries.")
        st.dataframe([{"Dimension":k,"Score":v,"Max":5} for k,v in scores.items()],width="stretch",hide_index=True)
        csv_buffer=io.StringIO()
        writer=csv.writer(csv_buffer,quoting=csv.QUOTE_MINIMAL)
        writer.writerow(["Dimension","Score","Max"])
        writer.writerows([[dimension,score,5] for dimension,score in scores.items()])
        writer.writerow(["Overall",total,100])
        concept_slug=re.sub(r"[^a-z0-9]+","-",concept.lower()).strip("-")
        st.download_button("Download evaluation as CSV",csv_buffer.getvalue(),file_name=f"opsforge-evaluation-{concept_slug}.csv",mime="text/csv")
    st.caption("Scores are user-entered and not independently verified. Do not interpret this score as a security certification or readiness guarantee.")


def render_linkedin_studio():
    st.markdown("### Turn a build into a research-backed LinkedIn post")
    selected=st.selectbox("Choose a build",[p["name"] for p in PROJECTS],key="publish_project")
    p=next(x for x in PROJECTS if x["name"]==selected)
    audience=st.selectbox("Audience",["CRM and MarTech leaders","Enterprise architects","AI engineers","Marketing operations leaders","Business transformation leaders"],key="publish_audience")
    angle=st.selectbox("Post angle",["Build in public","Research to implementation","Architecture deep dive","Business problem and measurable value"],key="publish_angle")

    # Reset editable content only when the selected project changes.
    if st.session_state.get("pub_last") != selected:
        st.session_state["punchline"] = p["punch"]
        st.session_state["pub_last"] = selected
        st.session_state["linkedin_draft"] = ""

    punchline=st.text_input("Opening punch line",key="punchline")
    related=[r for r in RESEARCH if r["id"] in p.get("research_ids",[])]
    research_section=""
    if related:
        research_section="\nResearch connection:\n"+"\n".join(
            f'• {r["title"]} ({r["source"]}, {r["date"]}): {r["idea"]}\n  Source: {r["url"]}'
            for r in related
        )
    elif angle=="Research to implementation":
        research_section="\nResearch note: No directly mapped research source is currently assigned to this build. Add a verified source before publishing a research-led claim.\n"

    draft=f"""The next AI breakthrough isn't another impressive demo. It's a system we can inspect, test and govern.

{punchline}

I built {p["name"]} to explore this enterprise problem:
{p["problem"]}

What the prototype demonstrates:
• {p["proof"]}
• A practical way to evaluate the design, not just describe it.
• A clear boundary between prototype evidence and production claims.

Why it matters to {audience.lower()}:
The conversation needs to move from AI capability to reliable business outcomes.
{research_section}
Build: {p["repo"]}
Demo / project: {p["demo"]}

What would you test before trusting this in a real enterprise workflow?

#EnterpriseAI #AgenticAI #MarTech #CRM #AIGovernance #BuildInPublic"""
    draft_signature=(selected,audience,angle,punchline)
    if st.session_state.get("pub_draft_signature") != draft_signature:
        st.session_state["linkedin_draft"] = draft
        st.session_state["pub_draft_signature"] = draft_signature
    edited_draft=st.text_area("Editable LinkedIn draft",key="linkedin_draft",height=380)
    slug=re.sub(r"[^a-z0-9]+","-",selected.lower()).strip("-")
    st.download_button("Download LinkedIn draft",edited_draft,file_name=f"linkedin-{slug}.txt",mime="text/plain")
    if related:
        st.markdown("**Mapped research sources**")
        for r in related:
            st.markdown(f'- [{r["title"]}]({r["url"]}) · {r["source"]}')
    st.caption("Edit the draft to reflect what you personally tested. Research connections are explicitly mapped per project; no keyword-based matching is used.")


PAGES = [
    st.Page(render_portfolio, title="Build portfolio", icon="🚀", default=True),
    st.Page(render_concepts, title="Concept gallery", icon="✨"),
    st.Page(render_research, title="Research radar", icon="🧠"),
    st.Page(render_evaluate, title="Evaluate a concept", icon="🧪"),
    st.Page(render_linkedin_studio, title="LinkedIn studio", icon="📣"),
]

st.sidebar.markdown("### ⚙️ OPSFORGE")
st.sidebar.caption("AI Build Lab · Engineering, evaluation and governance")
navigation = st.navigation(PAGES)
navigation.run()

st.divider()
st.markdown("**OPSFORGE AI BUILD LAB** · Independent prototypes. Synthetic-data-first demonstrations. Evidence before claims.")
st.markdown("[GitHub profile](https://github.com/sghatge) · [Portfolio](https://sghatge.github.io/adobe-campaign-v8-governance/) · [OPSFORGE](https://github.com/sghatge/opsforge)")
