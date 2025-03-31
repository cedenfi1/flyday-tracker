import streamlit as st
from datetime import date

# --- App Setup ---
st.set_page_config(page_title="Flyday Assistant", layout="centered")

# --- Sample Airport List (expand as needed) ---
AIRPORTS = sorted([
    "Atlanta (ATL) - USA", "Chicago O'Hare (ORD) - USA", "Los Angeles (LAX) - USA",
    "Dallas/Fort Worth (DFW) - USA", "Denver (DEN) - USA", "New York JFK (JFK) - USA",
    "San Francisco (SFO) - USA", "Seattle (SEA) - USA", "Orlando (MCO) - USA",
    "Boston Logan (BOS) - USA", "Charlotte (CLT) - USA", "Las Vegas (LAS) - USA",
    "Miami (MIA) - USA", "Phoenix (PHX) - USA", "Houston (IAH) - USA",
    "Washington Dulles (IAD) - USA", "San Diego (SAN) - USA", "Tampa (TPA) - USA",
    "Philadelphia (PHL) - USA", "Minneapolis (MSP) - USA", "Detroit (DTW) - USA",
    "Salt Lake City (SLC) - USA", "Portland (PDX) - USA", "Nashville (BNA) - USA",
    "London Heathrow (LHR) - UK", "Paris Charles de Gaulle (CDG) - France",
    "Frankfurt (FRA) - Germany", "Tokyo Haneda (HND) - Japan",
    "Hong Kong (HKG) - China", "Dubai (DXB) - UAE", "Toronto Pearson (YYZ) - Canada",
    "Vancouver (YVR) - Canada", "Mexico City (MEX) - Mexico",
    "Amsterdam Schiphol (AMS) - Netherlands", "Madrid Barajas (MAD) - Spain",
    "Rome Fiumicino (FCO) - Italy", "Zurich (ZRH) - Switzerland",
    "Istanbul (IST) - Turkey", "Doha (DOH) - Qatar"
])

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

# --- Step 2: Destination (with autocomplete from local list) ---
elif st.session_state.step == 2:
    st.header("🌍 Where are you going?")
    destination = st.selectbox(
        "Start typing your destination",
        options=AIRPORTS,
        index=0 if not st.session_state.destination else AIRPORTS.index(st.session_state.destination)
    )
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
    st.write(f"📅 **Departure Date:** {st.session_state.departure_date.strftime('%A, %B %d, %Y')}")
    st.write(f"📍 **Destination:** {st.session_state.destination}")
    st.write(f"🛫 **Airline:** {st.session_state.airline}")
    if st.button("🔄 Start Over"):
        for key in ["step", "departure_date", "destination", "airline"]:
            del st.session_state[key]
