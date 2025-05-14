import streamlit as st
import pandas as pd
import datetime
from datetime import timedelta

# Function to calculate BMR using the Mifflin-St Jeor equation
def calculate_bmr(weight, height, age, gender):
    weight_kg = weight * 0.453592
    height_cm = height * 2.54
    if gender == "Male":
        s = 5
    else:
        s = -161
    return 10 * weight_kg + 6.25 * height_cm - 5 * age + s

# Function to get activity multiplier based on activity level
def get_activity_multiplier(level):
    return {
        "Sedentary": 1.2,
        "Lightly Active": 1.375,
        "Moderately Active": 1.55,
        "Very Active": 1.725,
        "Super Active": 1.9
    }[level]

# Function to convert pace (mm:ss) to seconds
def pace_to_seconds(pace_str):
    mins, secs = map(int, pace_str.split(":"))
    return mins * 60 + secs

# Function to convert seconds back to pace (mm:ss)
def seconds_to_pace(seconds):
    mins = seconds // 60
    secs = seconds % 60
    return f"{int(mins)}:{int(secs):02d}"

# Function to generate a realistic marathon training plan
def generate_training_plan(start_date, marathon_date, start_pace, goal_pace):
    days = (marathon_date - start_date).days + 1
    plan = []
    start_sec = pace_to_seconds(start_pace)
    goal_sec = pace_to_seconds(goal_pace)

    # Define long run details and taper periods
    long_run_distance = 8  # Initial long run distance in miles
    max_long_run_distance = 20  # Maximum long run distance
    taper_weeks = 3  # Weeks of tapering before race day
    max_peak_weeks = 12  # Weeks to peak the long runs

    # Determine number of weeks based on input dates
    total_weeks = (marathon_date - start_date).days // 7
    long_run_weeks = min(max_peak_weeks, total_weeks - taper_weeks)

    for week in range(total_weeks):
        for day in range(7):
            current_date = start_date + timedelta(days=week * 7 + day)
            day_of_week = current_date.strftime("%A")
            run_type, miles, pace_sec = None, 0, None

            if day_of_week == "Sunday":  # Long run day
                run_type = "Long Run"
                if week < long_run_weeks:  # Increase long runs until reaching max distance
                    miles = min(long_run_distance + 2 * week, max_long_run_distance)
                else:  # Taper period: Reduce mileage
                    miles = max(10, long_run_distance + 2 * (long_run_weeks - week))

                pace_sec = goal_sec + 90  # Long run pace (slower than marathon pace)
            elif day_of_week == "Saturday":  # Short run day (or cross-training)
                run_type = "Short Run"
                miles = 4  # Short recovery run or cross-training
                pace_sec = goal_sec + 60  # Slower than marathon pace
            elif day_of_week == "Wednesday":  # Medium-long run day
                run_type = "Medium-Long Run"
                miles = 7  # Typical mid-week long run distance
                pace_sec = goal_sec + 30  # Slightly slower than marathon pace
            elif day_of_week == "Tuesday":  # Tempo run day
                run_type = "Tempo Run"
                miles = 5  # Moderate tempo distance
                pace_sec = goal_sec - 20  # Faster than marathon pace
            elif day_of_week == "Thursday":  # Easy run day
                run_type = "Easy Run"
                miles = 4  # Easy recovery run
                pace_sec = goal_sec + 45  # Slower than marathon pace for recovery
            elif day_of_week == "Monday" or day_of_week == "Friday":  # Rest day
                run_type = "Rest"
                miles = 0
                pace_sec = None

            plan.append({
                "Date": current_date.strftime("%Y-%m-%d"),
                "Day": day_of_week,
                "Run Type": run_type,
                "Miles": round(miles, 1),
                "Pace": seconds_to_pace(pace_sec) if pace_sec else "–",
            })

    return plan

# Streamlit app main function
def main():
    st.title("🏃‍♀️ Marathon Training Plan Generator")

    with st.form("training_form"):
        start_date = st.date_input("Start Date")
        marathon_date = st.date_input("Marathon Date")
        height = st.number_input("Height (inches)", min_value=48.0, max_value=84.0)
        weight = st.number_input("Current Weight (lbs)", min_value=80.0)
        goal_weight = st.number_input("Goal Weight (lbs)", min_value=80.0)
        age = st.number_input("Age", min_value=10, max_value=100)
        gender = st.selectbox("Gender", ["Male", "Female"])
        start_pace = st.text_input("Current Average Pace (mm:ss)", "9:00")
        goal_pace = st.text_input("Goal Marathon Pace (mm:ss)", "8:30")
        activity = st.selectbox("Activity Level", ["Sedentary", "Lightly Active", "Moderately Active", "Very Active", "Super Active"])

        submitted = st.form_submit_button("Generate Plan")

    if submitted:
        # Generate the training plan
        plan = generate_training_plan(start_date, marathon_date, start_pace, goal_pace)

        # Calculate BMR and TDEE for calorie calculation
        total_days = (marathon_date - start_date).days + 1
        total_weight_loss = weight - goal_weight
        lbs_per_day = total_weight_loss / total_days
        cal_deficit = lbs_per_day * 3500

        bmr = calculate_bmr(weight, height, age, gender)
        activity_multiplier = get_activity_multiplier(activity)

        # Create a DataFrame to display the plan
        df = pd.DataFrame(plan)
        daily_cals = []

        for i in range(len(df)):
            weight_today = weight - (i * lbs_per_day)
            bmr_today = calculate_bmr(weight_today, height, age, gender)
            tdee_today = bmr_today * activity_multiplier
            calories = round(tdee_today - cal_deficit)
            daily_cals.append(calories)

        df["Calories"] = daily_cals

        # Display the plan
        st.subheader("📅 Your Training Plan")
        st.dataframe(df, use_container_width=True)

        # Add export functionality
        export_option = st.selectbox("Export Plan as", ["None", "CSV", "Excel"])

        if export_option == "CSV":
            csv = df.to_csv(index=False)
            st.download_button("Download CSV", csv, "training_plan.csv", "text/csv")
        elif export_option == "Excel":
            excel = df.to_excel(index=False)
            st.download_button("Download Excel", excel, "training_plan.xlsx", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

if __name__ == "__main__":
    main()
