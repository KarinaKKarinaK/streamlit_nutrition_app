import streamlit as st
from database import create_user, check_login, log_food, get_food_log

# Streamlit Page Config
st.set_page_config(page_title="Calorie Counter", layout="centered")

# Login or Register Section
st.title("Calorie Counter App")

#Adding a comment

# Sidebar Navigation
menu = ["Login", "Register"]
choice = st.sidebar.selectbox("Menu", menu)

# User Session
if "username" not in st.session_state:
    st.session_state.username = None

# Registration Page
if choice == "Register":
    st.subheader("Create an Account")
    new_username = st.text_input("Username")
    new_password = st.text_input("Password", type="password")
    if st.button("Sign Up"):
        if create_user(new_username, new_password):
            st.success("Account created successfully! Please log in.")
        else:
            st.error("Username already exists, try a different one.")

# Login Page
elif choice == "Login":
    st.subheader("Login to Your Account")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if check_login(username, password):
            st.session_state.username = username
            st.success(f"Welcome, {username}!")
        else:
            st.error("Invalid login credentials.")

# If user is logged in, show calorie tracker
if st.session_state.username:
    st.sidebar.success(f"Logged in as: {st.session_state.username}")

    # Set Daily Goals
    st.subheader("Set Your Daily Goals")
    calories_goal = st.number_input("Max Calories", min_value=0, value=2000)
    protein_goal = st.number_input("Protein (g)", min_value=0, value=150)
    fats_goal = st.number_input("Fats (g)", min_value=0, value=70)
    fiber_goal = st.number_input("Fiber (g)", min_value=0, value=30)

    # Food Logging Section
    st.subheader("Log Your Food Intake")
    food_name = st.text_input("Food Name")
    calories = st.number_input("Calories", min_value=0, value=0)
    protein = st.number_input("Protein (g)", min_value=0, value=0)
    fats = st.number_input("Fats (g)", min_value=0, value=0)
    fiber = st.number_input("Fiber (g)", min_value=0, value=0)

    if st.button("Add Food"):
        log_food(st.session_state.username, food_name, calories, protein, fats, fiber)
        st.success(f"Added {food_name} to your food log!")

    # Display Logged Food
    st.subheader("Today's Food Log")
    food_log = get_food_log(st.session_state.username)
    
    total_calories = sum(item[1] for item in food_log)
    total_protein = sum(item[2] for item in food_log)
    total_fats = sum(item[3] for item in food_log)
    total_fiber = sum(item[4] for item in food_log)

    st.write("### Summary of Intake")
    st.write(f"Total Calories: {total_calories} / {calories_goal}")
    st.write(f"Total Protein: {total_protein}g / {protein_goal}g")
    st.write(f"Total Fats: {total_fats}g / {fats_goal}g")
    st.write(f"Total Fiber: {total_fiber}g / {fiber_goal}g")

    st.write("### Food Log")
    for food in food_log:
        st.write(f"- {food[0]}: {food[1]} kcal, {food[2]}g protein, {food[3]}g fats, {food[4]}g fiber")

    # Logout Option
    if st.button("Logout"):
        st.session_state.username = None
        st.experimental_rerun()
