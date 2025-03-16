import streamlit as st
from database import create_user, check_login, log_food, get_food_log

# Streamlit Page Config
st.set_page_config(page_title="Calorie Counter", layout="centered")

# User Session State
if "username" not in st.session_state:
    st.session_state.username = None

# Show login/register only if user is NOT logged in
if st.session_state.username is None:
    st.title("Calorie Counter App")

    # Sidebar Navigation
    menu = ["Login", "Register"]
    choice = st.sidebar.selectbox("Menu", menu, key="menu_select")

    if choice == "Register":
        st.subheader("Create an Account")
        new_username = st.text_input("Username", key="reg_username")
        new_password = st.text_input("Password", type="password", key="reg_password")
        if st.button("Sign Up", key="signup_button"):
            if create_user(new_username, new_password):
                st.success("Account created successfully! Please log in.")
            else:
                st.error("Username already exists, please try a different one.")

    elif choice == "Login":
        st.subheader("Login to Your Account")
        username = st.text_input("Username", key="login_username")
        password = st.text_input("Password", type="password", key="login_password")
        if st.button("Login", key="login_button"):
            if check_login(username, password):
                st.session_state.username = username
                st.rerun()  # Reload to show the calorie tracker
            else:
                st.error("Invalid login credentials. Please try again.")

# Show calorie tracker only if user IS logged in
if st.session_state.username:
    st.sidebar.success(f"Logged in as: {st.session_state.username}")
    st.title(f"Welcome, {st.session_state.username}!")

    # Set Daily Goals
    st.subheader("Set Your Daily Goals")
    calories_goal = st.number_input("Max Calories", min_value=0, value=2000, key="calories_goal")
    protein_goal = st.number_input("Protein (g)", min_value=0, value=150, key="protein_goal")
    fats_goal = st.number_input("Fats (g)", min_value=0, value=70, key="fats_goal")
    fiber_goal = st.number_input("Fiber (g)", min_value=0, value=30, key="fiber_goal")

    # Food Logging Section
    st.subheader("Log Your Food Intake")
    food_name = st.text_input("Food Name", key="food_name")
    calories = st.number_input("Calories", min_value=0, value=0, key="food_calories")
    protein = st.number_input("Protein (g)", min_value=0, value=0, key="food_protein")
    fats = st.number_input("Fats (g)", min_value=0, value=0, key="food_fats")
    fiber = st.number_input("Fiber (g)", min_value=0, value=0, key="food_fiber")

    if st.button("Add Food", key="add_food_button"):
        log_food(st.session_state.username, food_name, calories, protein, fats, fiber)
        st.success(f"Added {food_name} to your food log!")
        st.rerun()  # Reload to update log

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

    # Logout Button
    if st.button("Logout", key="logout_button"):
        st.session_state.username = None
        st.rerun()
