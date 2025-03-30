import streamlit as st
from datetime import date

# --- App Setup ---
st.set_page_config(page_title="Flyday Assistant", layout="centered")

# --- Session State Defaults ---
st.session_state.setdefault("step", 1)
st.session_state.setdefault("departure_date", None)
st.session_state.setdefault("destination", "")
st.session_state.setdefault("airline", "")

# --- Step 1: Departure Date ---
if st.session_state.step == 1:
    st.header("🛫 When are you leaving?")
    departure = st.date_input("Select your departure date", min_value=date.today())
    if departure:
        st.session_state.departure_date = departure
        st.session_state.step = 2

# --- Step 2: Destination ---
elif st.session_state.step == 2:
    st.header("🌍 Where are you going?")
    destination = st.text_input("Enter your destination")
    if destination:
        st.session_state.destination = destination
        st.session_state.step = 3

# --- Step 3: Airline ---
elif st.session_state.step == 3:
    st.header("✈️ What airline are you flying?")
    airline = st.text_input("Enter your airline")
    if airline:
        st.session_state.airline = airline
        st.session_state.step = 4

# --- Step 4: Summary ---
elif st.session_state.step == 4:
    st.header("✅ You're all set!")
    st.write(f"📅 **Leaving on:** {st.session_state.departure_date.strftime('%A, %B %d, %Y')}")
    st.write(f"📍 **Destination:** {st.session_state.destination}")
    st.write(f"🛫 **Airline:** {st.session_state.airline}")
    if st.button("Start Over"):
        for key in ["step", "departure_date", "destination", "airline"]:
            del st.session_state[key]
