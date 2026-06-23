import streamlit as st
import sys
import os
import builtins

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Research Agent",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Custom CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;600&family=IBM+Plex+Sans:wght@300;400;500;600;700&display=swap');

/* ── Base ── */
html, body, [class*="css"] {
    font-family: 'IBM Plex Sans', sans-serif;
    background-color: #080a0e;
    color: #e2e8f0;
}
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 2.5rem 3rem 4rem; max-width: 1000px; margin: auto; }

/* ── Header ── */
.site-header {
    display: flex;
    align-items: center;
    gap: 1rem;
    margin-bottom: 0.25rem;
}
.site-title {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 2rem;
    font-weight: 700;
    letter-spacing: -0.04em;
    background: linear-gradient(90deg, #4f8ef7, #a78bfa, #f472b6);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.site-badge {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.68rem;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: #4f8ef7;
    border: 1px solid #1e3a5f;
    background: rgba(79,142,247,0.07);
    padding: 3px 10px;
    border-radius: 20px;
}
.divider {
    border: none;
    border-top: 1px solid #151c28;
    margin: 1rem 0 2rem;
}

/* ── Input ── */
.stTextInput > label {
    font-size: 0.75rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.12em !important;
    text-transform: uppercase !important;
    color: #4f8ef7 !important;
    margin-bottom: 0.4rem !important;
}
.stTextInput > div > div > input {
    background: #0d1117 !important;
    border: 1px solid #1e2d3d !important;
    border-radius: 8px !important;
    color: #e2e8f0 !important;
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 0.95rem !important;
    padding: 0.7rem 1rem !important;
    transition: border-color 0.2s, box-shadow 0.2s;
}
.stTextInput > div > div > input:focus {
    border-color: #4f8ef7 !important;
    box-shadow: 0 0 0 3px rgba(79,142,247,0.12) !important;
}

/* ── Button ── */
.stButton > button {
    background: linear-gradient(135deg, #4f8ef7, #7c5cbf) !important;
    color: #fff !important;
    font-family: 'IBM Plex Mono', monospace !important;
    font-weight: 700 !important;
    font-size: 0.82rem !important;
    letter-spacing: 0.1em !important;
    text-transform: uppercase !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 0.6rem 1.8rem !important;
    cursor: pointer !important;
    transition: opacity 0.2s, transform 0.1s !important;
}
.stButton > button:hover  { opacity: 0.88 !important; transform: translateY(-1px) !important; }
.stButton > button:active { transform: translateY(0) !important; }

/* ── Agent colors ── */
/* Search  = blue   #4f8ef7 */
/* Scrape  = purple #a78bfa */
/* Writer  = pink   #f472b6 */
/* Critic  = amber  #fbbf24 */

/* ── Pipeline stepper ── */
.pipeline-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 1rem;
    margin: 2rem 0;
}
.step-card {
    background: #0d1117;
    border: 1px solid #1e2530;
    border-radius: 12px;
    padding: 1.2rem 1.1rem 1rem;
    position: relative;
    transition: border-color 0.3s, box-shadow 0.3s, background 0.3s;
    overflow: hidden;
}
/* colour stripe top */
.step-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    border-radius: 12px 12px 0 0;
    opacity: 0;
    transition: opacity 0.3s;
}
.step-card.s1::before { background: #4f8ef7; }
.step-card.s2::before { background: #a78bfa; }
.step-card.s3::before { background: #f472b6; }
.step-card.s4::before { background: #fbbf24; }

.step-card.active::before, .step-card.done::before { opacity: 1; }

.step-card.active.s1 { border-color: #4f8ef7; box-shadow: 0 0 20px rgba(79,142,247,0.18); background: rgba(79,142,247,0.05); }
.step-card.active.s2 { border-color: #a78bfa; box-shadow: 0 0 20px rgba(167,139,250,0.18); background: rgba(167,139,250,0.05); }
.step-card.active.s3 { border-color: #f472b6; box-shadow: 0 0 20px rgba(244,114,182,0.18); background: rgba(244,114,182,0.05); }
.step-card.active.s4 { border-color: #fbbf24; box-shadow: 0 0 20px rgba(251,191,36,0.18);  background: rgba(251,191,36,0.05); }

.step-card.done.s1 { border-color: rgba(79,142,247,0.3);  background: rgba(79,142,247,0.04); }
.step-card.done.s2 { border-color: rgba(167,139,250,0.3); background: rgba(167,139,250,0.04); }
.step-card.done.s3 { border-color: rgba(244,114,182,0.3); background: rgba(244,114,182,0.04); }
.step-card.done.s4 { border-color: rgba(251,191,36,0.3);  background: rgba(251,191,36,0.04); }

.step-card.waiting { border-color: #1a2030; opacity: 0.45; }

.step-num {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.6rem;
    color: #475569;
    letter-spacing: 0.16em;
    margin-bottom: 0.6rem;
}
.step-icon { font-size: 1.8rem; margin-bottom: 0.5rem; line-height: 1; }

.step-agent-name {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 1.05rem;
    font-weight: 700;
    letter-spacing: -0.01em;
    margin-bottom: 0.2rem;
    transition: color 0.3s;
}
.step-card.waiting .step-agent-name { color: #334155; }
.step-card.done.s1 .step-agent-name,
.step-card.active.s1 .step-agent-name { color: #4f8ef7; }
.step-card.done.s2 .step-agent-name,
.step-card.active.s2 .step-agent-name { color: #a78bfa; }
.step-card.done.s3 .step-agent-name,
.step-card.active.s3 .step-agent-name { color: #f472b6; }
.step-card.done.s4 .step-agent-name,
.step-card.active.s4 .step-agent-name { color: #fbbf24; }

.step-desc {
    font-size: 0.7rem;
    color: #475569;
    line-height: 1.4;
}
.step-card.active .step-desc { color: #94a3b8; }

/* tick for done */
.step-tick {
    position: absolute;
    top: 10px; right: 12px;
    font-size: 0.75rem;
    display: none;
}
.step-card.done .step-tick { display: block; }
.step-card.done.s1 .step-tick { color: #4f8ef7; }
.step-card.done.s2 .step-tick { color: #a78bfa; }
.step-card.done.s3 .step-tick { color: #f472b6; }
.step-card.done.s4 .step-tick { color: #fbbf24; }

/* pulse ring for active */
.step-ring {
    position: absolute;
    top: 10px; right: 12px;
    width: 8px; height: 8px;
    border-radius: 50%;
    display: none;
}
.step-card.active .step-ring { display: block; animation: ring-pulse 1.2s infinite; }
.step-card.active.s1 .step-ring { background: #4f8ef7; box-shadow: 0 0 0 0 rgba(79,142,247,0.6); }
.step-card.active.s2 .step-ring { background: #a78bfa; box-shadow: 0 0 0 0 rgba(167,139,250,0.6); }
.step-card.active.s3 .step-ring { background: #f472b6; box-shadow: 0 0 0 0 rgba(244,114,182,0.6); }
.step-card.active.s4 .step-ring { background: #fbbf24; box-shadow: 0 0 0 0 rgba(251,191,36,0.6); }

@keyframes ring-pulse {
    0%   { transform: scale(1);   opacity: 1; }
    70%  { transform: scale(2.2); opacity: 0; }
    100% { transform: scale(1);   opacity: 0; }
}

/* ── Status row ── */
.status-row {
    display: flex;
    align-items: center;
    gap: 0.6rem;
    margin-bottom: 1.5rem;
}
.status-dot {
    width: 7px; height: 7px;
    border-radius: 50%;
    animation: dot-pulse 1.2s ease-in-out infinite;
}
.status-dot.s1 { background: #4f8ef7; }
.status-dot.s2 { background: #a78bfa; }
.status-dot.s3 { background: #f472b6; }
.status-dot.s4 { background: #fbbf24; }
.status-dot.done { background: #22c55e; animation: none; }
@keyframes dot-pulse {
    0%, 100% { opacity: 1; } 50% { opacity: 0.25; }
}
.status-text {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.73rem;
    color: #64748b;
    letter-spacing: 0.06em;
}

/* ── Result panels ── */
.result-panel {
    background: #0d1117;
    border-radius: 12px;
    padding: 0;
    margin-bottom: 1.4rem;
    overflow: hidden;
    border: 1px solid #1e2530;
}
.panel-header {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    padding: 1rem 1.4rem 0.9rem;
    border-bottom: 1px solid #151c28;
}
.panel-color-bar {
    width: 4px;
    height: 38px;
    border-radius: 4px;
    flex-shrink: 0;
}
.panel-header-text { flex: 1; }
.panel-eyebrow {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.6rem;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    margin-bottom: 0.25rem;
    opacity: 0.7;
}
.panel-agent-name {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 1.15rem;
    font-weight: 700;
    letter-spacing: -0.01em;
}
.panel-heading {
    font-size: 0.8rem;
    color: #475569;
    margin-top: 0.15rem;
    font-weight: 400;
}
.panel-emoji { font-size: 1.6rem; }
.panel-body {
    padding: 1.2rem 1.4rem;
    font-size: 0.86rem;
    color: #94a3b8;
    line-height: 1.8;
    white-space: pre-wrap;
    word-break: break-word;
}
.panel-body.report { color: #cbd5e1; font-size: 0.88rem; }

/* per-agent panel accent */
.panel-s1 .panel-color-bar  { background: #4f8ef7; }
.panel-s1 .panel-eyebrow    { color: #4f8ef7; }
.panel-s1 .panel-agent-name { color: #4f8ef7; }
.panel-s1 { border-color: rgba(79,142,247,0.2); }

.panel-s2 .panel-color-bar  { background: #a78bfa; }
.panel-s2 .panel-eyebrow    { color: #a78bfa; }
.panel-s2 .panel-agent-name { color: #a78bfa; }
.panel-s2 { border-color: rgba(167,139,250,0.2); }

.panel-s3 .panel-color-bar  { background: #f472b6; }
.panel-s3 .panel-eyebrow    { color: #f472b6; }
.panel-s3 .panel-agent-name { color: #f472b6; }
.panel-s3 { border-color: rgba(244,114,182,0.2); }

.panel-s4 .panel-color-bar  { background: #fbbf24; }
.panel-s4 .panel-eyebrow    { color: #fbbf24; }
.panel-s4 .panel-agent-name { color: #fbbf24; }
.panel-s4 { border-color: rgba(251,191,36,0.2); }

/* ── Error box ── */
.error-box {
    background: #1a0e0e;
    border: 1px solid #7f1d1d;
    border-radius: 10px;
    padding: 1rem 1.3rem;
    color: #fca5a5;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.82rem;
    line-height: 1.6;
}

/* ── Download button ── */
.stDownloadButton > button {
    background: transparent !important;
    border: 1px solid #1e3a5f !important;
    color: #4f8ef7 !important;
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 0.78rem !important;
    border-radius: 8px !important;
    padding: 0.5rem 1.2rem !important;
    transition: background 0.2s, border-color 0.2s !important;
}
.stDownloadButton > button:hover {
    background: rgba(79,142,247,0.08) !important;
    border-color: #4f8ef7 !important;
}
</style>
""", unsafe_allow_html=True)


# ── Agent definitions ──────────────────────────────────────────────────────────
AGENTS = [
    ("01", "🔍", "Search Agent",  "Finds recent & reliable sources",   "s1"),
    ("02", "📄", "Reader Agent",  "Scrapes top resource for content",  "s2"),
    ("03", "✍️",  "Writer",  "Drafts the full research report",   "s3"),
    ("04", "🎯", "Critic ",  "Reviews & provides feedback",       "s4"),
]


# ── Render pipeline steps ──────────────────────────────────────────────────────
def render_steps(active: int):
    cards = ""
    for i, (num, icon, name, desc, color) in enumerate(AGENTS, start=1):
        if active == 0:
            cls = "waiting"
        elif i < active:
            cls = "done"
        elif i == active:
            cls = "active"
        else:
            cls = "waiting"

        cards += f"""
        <div class="step-card {cls} {color}">
            <div class="step-ring"></div>
            <div class="step-tick">✓</div>
            <div class="step-num">STEP {num}</div>
            <div class="step-icon">{icon}</div>
            <div class="step-agent-name">{name}</div>
            <div class="step-desc">{desc}</div>
        </div>"""

    st.markdown(f'<div class="pipeline-grid">{cards}</div>', unsafe_allow_html=True)


# ── Render result panel ────────────────────────────────────────────────────────
def render_panel(step_idx, heading, content, extra_class=""):
    _, icon, name, _, color = AGENTS[step_idx - 1]
    num = AGENTS[step_idx - 1][0]
    st.markdown(f"""
    <div class="result-panel panel-{color}">
        <div class="panel-header">
            <div class="panel-color-bar"></div>
            <div class="panel-header-text">
                <div class="panel-eyebrow">STEP {num}</div>
                <div class="panel-agent-name">{icon} {name}</div>
                <div class="panel-heading">{heading}</div>
            </div>
        </div>
        <div class="panel-body {extra_class}">{content}</div>
    </div>""", unsafe_allow_html=True)


# ── Status message ─────────────────────────────────────────────────────────────
def show_status(placeholder, text, color_cls="s1", done=False):
    dot_cls = "done" if done else color_cls
    placeholder.markdown(f"""
    <div class="status-row">
        <div class="status-dot {dot_cls}"></div>
        <span class="status-text">{text}</span>
    </div>""", unsafe_allow_html=True)


# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="site-header">
    <span class="site-title">ResearchAgent</span>
    <span class="site-badge">Multi-Agent · 4 Steps</span>
</div>
<hr class="divider">
""", unsafe_allow_html=True)

# ── Input row ─────────────────────────────────────────────────────────────────
col_input, col_btn = st.columns([5, 1], vertical_alignment="bottom")
with col_input:
    topic = st.text_input(
        "Research topic",
        placeholder="e.g.  Advances in quantum error correction 2024",
        label_visibility="visible",
    )
with col_btn:
    run = st.button("Run →")

# ── Idle state ────────────────────────────────────────────────────────────────
if not run:
    render_steps(0)
    st.markdown("""
    <div style="text-align:center; padding: 3rem 0; color: #1e2d3d;">
        <div style="font-size:2rem; margin-bottom:0.75rem;">🔬</div>
        <div style="font-family:'IBM Plex Mono',monospace; font-size:0.72rem;
                    letter-spacing:0.16em; color:#2d3f55;">
            ENTER A TOPIC AND HIT RUN
        </div>
    </div>""", unsafe_allow_html=True)
    st.stop()

# ── Validate ──────────────────────────────────────────────────────────────────
if not topic.strip():
    render_steps(0)
    st.markdown('<div class="error-box">⚠ Please enter a research topic before running.</div>',
                unsafe_allow_html=True)
    st.stop()

# ── Lazy import ───────────────────────────────────────────────────────────────
try:
    import agents as ag
except ImportError as e:
    st.markdown(f'<div class="error-box">Import error: {e}<br>Make sure agents.py, tools.py, and pipeline.py are in the same directory.</div>',
                unsafe_allow_html=True)
    st.stop()

# ── Placeholders ──────────────────────────────────────────────────────────────
step_ph   = st.empty()
status_ph = st.empty()
results_ph = st.empty()

# ── Capture print silently ────────────────────────────────────────────────────
_original_print = builtins.print
def capturing_print(*args, **kwargs): _original_print(*args, **kwargs)
builtins.print = capturing_print

try:
    state = {}

    # ── Step 1: Search ──────────────────────────────────────────────────────
    with step_ph: render_steps(1)
    show_status(status_ph, "Search Agent is querying the web…", "s1")

    search_agent = ag.build_search_agent()
    search_result = search_agent.invoke({
        "messages": [("user", f"Find recent, reliable and detailed information about: {topic}")]
    })
    state["search_results"] = search_result["messages"][-1].content

    # ── Step 2: Scrape ──────────────────────────────────────────────────────
    with step_ph: render_steps(2)
    show_status(status_ph, "Reader Agent is scraping top resources…", "s2")

    reader_agent = ag.build_reader_agent()
    reader_result = reader_agent.invoke({
        "messages": [("user",
            f"Based on the following search results about '{topic}', "
            f"pick the most relevant URL and scrape it for deeper content.\n\n"
            f"Search Results:\n{state['search_results'][:800]}"
        )]
    })
    state["scraped_content"] = reader_result["messages"][-1].content

    # ── Step 3: Write ───────────────────────────────────────────────────────
    with step_ph: render_steps(3)
    show_status(status_ph, "Writer Chain is drafting the report…", "s3")

    research_combined = (
        f"SEARCH RESULTS:\n{state['search_results']}\n\n"
        f"DETAILED SCRAPED CONTENT:\n{state['scraped_content']}"
    )
    state["report"] = ag.writer_chain.invoke({
        "topic": topic,
        "research": research_combined,
    })

    # ── Step 4: Critique ────────────────────────────────────────────────────
    with step_ph: render_steps(4)
    show_status(status_ph, "Critic Chain is reviewing the report…", "s4")

    state["feedback"] = ag.critic_chain.invoke({"report": state["report"]})

    # ── All done ────────────────────────────────────────────────────────────
    with step_ph: render_steps(5)
    show_status(status_ph, "PIPELINE COMPLETE — all 4 agents finished", done=True)

    # ── Results ─────────────────────────────────────────────────────────────
    with results_ph.container():
        st.markdown("<br>", unsafe_allow_html=True)

        render_panel(
            1,
            f"Web results for: {topic}",
            state["search_results"][:2000] + ("…" if len(state["search_results"]) > 2000 else ""),
        )
        render_panel(
            2,
            "Scraped content from top resource",
            state["scraped_content"][:2000] + ("…" if len(state["scraped_content"]) > 2000 else ""),
        )
        render_panel(
            3,
            "Final research report",
            state["report"],
            extra_class="report",
        )
        render_panel(
            4,
            "Editorial feedback & improvement suggestions",
            state["feedback"],
        )

        st.markdown("<br>", unsafe_allow_html=True)

        full_output = (
            f"RESEARCH TOPIC: {topic}\n"
            f"{'='*60}\n\n"
            f"[SEARCH RESULTS]\n{state['search_results']}\n\n"
            f"[SCRAPED CONTENT]\n{state['scraped_content']}\n\n"
            f"[REPORT]\n{state['report']}\n\n"
            f"[CRITIC FEEDBACK]\n{state['feedback']}\n"
        )
        st.download_button(
            label="⬇  Download full report (.txt)",
            data=full_output,
            file_name=f"research_{topic[:40].replace(' ', '_')}.txt",
            mime="text/plain",
        )

except Exception as e:
    with step_ph: render_steps(0)
    status_ph.empty()
    st.markdown(f'<div class="error-box">Pipeline error — Step failed:<br><br>{e}</div>',
                unsafe_allow_html=True)

finally:
    builtins.print = _original_print