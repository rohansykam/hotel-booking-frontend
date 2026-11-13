
// ========================================
// API CONFIGURATION
// ========================================

// Replace this with your actual Render backend URL.
// Example: https://hotel-booking-backend.onrender.com

const API_URL = "https://hotel-booking-backend-jqp9.onrender.com";


// ========================================
// HTML ELEMENTS
// ========================================

const bookingForm = document.getElementById("bookingForm");
const predictBtn = document.getElementById("predictBtn");

const resultSection = document.getElementById("result");
const predictionText = document.getElementById("predictionText");
const probabilityText = document.getElementById("probabilityText");
const thresholdText = document.getElementById("thresholdText");
const modelText = document.getElementById("modelText");
const errorMessage = document.getElementById("errorMessage");


// ========================================
// HELPER FUNCTIONS
// ========================================

function getValue(id) {
    return document.getElementById(id).value;
}

function getNumber(id) {
    return Number(getValue(id));
}

function getOptionalNumber(id) {
    const value = getValue(id).trim();
    return value === "" ? null : Number(value);
}

function getOptionalText(id) {
    const value = getValue(id).trim();
    return value === "" ? null : value;
}


// ========================================
// COLLECT FORM DATA
// ========================================

function collectBookingData() {

    return {
        hotel: getValue("hotel"),

        lead_time: getNumber("lead_time"),

        arrival_date_year: getNumber("arrival_date_year"),
        arrival_date_month: getValue("arrival_date_month"),
        arrival_date_week_number: getNumber("arrival_date_week_number"),
        arrival_date_day_of_month: getNumber("arrival_date_day_of_month"),

        stays_in_weekend_nights: getNumber("stays_in_weekend_nights"),
        stays_in_week_nights: getNumber("stays_in_week_nights"),

        adults: getNumber("adults"),
        children: getOptionalNumber("children") ?? 0,
        babies: getNumber("babies"),

        meal: getValue("meal"),
        country: getOptionalText("country"),

        market_segment: getValue("market_segment"),
        distribution_channel: getValue("distribution_channel"),

        is_repeated_guest: getNumber("is_repeated_guest"),

        previous_cancellations: getNumber("previous_cancellations"),
        previous_bookings_not_canceled: getNumber("previous_bookings_not_canceled"),

        reserved_room_type: getValue("reserved_room_type"),

        booking_changes: getNumber("booking_changes"),

        deposit_type: getValue("deposit_type"),

        agent: getOptionalNumber("agent"),
        company: getOptionalNumber("company"),

        days_in_waiting_list: getNumber("days_in_waiting_list"),

        customer_type: getValue("customer_type"),

        adr: getNumber("adr"),

        required_car_parking_spaces: getNumber("required_car_parking_spaces"),

        total_of_special_requests: getNumber("total_of_special_requests")
    };
}


// ========================================
// DISPLAY PREDICTION RESULT
// ========================================

function displayResult(data) {

    resultSection.classList.remove("hidden");
    errorMessage.classList.add("hidden");

    predictionText.textContent = "Prediction: " + data.result;

    probabilityText.textContent =
        "Cancellation Probability: " +
        Number(data.cancellation_probability).toFixed(2) + "%";

    thresholdText.textContent =
        "Model Threshold: " + data.threshold;

    modelText.textContent =
        "Model Used: " + data.model;

    resultSection.scrollIntoView({
        behavior: "smooth",
        block: "center"
    });
}


// ========================================
// DISPLAY ERROR
// ========================================

function displayError(message) {

    resultSection.classList.add("hidden");
    errorMessage.textContent = message;
    errorMessage.classList.remove("hidden");

    errorMessage.scrollIntoView({
        behavior: "smooth",
        block: "center"
    });
}


// ========================================
// SEND DATA TO FASTAPI BACKEND
// ========================================

bookingForm.addEventListener("submit", async function (event) {

    event.preventDefault();

    resultSection.classList.add("hidden");
    errorMessage.classList.add("hidden");

    if (API_URL.includes("YOUR-BACKEND-NAME")) {
        displayError("Please configure your Render backend URL in script.js.");
        return;
    }

    predictBtn.disabled = true;
    predictBtn.textContent = "Predicting...";

    try {

        const bookingData = collectBookingData();

        const response = await fetch(`${API_URL}/predict`, {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify(bookingData)

        });

        const data = await response.json();

        if (!response.ok) {

            const detail = data.detail;

            const message = Array.isArray(detail)
                ? detail.map(item => item.msg).join(", ")
                : (typeof detail === "string" ? detail : "Prediction request failed.");

            throw new Error(message);
        }

        displayResult(data);

    } catch (error) {

        console.error("Prediction Error:", error);

        displayError(
            error.message ||
            "Unable to connect to the backend. Please try again."
        );

    } finally {

        predictBtn.disabled = false;
        predictBtn.textContent = "Predict Cancellation";

    }

});


// ========================================
// RESET FORM AND RESULTS
// ========================================

bookingForm.addEventListener("reset", function () {

    resultSection.classList.add("hidden");
    errorMessage.classList.add("hidden");

});
