import streamlit as st
from datetime import date

# --- App Config ---
st.set_page_config(page_title="Flyday Assistant", layout="centered")

# --- Session State Defaults ---
if "step" not in st.session_state:
    st.session_state.step = 1
if "departure_date" not in st.session_state:
    st.session_state.departure_date = None
if "destination" not in st.session_state:
    st.session_state.destination = ""
if "airline" not in st.session_state:
    st.session_state.airline = ""

# --- Heavenly Styling ---
st.markdown("""
<style>
body {
    background-color: #fdfdfd;
}

.question-box {
    background: #ffffffdd;
    padding: 3rem 2rem;
    border-radius: 1.5rem;
    box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
    max-width: 600px;
    margin: 5rem auto;
    text-align: center;
}

.question-box h1 {
    font-size: 2.2rem;
    color: #333;
}

input, .stDateInput {
    text-align: center;
}
</style>
""", unsafe_allow_html=True)

# --- STEP 1: Ask for Departure Date ---
if st.session_state.step == 1:
    with st.container():
        st.markdown('<div class="question-box">', unsafe_allow_html=True)
        st.markdown("### 🛫 When are you leaving?")
        departure = st.date_input(
            "Select departure date",
            min_value=date.today(),
            label_visibility="collapsed",
            key="departure_date_picker"
        )
        if departure:
            st.session_state.departure_date = departure
            st.session_state.step = 2
        st.markdown("</div>", unsafe_allow_html=True)

# --- STEP 2: Ask for Destination ---
elif st.session_state.step == 2:
    with st.container():
        st.markdown('<div class="question-box">', unsafe_allow_html=True)
        st.markdown("### 🌍 Where are you going?")
        destination = st.text_input(
            "Enter your destination",
            placeholder="e.g. Seattle (SEA)",
            label_visibility="collapsed",
            key="destination_input"
        )
        if destination:
            st.session_state.destination = destination
            st.session_state.step = 3
        st.markdown("</div>", unsafe_allow_html=True)

# --- STEP 3: Ask for Airline ---
elif st.session_state.step == 3:
    with st.container():
        st.markdown('<div class="question-box">', unsafe_allow_html=True)
        st.markdown("### ✈️ What airline are you flying?")
        airline = st.text_input(
            "Enter your airline",
            placeholder="e.g. Delta",
            label_visibility="collapsed",
            key="airline_input"
        )
        if airline:
            st.session_state.airline = airline
            st.session_state.step = 4
        st.markdown("</div>", unsafe_allow_html=True)

# --- STEP 4: Show Summary ---
elif st.session_state.step == 4:
    with st.container():
        st.markdown('<div class="question-box">', unsafe_allow_html=True)
        st.markdown("### ✅ You're all set!")
        st.markdown(f"📅 **Leaving on:** `{st.session_state.departure_date.strftime('%A, %B %d, %Y')}`")
        st.markdown(f"📍 **Destination:** `{st.session_state.destination}`")
        st.markdown(f"🛫 **Airline:** `{st.session_state.airline}`")
        if st.button("🔄 Start Over"):
            for key in ["step", "departure_date", "destination", "airline"]:
                del st.session_state[key]
        st.markdown("</div>", unsafe_allow_html=True)
