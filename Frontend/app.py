import requests
import streamlit as st

BACKEND_URL = "http://127.0.0.1:8000/generate"
MAX_TOPIC_LENGTH = 300

EMPTY_TOPIC_MESSAGE = "Please enter a study topic. Empty topics are not allowed."
LONG_TOPIC_MESSAGE = "That topic is too long. Please enter a shorter study topic."
INVALID_TOPIC_MESSAGE = "Please enter a valid study topic."
BACKEND_UNAVAILABLE_MESSAGE = (
    "Could not connect to the study assistant. Make sure the FastAPI backend is running."
)
TIMEOUT_MESSAGE = "The request took too long. Please try again."
GEMINI_FAILURE_MESSAGE = (
    "The AI service is unavailable right now. Please try again in a moment."
)
UNEXPECTED_AI_MESSAGE = "The AI returned an unexpected response. Please try again."
GENERIC_FAILURE_MESSAGE = "Unable to generate study material. Please try again."


def is_complete_study_material(data: object) -> bool:
    if not isinstance(data, dict):
        return False
    explanation = data.get("explanation")
    key_points = data.get("key_points")
    quiz_questions = data.get("quiz_questions")
    if not isinstance(explanation, str) or not explanation.strip():
        return False
    if not isinstance(key_points, list) or len(key_points) != 3:
        return False
    if not isinstance(quiz_questions, list) or len(quiz_questions) != 2:
        return False
    if any(not isinstance(point, str) or not point.strip() for point in key_points):
        return False
    if any(
        not isinstance(question, str) or not question.strip()
        for question in quiz_questions
    ):
        return False
    return True


def error_message(response: requests.Response) -> str:
    if response.status_code in {500, 502, 503}:
        detail = _response_detail(response)
        if detail:
            return detail
        return GEMINI_FAILURE_MESSAGE

    if response.status_code == 422:
        detail = _response_detail(response)
        if detail:
            lowered = detail.lower()
            if "empty" in lowered:
                return EMPTY_TOPIC_MESSAGE
            if "too long" in lowered or "longer" in lowered:
                return LONG_TOPIC_MESSAGE
            return detail
        return INVALID_TOPIC_MESSAGE

    if response.status_code == 400:
        return INVALID_TOPIC_MESSAGE

    return GENERIC_FAILURE_MESSAGE


def _response_detail(response: requests.Response) -> str:
    try:
        payload = response.json()
    except requests.exceptions.JSONDecodeError:
        return ""

    if not isinstance(payload, dict):
        return ""

    detail = payload.get("detail")
    if isinstance(detail, str) and detail.strip():
        return detail.strip()
    if isinstance(detail, list) and detail:
        first_error = detail[0]
        if isinstance(first_error, dict):
            message = str(first_error.get("msg", "")).replace("Value error, ", "")
            return message.strip()
        if isinstance(first_error, str):
            return first_error.strip()
    return ""


st.set_page_config(page_title="AI Study Assistant")

st.title("AI Study Assistant")
st.write(
    "Enter a study topic to receive a short explanation, three key points, and two quiz questions."
)

topic = st.text_area("Study topic")

if st.button("Generate Study Material"):
    if not topic.strip():
        st.error(EMPTY_TOPIC_MESSAGE)
    elif len(topic.strip()) > MAX_TOPIC_LENGTH:
        st.error(LONG_TOPIC_MESSAGE)
    else:
        try:
            with st.spinner("Generating study material..."):
                response = requests.post(
                    BACKEND_URL,
                    json={"topic": topic.strip()},
                    timeout=60,
                )
        except requests.exceptions.ConnectionError:
            st.error(BACKEND_UNAVAILABLE_MESSAGE)
        except requests.exceptions.Timeout:
            st.error(TIMEOUT_MESSAGE)
        except requests.exceptions.RequestException:
            st.error(GENERIC_FAILURE_MESSAGE)
        else:
            if not response.ok:
                st.error(error_message(response))
            else:
                try:
                    data = response.json()
                except requests.exceptions.JSONDecodeError:
                    st.error(UNEXPECTED_AI_MESSAGE)
                else:
                    if not is_complete_study_material(data):
                        st.error(UNEXPECTED_AI_MESSAGE)
                    else:
                        st.subheader("Explanation")
                        st.write(data["explanation"])

                        st.subheader("Key Points")
                        for point in data["key_points"]:
                            st.write(f"- {point}")

                        st.subheader("Quiz Questions")
                        for question in data["quiz_questions"]:
                            st.write(f"- {question}")
