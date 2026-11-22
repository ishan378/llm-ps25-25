
import streamlit as st
import pandas as pd
import os
import json
from datetime import date
from dotenv import load_dotenv
from google import genai

# -------------------------------
# PAGE CONFIGURATION
# -------------------------------

st.set_page_config(
    page_title="Study Plan Generator",
    page_icon="📚",
    layout="wide"
)

# -------------------------------
# LOAD API KEY
# -------------------------------

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if api_key:
    client = genai.Client(api_key=api_key)
else:
    client = None

# -------------------------------
# SESSION STATE
# -------------------------------

if "timetable" not in st.session_state:
    st.session_state.timetable = None

if "days_left" not in st.session_state:
    st.session_state.days_left = None

if "total_hours" not in st.session_state:
    st.session_state.total_hours = None

# -------------------------------
# APPLICATION HEADER
# -------------------------------

st.title("📚 Study Plan Generator")

st.write(
    "Generate a personalized, day-wise exam study timetable "
    "using Artificial Intelligence."
)

st.divider()

# -------------------------------
# STUDENT INPUT FORM
# -------------------------------

st.header("Enter Your Details")

with st.form("study_plan_form"):

    subjects = st.text_input(
        "Enter your subjects (separated by commas)",
        placeholder="Java, Python, DBMS"
    )

    syllabus = st.text_area(
        "Enter your syllabus or important topics",
        placeholder="Java - Arrays, OOP, Loops, Collections"
    )

    col1, col2 = st.columns(2)

    with col1:
        exam_date = st.date_input(
            "Select your exam date",
            min_value=date.today()
        )

    with col2:
        hours = st.number_input(
            "Daily available study hours",
            min_value=1,
            max_value=15,
            value=4
        )

    generate = st.form_submit_button(
        "Generate Study Plan",
        use_container_width=True
    )

# -------------------------------
# GENERATE STUDY PLAN
# -------------------------------

if generate:

    today = date.today()
    days_left = (exam_date - today).days

    if not api_key:

        st.error("Gemini API key not found. Check your .env file.")

    elif not subjects.strip():

        st.warning("Please enter your subjects.")

    elif not syllabus.strip():

        st.warning("Please enter your syllabus.")

    elif days_left <= 0:

        st.error("Please select a future exam date.")

    else:

        prompt = f"""
        You are an expert exam study planner.

        Create a practical day-wise study timetable.

        Subjects: {subjects}
        Syllabus: {syllabus}
        Today's date: {today}
        Exam date: {exam_date}
        Days remaining: {days_left}
        Available study hours per day: {hours}

        Instructions:

        1. Create a timetable for every study day before the exam.
        2. Divide study hours between the subjects.
        3. Cover all provided syllabus topics.
        4. Include revision and practice questions.
        5. Give more time to difficult topics.
        6. Do not exceed the daily available study hours.
        7. Include practical activities for every session.
        8. Do not schedule study sessions on exam day.
        9. Use actual calendar dates.
        10. Return only valid JSON.

        Follow this exact structure:

        {{
            "timetable": [
                {{
                    "day": "Day 1",
                    "date": "2026-11-22",
                    "duration": "2 hours",
                    "subject": "JAVA",
                    "topic": "Loops",
                    "activities": "Practice loops and solve questions"
                }}
            ]
        }}

        Do not include Markdown code fences.
        """

        try:

            with st.spinner(
                "Gemini AI is preparing your personalized timetable..."
            ):

                response = client.interactions.create(
                    model="gemini-4-hydrogen",
                    input=prompt
                )

                result = json.loads(response.output_text)

                timetable = result["timetable"]

                if not timetable:
                    raise ValueError("The generated timetable is empty.")

                df = pd.DataFrame(timetable)

                required_columns = [
                    "day",
                    "date",
                    "duration",
                    "subject",
                    "topic",
                    "activities"
                ]

                if not all(
                    column in df.columns
                    for column in required_columns
                ):
                    raise ValueError(
                        "The generated timetable has missing columns."
                    )

                # Save results in Session State
                st.session_state.timetable = df
                st.session_state.days_left = days_left
                st.session_state.total_hours = days_left * hours

            st.success("Your study plan is ready!")

        except json.JSONDecodeError:

            st.error(
                "Gemini returned an invalid JSON response. Please try again."
            )

        except Exception as e:

            st.error(f"Something went wrong: {e}")

# -------------------------------
# DISPLAY SAVED STUDY PLAN
# -------------------------------

if st.session_state.timetable is not None:

    st.divider()

    st.success("Your study plan is ready!")

    st.header("Exam Countdown")

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Days Remaining",
            st.session_state.days_left
        )

    with col2:
        st.metric(
            "Total Available Study Hours",
            f"{st.session_state.total_hours} hours"
        )

    st.divider()

    st.header("Your Personalized Study Timetable")

    st.dataframe(
        st.session_state.timetable,
        use_container_width=True,
        hide_index=True
    )

    # -------------------------------
    # CSV DOWNLOAD
    # -------------------------------

    csv = st.session_state.timetable.to_csv(
        index=False
    ).encode("utf-8-sig")

    st.download_button(
        label="📥 Download Study Plan (CSV)",
        data=csv,
        file_name="study_plan.csv",
        mime="text/csv",
        use_container_width=True
    )

    st.caption(
        "Your generated timetable is saved during this Streamlit session."
    )

st.divider()

st.caption("Study Plan Generator | Powered by Python, Streamlit and Gemini AI")
