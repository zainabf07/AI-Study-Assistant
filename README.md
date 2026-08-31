# AI Study Assistant

[![Python](https://img.shields.io/badge/Python-3.13-blue?logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-Frontend-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Google Gemini](https://img.shields.io/badge/Google-Gemini%20AI-4285F4?logo=google&logoColor=white)](https://ai.google.dev/)
[![Pydantic](https://img.shields.io/badge/Pydantic-Validation-E92063)](https://docs.pydantic.dev/)
[![GitHub](https://img.shields.io/badge/GitHub-Repository-181717?logo=github&logoColor=white)](https://github.com/)

> An AI-powered study assistant that generates explanations, key points, and quiz questions for students.

## 📚 Project Description

AI Study Assistant is a simple AI-powered learning application that helps students quickly understand a study topic and test their knowledge.

The user enters a study topic, and the application uses Google Gemini AI to generate:

- A short explanation
- Three important key points
- Two quiz questions

The project demonstrates AI-assisted software development using FastAPI, Streamlit, Google Gemini, Pydantic, and Python.

---

## 🎯 Objectives

The main objectives of this project are to:

- Provide students with quick and simple study material.
- Use Generative AI to explain educational topics.
- Generate key points for easy revision.
- Generate quiz questions for self-assessment.
- Demonstrate an AI-powered full-stack application.

---

## ✨ Features

### 1. Short Explanation
Generates a simple explanation of the selected study topic.

### 2. Key Points
Generates exactly three important points about the topic.

### 3. Quiz Questions
Generates exactly two questions to help students test their understanding.

### 4. Input Validation
The application handles empty or invalid topic inputs.

### 5. Error Handling
The application displays user-friendly messages when the AI service or backend is unavailable.

---

## 🏗️ Application Architecture

```text
              ┌─────────────────────┐
              │       Student       │
              └──────────┬──────────┘
                         │
                         ▼
              ┌─────────────────────┐
              │     Streamlit       │
              │     Frontend        │
              └──────────┬──────────┘
                         │
                      HTTP Request
                         │
                         ▼
              ┌─────────────────────┐
              │       FastAPI       │
              │       Backend       │
              └──────────┬──────────┘
                         │
                       Prompt
                         │
                         ▼
              ┌─────────────────────┐
              │    Google Gemini    │
              │       AI            │
              └──────────┬──────────┘
                         │
                    AI Response
                         │
                         ▼
              ┌─────────────────────┐
              │     Streamlit       │
              │   Display Results   │
              └─────────────────────┘
