
import requests
import streamlit as st

API_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="Banking Customer Intelligence",
    page_icon="🏦",
    layout="wide"
)

st.title("🏦 Banking Customer Intelligence")
st.write(
    "Analyze banking customer messages, predict their intent, "
    "and get answers supported by official sources."
)

st.info(
    "This is a portfolio demonstration, not an official banking service. "
    "Do not enter account numbers, passwords, PINs, or OTPs."
)

try:
    health_response = requests.get(
        f"{API_URL}/health",
        timeout=3
    )
    api_available = health_response.status_code == 200
except requests.RequestException:
    api_available = False

if api_available:
    st.success("API connected")
else:
    st.error(
        "API is unavailable. Start the FastAPI server in another terminal."
    )

intent_tab, answer_tab = st.tabs(
    ["Intent Prediction", "Banking Q&A"]
)

with intent_tab:
    st.subheader("Customer Intent Prediction")
    st.write("Enter a customer message to predict its Banking77 intent.")

    customer_message = st.text_area(
        "Customer message",
        placeholder="Example: I want to check my bank balance",
        key="customer_message"
    )

    if st.button("Predict Intent", disabled=not api_available):
        if not customer_message.strip():
            st.warning("Please enter a customer message.")
        else:
            try:
                response = requests.post(
                    f"{API_URL}/predict-intent",
                    json={"text": customer_message},
                    timeout=30
                )

                if response.ok:
                    result = response.json()
                    st.success("Prediction completed")
                    st.write("**Predicted intent:**")
                    st.code(result["intent"])
                    st.caption(
                        "The prediction is a model output and may be incorrect."
                    )
                else:
                    st.error(f"API error: {response.text}")

            except requests.RequestException as error:
                st.error(f"Could not reach the API: {error}")

with answer_tab:
    st.subheader("Evidence-Based Banking Q&A")
    st.write(
        "Ask a banking question and review the answer and its supporting sources."
    )

    banking_question = st.text_area(
        "Your question",
        placeholder="Example: What should I do if my payment card is lost?",
        key="banking_question"
    )

    if st.button("Get Answer", disabled=not api_available):
        if not banking_question.strip():
            st.warning("Please enter a question.")
        else:
            try:
                response = requests.post(
                    f"{API_URL}/ask",
                    json={"question": banking_question},
                    timeout=180
                )

                if response.ok:
                    result = response.json()

                    if result["status"] == "answered":
                        st.success("Answer found")
                    else:
                        st.warning(
                            "The knowledge base did not provide enough evidence."
                        )

                    st.write("### Answer")
                    st.write(result["answer"])

                    st.write("### Supporting sources")

                    if result["sources"]:
                        for source in result["sources"]:
                            with st.expander(source["title"]):
                                st.write(f"**Publisher:** {source['publisher']}")
                                st.write(
                                    f"**Similarity:** {source['similarity']:.3f}"
                                )
                                st.markdown(
                                    f"[Open source]({source['url']})"
                                )
                    else:
                        st.write("No supporting sources were retrieved.")

                else:
                    st.error(f"API error: {response.text}")

            except requests.RequestException as error:
                st.error(f"Could not reach the API: {error}")
