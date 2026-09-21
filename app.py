import html
import streamlit as st

from src.parser import load_all_transcripts, load_interview_guide
from src.analysis import CaseStudyAnalyzer


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Hasamex Research AI",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# CASE DATA
# ============================================================

@st.cache_data
def load_case():
    return load_all_transcripts(), load_interview_guide()


transcripts, interview_questions = load_case()


@st.cache_resource(show_spinner=False)
def get_analyzer():
    return CaseStudyAnalyzer()


# ============================================================
# SESSION STATE
# ============================================================

defaults = {
    "theme": "Light",
    "question_input": "",
    "qa_result": None,
    "last_question": "",
    "theme_result": None,
    "difference_result": None,
    "guide_results": {},
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


# ============================================================
# SIDEBAR THEME CONTROL
# ============================================================

with st.sidebar:

    st.markdown(
        """
        <div style="
            font-size:23px;
            font-weight:800;
            letter-spacing:-0.7px;
            margin-top:5px;
        ">
            ◈ Hasamex
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.caption("Expert Call Intelligence")

    st.markdown("")

    selected_theme = st.segmented_control(
        "Appearance",
        ["Light", "Dark"],
        default=st.session_state.theme,
        key="appearance_control",
        label_visibility="collapsed",
    )

    if selected_theme:
        st.session_state.theme = selected_theme


dark_mode = st.session_state.theme == "Dark"


# ============================================================
# THEME VARIABLES
# ============================================================

if dark_mode:

    colors = {
        "bg": "#111311",
        "surface": "#181b19",
        "surface2": "#202421",
        "sidebar": "#151815",
        "border": "#303531",
        "text": "#f2f4f1",
        "muted": "#a7ada8",
        "muted2": "#828a84",
        "accent": "#55c7b7",
        "accent_hover": "#69d4c4",
        "accent_soft": "#18332f",
        "input_bg": "#1d211e",
        "input_text": "#f5f7f5",
        "button_text": "#071c19",
        "quote": "#c4cac5",
        "shadow": "rgba(0,0,0,.30)",
    }

else:

    colors = {
        "bg": "#fbfbfa",
        "surface": "#ffffff",
        "surface2": "#f4f5f2",
        "sidebar": "#f5f5f2",
        "border": "#e2e3de",
        "text": "#181918",
        "muted": "#656a66",
        "muted2": "#858a85",
        "accent": "#168c80",
        "accent_hover": "#11786e",
        "accent_soft": "#e8f4f1",
        "input_bg": "#ffffff",
        "input_text": "#171817",
        "button_text": "#ffffff",
        "quote": "#505550",
        "shadow": "rgba(0,0,0,.07)",
    }


# ============================================================
# CSS
# ============================================================

st.markdown(
    f"""
<style>

/* =========================================================
   GLOBAL
========================================================= */

:root {{
    --bg: {colors["bg"]};
    --surface: {colors["surface"]};
    --surface2: {colors["surface2"]};
    --sidebar: {colors["sidebar"]};
    --border: {colors["border"]};
    --text: {colors["text"]};
    --muted: {colors["muted"]};
    --muted2: {colors["muted2"]};
    --accent: {colors["accent"]};
    --accent-hover: {colors["accent_hover"]};
    --accent-soft: {colors["accent_soft"]};
    --input-bg: {colors["input_bg"]};
    --input-text: {colors["input_text"]};
    --button-text: {colors["button_text"]};
    --quote: {colors["quote"]};
}}

html,
body,
.stApp {{
    background: var(--bg) !important;
    color: var(--text) !important;
}}

.stApp {{
    min-height: 100vh;
}}

html,
body,
[class*="css"] {{
    font-family:
        Inter,
        -apple-system,
        BlinkMacSystemFont,
        "Segoe UI",
        sans-serif;
}}

.block-container {{
    max-width: 1120px;
    padding-top: 2.2rem;
    padding-bottom: 4rem;
}}


/* =========================================================
   FORCE READABLE TEXT
========================================================= */

.stApp p,
.stApp span,
.stApp label {{
    color: var(--text);
}}

.stMarkdown,
.stMarkdown p {{
    color: var(--text);
}}

h1, h2, h3, h4, h5, h6 {{
    color: var(--text) !important;
}}


/* =========================================================
   SIDEBAR
========================================================= */

section[data-testid="stSidebar"] {{
    background: var(--sidebar) !important;
    border-right: 1px solid var(--border);
}}

section[data-testid="stSidebar"] > div {{
    background: var(--sidebar) !important;
}}

section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] span,
section[data-testid="stSidebar"] label {{
    color: var(--text) !important;
}}

.sidebar-brand {{
    color: var(--text);
    font-size: 23px;
    font-weight: 800;
    letter-spacing: -0.7px;
}}

.sidebar-subtitle {{
    color: var(--muted);
    font-size: 12px;
    margin-top: 3px;
    margin-bottom: 20px;
}}

.sidebar-heading {{
    color: var(--muted2);
    font-size: 10px;
    font-weight: 750;
    letter-spacing: 1.25px;
    text-transform: uppercase;
    margin-top: 22px;
    margin-bottom: 10px;
}}

.market-row {{
    color: var(--muted);
    font-size: 13px;
    margin-bottom: 10px;
}}

.grounding-pill {{
    display: inline-block;
    padding: 7px 10px;
    background: var(--accent-soft);
    color: var(--accent) !important;
    border: 1px solid var(--border);
    border-radius: 8px;
    font-size: 11px;
    font-weight: 700;
}}


/* =========================================================
   SIDEBAR RADIO
========================================================= */

section[data-testid="stSidebar"]
div[role="radiogroup"] label {{
    border-radius: 8px;
    padding: 7px 8px;
}}

section[data-testid="stSidebar"]
div[role="radiogroup"] label:hover {{
    background: var(--surface2);
}}

section[data-testid="stSidebar"]
div[role="radiogroup"] p {{
    color: var(--text) !important;
    font-size: 14px;
}}


/* =========================================================
   SEGMENTED THEME CONTROL
========================================================= */

div[data-testid="stSegmentedControl"] {{
    margin-bottom: 15px;
}}

div[data-testid="stSegmentedControl"] button {{
    color: var(--text) !important;
}}


/* =========================================================
   HERO
========================================================= */

.hero {{
    max-width: 800px;
    margin: 3.2rem auto 2rem auto;
    text-align: center;
}}

.hero-badge {{
    display: inline-block;
    padding: 7px 13px;
    border: 1px solid var(--border);
    background: var(--surface);
    border-radius: 999px;
    color: var(--muted);
    font-size: 12px;
    margin-bottom: 20px;
}}

.hero-title {{
    color: var(--text);
    font-size: 52px;
    line-height: 1.04;
    font-weight: 770;
    letter-spacing: -2.2px;
    margin-bottom: 16px;
}}

.hero-subtitle {{
    max-width: 720px;
    margin: auto;
    color: var(--muted);
    font-size: 16px;
    line-height: 1.7;
}}


/* =========================================================
   PAGE HEADER
========================================================= */

.eyebrow {{
    color: var(--muted2);
    font-size: 10px;
    font-weight: 760;
    letter-spacing: 1.3px;
    text-transform: uppercase;
    margin-bottom: 8px;
}}

.page-title {{
    color: var(--text);
    font-size: 36px;
    font-weight: 760;
    letter-spacing: -1.2px;
    line-height: 1.15;
    margin-bottom: 8px;
}}

.page-description {{
    color: var(--muted);
    font-size: 14px;
    line-height: 1.65;
    max-width: 800px;
    margin-bottom: 27px;
}}


/* =========================================================
   SEARCH AREA
========================================================= */

.search-wrapper {{
    max-width: 760px;
    margin: 0 auto;
}}


/* =========================================================
   TEXT INPUT
========================================================= */

/*
Important fix:
force both input background AND typed text color.
*/

div[data-testid="stTextInput"] {{
    margin-bottom: 8px;
}}

div[data-testid="stTextInput"] > div {{
    background: transparent !important;
}}

div[data-testid="stTextInput"] div[data-baseweb="input"] {{
    background: var(--input-bg) !important;
    border: 1px solid var(--border) !important;
    border-radius: 14px !important;
    min-height: 58px;
    box-shadow:
        0 8px 25px {colors["shadow"]};
}}

div[data-testid="stTextInput"] div[data-baseweb="input"]:focus-within {{
    border: 1px solid var(--accent) !important;
    box-shadow:
        0 0 0 2px var(--accent-soft),
        0 8px 25px {colors["shadow"]};
}}

div[data-testid="stTextInput"] input {{
    background: var(--input-bg) !important;
    color: var(--input-text) !important;
    -webkit-text-fill-color: var(--input-text) !important;
    caret-color: var(--accent) !important;
    font-size: 16px !important;
    min-height: 56px;
    padding-left: 16px !important;
}}

div[data-testid="stTextInput"] input::placeholder {{
    color: var(--muted2) !important;
    -webkit-text-fill-color: var(--muted2) !important;
    opacity: 1 !important;
}}


/* =========================================================
   BUTTON
========================================================= */

.stButton > button {{
    width: 100%;
    min-height: 50px;
    border: none !important;
    border-radius: 12px !important;
    background: var(--accent) !important;
    color: var(--button-text) !important;
    font-weight: 700 !important;
    box-shadow: none !important;
}}

.stButton > button:hover {{
    background: var(--accent-hover) !important;
    color: var(--button-text) !important;
    border: none !important;
}}

.stButton > button p {{
    color: var(--button-text) !important;
}}


/* =========================================================
   METRICS
========================================================= */

.metric-card {{
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 18px 19px;
    min-height: 105px;
}}

.metric-number {{
    color: var(--text);
    font-size: 27px;
    font-weight: 750;
}}

.metric-label {{
    color: var(--muted);
    font-size: 11px;
    margin-top: 5px;
}}


/* =========================================================
   SUGGESTIONS
========================================================= */

.suggestion {{
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 13px;
    padding: 16px 17px;
    min-height: 68px;
    color: var(--text);
    font-size: 13px;
    font-weight: 620;
    line-height: 1.45;
    margin-bottom: 9px;
}}


/* =========================================================
   QUESTION CARD
========================================================= */

.question-card {{
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 18px 20px;
    margin-top: 12px;
    margin-bottom: 10px;
}}

.question-number {{
    color: var(--accent);
    font-size: 10px;
    font-weight: 760;
    letter-spacing: 1px;
    margin-bottom: 6px;
}}

.question-text {{
    color: var(--text);
    font-size: 15px;
    font-weight: 650;
    line-height: 1.5;
}}


/* =========================================================
   SOURCES
========================================================= */

.source-card {{
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 13px;
    padding: 16px 17px;
    margin-bottom: 10px;
}}

.source-badge {{
    display: inline-block;
    background: var(--surface2);
    color: var(--muted);
    border-radius: 999px;
    padding: 4px 8px;
    font-size: 10px;
    font-weight: 700;
    margin-right: 5px;
}}

.source-time {{
    display: inline-block;
    border: 1px solid var(--border);
    color: var(--muted);
    border-radius: 999px;
    padding: 4px 8px;
    font-size: 10px;
}}

.source-person {{
    color: var(--text);
    font-size: 13px;
    font-weight: 700;
    margin-top: 10px;
}}

.source-quote {{
    color: var(--quote);
    font-size: 13px;
    line-height: 1.62;
    margin-top: 7px;
}}


/* =========================================================
   EXPERT CARD
========================================================= */

.expert-card {{
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 15px;
    padding: 20px;
    margin-bottom: 18px;
}}

.expert-market {{
    color: var(--muted2);
    font-size: 10px;
    font-weight: 750;
    letter-spacing: 1.2px;
    text-transform: uppercase;
}}

.expert-name {{
    color: var(--text);
    font-size: 20px;
    font-weight: 730;
    margin-top: 6px;
}}

.expert-role {{
    color: var(--muted);
    font-size: 13px;
    margin-top: 3px;
}}


/* =========================================================
   TRANSCRIPT
========================================================= */

.transcript-item {{
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 14px 16px;
    margin-bottom: 9px;
}}

.transcript-meta {{
    color: var(--muted2);
    font-size: 10px;
    font-weight: 700;
    margin-bottom: 7px;
}}

.transcript-speaker {{
    color: var(--accent);
}}

.transcript-text {{
    color: var(--text);
    font-size: 13px;
    line-height: 1.62;
}}


/* =========================================================
   ARCHITECTURE
========================================================= */

.pipeline-card {{
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 19px;
    min-height: 120px;
}}

.pipeline-step {{
    color: var(--accent);
    font-size: 10px;
    font-weight: 760;
}}

.pipeline-title {{
    color: var(--text);
    font-size: 14px;
    font-weight: 680;
    line-height: 1.45;
    margin-top: 10px;
}}


/* =========================================================
   TABS
========================================================= */

button[data-baseweb="tab"] {{
    color: var(--muted) !important;
}}

button[data-baseweb="tab"][aria-selected="true"] {{
    color: var(--accent) !important;
}}

div[data-baseweb="tab-highlight"] {{
    background: var(--accent) !important;
}}


/* =========================================================
   EXPANDERS / SELECTBOX / TOGGLE
========================================================= */

div[data-testid="stExpander"] {{
    background: var(--surface);
    border-color: var(--border);
}}

div[data-baseweb="select"] > div {{
    background: var(--surface) !important;
    color: var(--text) !important;
    border-color: var(--border) !important;
}}

div[data-baseweb="select"] span {{
    color: var(--text) !important;
}}


/* =========================================================
   CODE
========================================================= */

.stCodeBlock {{
    border: 1px solid var(--border);
    border-radius: 12px;
}}


/* =========================================================
   DIVIDER
========================================================= */

.divider {{
    height: 1px;
    background: var(--border);
    margin: 29px 0;
}}


/* =========================================================
   STREAMLIT UI
========================================================= */

#MainMenu {{
    visibility: hidden;
}}

footer {{
    visibility: hidden;
}}

header[data-testid="stHeader"] {{
    background: transparent;
}}

</style>
""",
    unsafe_allow_html=True,
)


# ============================================================
# HELPERS
# ============================================================

def clean(value):
    return html.escape(str(value or ""))


def divider():
    st.markdown(
        '<div class="divider"></div>',
        unsafe_allow_html=True,
    )


def page_header(label, title, description):

    st.markdown(
        f'<div class="eyebrow">{clean(label)}</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        f'<div class="page-title">{clean(title)}</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        f'<div class="page-description">{clean(description)}</div>',
        unsafe_allow_html=True,
    )


def render_sources(sources, maximum=None):

    if not sources:
        st.info("No supporting transcript evidence was retrieved.")
        return

    if maximum:
        sources = sources[:maximum]

    st.markdown(
        '<div class="eyebrow">Verified transcript evidence</div>',
        unsafe_allow_html=True,
    )

    for number, source in enumerate(sources, start=1):

        market = clean(source.get("market"))
        timestamp = clean(source.get("timestamp"))
        expert = clean(source.get("expert"))
        role = clean(source.get("role"))
        quote = clean(source.get("quote"))

        card = (
            '<div class="source-card">'
            '<div>'
            f'<span class="source-badge">{number} · {market}</span>'
            f'<span class="source-time">{timestamp}</span>'
            '</div>'
            f'<div class="source-person">{expert} · {role}</div>'
            f'<div class="source-quote">“{quote}”</div>'
            '</div>'
        )

        st.markdown(
            card,
            unsafe_allow_html=True,
        )


def render_result(result):

    if not result:
        return

    st.markdown(
        '<div class="eyebrow">AI synthesis</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        result.get("answer", "")
    )

    divider()

    render_sources(
        result.get("sources", [])
    )


def get_transcript(market):

    for transcript in transcripts:
        if transcript["market"] == market:
            return transcript

    return None


# ============================================================
# SIDEBAR NAVIGATION
# ============================================================

with st.sidebar:

    st.markdown(
        '<div class="sidebar-heading">Workspace</div>',
        unsafe_allow_html=True,
    )

    page = st.radio(
        "Workspace",
        [
            "Ask",
            "Interview Guide",
            "Cross-Call Insights",
            "Transcripts",
            "Architecture",
        ],
        label_visibility="collapsed",
    )

    st.markdown(
        '<div class="sidebar-heading">Case pack</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="market-row">FR &nbsp; France</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="market-row">DE &nbsp; Germany</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="market-row">GB &nbsp; United Kingdom</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="sidebar-heading">Grounding</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="grounding-pill">'
        '✓ Transcript-only evidence'
        '</div>',
        unsafe_allow_html=True,
    )

    st.caption(
        "Answers use retrieved transcript evidence. "
        "Quotes and timestamps come directly from source metadata."
    )


# ============================================================
# ASK
# ============================================================

if page == "Ask":

    st.markdown(
        '<div class="hero">'
        '<div class="hero-badge">'
        '3 expert calls · France · Germany · United Kingdom'
        '</div>'
        '<div class="hero-title">Ask the expert calls</div>'
        '<div class="hero-subtitle">'
        'Turn expert interviews into evidence-backed market intelligence. '
        'Ask across all calls and trace every answer back to exact quotes '
        'and timestamps.'
        '</div>'
        '</div>',
        unsafe_allow_html=True,
    )

    left, center, right = st.columns(
        [1.1, 5.5, 1.1]
    )

    with center:

        question = st.text_input(
            "Research question",
            key="question_input",
            placeholder=(
                "Ask about adoption, ROI, training, "
                "growth or purchasing decisions..."
            ),
            label_visibility="collapsed",
        )

        search_clicked = st.button(
            "Search expert calls",
            type="primary",
            use_container_width=True,
            key="search_button",
        )

        if search_clicked:

            cleaned_question = question.strip()

            if not cleaned_question:

                st.warning(
                    "Enter a research question first."
                )

            else:

                with st.spinner(
                    "Retrieving evidence across France, Germany and the UK..."
                ):

                    analyzer = get_analyzer()

                    result = analyzer.ask_transcripts(
                        cleaned_question
                    )

                    st.session_state.qa_result = result
                    st.session_state.last_question = (
                        cleaned_question
                    )

    if st.session_state.qa_result:

        divider()

        st.markdown(
            '<div class="eyebrow">Research question</div>',
            unsafe_allow_html=True,
        )

        st.markdown(
            f"## {st.session_state.last_question}"
        )

        render_result(
            st.session_state.qa_result
        )

    else:

        divider()

        m1, m2, m3 = st.columns(3)

        with m1:
            st.markdown(
                '<div class="metric-card">'
                '<div class="metric-number">3</div>'
                '<div class="metric-label">Expert calls</div>'
                '</div>',
                unsafe_allow_html=True,
            )

        with m2:
            st.markdown(
                '<div class="metric-card">'
                '<div class="metric-number">3</div>'
                '<div class="metric-label">European markets</div>'
                '</div>',
                unsafe_allow_html=True,
            )

        with m3:
            st.markdown(
                '<div class="metric-card">'
                '<div class="metric-number">21</div>'
                '<div class="metric-label">Expert statements</div>'
                '</div>',
                unsafe_allow_html=True,
            )

        st.markdown("")

        st.markdown(
            '<div class="eyebrow">Suggested research</div>',
            unsafe_allow_html=True,
        )

        suggestions = [
            "What are the main barriers to robotic surgery adoption?",
            "How important are hospital budgets and ROI?",
            "How do growth expectations differ across markets?",
            "How important are surgeon training and clinical outcomes?",
        ]

        s1, s2 = st.columns(2)

        for index, suggestion in enumerate(suggestions):

            column = s1 if index % 2 == 0 else s2

            with column:

                st.markdown(
                    f'<div class="suggestion">'
                    f'{clean(suggestion)}'
                    f'</div>',
                    unsafe_allow_html=True,
                )


# ============================================================
# INTERVIEW GUIDE
# ============================================================

elif page == "Interview Guide":

    page_header(
        "Case study",
        "Interview Guide",
        "Answer the six supplied research questions across France, "
        "Germany and the United Kingdom with traceable evidence.",
    )

    if not interview_questions:

        st.error(
            "No interview-guide questions were loaded."
        )

    for number, guide_question in enumerate(
        interview_questions,
        start=1,
    ):

        st.markdown(
            '<div class="question-card">'
            f'<div class="question-number">'
            f'QUESTION {number:02}'
            f'</div>'
            f'<div class="question-text">'
            f'{clean(guide_question)}'
            f'</div>'
            '</div>',
            unsafe_allow_html=True,
        )

        if number not in st.session_state.guide_results:

            if st.button(
                "Generate evidence-backed answer",
                key=f"guide_button_{number}",
            ):

                analyzer = get_analyzer()

                prompt = f"""
INTERVIEW GUIDE QUESTION

{guide_question}

Answer this exact question using evidence from:
France, Germany and the United Kingdom.

Compare the markets directly.

Preserve all numerical qualifications and scope.

Do not transform forecasts about selected centres or areas
into national market forecasts.

Do not infer that information was never discussed merely
because one retrieved passage does not contain it.

Do not invent facts.

Do not reproduce exact quotations or timestamps in the
narrative because verified evidence is displayed separately.
"""

                with st.spinner(
                    f"Analysing question {number}..."
                ):

                    result = analyzer.engine.ask(
                        prompt,
                        top_k=18,
                        balanced=True,
                    )

                st.session_state.guide_results[number] = (
                    result
                )

                st.rerun()

        else:

            st.markdown(
                st.session_state.guide_results[
                    number
                ]["answer"]
            )

            with st.expander(
                "View verified evidence"
            ):

                render_sources(
                    st.session_state.guide_results[
                        number
                    ]["sources"]
                )

        st.markdown("")


# ============================================================
# CROSS-CALL INSIGHTS
# ============================================================

elif page == "Cross-Call Insights":

    page_header(
        "Synthesis",
        "Cross-Call Insights",
        "Surface recurring themes, market-specific differences "
        "and genuine disagreements across the three expert calls.",
    )

    themes_tab, differences_tab = st.tabs(
        [
            "Common Themes",
            "Differences & Disagreements",
        ]
    )

    with themes_tab:

        st.markdown(
            "### What is consistent across the calls?"
        )

        st.caption(
            "Synthesise adoption, economics, utilisation, "
            "training, clinical outcomes and growth."
        )

        if st.session_state.theme_result is None:

            if st.button(
                "Generate common themes",
                type="primary",
                key="theme_button",
            ):

                with st.spinner(
                    "Synthesising the three expert calls..."
                ):

                    analyzer = get_analyzer()

                    st.session_state.theme_result = (
                        analyzer.analyze_themes()
                    )

                st.rerun()

        else:

            render_result(
                st.session_state.theme_result
            )

    with differences_tab:

        st.markdown(
            "### Where do perspectives differ?"
        )

        st.caption(
            "Separate genuine contradiction from differences "
            "in emphasis and market-specific context."
        )

        if st.session_state.difference_result is None:

            if st.button(
                "Compare expert perspectives",
                type="primary",
                key="difference_button",
            ):

                with st.spinner(
                    "Comparing expert perspectives..."
                ):

                    analyzer = get_analyzer()

                    st.session_state.difference_result = (
                        analyzer.analyze_disagreements()
                    )

                st.rerun()

        else:

            render_result(
                st.session_state.difference_result
            )


# ============================================================
# TRANSCRIPTS
# ============================================================

elif page == "Transcripts":

    page_header(
        "Evidence library",
        "Expert Transcripts",
        "Inspect the original timestamped source material behind "
        "the retrieval and analysis pipeline.",
    )

    markets = [
        transcript["market"]
        for transcript in transcripts
    ]

    selected_market = st.selectbox(
        "Market",
        markets,
        label_visibility="collapsed",
    )

    transcript = get_transcript(
        selected_market
    )

    if transcript:

        expert_html = (
            '<div class="expert-card">'
            f'<div class="expert-market">'
            f'{clean(transcript["market"])}'
            f'</div>'
            f'<div class="expert-name">'
            f'{clean(transcript["expert"])}'
            f'</div>'
            f'<div class="expert-role">'
            f'{clean(transcript["role"])}'
            f'</div>'
            '</div>'
        )

        st.markdown(
            expert_html,
            unsafe_allow_html=True,
        )

        c1, c2 = st.columns(
            [2, 5]
        )

        with c1:

            show_interviewer = st.toggle(
                "Show interviewer",
                value=True,
            )

        with c2:

            expert_count = sum(
                1
                for segment in transcript["segments"]
                if segment["speaker"].strip().lower()
                != "interviewer"
            )

            st.caption(
                f"{expert_count} expert statements · "
                f"{len(transcript['segments'])} timestamped segments"
            )

        for segment in transcript["segments"]:

            speaker = segment["speaker"].strip()

            if (
                not show_interviewer
                and speaker.lower() == "interviewer"
            ):
                continue

            transcript_html = (
                '<div class="transcript-item">'
                '<div class="transcript-meta">'
                f'{clean(segment["timestamp"])}'
                ' &nbsp; · &nbsp; '
                f'<span class="transcript-speaker">'
                f'{clean(speaker)}'
                '</span>'
                '</div>'
                '<div class="transcript-text">'
                f'{clean(segment["text"])}'
                '</div>'
                '</div>'
            )

            st.markdown(
                transcript_html,
                unsafe_allow_html=True,
            )


# ============================================================
# ARCHITECTURE
# ============================================================

elif page == "Architecture":

    page_header(
        "Technical design",
        "Grounded RAG Architecture",
        "A transparent retrieval-augmented generation pipeline "
        "for evidence-backed expert-call research.",
    )

    columns = st.columns(4)

    steps = [
        ("01", "Parse timestamped transcripts"),
        ("02", "Generate semantic embeddings"),
        ("03", "Retrieve balanced evidence"),
        ("04", "Generate grounded synthesis"),
    ]

    for column, (step, title) in zip(
        columns,
        steps,
    ):

        with column:

            st.markdown(
                '<div class="pipeline-card">'
                f'<div class="pipeline-step">'
                f'STEP {step}'
                f'</div>'
                f'<div class="pipeline-title">'
                f'{clean(title)}'
                f'</div>'
                '</div>',
                unsafe_allow_html=True,
            )

    divider()

    st.markdown(
        "### Retrieval pipeline"
    )

    st.code(
        """Expert Call Transcripts
        │
        ▼
Timestamp-aware Parser
        │
        ▼
Structured Segments + Metadata
        │
        ▼
SentenceTransformer Embeddings
        │
        ▼
FAISS Semantic Index
        │
        ▼
Market-Balanced Retrieval
     ┌──┼──┐
     │  │  │
    FR  DE  UK
     │  │  │
     └──┼──┘
        │
        ▼
Grounded LLM Synthesis
        │
        ├── Research Answer
        │
        └── Verified Evidence
            • Expert
            • Market
            • Timestamp
            • Exact Quote""",
        language="text",
    )

    st.markdown(
        "### Evidence integrity"
    )

    st.write(
        """
The LLM generates the analytical synthesis but does not generate
the displayed source quotations or timestamps. Expert name, role,
market, timestamp and exact transcript text are attached as
metadata during parsing and preserved through retrieval.
"""
    )

    st.markdown(
        "### Market-balanced retrieval"
    )

    st.write(
        """
For comparative questions, evidence is retrieved independently
from France, Germany and the United Kingdom before synthesis.
This reduces the chance that one transcript dominates the
retrieved context.
"""
    )

    st.markdown(
        "### Production scaling"
    )

    st.write(
        """
For a larger expert-call library, the same architecture could use
a persistent vector database with metadata filters for market,
expert, date, project and research topic. Only relevant passages
would be supplied to the language model.
"""
    )


# ============================================================
# FOOTER
# ============================================================

divider()

st.caption(
    "Hasamex Research AI · "
    "Grounded exclusively in the supplied expert-call transcripts"
)