# AI Study Assistant

## 1. Problem Statement

Students often need a quick and simple way to understand a topic and test their knowledge. The AI Study Assistant provides a simple interface where a student enters a study topic and receives an AI-generated explanation, key points, and quiz questions.

## 2. Target User

The primary users are students who want quick assistance while studying.

## 3. MVP Scope

The application will provide exactly three core features:

1. Generate a short explanation of a study topic.
2. Generate three important key points about the topic.
3. Generate two quiz questions about the topic.

The application will not include login, database storage, file uploads, chat history, or other additional features.

## 4. Technology Stack

* Python
* FastAPI
* Streamlit
* Google GenAI
* Pydantic
* python-dotenv
* requests
* Git/GitHub

## 5. Application Flow

1. User enters a study topic.
2. Streamlit sends the topic to the FastAPI backend.
3. FastAPI validates the input.
4. FastAPI sends an appropriate prompt to the Google Gemini model.
5. Gemini generates the study content.
6. FastAPI returns the result.
7. Streamlit displays the explanation, key points, and quiz questions.

## 6. Environment Setup

The Gemini API key will be stored in an environment variable.

Required variable:

`GEMINI_API_KEY`

The `.env` file must not be committed to GitHub.

## 7. Validation

The application should reject empty topics and provide a clear error message.

## 8. Error Handling

The application should display a user-friendly message if the AI API fails or an invalid request is submitted.

## 9. Success Criteria

The project will be considered successful when a user can:

* Enter a study topic.
* Generate AI study material.
* View a short explanation.
* View three key points.
* View two quiz questions.
* Receive a clear error message for empty input.
