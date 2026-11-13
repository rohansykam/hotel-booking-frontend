
import streamlit as st
import requests


# ==========================================
# 1. PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="Hotel Booking Cancellation Predictor",
    page_icon="🏨",
    layout="wide"
    
)

API_URL = st.secrets.get(
    "API_URL",
    "http://127.0.0.1:8000"
)


# ==========================================
# 2. PAGE HEADER
# ==========================================

st.title("🏨 Hotel Booking Cancellation Predictor")

st.write(
    "Enter the hotel booking details below to predict "
    "whether the reservation is likely to be cancelled."
)

# Check backend connection
try:
    api_response = requests.get(API_URL, timeout=5)

    if api_response.status_code == 200:
        st.success("Backend API Connected")
    else:
        st.warning("Backend API is responding with an error.")

except requests.exceptions.RequestException:
    st.error(
        "Backend API is not running. "
        "Please start FastAPI before making predictions."
    )

st.divider()


# ==========================================
# 3. BOOKING INPUT FORM
# ==========================================

with st.form("booking_prediction_form",enter_to_submit=False):

    # --------------------------------------
    # SECTION 1: HOTEL AND ARRIVAL DETAILS
    # --------------------------------------

    with st.expander(
        "🏨 Hotel & Arrival Information",
        expanded=True
    ):

        col1, col2, col3 = st.columns(3)

        with col1:

            hotel = st.selectbox(
                "Hotel",
                ["Resort Hotel", "City Hotel"]
            )

            arrival_date_year = st.selectbox(
                "Arrival Year",
                [2015, 2016, 2017]
            )

        with col2:

            lead_time = st.number_input(
                "Lead Time (days)",
                min_value=0,
                value=50
            )

            arrival_date_month = st.selectbox(
                "Arrival Month",
                [
                    "January", "February", "March",
                    "April", "May", "June", "July",
                    "August", "September", "October",
                    "November", "December"
                ]
            )

        with col3:

            arrival_date_week_number = st.number_input(
                "Arrival Week Number",
                min_value=1,
                max_value=53,
                value=25
            )

            arrival_date_day_of_month = st.number_input(
                "Arrival Day",
                min_value=1,
                max_value=31,
                value=15
            )

    # --------------------------------------
    # SECTION 2: GUEST DETAILS
    # --------------------------------------

    with st.expander("👥 Guest Information"):

        col1, col2, col3 = st.columns(3)

        with col1:

            adults = st.number_input(
                "Adults",
                min_value=0,
                value=2
            )

            children = st.number_input(
                "Children",
                min_value=0.0,
                value=0.0
            )

        with col2:

            babies = st.number_input(
                "Babies",
                min_value=0,
                value=0
            )

            is_repeated_guest = st.selectbox(
                "Repeated Guest",
                [0, 1],
                format_func=lambda x: (
                    "Yes" if x == 1 else "No"
                )
            )

        with col3:

            country = st.text_input(
                "Country Code",
                value="PRT",
                help="Enter a three-letter country code."
            )

    # --------------------------------------
    # SECTION 3: BOOKING INFORMATION
    # --------------------------------------

    with st.expander("📋 Booking Information"):

        col1, col2 = st.columns(2)

        with col1:

            stays_in_weekend_nights = st.number_input(
                "Weekend Nights",
                min_value=0,
                value=1
            )

            stays_in_week_nights = st.number_input(
                "Week Nights",
                min_value=0,
                value=2
            )

            meal = st.selectbox(
                "Meal",
                ["BB", "FB", "HB", "SC", "Undefined"]
            )

            market_segment = st.selectbox(
                "Market Segment",
                [
                    "Direct", "Corporate",
                    "Online TA", "Offline TA/TO",
                    "Complementary", "Groups",
                    "Aviation", "Undefined"
                ]
            )

            distribution_channel = st.selectbox(
                "Distribution Channel",
                [
                    "Direct", "Corporate",
                    "TA/TO", "GDS", "Undefined"
                ]
            )

            reserved_room_type = st.selectbox(
                "Reserved Room Type",
                ["A", "B", "C", "D", "E", "F", "G", "H", "P"]
            )

        with col2:

            previous_cancellations = st.number_input(
                "Previous Cancellations",
                min_value=0,
                value=0
            )

            previous_bookings_not_canceled = st.number_input(
                "Previous Successful Bookings",
                min_value=0,
                value=0
            )

            booking_changes = st.number_input(
                "Booking Changes",
                min_value=0,
                value=0
            )

            deposit_type = st.selectbox(
                "Deposit Type",
                ["No Deposit", "Non Refund", "Refundable"]
            )

            customer_type = st.selectbox(
                "Customer Type",
                [
                    "Transient",
                    "Transient-Party",
                    "Contract",
                    "Group"
                ]
            )

    # --------------------------------------
    # SECTION 4: ADDITIONAL SERVICES
    # --------------------------------------

    with st.expander("🛎️ Additional Booking Details"):

        col1, col2 = st.columns(2)

        with col1:

            agent = st.text_input(
                "Agent ID",
                value="",
                help="Leave blank if not available."
            )

            company = st.text_input(
                "Company ID",
                value="",
                help="Leave blank if not available."
            )

            days_in_waiting_list = st.number_input(
                "Days in Waiting List",
                min_value=0,
                value=0
            )

        with col2:

            adr = st.number_input(
                "Average Daily Rate (ADR)",
                min_value=0.0,
                value=75.0,
                step=1.0
            )

            required_car_parking_spaces = st.number_input(
                "Required Parking Spaces",
                min_value=0,
                value=0
            )

            total_of_special_requests = st.number_input(
                "Total Special Requests",
                min_value=0,
                value=0
            )

    # --------------------------------------
    # SUBMIT BUTTON
    # --------------------------------------

    st.divider()

    submitted = st.form_submit_button(
        "🔍 Predict Cancellation",
        use_container_width=True
    )
# Reset Form Button

if st.button("🔄 Reset Form", use_container_width=True):
    st.session_state.clear()
    st.rerun()

# ==========================================
# 4. SEND REQUEST TO FASTAPI
# ==========================================

if submitted:

    booking_data = {

        "hotel": hotel,
        "lead_time": lead_time,
        "arrival_date_year": arrival_date_year,
        "arrival_date_month": arrival_date_month,
        "arrival_date_week_number": arrival_date_week_number,
        "arrival_date_day_of_month": arrival_date_day_of_month,

        "stays_in_weekend_nights": stays_in_weekend_nights,
        "stays_in_week_nights": stays_in_week_nights,

        "adults": adults,
        "children": children,
        "babies": babies,

        "meal": meal,
        "country": country.strip() or None,

        "market_segment": market_segment,
        "distribution_channel": distribution_channel,

        "is_repeated_guest": is_repeated_guest,
        "previous_cancellations": previous_cancellations,
        "previous_bookings_not_canceled": previous_bookings_not_canceled,

        "reserved_room_type": reserved_room_type,
        "booking_changes": booking_changes,
        "deposit_type": deposit_type,

        "agent": agent.strip() or None,
        "company": company.strip() or None,

        "days_in_waiting_list": days_in_waiting_list,
        "customer_type": customer_type,
        "adr": adr,

        "required_car_parking_spaces": required_car_parking_spaces,
        "total_of_special_requests": total_of_special_requests

    }

    # ======================================
    # 5. GET PREDICTION FROM FASTAPI
    # ======================================

    try:

        with st.spinner("Analyzing booking details..."):

            response = requests.post(
                f"{API_URL}/predict",
                json=booking_data,
                timeout=30
            )

        if response.status_code == 200:

            result = response.json()

            st.divider()
            st.header("Prediction Result")

            probability = result[
                "cancellation_probability"
            ]

            if result["prediction"] == 1:

                st.error(
                    "⚠️ Booking is predicted to be CANCELLED"
                )

            else:

                st.success(
                    "✅ Booking is predicted to be NOT CANCELLED"
                )

            col1, col2 = st.columns(2)

            col1.metric(
                "Cancellation Probability",
                f"{probability:.2f}%"
            )

            col2.metric(
                "Classification Threshold",
                f"{result['threshold'] * 100:.0f}%"
            )

            st.progress(
                min(max(probability / 100, 0), 1)
            )

            st.caption(
                f"Prediction Model: {result['model']}"
            )

        else:

            st.error(
                f"API Error: {response.status_code}"
            )

            st.code(response.text)

    except requests.exceptions.RequestException as e:

        st.error(f"Connection Error: {e}")


# ==========================================
# 6. FOOTER
# ==========================================

st.divider()

st.caption(
    "Hotel Booking Cancellation Prediction | "
    "Powered by Streamlit, FastAPI and Machine Learning"
)
