import streamlit as st
import pymongo
import bcrypt
import hashlib

import profiles
from profiles import student_profile
from profiles import admin_profile
from profiles import tutor_profile
from profiles import view_profile

# Connect to the MongoDB server
client = pymongo.MongoClient("mongodb+srv://richiekumar:Srirama10@csce-310.t0eeunr.mongodb.net/")
db = client["mydatabase"]
users = db["users"]
tutors = db["tutors"]
admins = db["admins"]
students = db["students"]

# Define the session state
if "login_state" not in st.session_state:
    st.session_state.login_state = {}

# Define the login function
def login():
    st.write("## Login")

    # Get the user's details
    user_email = st.text_input("Email")
    user_password = st.text_input("Password", type="password")

    # Check if the user exists
    user = users.find_one({"user_email": user_email})
    if not user:
        st.warning("A user with that email address does not exist.")
        return

    # Check if the password is correct
    hashed_password = hashlib.sha256(user_password.encode()).hexdigest()
    if user["user_password"] != hashed_password:
        st.warning("Incorrect password.")
        return

    # Log in the user and store their details in session state
    st.session_state.login_state["user_id"] = user["_id"]
    st.session_state.login_state["user_email"] = user["user_email"]
    st.session_state.login_state["user_type"] = user["user_type"]

    # Redirect to the user's profile
    st.experimental_set_query_params(page="profile")

def signup():
    st.write("## Sign Up")

    # Initialize the user dictionary
    user = {}

    # Get the user's details
    user["user_fname"] = st.text_input("First Name")
    user["user_lname"] = st.text_input("Last Name")
    user["user_email"] = st.text_input("Email")
    user["user_password"] = st.text_input("Password", type="password")
    user["user_type"] = st.selectbox("User Type", ["Admin", "Tutor", "Student"])

    # Hash the user's password
    hashed_password = hashlib.sha256(user["user_password"].encode()).hexdigest()

    # Check if the user already exists
    if users.find_one({"user_email": user["user_email"]}):
        st.warning("A user with that email address already exists.")
        return

    # Add additional user attributes based on the user type
    if user["user_type"] == "Admin":
        user["admin_attribute"] = st.text_input("Admin Attribute")
    elif user["user_type"] == "Tutor":
        user["tutor_avail"] = st.text_input("Tutor Availability")
        user["tutor_subjects"] = st.text_input("Tutor Subjects")
    elif user["user_type"] == "Student":
        user["student_grade"] = st.text_input("Student Grade")
        user["student_major"] = st.text_input("Student Major")
        user["student_gpa"] = st.text_input("Student GPA")

    # Set the user's hashed password and insert them into the database
    user["user_password"] = hashed_password
    users.insert_one(user)

    # Show a success message and the login button
    st.success("You have successfully signed up.")
    if st.button("Log In"):
        login()

def main():
    # Set the page configuration
    st.set_page_config(page_title="Aggie Organizer", page_icon=":guardsman:")

    # Set the page style using CSS
    st.markdown(
        """
        <style>
        body {
            text-align: center;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Add a button to go back to login page
    if st.button("Back to Login", key="back_to_login"):
        login()

    # Display the appropriate page based on the query parameter
    page = st.experimental_get_query_params().get("page", ["login"])[0]
    if page == "signup_login":
        signup()
    elif page == "login":
        st.title("Login")
        user_email = st.text_input("Email")
        user_password = st.text_input("Password", type="password")
        if st.button("Log In"):
            user = login_user(user_email, user_password)
            if user:
                st.success("You have successfully logged in.")
                display_profile(user)
            else:
                st.warning("Incorrect email or password.")
        if st.button("Sign Up"):
            st.experimental_set_query_params(page="signup_login")
    elif page == "profile":
        view_profile()

def login_user(user_email, user_password):
    # Check if the user exists
    user = users.find_one({"user_email": user_email})
    if not user:
        return None

    # Check if the password is correct
    hashed_password = hashlib.sha256(user_password.encode()).hexdigest()
    if user["user_password"] != hashed_password:
        return None

    return user

def display_profile(user):
    if user["user_type"] == "Admin":
        admin_profile(user["user_email"])
    elif user["user_type"] == "Tutor":
        tutor_profile(user["user_email"])
    elif user["user_type"] == "Student":
        student_profile(user["user_email"])

def view_profile():
    user_email = st.text_input("Enter your email address:")
    if st.button("View Profile"):
        user = users.find_one({"user_email": user_email})
        if user:
            display_profile(user)
        else:
            st.warning("A user with that email address does not exist.")



if __name__ == "__main__":
    main()


