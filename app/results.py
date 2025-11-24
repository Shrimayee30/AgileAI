import json
import gradio as gr

# ---- import your sidebar helpers ----
from agileai_side import SIDEBAR_CSS, build_sidebar

RESULT_PATH = "training_example_1.json"   # adjust if needed

# Direct icon URLs (CDN) - small thumb favicons
THUMB_UP_ICON = "https://cdnjs.cloudflare.com/ajax/libs/bootstrap-icons/1.8.2/icons/hand-thumbs-up.svg"
THUMB_DOWN_ICON = "https://cdnjs.cloudflare.com/ajax/libs/bootstrap-icons/1.8.2/icons/hand-thumbs-down.svg"


# ----------------- DATA HELPERS ----------------- #

def load_result(path=RESULT_PATH):
    with open(path, "r") as f:
        return json.load(f)


def story_body_html(story):
    ac_list = "".join(f"<li>{item}</li>" for item in story["acceptance_criteria"])
    dor_list = "".join(f"<li>{item}</li>" for item in story["definition_of_ready"])
    return f"""
<p class="story-description">{story['description']}</p>

<div class="story-section-label">Acceptance criteria</div>
<ul class="story-list">{ac_list}</ul>

<div class="story-section-label">Definition of Ready</div>
<ul class="story-list">{dor_list}</ul>

<div class="story-raw-ref">Source: {story['raw_text_reference']}</div>
"""


# ----------------- FEEDBACK HANDLER ----------------- #

def handle_feedback(item_type, item_id, direction, state):
    """
    item_type: 'epic' | 'feature' | 'story'
    item_id:   'E1', 'F2', 'S3', etc.
    direction: 'up' | 'down'
    state:     dict stored in gr.State
    """
    if state is None:
        state = {}

    key = f"{item_type}:{item_id}"
    counts = state.get(key, {"up": 0, "down": 0})
    counts[direction] += 1
    state[key] = counts

    msg = f"Recorded {direction} vote for {item_type} {item_id}"
    return msg, state


# ----------------- RESULTS-PAGE CSS ----------------- #

RESULTS_CSS = f"""
body, .gradio-container {{
    background: #f5f7fb;
    font-family: system-ui, -apple-system, BlinkMacSystemFont, "SF Pro Text", sans-serif;
}}

/* main panel */
#results-main {{
    padding: 24px 32px 40px 32px;
}}

/* header bar */
.page-header {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 16px;
    margin-bottom: 12px;
}}

.page-title {{
    display: flex;
    align-items: center;
    gap: 10px;
}}

.page-title h1 {{
    font-size: 24px;
    font-weight: 600;
    margin: 0;
}}

.status-pill {{
    font-size: 12px;
    padding: 4px 10px;
    border-radius: 999px;
    background: #e0fbea;
    color: #15803d;
    font-weight: 500;
}}

.header-actions {{
    display: flex;
    gap: 8px;
}}

.header-actions button {{
    border-radius: 999px;
    padding: 8px 16px;
    font-size: 13px;
    border: 1px solid #d1d5db;
    background: #ffffff;
    cursor: pointer;
}}

.header-actions button.primary {{
    background: #2563eb;
    border-color: #2563eb;
    color: #ffffff;
}}

/* tiny toast for feedback */
#feedback-toast {{
    font-size: 11px;
    color: #4b5563;
    margin-bottom: 8px;
    opacity: 0.8;
}}

/* upload card */
.upload-card {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 14px 18px;
    border-radius: 16px;
    background: #ffffff;
    box-shadow: 0 1px 3px rgba(15, 23, 42, 0.06);
    margin-bottom: 14px;
}}

.upload-left {{
    display: flex;
    align-items: center;
    gap: 12px;
}}

.file-icon {{
    width: 36px;
    height: 36px;
    border-radius: 12px;
    background: #e5edff;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 20px;
}}

.file-text-title {{
    font-size: 14px;
    font-weight: 500;
}}

.file-text-subtitle {{
    font-size: 12px;
    color: #6b7280;
}}

.view-file-btn {{
    border-radius: 999px;
    padding: 8px 14px;
    font-size: 13px;
    border: 1px solid #d1d5db;
    background: #f9fafb;
    cursor: pointer;
}}

/* AI summary banner */
.ai-summary {{
    display: flex;
    align-items: flex-start;
    gap: 12px;
    padding: 16px 18px;
    border-radius: 16px;
    background: #ffffff;
    box-shadow: 0 1px 3px rgba(15, 23, 42, 0.06);
    margin-bottom: 18px;
}}

.ai-avatar {{
    width: 32px;
    height: 32px;
    border-radius: 999px;
    background: #2563eb;
    display: flex;
    align-items: center;
    justify-content: center;
    color: #ffffff;
    font-weight: 600;
    font-size: 16px;
}}

.ai-text {{
    font-size: 13px;
    color: #374151;
}}

/* stats cards */
.stats-row {{
    display: flex;
    gap: 16px;
    margin-bottom: 18px;
}}

.stat-card {{
    flex: 1;
    background: #ffffff;
    border-radius: 16px;
    padding: 14px 18px;
    box-shadow: 0 1px 3px rgba(15, 23, 42, 0.06);
}}

.stat-label {{
    font-size: 12px;
    color: #6b7280;
    margin-bottom: 6px;
}}

.stat-value {{
    font-size: 24px;
    font-weight: 600;
}}

/* ============ HIERARCHY COLORS ============ */

/* EPIC – soft blue */
.epic-accordion > details {{
    border-radius: 18px;
    overflow: hidden;
    border: 1px solid #c7d2fe;
    background: #eef2ff;
    box-shadow: 0 1px 3px rgba(37, 99, 235, 0.10);
}}

.epic-accordion summary {{
    background: linear-gradient(90deg, #dbeafe, #e0f2fe);
    padding: 12px 16px;
    font-weight: 500;
    font-size: 14px;
}}

/* FEATURE – minty green */
.feature-accordion > details {{
    border-radius: 16px;
    margin: 8px 12px 12px 12px;
    border: 1px solid #bbf7d0;
    background: #ecfdf3;
    box-shadow: 0 1px 3px rgba(22, 163, 74, 0.10);
}}

.feature-accordion summary {{
    padding: 10px 14px;
    font-weight: 500;
    font-size: 13px;
}}

.feature-header {{
    padding: 8px 16px 4px 16px;
    font-size: 13px;
}}

.feature-header-title {{
    font-weight: 500;
    margin-bottom: 2px;
}}

.feature-header-sub {{
    color: #4b5563;
}}

/* USER STORIES – “milk grey” */
.story-card {{
    border-radius: 14px;
    border: 1px solid #e5e7eb;
    background: #f5f5f7;
    padding: 10px 12px;
    margin-bottom: 10px;
    box-shadow: 0 1px 2px rgba(15, 23, 42, 0.06);
}}

.story-header-row {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 4px;
}}

.story-header-left {{
    display: flex;
    align-items: center;
    gap: 8px;
}}

.story-id {{
    font-size: 13px;
    font-weight: 600;
    padding: 2px 8px;
    border-radius: 999px;
    background: #e5e7eb;
}}

.story-title {{
    font-size: 13px;
    font-weight: 500;
}}

.story-description {{
    font-size: 13px;
    color: #374151;
    margin: 4px 0 8px 0;
}}

.story-section-label {{
    font-size: 12px;
    font-weight: 600;
    margin-top: 6px;
    margin-bottom: 2px;
}}

.story-list {{
    padding-left: 18px;
    margin: 0;
    font-size: 12px;
}}

.story-raw-ref {{
    font-size: 11px;
    color: #6b7280;
    margin-top: 6px;
}}

/* ====== VOTE BUTTONS (EPIC / FEATURE / STORY) ====== */

.vote-row {{
    display: flex;
    justify-content: flex-end;
    gap: 6px;
    padding: 4px 16px 0 16px;
}}

.vote-btn {{
    min-width: 22px !important;
    max-width: 22px !important;
    height: 22px !important;
    padding: 0 !important;
    border-radius: 999px !important;
    border: none !important;
    background-color: transparent !important;
    background-size: 16px 16px;
    background-position: center;
    background-repeat: no-repeat;
    cursor: pointer;
    box-shadow: none !important;
}}

.vote-btn:hover {{
    background-color: rgba(15,23,42,0.04) !important;
}}

.vote-up {{
    background-image: url('{THUMB_UP_ICON}');
}}

.vote-down {{
    background-image: url('{THUMB_DOWN_ICON}');
}}
"""

# combine sidebar + results css
COMBINED_CSS = SIDEBAR_CSS + RESULTS_CSS


# ----------------- UI ----------------- #

def build_results_app():
    data = load_result()
    epic = data["epic"]
    features = data["features"]
    total_features = len(features)
    total_stories = sum(len(f["stories"]) for f in features)

    with gr.Blocks(css=COMBINED_CSS) as demo:
        feedback_state = gr.State({})
        with gr.Row():
            # ---- SIDEBAR ----
            with gr.Column(elem_id="sidebar", scale=1, min_width=260):
                recent_projects = [
                    "E-commerce Platform",
                    "Mobile Banking App",
                    "Healthcare Portal",
                    "CRM System",
                    "Inventory Management",
                    "Social Media Dashboard",
                    "Analytics Platform",
                ]
                build_sidebar(recent_projects)

            # ---- MAIN RESULTS PANEL ----
            with gr.Column(elem_id="results-main", scale=4):

                # Header
                gr.Markdown(
                    """
<div class="page-header">
  <div class="page-title">
    <h1>E-commerce Platform</h1>
    <span class="status-pill">Generated</span>
  </div>
  <div class="header-actions">
    <button>✏️ Edit</button>
    <button class="primary">📤 Publish</button>
  </div>
</div>
"""
                )

                feedback_toast = gr.Markdown("", elem_id="feedback-toast")

                # Uploaded file card
                gr.Markdown(
                    """
<div class="upload-card">
  <div class="upload-left">
    <div class="file-icon">📄</div>
    <div>
      <div class="file-text-title">ecommerce-requirements.pdf</div>
      <div class="file-text-subtitle">Uploaded 2 minutes ago · 2.4 MB</div>
    </div>
  </div>
  <button class="view-file-btn">View File</button>
</div>
"""
                )

                # AI summary
                gr.Markdown(
                    """
<div class="ai-summary">
  <div class="ai-avatar">AI</div>
  <div class="ai-text">
    I've analyzed your requirements document and generated a comprehensive breakdown of epics,
    features, and user stories for this project. Review the items below and provide feedback.
  </div>
</div>
"""
                )

                # Stats
                gr.Markdown(
                    f"""
<div class="stats-row">
  <div class="stat-card">
    <div class="stat-label">Epics</div>
    <div class="stat-value">1</div>
  </div>
  <div class="stat-card">
    <div class="stat-label">Features</div>
    <div class="stat-value">{total_features}</div>
  </div>
  <div class="stat-card">
    <div class="stat-label">User Stories</div>
    <div class="stat-value">{total_stories}</div>
  </div>
</div>
"""
                )

                # ---------- Epic → Features → Stories ----------
                epic_label = f"E1 · {epic['title']} · {total_features} Features"
                with gr.Accordion(epic_label, open=True, elem_classes=["epic-accordion"]):
                    # Epic vote row
                    with gr.Row(elem_classes=["vote-row"]):
                        epic_up = gr.Button("", elem_classes=["vote-btn", "vote-up"])
                        epic_down = gr.Button("", elem_classes=["vote-btn", "vote-down"])

                    gr.Markdown(epic["summary"], elem_classes=["epic-summary"])

                    # Callbacks for epic
                    def epic_up_fn(state):
                        return handle_feedback("epic", "E1", "up", state)

                    def epic_down_fn(state):
                        return handle_feedback("epic", "E1", "down", state)

                    epic_up.click(epic_up_fn, [feedback_state], [feedback_toast, feedback_state])
                    epic_down.click(epic_down_fn, [feedback_state], [feedback_toast, feedback_state])

                    # Features
                    for f_idx, feat in enumerate(features, start=1):
                        feat_id = f"F{f_idx}"
                        feat_label = f"{feat_id} · {feat['title']} · {len(feat['stories'])} Stories"
                        with gr.Accordion(feat_label, open=False, elem_classes=["feature-accordion"]):
                            # Feature vote row
                            with gr.Row(elem_classes=["vote-row"]):
                                feat_up = gr.Button("", elem_classes=["vote-btn", "vote-up"])
                                feat_down = gr.Button("", elem_classes=["vote-btn", "vote-down"])

                            gr.Markdown(
                                f"""
<div class="feature-header">
  <div class="feature-header-title">{feat['title']}</div>
  <div class="feature-header-sub">{feat['description']}</div>
  <div class="feature-header-sub"><strong>Web page:</strong> {feat['webpage']}</div>
</div>
"""
                            )

                            # Feature callbacks (capture fid via default arg)
                            def make_feature_fns(fid):
                                def fup(state):
                                    return handle_feedback("feature", fid, "up", state)
                                def fdown(state):
                                    return handle_feedback("feature", fid, "down", state)
                                return fup, fdown

                            fup_fn, fdown_fn = make_feature_fns(feat_id)
                            feat_up.click(fup_fn, [feedback_state], [feedback_toast, feedback_state])
                            feat_down.click(fdown_fn, [feedback_state], [feedback_toast, feedback_state])

                            # Stories
                            for s_idx, story in enumerate(feat["stories"], start=1):
                                story_id = f"S{s_idx}"
                                with gr.Group(elem_classes=["story-card"]):
                                    with gr.Row(elem_classes=["story-header-row"]):
                                        gr.Markdown(
                                            f"""
<div class="story-header-left">
  <span class="story-id">{story_id}</span>
  <span class="story-title">{story['title']}</span>
</div>
""",
                                            elem_classes=["story-header-left"],
                                        )
                                        with gr.Row(elem_classes=["vote-row"]):
                                            story_up = gr.Button(
                                                "", elem_classes=["vote-btn", "vote-up"]
                                            )
                                            story_down = gr.Button(
                                                "", elem_classes=["vote-btn", "vote-down"]
                                            )

                                    # Story body
                                    body_html = story_body_html(story)
                                    gr.Markdown(body_html)

                                    # Story callbacks
                                    def make_story_fns(sid):
                                        def sup(state):
                                            return handle_feedback("story", sid, "up", state)
                                        def sdown(state):
                                            return handle_feedback("story", sid, "down", state)
                                        return sup, sdown

                                    sup_fn, sdown_fn = make_story_fns(story_id)
                                    story_up.click(
                                        sup_fn, [feedback_state], [feedback_toast, feedback_state]
                                    )
                                    story_down.click(
                                        sdown_fn, [feedback_state], [feedback_toast, feedback_state]
                                    )

    return demo


if __name__ == "__main__":
    demo = build_results_app()
    demo.launch()
