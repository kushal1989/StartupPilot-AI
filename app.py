from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_classic.memory import ConversationBufferMemory
from langchain_classic.chains import LLMChain
import streamlit as st
import os

# ---------------- LOAD ENV ---------------- #
load_dotenv()

# ---------------- PAGE CONFIG ---------------- #
st.set_page_config(
    page_title="StartupPilot AI",
    page_icon="🚀",
    layout="wide"
)

# ---------------- CUSTOM CSS ---------------- #
st.markdown("""
<style>

/* =========================
   MAIN BACKGROUND
========================= */
.stApp {
    background-image:
    linear-gradient(
        rgba(6,10,25,0.88),
        rgba(6,10,25,0.88)
    ),
    url("https://images.unsplash.com/photo-1516321318423-f06f85e504b3?q=80&w=2070&auto=format&fit=crop");

    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    background-attachment: fixed;
}

/* =========================
   REMOVE STREAMLIT STYLING
========================= */
#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

header {
    background: transparent !important;
}

/* =========================
   MAIN CONTAINER
========================= */
.block-container {
    padding-top: 1rem !important;
    padding-bottom: 6rem !important;
    padding-left: 3rem !important;
    padding-right: 3rem !important;
}

/* =========================
   GLOBAL TEXT
========================= */
html, body, p, li, span, label {
    color: white !important;
}

/* =========================
   SIDEBAR
========================= */
[data-testid="stSidebar"] {
    background: rgba(8,12,28,0.95);
    border-right: 1px solid rgba(255,255,255,0.08);
}

/* =========================
   FEATURE CARDS
========================= */
.feature-card {
    background: rgba(255,255,255,0.06);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 20px;
    padding: 18px;
    margin-bottom: 18px;
    backdrop-filter: blur(10px);
    transition: 0.3s ease;
}

.feature-card:hover {
    transform: translateY(-4px);
    border: 1px solid rgba(96,165,250,0.4);
}

.feature-title {
    font-size: 18px;
    font-weight: 700;
    margin-bottom: 8px;
    color: white;
}

.feature-desc {
    color: #d1d5db !important;
    font-size: 15px;
}

/* =========================
   BUTTONS
========================= */
.stButton > button {
    width: 100%;
    background: linear-gradient(135deg, #2563EB, #06B6D4);
    color: white !important;
    border: none;
    border-radius: 16px;
    padding: 14px 20px;
    font-size: 16px;
    font-weight: 700;
    transition: all 0.3s ease;
}

.stButton > button:hover {
    transform: translateY(-3px);
    box-shadow: 0 8px 25px rgba(37,99,235,0.35);
}

/* =========================
   CHAT MESSAGES
========================= */
[data-testid="stChatMessage"] {
    background: rgba(255,255,255,0.06);
    border-radius: 18px;
    padding: 16px;
    border: 1px solid rgba(255,255,255,0.08);
    backdrop-filter: blur(10px);
    margin-top: 14px;
}

[data-testid="stChatMessage"] * {
    color: white !important;
    line-height: 1.8;
}

/* =========================
   CHAT INPUT
========================= */
.stChatInput input {
    background: rgba(255,255,255,0.08) !important;
    border: 1px solid rgba(96,165,250,0.4) !important;
    border-radius: 25px !important;
    color: white !important;
}

.stChatInput input::placeholder {
    color: #CBD5E1 !important;
}

.stChatInput input:focus {
    border-color: #06B6D4 !important;
    box-shadow: 0 0 8px rgba(6,182,212,0.3) !important;
}
            
/* Remove white bottom container */
[data-testid="stBottomBlockContainer"] {
    background: transparent !important;
}

/* Floating chat container */
.stChatFloatingInputContainer {
    background: transparent !important;
}

/* Chat input wrapper */
[data-testid="stChatInput"] {
    background: transparent !important;
}

/* Actual input area */
.stChatInputContainer {
    background: transparent !important;
}

/* =========================
   FOOTER
========================= */
.footer {
    text-align: center;
    margin-top: 30px;
    color: #d1d5db !important;
}

</style>
""", unsafe_allow_html=True)

# ---------------- TITLE ---------------- #
st.markdown(
    """
    <h1 style='
        text-align: center;
        color: white;
        font-size: 52px;
        margin-bottom: 5px;
    '>
        🚀 StartupPilot AI
    </h1>

    <p style='
        text-align: center;
        font-size: 22px;
        color: #94A3B8;
        margin-top: 0px;
        margin-bottom: 30px;
    '>
        AI-Powered Startup & Business Guidance Assistant
    </p>
    """,
    unsafe_allow_html=True
)

# ---------------- SIDEBAR ---------------- #
with st.sidebar:

    st.title("🚀 StartupPilot AI")

    st.caption("AI Startup & Business Mentor")

    st.markdown("---")

    st.subheader("🎯 Core Capabilities")

    st.markdown("""
    ✅ Startup Idea Validation  
    ✅ Business Strategy Guidance  
    ✅ Revenue Model Suggestions  
    ✅ MVP Planning  
    ✅ Pitch Deck Assistance  
    ✅ Branding & Marketing Ideas  
    """)

    st.markdown("---")

    st.image(
        "https://cdn-icons-png.flaticon.com/512/3135/3135715.png",
        width=120
    )

    st.markdown("### 💡 Pro Startup Tip")

    st.info(
        "Focus on solving a real problem before scaling your startup idea."
    )

    st.markdown("---")

    if st.button("🗑️ Reset Conversation"):

        st.session_state.messages = []

        st.session_state.memory = ConversationBufferMemory(
            memory_key="history",
            return_messages=True
        )

        st.rerun()

# ---------------- FEATURE CARDS ---------------- #
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class='feature-card'>
        <div class='feature-title'>💡 Startup Validation</div>
        <div class='feature-desc'>
            Validate startup ideas, identify market gaps, and improve business potential.
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class='feature-card'>
        <div class='feature-title'>📈 Growth Strategies</div>
        <div class='feature-desc'>
            Receive practical marketing, branding, and scaling guidance for your startup.
        </div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class='feature-card'>
        <div class='feature-title'>💰 Revenue Models</div>
        <div class='feature-desc'>
            Discover monetization ideas, SaaS pricing models, and business opportunities.
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ---------------- QUICK ACTIONS ---------------- #
st.markdown(
    "<h2 style='text-align:center;'>⚡ Quick Startup Actions</h2>",
    unsafe_allow_html=True
)

prompt = None

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🚀 Validate Startup Idea"):
        prompt = "Validate my startup idea and suggest improvements"

    if st.button("🤖 AI Startup Ideas"):
        prompt = "Suggest innovative AI startup ideas for students"

with col2:
    if st.button("💰 Revenue Model Guide"):
        prompt = "Suggest the best revenue models for SaaS startups"

    if st.button("📱 MVP Development Plan"):
        prompt = "How do I build an MVP for my startup?"

with col3:
    if st.button("📈 Marketing Strategy"):
        prompt = "Create a marketing strategy for my startup"

    if st.button("🎯 Pitch Deck Help"):
        prompt = "Help me prepare a startup pitch deck"

st.markdown("---")

# ---------------- MEMORY ---------------- #
if "memory" not in st.session_state:

    st.session_state.memory = ConversationBufferMemory(
        memory_key="history",
        return_messages=True
    )

# ---------------- CHAT HISTORY ---------------- #
if "messages" not in st.session_state:
    st.session_state.messages = []

# ---------------- WELCOME MESSAGE ---------------- #
if len(st.session_state.messages) == 0:

    welcome_msg = """
👋 **Welcome to StartupPilot AI**

I can help you with:

- 🚀 Startup idea validation
- 💰 Revenue model suggestions
- 📈 Marketing & branding strategies
- 🎯 Investor pitch preparation
- 🌍 Market analysis
- 🧠 Business growth roadmaps

**What startup idea are you building today?** 🚀
"""

    st.session_state.messages.append({
        "role": "assistant",
        "content": welcome_msg
    })

# ---------------- LOAD TEMPLATE ---------------- #
with open("template.txt", "r", encoding="utf-8") as file:
    prompt_template = file.read()

# ---------------- PROMPT SETUP ---------------- #
chat_prompt = ChatPromptTemplate.from_messages([
    ("system", prompt_template),
    MessagesPlaceholder(variable_name="history"),
    ("human", "{input}")
])

# ---------------- GEMINI MODEL ---------------- #
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.7,
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

# ---------------- CHAIN ---------------- #
chain = LLMChain(
    llm=llm,
    prompt=chat_prompt,
    memory=st.session_state.memory
)

# ---------------- DISPLAY CHAT HISTORY ---------------- #
for msg in st.session_state.messages:

    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ---------------- CHAT INPUT ---------------- #
user_input = st.chat_input(
    "💬 Ask anything about startups, funding, marketing, or business growth..."
)

# ---------------- QUICK ACTION INPUT ---------------- #
if prompt:
    user_input = prompt

# ---------------- RESPONSE GENERATION ---------------- #
if user_input:

    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    with st.chat_message("user"):
        st.markdown(user_input)

    with st.spinner(
        "🚀 Analyzing your startup idea and generating insights..."
    ):

        response = chain.invoke({
            "input": user_input
        })

        ai_response = response["text"]

    st.session_state.messages.append({
        "role": "assistant",
        "content": ai_response
    })

    with st.chat_message("assistant"):
        st.markdown(ai_response)

# ---------------- FOOTER ---------------- #
st.markdown(
    """
    <div class='footer'>
        Powered by Gemini AI 🚀 | Built with Streamlit
    </div>
    """,
    unsafe_allow_html=True
)