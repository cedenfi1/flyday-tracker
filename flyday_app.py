import streamlit as st
from datetime import date

# --- Page Setup ---
st.set_page_config(page_title="✈️ Flyday Assistant", layout="centered")

# --- Styling ---
st.markdown("""
    <style>
    .big-question {
        font-size: 2.2rem;
        text-align: center;
        margin-top: 4rem;
        margin-bottom: 2rem;
    }
    .step-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 2rem;
    }
    .input-box {
        width: 300px;
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

# --- Title / Step 1 ---
st.markdown('<div class="big-question">🛫 When are you leaving?</div>', unsafe_allow_html=True)

with st.container():
    departure_date = st.date_input("Select your departure date", min_value=date.today(), label_visibility="collapsed")

# --- Step 2: Reveal Destination Input ---
if departure_date:
    st.markdown('<div class="big-question">🌍 Where are you going?</div>', unsafe_allow_html=True)
    destination = st.text_input("Enter your destination", placeholder="e.g. Chicago O'Hare", label_visibility="collapsed")

    # Optional: Show progress summary
    if destination:
        st.markdown("---")
        st.markdown(f"📅 **You’re flying on:** `{departure_date.strftime('%A, %B %d, %Y')}`")
        st.markdown(f"📍 **Your destination is:** `{destination}`")
