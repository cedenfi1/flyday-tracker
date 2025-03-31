import streamlit as st
from datetime import date, datetime, timedelta
import difflib
import random

# --- App Setup ---
st.set_page_config(page_title="Flyday Assistant", layout="centered")
st.markdown("""
    <style>
    .main { padding: 1rem; max-width: 400px; margin: 0 auto; }
    .stApp { background-color: #f7f9fc; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; }
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

# --- Major US Airports (Expanded) ---
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
    "Kansas City (MCI) - USA", "Austin-Bergstrom (AUS) - USA", "Sacramento (SMF) - USA",
    "Raleigh-Durham (RDU) - USA", "Cleveland Hopkins (CLE) - USA", "Indianapolis (IND) - USA",
    "San Jose (SJC) - USA", "Cincinnati/Northern Kentucky (CVG) - USA",
    "Pittsburgh (PIT) - USA", "Columbus (CMH) - USA", "New Orleans (MSY) - USA",
    "San Antonio (SAT) - USA", "Oakland (OAK) - USA", "Fort Lauderdale (FLL) - USA",
    "Honolulu (HNL) - USA", "Anchorage (ANC) - USA", "Palm Beach (PBI) - USA",
    "Jacksonville (JAX) - USA", "Buffalo Niagara (BUF) - USA", "Albany (ALB) - USA",
    "Boise (BOI) - USA", "Omaha (OMA) - USA", "El Paso (ELP) - USA", "Burbank (BUR) - USA",
    "Colorado Springs (COS) - USA", "Des Moines (DSM) - USA", "Greenville-Spartanburg (GSP) - USA",
    "Harrisburg (MDT) - USA", "Long Beach (LGB) - USA", "Manchester-Boston (MHT) - USA",
    "Milwaukee (MKE) - USA", "Norfolk (ORF) - USA", "Providence (PVD) - USA",
    "Reno-Tahoe (RNO) - USA", "Richmond (RIC) - USA", "Spokane (GEG) - USA",
    "Syracuse (SYR) - USA", "Tucson (TUS) - USA", "Tulsa (TUL) - USA",
    "Westchester County (HPN) - USA", "Sarasota-Bradenton (SRQ) - USA",
    "Punta Gorda (PGD) - USA", "St. Pete–Clearwater (PIE) - USA",
    "Fort Myers (RSW) - USA", "Gainesville Regional (GNV) - USA",
    "Tallahassee (TLH) - USA", "Asheville (AVL) - USA", "Columbia Metropolitan (CAE) - USA",
    "Augusta Regional (AGS) - USA", "Spartanburg Downtown (SPA) - USA",
    "Anderson Regional (AND) - USA", "Greenville Downtown (GMU) - USA"
])

# --- Cozy Kitty Departure Messages ---
DEPARTURE_MESSAGES = [
    "Your kitty will be keeping your seat warm while you're away.",
    "Off you go! Your home (and your cat) will be waiting when you return.",
    "Another adventure begins. Don’t worry—your kitty will guard the pillows.",
    "Enjoy your trip! Your favorite feline will be watching the door for you.",
    "Your paws may leave home, but your kitty’s heart stays with you.",
    "Fly safe—your cat will expect a full report and treats when you return.",
    "Have a great trip! Your whiskered friend will be here when you get back.",
    "Just don’t forget who rules the house while you’re gone. 😼",
    "Pack your bags, not your fur. 🧳🐾",
    "The window perch won’t be the same without you."
]

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
    st.header("📅 When are you flying away from home?")
    departure = st.date_input("Select your departure date", min_value=date.today())
    if departure:
        st.session_state.departure_date = departure
        st.session_state.step = 2

# --- Step 2: Destination (fuzzy search input) ---
elif st.session_state.step == 2:
    st.header("🌎 Where are you headed next, explorer?")
    search_term = st.text_input("Start typing your destination")
    if search_term:
        matches = difflib.get_close_matches(search_term, AIRPORTS, n=10, cutoff=0.2)
        if matches:
            selected = st.selectbox("Choose the best match:", matches)
            if selected:
                st.session_state.destination = selected
                st.session_state.step = 3

# --- Step 3: Airline Info ---
elif st.session_state.step == 3:
    st.header("🛫 How are you getting there?")
    st.session_state.airline = st.text_input("Airline", st.session_state.airline)
    st.session_state.flight_number = st.text_input("Flight number", st.session_state.flight_number)
    st.session_state.departure_time = st.time_input("Departure time")

    if all([st.session_state.airline, st.session_state.flight_number, st.session_state.departure_time]):
        st.session_state.step = 4

# --- Step 4: Summary ---
elif st.session_state.step == 4:
    st.header("✅ You’re all set, traveler!")
    st.write(f"📆 **Departure Date:** {st.session_state.departure_date.strftime('%A, %B %d, %Y')}")
    st.write(f"📍 **Destination:** {st.session_state.destination}")
    st.write(f"✈️ **Airline:** {st.session_state.airline}")
    st.write(f"🔢 **Flight #:** {st.session_state.flight_number}")
    st.write(f"⏰ **Departure Time:** {st.session_state.departure_time.strftime('%I:%M %p')}")

    # Countdown
    countdown = (st.session_state.departure_date - date.today()).days
    st.write(f"⏳ **Days Until Takeoff:** {countdown} day(s)")

    # Boarding time logic
    departure_datetime = datetime.combine(st.session_state.departure_date, st.session_state.departure_time)
    airline_lower = st.session_state.airline.lower()
    boarding_minutes = 40 if "delta" in airline_lower else 30
    boarding_time = (departure_datetime - timedelta(minutes=boarding_minutes)).strftime('%I:%M %p')
    st.write(f"🛎️ **Boarding Time:** {boarding_time} ({boarding_minutes} min before departure)")

    # Packing List
    st.subheader("🎒 Your Kitty-Approved Packing List")
    st.markdown("""
    - 🧳 Travel documents
    - 🪪 ID/passport
    - 🍫 Snacks
    - 🎧 Headphones
    - 🔌 Phone charger
    - 💧 Water bottle
    - 😴 Neck pillow
    - 🐾 Something that smells like home
    """)

    # Sweet departure message
    st.markdown(f"🐱 *{random.choice(DEPARTURE_MESSAGES)}*")

    # History
    st.session_state.history.append({
        "date": st.session_state.departure_date,
        "destination": st.session_state.destination,
        "airline": st.session_state.airline,
        "flight_number": st.session_state.flight_number
    })

    # Restart or download
    if st.button("🔄 Start Over"):
        for key in ["step", "departure_date", "destination", "airline", "flight_number", "departure_time"]:
            del st.session_state[key]

    itinerary = (
        f"Flyday Trip Summary\n\n"
        f"Departure Date: {st.session_state.departure_date}\n"
        f"Destination: {st.session_state.destination}\n"
        f"Airline: {st.session_state.airline}\n"
        f"Flight #: {st.session_state.flight_number}\n"
        f"Departure Time: {st.session_state.departure_time}\n"
        f"Boarding Time: {boarding_time} ({boarding_minutes} min before)\n"
    )

    st.download_button("📥 Download Itinerary", data=itinerary, file_name="flyday_itinerary.txt")
