import streamlit as st
from datetime import date

# --- App Config ---
st.set_page_config(page_title="Flyday Assistant", layout="centered")

# --- Session State Defaults ---
st.session_state.setdefault("step", 1)
st.session_state.setdefault("departure_date", None)
st.session_state.setdefault("destination", "")
st.session_state.setdefault("airline", "")

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

# --- STEP 1: Departure Date ---
if st.session_state.step == 1:
    st.markdown('<div class="big-question">🛫 When are you leaving?</div>', unsafe_allow_html=True)
    departure = st.date_input(
        "Select departure date",
        min_value=date.today(),
        label_visibility="collapsed",
        key="departure_date_picker"
    )
    if departure:
        st.session_state.departure_date = departure
        st.session_state.step = 2

# --- STEP 2: Destination ---
if st.session_state.step == 2:
    st.markdown('<div class="big-question">🌍 Where are you going?</div>', unsafe_allow_html=True)
    destination = st.text_input(
        "Enter your destination",
        placeholder="e.g. Seattle (SEA)",
        label_visibility="collapsed",
        key="destination_input"
    )
    if destination:
        st.session_state.destination = destination
        st.session_state.step = 3

# --- STEP 3: Airline ---
if st.session_state.step == 3:
    st.markdown('<div class="big-question">✈️ What airline are you flying?</div>', unsafe_allow_html=True)
    airline = st.text_input(
        "Enter your airline",
        placeholder="e.g. Delta",
        label_visibility="collapsed",
        key="airline_input"
    )
    if airline:
        st.session_state.airline = airline
        st.session_state.step = 4

# --- STEP 4: Summary ---
if st.session_state.step == 4:
    st.markdown("## ✅ Here's what we’ve got so far:")
    st.markdown(f"**📅 Departure Date:** `{st.session_state.departure_date.strftime('%A, %B %d, %Y')}`")
    st.markdown(f"**📍 Destination:** `{st.session_state.destination}`")
    st.markdown(f"**🛫 Airline:** `{st.session_state.airline}`")

    if st.button("🔄 Start Over"):
        for key in ["step", "departure_date", "destination", "airline"]:
            del st.session_state[key]
