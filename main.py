# This code connects to a MySQL database and defines a main function for a Streamlit app called "Aggie Scheduler". 
# The app displays a navigation sidebar with three pages: "Profile", "Calendar", and "File Storage". 
# When the user selects a page, the app calls the appropriate function to display the content. 
# The "Profile" page allows users to view and edit their personal information, including additional fields based on their user type. 
# The "Calendar" and "File Storage" pages do not currently have any content.

# RISHABH KUMAR: 10 - 149

# Import necessary libraries
import os
import datetime
import mysql.connector
import streamlit as st

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
        show_calendar_page(user_id)
    elif selection == "File Storage":
        show_file_storage_page()

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


def show_calendar_page(user_id):
    st.title('Your Appointments')
    # Check for null user_id
    if not user_id:
        st.write("User id not found in environment variable")
        return

    cursor.execute("SELECT * FROM user WHERE USER_ID=%s", (user_id,))
    user = cursor.fetchone()

    if not user:
        st.write(f'User with id {user_id} not found.')
        return

    user_type = user[5]

    col1, col2 = st.columns([1, 1])
    
    # Upcoming Events in left column 
    # Has SELECT, DELETE, and UPDATE queries
    with col1: 
        st.subheader("Upcoming")

        cursor.execute("SELECT * FROM attendee INNER JOIN appointment ON attendee.APPT_ID=appointment.APPT_ID WHERE USER_ID=%s", (user_id,))
        data = cursor.fetchall()
        if data:
            for appt in data:
                st.markdown("""---""")
                with st.container():
                    st.subheader(f'{appt[2]}')
                    st.write(f'On {appt[5].date()}')
                    st.write(f'Goes from {appt[5].time()} - {appt[6].time()}')
                    st.write(f'At {appt[7]}')
                    if st.button("Edit"):
                        pass
                    if user_type == 'TUTOR' or user_type == 'ADMIN':
                        if st.button("Delete"):
                            cursor.execute(f'DELETE FROM attendee WHERE APPT_ID={appt[0]}')
                            cursor.execute(f'DELETE FROM appointment WHERE APPT_ID={appt[0]}')
                            cnx.commit()

                    if st.button("Show Comments"):
                        pass
                        # Load Comments and display somehow. Maybe similar to the for loop with st.container above
                        # APPT_ID is appt[0] at this scope
                        # If you find a different way of doing it for the comments, feel free to change it, I will be using this structure though

            st.markdown("""---""")



    # Form to make new event in right column
    # Has INSERT queries
    if user_type == 'TUTOR' or user_type == 'ADMIN':
        with col2:
            user_ids_attending = [user_id]
            with st.form("add_student"):
                st.subheader("Step 1: Add Student")
                student_fname = st.text_input("Student First Name")
                student_lname = st.text_input("Student Last Name")
                if st.form_submit_button("Search"):
                    cursor.execute("SELECT * FROM user WHERE USER_FNAME=%s AND USER_LNAME=%s", (student_fname, student_lname,))
                    student = cursor.fetchone()
                    if not student:
                        st.write(f'Could not find student by the name of {student_fname} {student_lname}')
                    elif student[0] == user_id:
                        st.write(f'Unable to add yourself to an appointment')
                    else:
                        user_ids_attending.append(student[0])
                        st.write(f'{student_fname} {student_lname} Added to Appointment!')
                    
            with st.form("event_information"):
                st.subheader("Step 2: Create Event")
                appt_name = st.text_input("Appointment Name")
                date = st.date_input("Date of Event", 
                    value=(datetime.datetime.now() + datetime.timedelta(days=1)).date(),
                    min_value=datetime.datetime.now().date(),
                    max_value=(datetime.datetime.now() + datetime.timedelta(days=30)) 
                )
                start_time = st.time_input("Start Time" , value=(datetime.datetime.now() + datetime.timedelta(days=1)).time())
                end_time = st.time_input("End Time", value=(datetime.datetime.now() + datetime.timedelta(days=1, hours=1)).time())
                location = st.text_input("Street Address or Zoom Link")
                if st.form_submit_button("Create Appointment"):
                    start_datetime = datetime.datetime.combine(date=date, time=start_time)
                    end_datetime = datetime.datetime.combine(date=date, time=end_time)
                    
                    # Add appointment
                    appt_sql = "INSERT INTO appointment (START_TIME, END_TIME, LOCATION) VALUES(%s, %s, %s)"
                    appt_val = (start_datetime, end_datetime, location)
                    
                    cursor.execute(appt_sql, appt_val)
                    cnx.commit()

                    # Get auto generated appt_id to use for attendee inserts
                    appt_id = cursor.lastrowid

                    # Add attendee(s)
                    sql = ("INSERT INTO attendee (APPT_ID, USER_ID, APPT_NAME, IS_ORGANIZER) VALUES (%s, %s, %s, %s)")
                    for uid in user_ids_attending:
                        is_organizer = True if uid == user_id else False 
                        val = (appt_id, uid, appt_name, is_organizer)
                        cursor.execute(sql, val)
                        cnx.commit()
    

    # Add your calendar page content here

def show_file_storage_page():
    st.title("File Storage Page")
    # Add your file storage page content here

if __name__ == "__main__":
    main()
