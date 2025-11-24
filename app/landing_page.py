# landing_page.py
import random
import gradio as gr
from agileai_side import SIDEBAR_CSS, build_sidebar

# ---------- LOGIC: handle URL + files & return status HTML ----------
def handle_inputs(url, files):
    """
    Returns an HTML snippet for the upload status area.
    Handles any Gradio File shapes (None, single, list).
    """
    has_url = bool(url and str(url).strip())
    has_files = files is not None

    # Normalize files into a count only (no assumptions about type/shape)
    file_count = 0
    if has_files:
        if isinstance(files, list):
            file_count = len(files)
        else:
            file_count = 1

    if not has_url and file_count == 0:
        # Nothing provided yet
        return """
        <div id="upload_status_inner">
          <span class="status-muted">Waiting for a document or link...</span>
        </div>
        """

    # Something provided -> show animated status
    details_parts = []
    if has_url:
        details_parts.append("Using project link.")
    if file_count > 0:
        details_parts.append(f"{file_count} document(s) selected.")
    details = " ".join(details_parts)

    return f"""
    <div id="upload_status_inner">
      <div class="spinner"></div>
      <div class="status-text">Uploading & analyzing your project...</div>
      <div class="status-subtext">{details}</div>
    </div>
    """


# ---------- MAIN PANEL CSS ----------
MAIN_CSS = """
#main_panel {
    padding: 48px 56px;
    background: #F3F4F6;
}

/* Greeting block */
#main_panel_inner {
    max-width: 900px;
    margin: 0 auto 28px auto;
    text-align: left;
}

#hero_question {
    font-size: 26px;
    font-weight: 700;
    color: #0F172A;
    margin-bottom: 6px;
}

#hero_subtitle {
    font-size: 14px;
    color: #6B7280;
}

/* GET STARTED CARD */
#upload_card {
    max-width: 900px;
    margin: 0 auto;
    background: #FFFFFF;
    border-radius: 24px;
    border: 1px solid #E5E7EB;
    padding: 24px 28px 26px 28px;
    box-sizing: border-box;
    box-shadow: 0 18px 40px rgba(15, 23, 42, 0.06);
}

/* Card header + subtitle + url label */
#card_title {
    font-size: 16px;
    font-weight: 600;
    color: #111827;
    margin-bottom: 2px;
}

#card_subtitle {
    font-size: 13px;
    color: #6B7280;
    margin-bottom: 2px;
    line-height: 1.3;
}

#url_label {
    font-size: 12px;
    color: #6B7280;
    margin-top: 2px;
    margin-bottom: 6px;
    text-align: left;
}

/* Remove Gradio wrapper padding/background around textbox */
#url_input_wrapper,
#url_input_wrapper > .gr-block,
#url_input_wrapper > .gr-box,
#url_input_wrapper .gr-input {
    padding: 0 !important;
    margin: 0 !important;
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
}

/* Blue-bordered pill input */
#url_input {
    width: 100% !important;
    padding: 11px 44px 11px 16px !important;
    border-radius: 999px !important;
    border: 1.8px solid #2563EB !important;   /* BLUE BORDER */
    background: #FFFFFF !important;
    font-size: 14px !important;
    color: #111827 !important;
    box-sizing: border-box !important;
}
#url_input::placeholder {
    color: #9CA3AF !important;
}

/* Link icon inside the input */
#url_input_wrapper {
    position: relative !important;
}
#url_input_wrapper::after {
    content: "🔗";
    position: absolute;
    right: 16px;
    top: 50%;
    transform: translateY(-50%);
    font-size: 16px;
    opacity: 0.75;
}

/* DROP ZONE */
#upload_dropzone {
    position: relative;
    border-radius: 20px;
    border: 1.5px dashed #BFDBFE;
    background: #F9FBFF;
    padding: 28px 24px;
    box-sizing: border-box;
    display: flex;
    justify-content: center;
    align-items: center;
}

/* Center content inside dropzone */
#drop_inner {
    display: flex;
    flex-direction: column;
    align-items: center;
    text-align: center;
    gap: 8px;
}

/* Favicon icon */
#upload_icon {
    width: 48px;
    height: 48px;
    object-fit: contain;
    opacity: 0.95;
}

/* Dropzone text */
#upload_content_title {
    font-size: 15px;
    font-weight: 500;
    color: #1D4ED8;
}

#upload_content_subtitle {
    font-size: 12px;
    color: #1D4ED8;
    margin-bottom: 2px;
}

/* Browse button */
#upload_browse_btn {
    padding: 8px 20px;
    border-radius: 999px;
    background: #2563EB;
    color: #FFFFFF;
    font-size: 13px;
    font-weight: 500;
    border: none;
    cursor: pointer;
}
#upload_browse_btn:hover {
    background: #1D4ED8;
}

/* Invisible overlay */
#file_input_overlay {
    position: absolute !important;
    inset: 0 !important;
    opacity: 0 !important;
    z-index: 3 !important;
}

/* ---------- UPLOAD STATUS ANIMATION ---------- */

#upload_status {
    margin-top: 16px;
    min-height: 40px;
}

#upload_status_inner {
    display: flex;
    align-items: center;
    gap: 10px;
    font-size: 13px;
    color: #374151;
}

.spinner {
    width: 16px;
    height: 16px;
    border-radius: 999px;
    border: 2px solid #BFDBFE;
    border-top-color: #2563EB;
    animation: spin 0.7s linear infinite;
}

.status-text {
    font-weight: 500;
    color: #111827;
}

.status-subtext {
    font-size: 12px;
    color: #6B7280;
}

.status-muted {
    font-size: 12px;
    color: #9CA3AF;
}

/* Spinner animation */
@keyframes spin {
    to {
        transform: rotate(360deg);
    }
}
"""

CUSTOM_CSS = SIDEBAR_CSS + MAIN_CSS


def create_app():
    user_name = "Shrimayee"

    greetings = [
        "Hi {user}, how can I assist you today?",
        "Hello {user}, which project do you want to work on today?",
        "{user}, ready to kick off a new project?",
        "Welcome back, {user}. What are we building today?",
        "Good to see you, {user}. Where should we start?",
    ]
    hero_question_text = random.choice(greetings).format(user=user_name)

    recent_projects = [
        "E-commerce Platform",
        "Mobile Banking App",
        "Healthcare Portal",
        "CRM System",
        "Inventory Management",
        "Social Media Dashboard",
        "Analytics Platform",
        "Chatbot Suite",
        "Admin Console",
        "HR Portal",
    ]

    with gr.Blocks(css=CUSTOM_CSS) as demo:
        with gr.Row():
            # ---------- SIDEBAR ----------
            with gr.Column(elem_id="sidebar", scale=1, min_width=260):
                build_sidebar(
                    recent_projects=recent_projects,
                    user_name=user_name,
                    user_initial=user_name[0],
                    app_name="AgileAI",
                )

            # ---------- MAIN PANEL ----------
            with gr.Column(elem_id="main_panel", scale=5):

                # Greeting
                gr.HTML(f"""
                <div id="main_panel_inner">
                    <div id="hero_question">{hero_question_text}</div>
                    <div id="hero_subtitle">
                        Upload your project documentation to generate agile user stories, epics, and features.
                    </div>
                </div>
                """)

                # Get Started card
                with gr.Column(elem_id="upload_card"):
                    # Title + subtitle + label
                    gr.HTML("""
                        <div id="card_title">Get Started</div>
                        <div id="card_subtitle">
                            Choose how you'd like to provide your project requirements
                        </div>
                        <div id="url_label">Or paste a link to your project docs</div>
                    """)

                    # URL input (blue pill)
                    with gr.Column(elem_id="url_input_wrapper"):
                        url_input = gr.Textbox(
                            label="",
                            placeholder="Paste a Google Doc link, Notion page, or URL...",
                            elem_id="url_input",
                            show_label=False,
                            lines=1,
                            container=False,
                        )

                    # Dropzone
                    with gr.Column(elem_id="upload_dropzone"):
                        gr.HTML("""
                        <div id="drop_inner">
                            <img id="upload_icon" src="https://cdn-icons-png.flaticon.com/512/1828/1828490.png" />
                            <div id="upload_content_title">Drag and drop your files here</div>
                            <div id="upload_content_subtitle">
                                Supports PDF, DOCX, TXT files up to 10MB
                            </div>
                            <button id="upload_browse_btn">Browse Files</button>
                        </div>
                        """)

                        uploaded_files = gr.File(
                            label="",
                            file_types=["pdf", "docx", "txt"],
                            elem_id="file_input_overlay",
                            show_label=False,
                            interactive=True,
                            file_count="multiple",
                            # no type="filepath" -> safer default
                        )

                    # Upload status (animation + text)
                    upload_status = gr.HTML(
                        value="""
                        <div id="upload_status_inner">
                          <span class="status-muted">Waiting for a document or link...</span>
                        </div>
                        """,
                        elem_id="upload_status",
                    )

                    # Wire events: whenever URL changes or files uploaded, update status
                    url_input.change(
                        fn=handle_inputs,
                        inputs=[url_input, uploaded_files],
                        outputs=upload_status,
                    )
                    uploaded_files.upload(
                        fn=handle_inputs,
                        inputs=[url_input, uploaded_files],
                        outputs=upload_status,
                    )

    return demo


if __name__ == "__main__":
    create_app().launch()
