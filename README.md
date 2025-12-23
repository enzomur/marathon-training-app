# marathon-training-app

Marathon Training Plan Generator
A Streamlit web app that creates a personalized marathon training plan based on your current fitness level, goals, and timeline. It also calculates your daily calorie targets based on your activity level, weight goals, and Basal Metabolic Rate (BMR).

Features
Generate a day-by-day marathon training plan

Supports personalized inputs:

Current and goal weight

Current and target running pace

Activity level

Start and marathon dates

Calculates:

BMR using the Mifflin-St Jeor equation

TDEE (Total Daily Energy Expenditure)

Daily calorie targets to support gradual weight loss

Export training plan as CSV or Excel

How It Works
Training Plan

Custom weekly schedule with long runs, tempo runs, easy runs, rest days, and tapering

Training adapts to your input dates and paces

Calories Calculation

Uses your weight, height, age, gender, and activity level to estimate daily caloric needs

Includes a calculated deficit based on your goal weight and timeline

Tech Stack
Python
Streamlit
Pandas

Installation
Clone the repository:
git clone https://github.com/your-username/your-repo-name.git

cd your-repo-name

Create and activate a virtual environment:
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

Install dependencies:
pip install -r requirements.txt

Run the app:
streamlit run app.py

Project Structure
├── app.py              # Streamlit app source code
├── requirements.txt    # Python dependencies
└── README.md           # Project documentation

To Do
Add user authentication
Add more export formats (PDF)
Enable dynamic pace adjustment based on progress
Add running phase
Updates to recommended running routines and daily calorie intake

License
This project is open-source under the MIT License.

