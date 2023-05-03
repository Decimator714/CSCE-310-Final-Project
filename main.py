# This code connects to a MySQL database and defines a main function for a Streamlit app called "Aggie Scheduler". 
# The app displays a navigation sidebar with three pages: "Profile", "Calendar", and "File Storage". 
# When the user selects a page, the app calls the appropriate function to display the content. 
# The "Profile" page allows users to view and edit their personal information, including additional fields based on their user type. 
# The "Calendar" and "File Storage" pages do not currently have any content.

# RISHABH KUMAR: 10 - 149

# Import necessary libraries
import os
import mysql.connector
import streamlit as st
import pandas as pd
from datetime import datetime

# Connect to MySQL database
cnx = mysql.connector.connect(user='root', password='', host='localhost', database='csce310')
cursor = cnx.cursor()

# Define main function for the Streamlit app
def main():
    # Set the page configuration for the app
    st.set_page_config(page_title="Aggie Scheduler")
    # Create the navigation sidebar with the available pages
    st.sidebar.title("Navigation")
    pages = ["Profile", "Calendar", "File Storage"]
    selection = st.sidebar.radio("Go to", pages)
    # Get the current user's ID from the currentUser table in the database
    cursor.execute("SELECT current_id FROM currentUser")
    result = cursor.fetchone()
    if result:
        user_id = result[0]
    else:
        user_id = None
    # Based on the selected page, call the appropriate function to display the content
    if selection == "Profile":
        show_profile_page(user_id)
    elif selection == "Calendar":
        show_calendar_page()
    elif selection == "File Storage":
        show_file_storage_page(user_id)

# Displaying profile page information    
def show_profile_page(user_id):  
    if user_id:
        # Add signout button
        if st.button('Sign Out', key='signout'):
                st.success("Logged out!")
                redirect_button = '''
                <script>
                    window.open("http://localhost:8501/", "_blank");
                </script>
                '''
                st.components.v1.html(redirect_button)
        # Retrieve the user document from MySQL
        cursor.execute("SELECT * FROM user WHERE user_id=%s", (user_id,))
        user_doc = cursor.fetchone()
        if user_doc:
            st.title(f"{user_doc[1]} {user_doc[2]}")
            st.markdown("<style>body {background-color: #000000;}</style>", unsafe_allow_html=True)
            # Display user information
            st.subheader("Personal Information")
            col1, col2 = st.columns([1, 2])
            with col1:
                first_name = st.text_input("First Name", user_doc[1], key="first_name")
                email = st.text_input("Email", user_doc[3], key="email")
            with col2:
                last_name = st.text_input("Last Name", user_doc[2], key="last_name")
                user_type = st.text_input("User Type", user_doc[5], key="user_type")
            # Display additional fields based on user type
            if user_type == 'TUTOR':
                st.subheader("Additional Information")
                # Retrieve the tutor document from MySQL based on the user_id
                cursor.execute("SELECT * FROM tutor WHERE user_id=%s", (user_id,))
                tutor_doc = cursor.fetchone()
                if tutor_doc:
                    tutor_avail = eval(tutor_doc[2])
                    tutor_subjects = tutor_doc[3]
                    st.write("Availability")
                    days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
                    selected_days = [day for day in days_of_week if day in tutor_avail]
                    new_days = st.multiselect("Add new availability days", list(set(days_of_week) - set(selected_days)))
                    del_days = st.multiselect("Remove availability days", selected_days)
                    for day in new_days:
                        tutor_avail[day] = []
                    for day in del_days:
                        del tutor_avail[day]
                    for day in tutor_avail:
                        tutor_avail[day] = st.multiselect(f"{day} Available Times", ["9:00", "10:00", "11:00", "12:00", "1:00", "2:00", "3:00", "4:00", "5:00", "6:00", "7:00", "8:00"], default=tutor_avail[day])
                    tutor_subjects = st.selectbox("Subjects", ['ECEN', 'CSCE'], index=['ECEN', 'CSCE'].index(tutor_subjects))
                    
                    # Save button to update information in the SQL DB
                    if st.button("Update Profile", key = "a"):
                        cursor.execute("UPDATE user SET user_fname=%s, user_lname=%s, user_email=%s WHERE user_id=%s", (first_name, last_name, email, user_id))
                        cursor.execute("UPDATE tutor SET tutor_avail=%s, tutor_subjects=%s WHERE user_id=%s", (str(tutor_avail), tutor_subjects, user_id))
                        cnx.commit()
                    
                    # Delete button to delete user from the SQL DB
                    if st.button("Delete Account", key ="x"):
                        cursor.execute("DELETE FROM tutor WHERE user_id=%s", (user_id,))
                        cursor.execute("DELETE FROM user WHERE user_id=%s", (user_id,))
                        cnx.commit()
                else:
                    st.write(f"No tutor found for user with id {user_id}")
            elif user_type == 'STUDENT':
                st.subheader("Additional Information")
                # Retrieve the student document from MySQL based on the user_id
                cursor.execute("SELECT * FROM student WHERE user_id=%s", (user_id,))
                student_doc = cursor.fetchone()
                if student_doc:
                    grade = st.selectbox("Grade", ['9', '10', '11', '12'], index=['9', '10', '11', '12'].index(str(student_doc[2])), key="grade")
                    major = st.selectbox("Major", ['ECEN', 'CSCE'], index=['ECEN', 'CSCE'].index(student_doc[3]), key="major")
                    gpa = st.text_input("GPA", student_doc[4], key="gpa")
                    # Save button to update information in the SQL DB
                    if st.button("Update Profile", key = "b"):
                        cursor.execute("UPDATE user SET user_fname=%s, user_lname=%s, user_email=%s WHERE user_id=%s", (first_name, last_name, email, user_id))
                        cursor.execute("UPDATE student SET student_grade=%s, student_major=%s, student_gpa=%s WHERE user_id=%s", (grade, major, gpa, user_id))
                        cnx.commit()

                    # Delete button to delete user from the SQL DB
                    if st.button("Delete Account", key ="y"):
                        cursor.execute("DELETE FROM student WHERE user_id=%s", (user_id,))
                        cursor.execute("DELETE FROM user WHERE user_id=%s", (user_id,))
                        cnx.commit()       
                else:
                    st.write(f"No student found for user with id {user_id}")
            elif user_type == 'ADMIN':
                st.subheader("Additional Information")
                # Retrieve the admin document from MySQL based on the user_id
                cursor.execute("SELECT * FROM admin WHERE user_id=%s", (user_id,))
                admin_doc = cursor.fetchone()
                if admin_doc:
                    admin_info = st.selectbox("Title", ['Professor', 'Counselor'], index=['Professor', 'Counselor'].index(admin_doc[2]), key="major")
                    # Save button to update information in the SQL DB
                    if st.button("Update Profile", key = "c"):
                        cursor.execute("UPDATE user SET user_fname=%s, user_lname=%s, user_email=%s WHERE user_id=%s", (first_name, last_name, email, user_id))
                        # Update admin information in the ADMIN table
                        cursor.execute("UPDATE ADMIN SET ADMIN_INFO=%s WHERE USER_ID=%s", (admin_info, user_id))
                        cnx.commit()

                    # Delete button to delete user from the SQL DB
                    if st.button("Delete Account", key ="y"):
                        cursor.execute("DELETE FROM admin WHERE user_id=%s", (user_id,))
                        cursor.execute("DELETE FROM user WHERE user_id=%s", (user_id,))
                        cnx.commit()       
                else:
                    st.write(f"No user found")
        else:
            st.write(f"No user found")
    else:
        st.write("User id not found in environment variable")


def show_calendar_page():
    st.title("Calendar Page")
    # Add your calendar page content here

def show_file_storage_page(user_id):
    st.title("File Storage Page")
    # Upload file button to allow user to insert files
    uploaded_file = st.file_uploader("Choose a file")
    
    # Once a file is uploaded, insert the data into the FILE table
    if uploaded_file is not None:
        file_name = uploaded_file.name
        file_upload_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        file_size = uploaded_file.size
        file_extension = file_name.split('.')[-1]
        query = "INSERT INTO FILE (USER_ID, FILE_NAME, FILE_UPLOAD_DATE, FILE_SIZE, FILE_EXTENSION) VALUES (%s, %s, %s, %s, %s)"
        values = (user_id, file_name, file_upload_date, file_size, file_extension)
        cursor.execute(query, values)
        cnx.commit()

    # Data from FILE table is obtained using current user_id
    query = "SELECT * FROM FILE WHERE USER_ID = %s"
    values = (user_id,)
    cursor.execute(query, values)
    data = cursor.fetchall()

    # If data is in the database display all rows into the table
    if data:
        st.write("Uploaded Files:")
        df = pd.DataFrame(data, columns=["File_ID", "User_ID", "File_Name", "File_Upload_Date", "File_Size", "File_Extension"])
        st.table(df)
    else:
        st.write("No files uploaded.")

if __name__ == "__main__":
    main()
