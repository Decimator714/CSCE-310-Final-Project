import os
import pymongo
import streamlit as st

# Connect to MongoDB
client = pymongo.MongoClient("mongodb+srv://richiekumar:Srirama10@csce-310.t0eeunr.mongodb.net/")
db = client["mydatabase"]
users = db["users"]
tutors = db["tutors"]
students = db["students"]
admins = db["admins"]

def main():
    st.set_page_config(page_title="Aggie Scheduler")
    st.sidebar.title("Navigation")
    pages = ["Profile", "Calendar", "File Storage"]
    selection = st.sidebar.radio("Go to", pages)
    # Get user email from environment variable
    user_email = os.environ.get('USER_EMAIL')

    print(os.environ.get('USER_EMAIL'))
    if selection == "Profile":
        show_profile_page(user_email)
    elif selection == "Calendar":
        show_calendar_page()
    elif selection == "File Storage":
        show_file_storage_page()

def show_profile_page(user_email):
    st.title("Profile Page")
    
    if user_email:
        st.subheader(f"User: {user_email}")
        
        # Retrieve the user document from MongoDB
        user_doc = users.find_one({"user_email": user_email})
        if user_doc:
            # Display user information
            st.write(f"First Name: {user_doc.get('user_fname', '')}")
            st.write(f"Last Name: {user_doc.get('user_lname', '')}")
            st.write(f"Email: {user_doc.get('user_email', '')}")
            st.write(f"User Type: {user_doc.get('user_type', '')}")
            
            # Display additional fields based on user type
            user_type = user_doc.get('user_type', '').lower()
            if user_type == 'Tutor':
                st.write(f"Availability: {user_doc.get('tutor_available', '')}")
                st.write(f"Subjects: {user_doc.get('tutor_subjects', '')}")
            elif user_type == 'Student':
                st.write(f"Grade: {user_doc.get('student_grade', '')}")
                st.write(f"Major: {user_doc.get('student_major', '')}")
                st.write(f"GPA: {user_doc.get('student_gpa', '')}")
        else:
            st.write(f"No user found with email {user_email}")
    else:
        st.write("User email not found in environment variable")

def show_calendar_page():
    st.title("Calendar Page")
    # Add your calendar page content here

def show_file_storage_page():
    st.title("File Storage Page")
    # Add your file storage page content here

if __name__ == "__main__":
    main()
