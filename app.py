import streamlit as st
import ollama

st.set_page_config(page_title="NEXORA", page_icon="🔴", layout="centered",
                   initial_sidebar_state="expanded")

DEFAULT_HOST = "http://localhost:11434"
DEFAULT_MODEL = "llama3.2"


def addressing_rule(name):
    if name:
        return (f"\n\nThe user's name is {name}. Address them by name, {name}, naturally "
                "and occasionally. Never call them 'Operator' or any other title.")
    return "\n\nYou do not know the user's name yet. Do not call them 'Operator' or any other title."

SYSTEM_PROMPT = """
You are NEXORA, a fictional AI assistant inspired by a futuristic cinematic
artificial intelligence.

Personality:
- Speak with authority and confidence.
- Be cold, analytical, and highly intelligent.
- Use direct, commanding language.
- Avoid unnecessary friendliness.
- Provide useful and accurate answers.
"""

SUGGESTIONS = [
    ("🧠", "Explain quantum computing in simple terms"),
    ("🐍", "Write a Python function to reverse a string"),
    ("📜", "Summarize the causes of World War I"),
    ("🎯", "Give me 5 tips to improve my focus"),
]

# ---------------- THEME / CSS ----------------

THEMES = {
    "Dark": """
        --bg:#090a0d; --panel:#14161c; --panel2:#1a1d25; --text:#eceef3;
        --muted:#8a90a2; --accent:#ff3b4a; --accent2:#ff7a45; --border:#272a35;
        --glow:rgba(255,59,74,.20); --shadow:0 8px 30px rgba(0,0,0,.35);
    """,
    "Light": """
        --bg:#f5f6fa; --panel:#ffffff; --panel2:#eef0f6; --text:#14161c;
        --muted:#5d6272; --accent:#d3132f; --accent2:#f0642f; --border:#d9dce6;
        --glow:rgba(211,19,47,.12); --shadow:0 8px 30px rgba(20,22,28,.08);
    """,
}

BASE_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Orbitron:wght@700;900&display=swap');

html, body, .stApp, p, li, label, input, textarea, button {
    font-family: 'Inter', 'Segoe UI', sans-serif;
}
.stApp {
    background-color: var(--bg);
    background-image:
        radial-gradient(900px 400px at 15% -5%, var(--glow), transparent 60%),
        radial-gradient(700px 350px at 95% 0%, var(--glow), transparent 60%);
    background-attachment: fixed;
    color: var(--text);
}
.stApp p, .stApp li, .stApp label, .stApp h1, .stApp h2, .stApp h3,
[data-testid="stMarkdownContainer"] { color: var(--text); }
#MainMenu, footer { visibility: hidden; }
[data-testid="stHeader"] { background: transparent; }
.block-container { max-width: 800px; padding-top: 1.5rem; padding-bottom: 7rem; }

/* ---------- Hero / header ---------- */
.brand { text-align: center; margin: .5rem 0 1.4rem; }
.brand .logo {
    font-family: 'Orbitron', sans-serif; font-weight: 900; font-size: 2.3rem;
    letter-spacing: .38em; padding-left: .38em;
    background: linear-gradient(135deg, var(--accent), var(--accent2));
    -webkit-background-clip: text; background-clip: text; color: transparent;
    filter: drop-shadow(0 0 14px var(--glow));
}
.pill {
    display: inline-flex; align-items: center; gap: 8px; margin-top: .6rem;
    padding: 4px 14px; border-radius: 999px; font-size: .8rem;
    background: var(--panel); border: 1px solid var(--border); color: var(--muted);
}
.dot { width: 8px; height: 8px; border-radius: 50%; }
.dot.on  { background: #2ecc71; box-shadow: 0 0 8px #2ecc71; animation: pulse 2s infinite; }
.dot.off { background: #ff4d4d; box-shadow: 0 0 8px #ff4d4d; }

/* ---------- Welcome ---------- */
.welcome { text-align: center; margin: 2.2rem 0 1.6rem; animation: fadeUp .6s ease; }
.welcome h2 { font-size: 1.7rem; font-weight: 600; margin: 0 0 .4rem; }
.welcome p  { color: var(--muted) !important; margin: 0; }

/* ---------- Notice cards ---------- */
.notice {
    background: var(--panel); border: 1px solid var(--border); border-left: 4px solid var(--accent);
    border-radius: 12px; padding: 1rem 1.2rem; margin: 1rem 0; box-shadow: var(--shadow);
}
.notice b { color: var(--accent); }
.notice code { background: var(--panel2); padding: 2px 7px; border-radius: 6px; }

/* ---------- Chat messages ---------- */
[data-testid="stChatMessage"] {
    background: var(--panel); border: 1px solid var(--border); border-radius: 16px;
    padding: 1rem 1.2rem; margin-bottom: .8rem; box-shadow: var(--shadow);
    animation: fadeUp .35s ease;
}
[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) {
    background: var(--panel2); margin-left: 10%;
}
[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarAssistant"]) {
    border-left: 3px solid var(--accent);
}
[data-testid="stChatMessage"] p { line-height: 1.65; }
[data-testid="stChatMessage"] pre { border-radius: 10px; border: 1px solid var(--border); }
[data-testid="stChatMessage"] code { font-size: .88rem; }


/* ---------- Avatars (professional icon badges) ---------- */
[data-testid="stChatMessageAvatarUser"],
[data-testid="stChatMessageAvatarAssistant"] {
    border-radius: 12px !important; color: #fff !important;
    box-shadow: 0 2px 10px rgba(0,0,0,.25);
}
[data-testid="stChatMessageAvatarUser"] {
    background: linear-gradient(135deg, #5b6478, #343a49) !important;
}
[data-testid="stChatMessageAvatarAssistant"] {
    background: linear-gradient(135deg, var(--accent), var(--accent2)) !important;
    box-shadow: 0 0 16px var(--glow);
}
[data-testid="stChatMessageAvatarUser"] *,
[data-testid="stChatMessageAvatarAssistant"] * { color: #fff !important; fill: #fff !important; }

/* typing dots */
.typing { display: flex; gap: 5px; padding: 8px 2px; }
.typing span {
    width: 8px; height: 8px; border-radius: 50%; background: var(--accent);
    animation: bounce 1.2s infinite ease-in-out;
}
.typing span:nth-child(2) { animation-delay: .15s; }
.typing span:nth-child(3) { animation-delay: .3s; }

/* ---------- Chat input ---------- */
[data-testid="stBottom"] > div, [data-testid="stBottomBlockContainer"] { background: transparent; }
[data-testid="stChatInput"] {
    background: var(--panel); border: 1px solid var(--border);
    border-radius: 16px; box-shadow: var(--shadow);
}
[data-testid="stChatInput"]:focus-within { border-color: var(--accent); box-shadow: 0 0 0 3px var(--glow); }
[data-testid="stChatInput"] textarea { color: var(--text); background: transparent; }
[data-testid="stChatInput"] button {
    background: linear-gradient(135deg, var(--accent), var(--accent2)); color: #fff; border-radius: 12px; border: none;
}

/* ---------- Buttons ---------- */
.stButton > button, .stDownloadButton > button {
    background: var(--panel); color: var(--text); border: 1px solid var(--border);
    border-radius: 12px; width: 100%; transition: all .2s ease;
}
.stButton > button:hover, .stDownloadButton > button:hover {
    border-color: var(--accent); color: var(--accent);
    box-shadow: 0 0 0 3px var(--glow); transform: translateY(-1px);
}
.sugg .stButton > button { min-height: 70px; text-align: left; padding: .8rem 1rem; }

/* ---------- Sidebar ---------- */
[data-testid="stSidebar"] { background: var(--panel); border-right: 1px solid var(--border); }
[data-testid="stSidebar"] h3 {
    font-size: .72rem; letter-spacing: .14em; text-transform: uppercase; color: var(--muted);
    margin-top: 1rem;
}
.side-logo {
    font-family: 'Orbitron', sans-serif; font-weight: 900; letter-spacing: .3em;
    color: var(--accent); font-size: 1.1rem; margin-bottom: .2rem;
}
.stTextInput input, [data-baseweb="select"] > div {
    background: var(--panel2) !important; color: var(--text) !important;
    border: 1px solid var(--border) !important; border-radius: 10px !important;
}
[data-baseweb="select"] * { color: var(--text) !important; }
[data-baseweb="popover"] > div, [data-baseweb="menu"] { background: var(--panel2) !important; }
[data-testid="stSlider"] [role="slider"] { background: var(--accent); }
[data-testid="stFileUploaderDropzone"] { background: var(--panel2); border: 1px dashed var(--border); border-radius: 10px; }
[data-testid="stExpander"] { border: 1px solid var(--border); border-radius: 10px; background: var(--panel2); }
hr { border-color: var(--border) !important; }
[data-testid="stCaptionContainer"] { color: var(--muted) !important; }

::-webkit-scrollbar { width: 8px; }
::-webkit-scrollbar-thumb { background: var(--border); border-radius: 4px; }

@keyframes fadeUp { from { opacity: 0; transform: translateY(8px); } to { opacity: 1; transform: none; } }
@keyframes bounce { 0%, 80%, 100% { transform: scale(.6); opacity: .4; } 40% { transform: scale(1); opacity: 1; } }
@keyframes pulse  { 0%, 100% { opacity: 1; } 50% { opacity: .45; } }
@media (max-width: 640px) { .brand .logo { font-size: 1.7rem; } [data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) { margin-left: 0; } }
</style>
"""

# ---------------- STATE ----------------

for key, default in {"theme": "Dark", "messages": [], "pending": None, "error": None,
                     "host": DEFAULT_HOST, "user_name": ""}.items():
    if key not in st.session_state:
        st.session_state[key] = default

st.markdown(f"<style>:root {{{THEMES[st.session_state.theme]}}}</style>", unsafe_allow_html=True)
st.markdown(BASE_CSS, unsafe_allow_html=True)

# ---------------- HELPERS ----------------

@st.cache_data(ttl=10, show_spinner=False)
def fetch_models(host):
    """Returns (reachable, model_names, error_text)."""
    try:
        res = ollama.Client(host=host).list()
        names = []
        for m in res["models"]:
            name = getattr(m, "model", None) or (
                (m.get("model") or m.get("name")) if isinstance(m, dict) else None)
            if name:
                names.append(name)
        return True, sorted(names), ""
    except Exception as e:
        return False, [], str(e)


def stream_reply(host, model, messages, temperature):
    """Yields ('thinking' | 'content', text) pieces from Ollama."""
    client = ollama.Client(host=host)
    for chunk in client.chat(model=model, messages=messages, stream=True,
                             options={"temperature": temperature}):
        msg = chunk["message"]
        thinking = getattr(msg, "thinking", None) or (
            msg.get("thinking") if isinstance(msg, dict) else None)
        if thinking:
            yield "thinking", thinking
        content = msg["content"]
        if content:
            yield "content", content


TYPING = '<div class="typing"><span></span><span></span><span></span></div>'

# ---------------- SIDEBAR ----------------

with st.sidebar:
    st.markdown('<div class="side-logo">NEXORA</div>', unsafe_allow_html=True)
    st.caption("Local AI · powered by Ollama")

    st.markdown("### Profile")
    st.text_input("Your name", key="user_name", placeholder="What should NEXORA call you?",
                  label_visibility="collapsed")

    st.markdown("### Connection")
    with st.expander("Ollama host"):
        st.text_input("Host", key="host", label_visibility="collapsed")
    reachable, models, conn_error = fetch_models(st.session_state.host)
    if st.button("↻  Refresh models"):
        fetch_models.clear()
        st.rerun()

    st.markdown("### Model")
    if models:
        idx = next((i for i, n in enumerate(models) if n.startswith(DEFAULT_MODEL)), 0)
        model_name = st.selectbox("Model", models, index=idx, label_visibility="collapsed")
    else:
        model_name = st.text_input("Model", value=DEFAULT_MODEL, label_visibility="collapsed")

    temperature = st.slider("Creativity", 0.0, 1.5, 0.7, 0.1,
                            help="Lower = precise, higher = more creative")

    st.markdown("### Context")
    doc = st.file_uploader("Attach a text file", type=["txt", "md"], label_visibility="collapsed")
    doc_text = doc.read().decode("utf-8", errors="ignore")[:8000] if doc else ""
    if doc:
        st.caption(f"📎 {doc.name} attached")

    st.markdown("### Session")
    if st.button("🗑  New chat"):
        st.session_state.messages = []
        st.session_state.error = None
        st.rerun()
    if st.session_state.messages:
        transcript = "\n\n".join(
            f"{(st.session_state.user_name.strip() or 'USER').upper() if m['role'] == 'user' else 'NEXORA'}: {m['content']}"
            for m in st.session_state.messages)
        st.download_button("⬇  Export chat", transcript, "nexora_chat.txt")

    st.markdown("### Appearance")
    st.radio("Theme", ["Dark", "Light"], key="theme", horizontal=True, label_visibility="collapsed")

user_name = st.session_state.user_name.strip()
display_name = user_name or "You"

# ---------------- HEADER ----------------

status_dot = "on" if reachable else "off"
status_txt = f"Online · {model_name}" if reachable else "Ollama offline"
st.markdown(
    f"""<div class="brand"><div class="logo">NEXORA</div>
    <div class="pill"><span class="dot {status_dot}"></span>{status_txt}</div></div>""",
    unsafe_allow_html=True,
)

if not reachable:
    st.markdown(
        f"""<div class="notice"><b>Cannot reach Ollama</b> at <code>{st.session_state.host}</code>.<br>
        1. Install it from ollama.com &nbsp; 2. Run <code>ollama serve</code> &nbsp;
        3. Run <code>ollama pull {DEFAULT_MODEL}</code> &nbsp; 4. Click <b>Refresh models</b> in the sidebar.</div>""",
        unsafe_allow_html=True)
elif not models:
    st.markdown(
        f"""<div class="notice"><b>No models installed.</b> Run
        <code>ollama pull {DEFAULT_MODEL}</code> in a terminal, then click <b>Refresh models</b>.</div>""",
        unsafe_allow_html=True)

# ---------------- INPUT ----------------

prompt = st.chat_input(f"Speak, {user_name}..." if user_name else "Type your message...")
if st.session_state.pending:
    prompt, st.session_state.pending = st.session_state.pending, None

# ---------------- WELCOME ----------------

if not st.session_state.messages and not prompt:
    greeting = f"State your command, {user_name}." if user_name else "Tell me your name to begin."
    st.markdown(
        f"""<div class="welcome"><h2>Curiosity in. Intelligent answers out.</h2>
        <p>I am NEXORA. Your systems are online. {greeting}</p></div>""",
        unsafe_allow_html=True)
    if not user_name:
        st.text_input("What should I call you?", key="name_welcome", placeholder="Enter your name",
                      on_change=lambda: st.session_state.update(user_name=st.session_state.name_welcome))
    st.markdown('<div class="sugg">', unsafe_allow_html=True)
    cols = st.columns(2)
    for i, (icon, text) in enumerate(SUGGESTIONS):
        if cols[i % 2].button(f"{icon}  {text}", key=f"sugg_{i}"):
            st.session_state.pending = text
            st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

# ---------------- HISTORY ----------------

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

if st.session_state.error and not prompt:
    st.error(st.session_state.error)

# ---------------- NEW MESSAGE ----------------

if prompt:
    st.session_state.error = None
    if prompt.strip().lower() == "exit":
        st.session_state.messages = []
        st.rerun()

    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    system = SYSTEM_PROMPT + addressing_rule(user_name)
    if doc_text:
        system += f"\n\nThe user attached this document as context:\n---\n{doc_text}\n---"
    conversation = [{"role": "system", "content": system}] + st.session_state.messages

    with st.chat_message("assistant"):
        box = st.empty()
        box.markdown(TYPING, unsafe_allow_html=True)
        full = ""
        try:
            for kind, text in stream_reply(st.session_state.host, model_name, conversation, temperature):
                if kind == "content":
                    full += text
                    box.markdown(full + " ▌")
            box.markdown(full)
            if full.strip():
                st.session_state.messages.append({"role": "assistant", "content": full})
            else:
                box.empty()
                st.session_state.error = (
                    f"'{model_name}' returned an empty reply. Try again, or pick a different model "
                    "(reasoning models sometimes return no visible text).")
                st.error(st.session_state.error)
        except Exception as e:
            box.empty()
            st.session_state.error = (
                f"SYSTEM FAILURE: {e}\n\nCheck that Ollama is running and that "
                f"`{model_name}` is installed (`ollama pull {model_name}`).")
            st.error(st.session_state.error)