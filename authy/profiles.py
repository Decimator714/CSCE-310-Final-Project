import streamlit as st
import pymongo

# Connect to MongoDB
client = pymongo.MongoClient("mongodb+srv://richiekumar:Srirama10@csce-310.t0eeunr.mongodb.net/")
db = client["mydatabase"]
users = db["users"]

# Profile page for a student
def student_profile(user_email):
    user = users.find_one({"user_email": user_email})
    st.write(f"Hello {user['user_fname']} {user['user_lname']}, welcome to your profile page!")
    st.write("Here is your student information:")
    st.write(f"Grade: {user['student_grade']}")
    st.write(f"Major: {user['student_major']}")
    st.write(f"GPA: {user['student_gpa']}")

# Profile page for a tutor
def tutor_profile(user_email):
    user = users.find_one({"user_email": user_email})
    st.write(f"Hello {user['user_fname']} {user['user_lname']}, welcome to your profile page!")
    st.write("Here is your tutor information:")
    st.write(f"Availability: {user['tutor_avail']}")
    st.write(f"Subjects: {user['tutor_subjects']}")

# Profile page for an admin
def admin_profile(user_email):
    user = users.find_one({"user_email": user_email})
    st.write(f"Hello {user['user_fname']} {user['user_lname']}, welcome to your profile page!")
    st.write("Here is your admin information:")
    # Add admin-specific information here

# View profile based on user type
def view_profile(user_email):
    user = users.find_one({"user_email": user_email})
    if user["user_type"] == "Student":
        student_profile(user_email)
    elif user["user_type"] == "Tutor":
        tutor_profile(user_email)
    elif user["user_type"] == "Admin":
        admin_profile(user_email)
