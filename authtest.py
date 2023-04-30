import streamlit as st
import mysql.connector
import hashlib

# Connect to MySQL
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="csce310"
)

mycursor = mydb.cursor()

# Define function to create a new user account
def create_account(user_fname, user_lname, user_email, user_password, user_type, **kwargs):
    # Hash the password
    hashed_password = hashlib.sha256(user_password.encode()).hexdigest()

    # Insert the document into the appropriate MySQL table based on the user type
    if user_type.lower() == "admin":
        sql = """
            INSERT INTO ADMIN (USER_ID, ADMIN_INFO)
            VALUES ((SELECT USER_ID FROM USER WHERE USER_EMAIL=%s), %s)
        """
        val = (user_email.strip(), kwargs.pop('admin_info', ''))
    elif user_type.lower() == "tutor":
        tutor_avail = kwargs.pop('tutor_avail', {})
        tutor_subjects = kwargs.pop('tutor_subjects', '')
        sql = """
            INSERT INTO TUTOR (USER_ID, TUTOR_AVAIL, TUTOR_SUBJECTS)
            VALUES ((SELECT USER_ID FROM USER WHERE USER_EMAIL=%s), %s, %s)
        """
        val = (user_email.strip(), str(tutor_avail), tutor_subjects)
    elif user_type.lower() == "student":
        grade = kwargs.pop('student_grade', None)
        major = kwargs.pop('student_major', None)
        gpa = kwargs.pop('student_gpa', None)
        sql = """
            INSERT INTO STUDENT (USER_ID, STUDENT_GRADE, STUDENT_MAJOR, STUDENT_GPA)
            VALUES ((SELECT USER_ID FROM USER WHERE USER_EMAIL=%s), %s, %s, %s)
        """
        val = (user_email.strip(), grade, major, gpa)
    else:
        raise ValueError(f"Invalid user type: {user_type}")

    mycursor.execute("""
        INSERT INTO USER (USER_FNAME, USER_LNAME, USER_EMAIL, USER_PASSWORD, USER_TYPE)
        VALUES (%s, %s, %s, %s, %s)
    """, (user_fname.strip(), user_lname.strip(), user_email.strip(), hashed_password, user_type.upper()))
    mydb.commit()

    mycursor.execute(sql, val)
    mydb.commit()

    st.success(f"Account created for {user_email}!")

def authenticate(username, password):
    # Check if the user exists in any of the tables
    user = None
    tables = ["USER", "TUTOR", "STUDENT", "ADMIN"]
    for table in tables:
        mycursor.execute(f"""
            SELECT * FROM {table}
            WHERE USER_EMAIL = %s
        """, (username,))
        user = mycursor.fetchone()
        if user:
            break

    if user:
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        if user[4] == hashed_password:
            user_id = user[0]
            return True, user[5], user_id

    print(f"Invalid email or password: {username} {password}")
    return False, None, None
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
            # Call the authenticate function and store the returned user_type and user_id
            auth_success, user_type, user_id = authenticate(user_email, user_password)
            if auth_success:
                # Clear the currentUser table
                mycursor.execute("DELETE FROM currentUser")

                # Insert the user ID into the currentUser table
                mycursor.execute("INSERT INTO currentUser (current_id) VALUES (%s)", (user_id,))
                mydb.commit()

                st.success("Logged in!")
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
            admin_info = st.selectbox("Select a title", ["Professor", "Counselor"])
            if st.button("Create Account"):
                create_account(user_fname, user_lname, user_email, user_password, user_type, admin_info=admin_info)

if __name__ == "__main__":
    main()
