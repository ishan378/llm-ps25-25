
# Study Plan Generator

An AI-powered Study Plan Generator built using Python, Streamlit, and Google Gemini AI.

## Problem Statement

Students often struggle to plan their exam preparation effectively. This application generates a personalized day-wise study timetable based on subjects, syllabus, exam date, and available study hours.

## Features

- Enter multiple subjects.
- Add syllabus and important topics.
- Select examination date.
- Specify daily available study hours.
- Calculate remaining days using Python.
- Generate personalized study timetables using Gemini AI.
- Download the timetable as a CSV file.

## Technologies Used

- Python
- Streamlit
- Google Gemini API
- Pandas
- Python-dotenv

## Installation

1. Clone or download this repository.
2. Install the required libraries:

   pip install -r requirements.txt

3. Create a `.env` file in the project folder.

4. Add your Gemini API key:

   GEMINI_API_KEY=your_api_key_here

5. Run the application:

   streamlit run app.py

## Project Structure

StudyPlanGenerator/
- app.py
- test_gemini.py
- requirements.txt
- .gitignore
- .env

## Author

Ishan
