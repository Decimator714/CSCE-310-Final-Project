MongoDB
----------------------------------------------------------------------------------------------------------------
Connection:
    # Connect to MongoDB
    client = pymongo.MongoClient("mongodb+srv://richiekumar:Srirama10@csce-310.t0eeunr.mongodb.net/")
    db = client["mydatabase"]
    users = db["users"]
    tutors = db["tutors"]
    students = db["students"]
    admins = db["admins"]
----------------------------------------------------------------------------------------------------------------




Dependencies
----------------------------------------------------------------------------------------------------------------
Streamlit: version 0.84.0 or higher
pymongo: version 3.12.0 or higher
hashlib: built-in module in Python
os: built-in module in Python

To install these dependencies, you can use pip, the Python package manager:

    pip install streamlit

And here's how to install pymongo:

    pip install pymongo
----------------------------------------------------------------------------------------------------------------



User Schema
----------------------------------------------------------------------------------------------------------------
USER
PK | USER_ID
    | USER_FNAME
    | USER_LNAME
    | USER_EMAIL
    | USER_PASSWORD
    | USER_TYPE

TUTOR
PK | TUTOR_ID
FK | USER_ID
    | TUTOR_AVAIL
    | TUTOR_SUBJECTS

ADMIN
PK | ADMIN_ID
FK | USER_ID

STUDENT
PK | STUDENT_ID
FK | USER_ID
    | STUDENT_GRADE
    | STUDENT_MAJOR
    | STUDENT_GPA
----------------------------------------------------------------------------------------------------------------