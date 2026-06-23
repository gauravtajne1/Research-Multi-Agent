# import streamlit as st
# import sys
# import os

# # ── Page config ────────────────────────────────────────────────────────────────
# st.set_page_config(
#     page_title="Research Agent",
#     page_icon="🔬",
#     layout="wide",
#     initial_sidebar_state="collapsed",
# )

# # ── Custom CSS ─────────────────────────────────────────────────────────────────
# st.markdown("""
# <style>
# @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;600&family=IBM+Plex+Sans:wght@300;400;500;600&display=swap');

# /* Base */
# html, body, [class*="css"] {
#     font-family: 'IBM Plex Sans', sans-serif;
#     background-color: #0d0f12;
#     color: #e2e8f0;
# }

# /* Hide Streamlit chrome */
# #MainMenu, footer, header { visibility: hidden; }
# .block-container { padding: 2.5rem 3rem 4rem; max-width: 960px; margin: auto; }

# /* ── Header ── */
# .site-header {
#     display: flex;
#     align-items: baseline;
#     gap: 0.75rem;
#     margin-bottom: 0.25rem;
# }
# .site-title {
#     font-family: 'IBM Plex Mono', monospace;
#     font-size: 1.6rem;
#     font-weight: 600;
#     color: #7ee8a2;
#     letter-spacing: -0.03em;
# }
# .site-sub {
#     font-size: 0.82rem;
#     color: #64748b;
#     font-weight: 300;
#     letter-spacing: 0.08em;
#     text-transform: uppercase;
# }
# .divider {
#     border: none;
#     border-top: 1px solid #1e2530;
#     margin: 1rem 0 2rem;
# }

# /* ── Input area ── */
# .stTextInput > label {
#     font-size: 0.78rem !important;
#     font-weight: 500 !important;
#     letter-spacing: 0.1em !important;
#     text-transform: uppercase !important;
#     color: #64748b !important;
#     margin-bottom: 0.4rem !important;
# }
# .stTextInput > div > div > input {
#     background: #131820 !important;
#     border: 1px solid #1e2d3d !important;
#     border-radius: 6px !important;
#     color: #e2e8f0 !important;
#     font-family: 'IBM Plex Mono', monospace !important;
#     font-size: 0.95rem !important;
#     padding: 0.65rem 1rem !important;
#     transition: border-color 0.2s;
# }
# .stTextInput > div > div > input:focus {
#     border-color: #7ee8a2 !important;
#     box-shadow: 0 0 0 2px rgba(126,232,162,0.08) !important;
# }

# /* ── Button ── */
# .stButton > button {
#     background: #7ee8a2 !important;
#     color: #0d0f12 !important;
#     font-family: 'IBM Plex Mono', monospace !important;
#     font-weight: 600 !important;
#     font-size: 0.82rem !important;
#     letter-spacing: 0.08em !important;
#     text-transform: uppercase !important;
#     border: none !important;
#     border-radius: 6px !important;
#     padding: 0.55rem 1.6rem !important;
#     cursor: pointer !important;
#     transition: background 0.2s, transform 0.1s !important;
# }
# .stButton > button:hover {
#     background: #5bd68a !important;
#     transform: translateY(-1px) !important;
# }
# .stButton > button:active { transform: translateY(0) !important; }

# /* ── Pipeline stepper ── */
# .pipeline-grid {
#     display: grid;
#     grid-template-columns: repeat(4, 1fr);
#     gap: 0.75rem;
#     margin: 2rem 0;
# }
# .step-card {
#     background: #131820;
#     border: 1px solid #1e2530;
#     border-radius: 8px;
#     padding: 0.9rem 1rem;
#     position: relative;
#     transition: border-color 0.3s;
# }
# .step-card.active  { border-color: #7ee8a2; }
# .step-card.done    { border-color: #334155; }
# .step-card.waiting { border-color: #1e2530; opacity: 0.55; }
# .step-num {
#     font-family: 'IBM Plex Mono', monospace;
#     font-size: 0.65rem;
#     color: #475569;
#     letter-spacing: 0.12em;
#     margin-bottom: 0.3rem;
# }
# .step-icon { font-size: 1.3rem; margin-bottom: 0.3rem; }
# .step-label {
#     font-size: 0.78rem;
#     font-weight: 500;
#     color: #94a3b8;
# }
# .step-card.active .step-label { color: #7ee8a2; }
# .step-card.done  .step-label  { color: #64748b; }

# /* ── Result panels ── */
# .result-panel {
#     background: #131820;
#     border: 1px solid #1e2530;
#     border-radius: 8px;
#     padding: 1.4rem 1.6rem;
#     margin-bottom: 1.25rem;
# }
# .panel-eyebrow {
#     font-family: 'IBM Plex Mono', monospace;
#     font-size: 0.65rem;
#     color: #7ee8a2;
#     letter-spacing: 0.14em;
#     text-transform: uppercase;
#     margin-bottom: 0.5rem;
# }
# .panel-heading {
#     font-size: 0.95rem;
#     font-weight: 600;
#     color: #cbd5e1;
#     margin-bottom: 0.75rem;
# }
# .panel-content {
#     font-size: 0.86rem;
#     color: #94a3b8;
#     line-height: 1.75;
#     white-space: pre-wrap;
#     word-break: break-word;
# }
# .panel-content.report-body {
#     font-family: 'IBM Plex Sans', sans-serif;
#     font-size: 0.88rem;
#     color: #cbd5e1;
# }

# /* ── Status badge ── */
# .status-row {
#     display: flex;
#     align-items: center;
#     gap: 0.5rem;
#     margin-bottom: 1.5rem;
# }
# .status-dot {
#     width: 7px; height: 7px;
#     border-radius: 50%;
#     background: #7ee8a2;
#     animation: pulse 1.2s ease-in-out infinite;
# }
# .status-dot.done { background: #334155; animation: none; }
# @keyframes pulse {
#     0%, 100% { opacity: 1; }
#     50%       { opacity: 0.35; }
# }
# .status-text {
#     font-family: 'IBM Plex Mono', monospace;
#     font-size: 0.72rem;
#     color: #64748b;
#     letter-spacing: 0.06em;
# }

# /* ── Error ── */
# .error-box {
#     background: #1a0e0e;
#     border: 1px solid #7f1d1d;
#     border-radius: 8px;
#     padding: 1rem 1.2rem;
#     color: #fca5a5;
#     font-family: 'IBM Plex Mono', monospace;
#     font-size: 0.82rem;
# }
# </style>
# """, unsafe_allow_html=True)


# # ── Helper: render step cards ──────────────────────────────────────────────────
# STEPS = [
#     ("01", "🔍", "Search"),
#     ("02", "📄", "Scrape"),
#     ("03", "✍️",  "Write"),
#     ("04", "🎯", "Critique"),
# ]

# def render_steps(active: int):
#     """active = 1-based index of current step; 0 = idle; 5 = all done"""
#     cards = ""
#     for i, (num, icon, label) in enumerate(STEPS, start=1):
#         if active == 0:
#             cls = "waiting"
#         elif i < active:
#             cls = "done"
#         elif i == active:
#             cls = "active"
#         else:
#             cls = "waiting"
#         cards += f"""
#         <div class="step-card {cls}">
#             <div class="step-num">STEP {num}</div>
#             <div class="step-icon">{icon}</div>
#             <div class="step-label">{label}</div>
#         </div>"""
#     st.markdown(f'<div class="pipeline-grid">{cards}</div>', unsafe_allow_html=True)


# def render_panel(eyebrow, heading, content, extra_class=""):
#     st.markdown(f"""
#     <div class="result-panel">
#         <div class="panel-eyebrow">{eyebrow}</div>
#         <div class="panel-heading">{heading}</div>
#         <div class="panel-content {extra_class}">{content}</div>
#     </div>""", unsafe_allow_html=True)


# # ── Header ────────────────────────────────────────────────────────────────────
# st.markdown("""
# <div class="site-header">
#     <span class="site-title">ResearchAgent</span>
#     <span class="site-sub">Multi-Agent Pipeline</span>
# </div>
# <hr class="divider">
# """, unsafe_allow_html=True)

# # ── Input row ─────────────────────────────────────────────────────────────────
# col_input, col_btn = st.columns([5, 1], vertical_alignment="bottom")
# with col_input:
#     topic = st.text_input(
#         "Research topic",
#         placeholder="e.g.  Advances in quantum error correction 2024",
#         label_visibility="visible",
#     )
# with col_btn:
#     run = st.button("Run →")

# # ── Idle state ────────────────────────────────────────────────────────────────
# if not run:
#     render_steps(0)
#     st.markdown("""
#     <div style="text-align:center; padding: 3rem 0; color: #334155;">
#         <div style="font-family:'IBM Plex Mono',monospace; font-size:0.75rem; letter-spacing:0.12em;">
#             ENTER A TOPIC AND HIT RUN
#         </div>
#     </div>""", unsafe_allow_html=True)
#     st.stop()

# # ── Validate ──────────────────────────────────────────────────────────────────
# if not topic.strip():
#     render_steps(0)
#     st.markdown('<div class="error-box">⚠ Please enter a research topic before running.</div>',
#                 unsafe_allow_html=True)
#     st.stop()

# # ── Import pipeline (lazy, so app loads even if deps missing) ─────────────────
# try:
#     from pipeline import run_research_pipeline
# except ImportError as e:
#     st.markdown(f'<div class="error-box">Import error: {e}<br>Make sure agents.py, tools.py, and pipeline.py are in the same directory.</div>',
#                 unsafe_allow_html=True)
#     st.stop()

# # ── Run pipeline with live step updates ───────────────────────────────────────
# step_placeholder   = st.empty()
# status_placeholder = st.empty()
# results_placeholder = st.empty()

# def show_status(text):
#     status_placeholder.markdown(f"""
#     <div class="status-row">
#         <div class="status-dot"></div>
#         <span class="status-text">{text}</span>
#     </div>""", unsafe_allow_html=True)

# # We monkey-patch print() so pipeline's console output is captured for status
# import builtins
# _original_print = builtins.print
# log_lines = []

# def capturing_print(*args, **kwargs):
#     line = " ".join(str(a) for a in args)
#     log_lines.append(line)
#     _original_print(*args, **kwargs)   # keep terminal output too

# builtins.print = capturing_print

# try:
#     # ── Step 1 ──
#     with step_placeholder:
#         render_steps(1)
#     show_status("Search agent is querying the web…")

#     # We need to run each step; the cleanest way is to call the full pipeline
#     # and use an intermediate callback approach. Since pipeline.py runs linearly,
#     # we stream progress via a thread + polling pattern — but for simplicity
#     # (and because Streamlit's execution is synchronous), we call the whole
#     # pipeline and update the UI at each natural pause using st.empty re-renders.

#     # To give live step feedback we override agents progressively via a wrapper.
#     import pipeline as pl
#     import agents as ag
#     import importlib

#     state = {}

#     # ── Step 1: Search ──
#     with step_placeholder:
#         render_steps(1)
#     show_status("Search agent is querying the web…")

#     search_agent = ag.build_search_agent()
#     search_result = search_agent.invoke({
#         "messages": [("user", f"Find recent, reliable and detailed information about: {topic}")]
#     })
#     state["search_results"] = search_result["messages"][-1].content

#     # ── Step 2: Scrape ──
#     with step_placeholder:
#         render_steps(2)
#     show_status("Reader agent is scraping top resources…")

#     reader_agent = ag.build_reader_agent()
#     reader_result = reader_agent.invoke({
#         "messages": [("user",
#             f"Based on the following search results about '{topic}', "
#             f"pick the most relevant URL and scrape it for deeper content.\n\n"
#             f"Search Results:\n{state['search_results'][:800]}"
#         )]
#     })
#     state["scraped_content"] = reader_result["messages"][-1].content

#     # ── Step 3: Write ──
#     with step_placeholder:
#         render_steps(3)
#     show_status("Writer is drafting the report…")

#     research_combined = (
#         f"SEARCH RESULTS:\n{state['search_results']}\n\n"
#         f"DETAILED SCRAPED CONTENT:\n{state['scraped_content']}"
#     )
#     state["report"] = ag.writer_chain.invoke({
#         "topic": topic,
#         "research": research_combined,
#     })

#     # ── Step 4: Critique ──
#     with step_placeholder:
#         render_steps(4)
#     show_status("Critic is reviewing the report…")

#     state["feedback"] = ag.critic_chain.invoke({
#         "report": state["report"]
#     })

#     # ── All done ──
#     with step_placeholder:
#         render_steps(5)
#     status_placeholder.markdown("""
#     <div class="status-row">
#         <div class="status-dot done"></div>
#         <span class="status-text">PIPELINE COMPLETE</span>
#     </div>""", unsafe_allow_html=True)

#     # ── Render results ─────────────────────────────────────────────────────────
#     with results_placeholder.container():
#         st.markdown("---")

#         render_panel(
#             "STEP 01 · SEARCH AGENT",
#             f"Web results for: {topic}",
#             state["search_results"][:2000] + ("…" if len(state["search_results"]) > 2000 else ""),
#         )

#         render_panel(
#             "STEP 02 · READER AGENT",
#             "Scraped content from top resource",
#             state["scraped_content"][:2000] + ("…" if len(state["scraped_content"]) > 2000 else ""),
#         )

#         render_panel(
#             "STEP 03 · WRITER",
#             "Final research report",
#             state["report"],
#             extra_class="report-body",
#         )

#         render_panel(
#             "STEP 04 · CRITIC",
#             "Editorial feedback",
#             state["feedback"],
#         )

#         # ── Download button ─────────────────────────────────────────────────
#         full_output = (
#             f"RESEARCH TOPIC: {topic}\n"
#             f"{'='*60}\n\n"
#             f"[SEARCH RESULTS]\n{state['search_results']}\n\n"
#             f"[SCRAPED CONTENT]\n{state['scraped_content']}\n\n"
#             f"[REPORT]\n{state['report']}\n\n"
#             f"[CRITIC FEEDBACK]\n{state['feedback']}\n"
#         )
#         st.download_button(
#             label="⬇  Download full report (.txt)",
#             data=full_output,
#             file_name=f"research_{topic[:40].replace(' ','_')}.txt",
#             mime="text/plain",
#         )

# except Exception as e:
#     with step_placeholder:
#         render_steps(0)
#     status_placeholder.empty()
#     st.markdown(f'<div class="error-box">Pipeline error:<br><br>{e}</div>',
#                 unsafe_allow_html=True)

# finally:
#     builtins.print = _original_print   # always restore print