import streamlit as st
from datetime import date, datetime, timedelta
import difflib

# --- App Setup ---
st.set_page_config(page_title="Flyday Assistant", layout="centered")
st.markdown("""
    <style>
    .main { padding: 1rem; max-width: 400px; margin: 0 auto; }
    .stApp { background-color: #f7f9fc; font-family: 'Segoe UI', sans-serif; }
    h1, h2, h3, h4, h5, h6 { color: #2c3e50; }
    .stButton > button, .stDownloadButton > button {
        width: 100%;
        padding: 0.5rem;
        font-size: 1rem;
        border-radius: 8px;
    }
    .stButton > button { background-color: #3498db; color: white; }
    .stDownloadButton > button { background-color: #27ae60; color: white; }
    .stTextInput > div > input,
    .stDateInput > div,
    .stTimeInput > div,
    .stSelectbox > div { border-radius: 8px; font-size: 1rem; }
    .css-1aumxhk { font-size: 1rem; }
</style>
""", unsafe_allow_html=True)

# --- Major US Airports (Further Expanded) ---
AIRPORTS = sorted([
    "Atlanta (ATL) - USA", "Chicago O'Hare (ORD) - USA", "Los Angeles (LAX) - USA",
    "Dallas/Fort Worth (DFW) - USA", "Denver (DEN) - USA", "New York JFK (JFK) - USA",
    "San Francisco (SFO) - USA", "Seattle (SEA) - USA", "Orlando (MCO) - USA",
    "Boston Logan (BOS) - USA", "Charlotte (CLT) - USA", "Las Vegas (LAS) - USA",
    "Miami (MIA) - USA", "Phoenix (PHX) - USA", "Houston (IAH) - USA",
    "Washington Dulles (IAD) - USA", "San Diego (SAN) - USA", "Tampa (TPA) - USA",
    "Philadelphia (PHL) - USA", "Minneapolis (MSP) - USA", "Detroit (DTW) - USA",
    "Salt Lake City (SLC) - USA", "Portland (PDX) - USA", "Nashville (BNA) - USA",
    "Baltimore/Washington (BWI) - USA", "St. Louis Lambert (STL) - USA",
    "Kansas City (MCI) - USA", "Austin-Bergstrom (AUS) - USA",
    "Sacramento (SMF) - USA", "Raleigh-Durham (RDU) - USA", "Cleveland Hopkins (CLE) - USA",
    "Indianapolis (IND) - USA", "San Jose (SJC) - USA", "Cincinnati/Northern Kentucky (CVG) - USA",
    "Pittsburgh (PIT) - USA", "Columbus (CMH) - USA", "New Orleans (MSY) - USA",
    "San Antonio (SAT) - USA", "Oakland (OAK) - USA", "Fort Lauderdale (FLL) - USA",
    "Honolulu (HNL) - USA", "Anchorage (ANC) - USA", "Palm Beach (PBI) - USA",
    "Jacksonville (JAX) - USA", "Buffalo Niagara (BUF) - USA", "Albany (ALB) - USA",
    "Boise (BOI) - USA", "Omaha (OMA) - USA", "El Paso (ELP) - USA",
    "Burbank (BUR) - USA", "Colorado Springs (COS) - USA", "Des Moines (DSM) - USA",
    "Greenville-Spartanburg (GSP) - USA", "Harrisburg (MDT) - USA", "Long Beach (LGB) - USA",
    "Manchester-Boston (MHT) - USA", "Milwaukee (MKE) - USA", "Norfolk (ORF) - USA",
    "Providence (PVD) - USA", "Reno-Tahoe (RNO) - USA", "Richmond (RIC) - USA",
    "Spokane (GEG) - USA", "Syracuse (SYR) - USA", "Tucson (TUS) - USA",
    "Tulsa (TUL) - USA", "Westchester County (HPN) - USA", "Sarasota-Bradenton (SRQ) - USA",
    "Punta Gorda (PGD) - USA", "St. Pete–Clearwater (PIE) - USA", "Fort Myers (RSW) - USA",
    "Gainesville Regional (GNV) - USA", "Tallahassee (TLH) - USA", "Asheville (AVL) - USA",
    "Columbia Metropolitan (CAE) - USA", "Augusta Regional (AGS) - USA", "Spartanburg Downtown (SPA) - USA",
    "Anderson Regional (AND) - USA", "Greenville Downtown (GMU) - USA"
])

# --- Session State Defaults ---
st.session_state.setdefault("step", 1)
st.session_state.setdefault("departure_date", None)
st.session_state.setdefault("destination", "")
st.session_state.setdefault("airline", "")
st.session_state.setdefault("flight_number", "")
st.session_state.setdefault("departure_time", "")
st.session_state.setdefault("history", [])

# --- Step 1: Departure Date ---
if st.session_state.step == 1:
    st.header("🛫 When are you leaving?")
    departure = st.date_input("Select your departure date", min_value=date.today())
    if departure:
        st.session_state.departure_date = departure
        st.session_state.step = 2

# --- Step 2: Destination (fuzzy search input) ---
elif st.session_state.step == 2:
    st.header("🌍 Where are you going?")
    search_term = st.text_input("Start typing your destination")
    if search_term:
        matches = difflib.get_close_matches(search_term, AIRPORTS, n=10, cutoff=0.2)
        if matches:
            selected = st.selectbox("Select from closest matches:", matches)
            if selected:
                st.session_state.destination = selected
                st.session_state.step = 3

# --- Step 3: Airline Info ---
elif st.session_state.step == 3:
    st.header("✈️ What airline are you flying?")
    st.session_state.airline = st.text_input("Enter your airline", st.session_state.airline)
    st.session_state.flight_number = st.text_input("Enter your flight number", st.session_state.flight_number)
    st.session_state.departure_time = st.time_input("Enter your departure time")

    if all([st.session_state.airline, st.session_state.flight_number, st.session_state.departure_time]):
        st.session_state.step = 4

# --- Step 4: Summary ---
elif st.session_state.step == 4:
    st.header("✅ You're all set!")
    st.write(f"📅 **Departure Date:** {st.session_state.departure_date.strftime('%A, %B %d, %Y')}")
    st.write(f"📍 **Destination:** {st.session_state.destination}")
    st.write(f"🛫 **Airline:** {st.session_state.airline}")
    st.write(f"🔢 **Flight Number:** {st.session_state.flight_number}")
    st.write(f"⏰ **Departure Time:** {st.session_state.departure_time.strftime('%I:%M %p')}")

    countdown = (st.session_state.departure_date - date.today()).days
    st.write(f"⏳ **Days Until Departure:** {countdown} day(s)")

    # Calculate Boarding Time
    departure_datetime = datetime.combine(st.session_state.departure_date, st.session_state.departure_time)
    airline_lower = st.session_state.airline.lower()
    boarding_minutes = 40 if "delta" in airline_lower else 30
    boarding_time = (departure_datetime - timedelta(minutes=boarding_minutes)).strftime('%I:%M %p')
    st.write(f"📋 **Boarding Time:** {boarding_time} ({boarding_minutes} minutes before departure)")

    st.subheader("📦 Suggested Packing List")
    st.markdown("""
    - 🧳 Travel documents
    - 🪪 ID/passport
    - 🍫 Snacks
    - 🎧 Headphones
    - 🔌 Phone charger
    - 💧 Reusable water bottle
    """)

    st.session_state.history.append({
        "date": st.session_state.departure_date,
        "destination": st.session_state.destination,
        "airline": st.session_state.airline,
        "flight_number": st.session_state.flight_number
    })

    if st.button("🔄 Start Over"):
        for key in ["step", "departure_date", "destination", "airline", "flight_number", "departure_time"]:
            del st.session_state[key]

    if st.download_button("📥 Download Itinerary", data=f"Flyday Trip\n\nDeparture: {st.session_state.departure_date}\nDestination: {st.session_state.destination}\nAirline: {st.session_state.airline}\nFlight Number: {st.session_state.flight_number}\nDeparture Time: {st.session_state.departure_time}\nBoarding Time: {boarding_time} ({boarding_minutes} min before)", file_name="flyday_itinerary.txt"):
        pass
