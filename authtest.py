import streamlit as st
import pymongo
import hashlib
import os
from streamlit.components.v1 import html
import os

# Connect to MongoDB
client = pymongo.MongoClient("mongodb+srv://richiekumar:Srirama10@csce-310.t0eeunr.mongodb.net/")
db = client["mydatabase"]
users = db["users"]
tutors = db["tutors"]
students = db["students"]
admins = db["admins"]

# Define function to create a new user account
def create_account(user_fname, user_lname, user_email, user_password, user_type, **kwargs):
    # Get the largest user ID in the database or return 0 if there are no users
    largest_id = users.find_one(sort=[("user_id", pymongo.DESCENDING)]) or {"user_id": 0}
    user_id = largest_id.get("user_id", 0) + 1

    # Hash the password
    hashed_password = hashlib.sha256(user_password.encode()).hexdigest()

    # Create a new document to insert into the MongoDB collection
    document = {
        "user_id": user_id,
        "user_fname": user_fname.strip(),
        "user_lname": user_lname.strip(),
        "user_email": user_email.strip(),
        "user_password": hashed_password,
        "user_type": user_type,
        **kwargs
    }

    # Insert the document into the appropriate MongoDB collection based on the user type
    if user_type.lower() == "admin":
        admins.insert_one(document)
    elif user_type.lower() == "tutor":
        tutor_avail = kwargs.pop('tutor_avail', {})
        tutor_subjects = kwargs.pop('tutor_subjects', [])
        document["tutor_avail"] = tutor_avail
        document["tutor_subjects"] = tutor_subjects
        tutors.insert_one(document)
    elif user_type.lower() == "student":
        grade = kwargs.pop('student_grade', None)
        major = kwargs.pop('student_major', None)
        gpa = kwargs.pop('student_gpa', None)
        document["student_grade"] = grade
        document["student_major"] = major
        document["student_gpa"] = gpa
        students.insert_one(document)
    else:
        raise ValueError(f"Invalid user type: {user_type}")

    st.success(f"Account created for {user_email}!")




def authenticate(username, password):
    # Check if the user exists in any of the collections
    user = None
    for collection in [users, tutors, students, admins]:
        user = collection.find_one({"user_email": username})
        if user:
            break

    if user:
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        if user["user_password"] == hashed_password:
            os.environ["USER_EMAIL"] = username
            return True, user["user_type"]


    print(f"Invalid email or password: {username} {password}")
    return False, None


def main():
    st.set_page_config(page_title="Aggie Scheduler")

    st.title("Aggie Scheduler")

    # Create a sidebar with options to login or create a new account
    menu = ["Login", "Create Account"]
    choice = st.sidebar.selectbox("Select an option", menu)

    # Show the login form if the user selects "Login"
    if choice == "Login":
        st.subheader("Login")
        user_email = st.text_input("Email")
        user_password = st.text_input("Password", type="password")
        if st.button("Login"):
            auth_success, user_type = authenticate(user_email, user_password)
            if auth_success:
                # Set the user_email environment variable
                
                st.success("Logged in!")
                os.environ['USER_EMAIL'] = user_email
                redirect_button = '''
                <script>
                    window.open("http://localhost:8502/", "_blank");
                </script>
            '''
                st.components.v1.html(redirect_button)
            else:
                st.error("Invalid email or password")

    # Show the create account form if the user selects "Create Account"
    elif choice == "Create Account":
        st.subheader("Create a New Account")
        user_fname = st.text_input("First Name")
        user_lname = st.text_input("Last Name")
        user_email = st.text_input("Email")
        user_password = st.text_input("Password", type="password")
        user_type = st.selectbox("Select a user type", ["Student", "Tutor", "Admin"])
        if user_type == "Tutor":
            st.write("Please select the days and hours that you are available below. When you click an hour, you will then be prompted to click another hour. This will allow you to create intervals when you are free to tutor.")
            tutor_avail = st.multiselect("Availability", ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])
            tutor_avail_times = {}
            for day in tutor_avail:
                times = st.multiselect(f"Available times for {day}", ["9:00", "10:00", "11:00", "12:00", "1:00", "2:00", "3:00", "4:00", "5:00", "6:00", "7:00", "8:00"])
                tutor_avail_times[day] = times
            tutor_subjects = st.selectbox("Subjects", ['ECEN', 'CSCE'])
            if st.button("Create Account"):
                create_account(user_fname, user_lname, user_email, user_password, user_type, tutor_avail=tutor_avail_times, tutor_subjects=tutor_subjects)

        elif user_type == "Student":
            student_grade = st.selectbox("Grade", ['9', '10', '11', '12'])
            student_major = st.selectbox("Major", ['ECEN', 'CSCE'])
            student_gpa = st.text_input("GPA")
            if st.button("Create Account"):
                create_account(user_fname, user_lname, user_email, user_password, user_type, student_grade=student_grade, student_major=student_major, student_gpa=student_gpa)
        elif user_type == "Admin":
            admin_info = st.text_input("Admin Information")
            if st.button("Create Account"):
                create_account(user_fname, user_lname, user_email, user_password, user_type, admin_info=admin_info)
        
if __name__ == "__main__":
    main()
