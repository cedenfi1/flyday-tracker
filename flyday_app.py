import streamlit as st
from datetime import date

# --- App Config ---
st.set_page_config(page_title="Flyday Assistant", layout="centered")

# --- Session State Setup ---
if "step" not in st.session_state:
    st.session_state.step = 1
if "departure_date" not in st.session_state:
    st.session_state.departure_date = None
if "destination" not in st.session_state:
    st.session_state.destination = ""
if "airline" not in st.session_state:
    st.session_state.airline = ""

# --- Styling ---
st.markdown("""
<style>
.big-question {
    font-size: 2.2rem;
    text-align: center;
    margin-top: 4rem;
    margin-bottom: 2rem;
}
input, .stDateInput {
    text-align: center;
}
</style>
""", unsafe_allow_html=True)

# --- Step 1: Ask for Departure Date ---
if st.session_state.step == 1:
    st.markdown('<div class="big-question">🛫 When are you leaving?</div>', unsafe_allow_html=True)
    departure = st.date_input("Select departure date", min_value=date.today(), label_visibility="collapsed")
    if departure:
        st.session_state.departure_date = departure
        st.session_state.step = 2
        st.experimental_rerun()

# --- Step 2: Ask for Destination ---
elif st.session_state.step == 2:
    st.markdown('<div class="big-question">🌍 Where are you going?</div>', unsafe_allow_html=True)
    destination = st.text_input("Enter your destination", placeholder="e.g. Seattle (SEA)", label_visibility="collapsed")
    if destination:
        st.session_state.destination = destination
        st.session_state.step = 3
        st.experimental_rerun()

# --- Step 3: Ask for Airline ---
elif st.session_state.step == 3:
    st.markdown('<div class="big-question">✈️ What airline are you flying?</div>', unsafe_allow_html=True)
    airline = st.text_input("Enter your airline", placeholder="e.g. Delta", label_visibility="collapsed")
    if airline:
        st.session_state.airline = airline
        st.session_state.step = 4
        st.experimental_rerun()

# --- Step 4: Show Summary ---
elif st.session_state.step == 4:
    st.markdown("## ✅ Here's what we’ve got so far:")
    st.markdown(f"**📅 Departure Date:** `{st.session_state.departure_date.strftime('%A, %B %d, %Y')}`")
    st.markdown(f"**📍 Destination:** `{st.session_state.destination}`")
    st.markdown(f"**🛫 Airline:** `{st.session_state.airline}`")

    # Button to restart flow (optional)
    if st.button("Start Over"):
        for key in ["step", "departure_date", "destination", "airline"]:
            st.session_state[key] = None if key != "step" else 1
        st.experimental_rerun()
