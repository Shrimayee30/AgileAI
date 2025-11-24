# agileai_side.py
import gradio as gr

# ---------- SIDEBAR CSS (only sidebar styling) ----------
SIDEBAR_CSS = """
/* ---------- SIDEBAR ROOT ---------- */
#sidebar {
    background: #0D1226;
    height: 100vh;
    padding: 24px 14px;
    color: white;
    overflow: hidden;  /* sidebar itself does not scroll */
}

/* Make ALL sidebar text white */
#sidebar * {
    color: white !important;
}

/* MAIN FLEX CONTAINER: header (fixed) + middle (scroll) + footer (fixed) */
#sidebar_inner {
    display: flex;
    flex-direction: column;
    height: 100%;
}

/* ---------- HEADER (LOGO + NEW CHAT) ---------- */
#sidebar_header {
    flex: 0 0 auto;
}

#logo_row {
    display: flex;
    align-items: center;
    gap: 12px;
    font-size: 20px;
    font-weight: 600;
    margin-bottom: 16px;
}

#logo_icon {
    background: #3B82F6;
    width: 38px;
    height: 38px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 10px;
    font-size: 18px;
}

#new_project_btn {
    width: 100%;
    padding: 10px 12px;
    background: #1E293B;
    border-radius: 8px;
    border: 1px solid #475569;
    text-align: center;
    font-size: 14px;
    font-weight: 500;
    cursor: pointer;
    margin-bottom: 10px;
}
#new_project_btn:hover {
    background: #334155;
}

/* ---------- RECENT PROJECTS (SCROLLABLE BLOCK) ---------- */
#projects_section {
    flex: 1 1 auto;            /* take all remaining vertical space */
    min-height: 0;             /* allows this area to shrink & scroll */
    display: flex;
    flex-direction: column;
    overflow-y: auto;          /* ONLY this block scrolls */
    padding-right: 6px;
    margin-top: 4px;
}

#projects_label {
    font-size: 13px;
    font-weight: 600;
    color: #A5B4FC !important;
    margin-bottom: 10px;
}

/* Inner list flows inside the scrollable section */
#project_list {}

/* Each project item */
.project_item {
    padding: 10px 12px;
    border-radius: 8px;
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.1);
    font-size: 14px;
    margin-bottom: 10px;
    cursor: pointer;
}
.project_item:last-child {
    margin-bottom: 0;
}
.project_item:hover {
    background: rgba(255,255,255,0.15);
}

/* ---------- FOOTER USER INFO (PINNED AT BOTTOM) ---------- */
#sidebar_footer {
    flex-shrink: 0;  /* footer never shrinks or moves */
    border-top: 1px solid rgba(255,255,255,0.15);
    padding-top: 12px;
    margin-top: 12px;
    display: flex;
    align-items: center;
    gap: 10px;
}

#user_avatar {
    width: 32px;
    height: 32px;
    background: #3B82F6;
    border-radius: 999px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 15px;
}

#user_name {
    font-size: 14px;
    font-weight: 500;
    color: white;
}
"""


def build_sidebar(
    recent_projects,
    user_name: str = "Shrimayee",
    user_initial: str | None = None,
    app_name: str = "AgileAI",
):
    """
    Render the sidebar HTML.

    Usage in landing_page.py:

        from agileai_side import SIDEBAR_CSS, build_sidebar

        with gr.Column(elem_id="sidebar", scale=1, min_width=260):
            build_sidebar(recent_projects)
    """
    if user_initial is None:
        user_initial = user_name[0].upper() if user_name else "U"

    project_html = "".join(
        f"<div class='project_item'>{p}</div>" for p in recent_projects
    )

    sidebar_html = f"""
    <div id="sidebar_inner">

      <!-- HEADER -->
      <div id="sidebar_header">
        <div id="logo_row">
          <div id="logo_icon">AI</div>
          <div>{app_name}</div>
        </div>
        <div id="new_project_btn">+ New Chat</div>
      </div>

      <!-- SCROLLABLE RECENT PROJECTS -->
      <div id="projects_section">
        <div id="projects_label">Recent Projects</div>
        <div id="project_list">
          {project_html}
        </div>
      </div>

      <!-- FOOTER (USER DETAILS) -->
      <div id="sidebar_footer">
        <div id="user_avatar">{user_initial}</div>
        <div id="user_name">{user_name}</div>
      </div>

    </div>
    """

    return gr.HTML(sidebar_html)
