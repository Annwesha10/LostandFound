import streamlit as st
from pymongo import MongoClient
from dotenv import load_dotenv
import os
from datetime import datetime

# Load MongoDB credentials
load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")

# Connect to MongoDB
@st.cache_resource
def init_connection():
    return MongoClient(MONGO_URI)

client = init_connection()
db = client.lost_and_found  # Database name
collection = db.items       # Collection name

# Streamlit UI
st.title("🏷️ Lost & Found System")

# Add a lost item
with st.form("lost_form"):
    st.subheader("Report Lost Item")
    name = st.text_input("Item Name")
    description = st.text_area("Description")
    location = st.text_input("Location Lost")
    submit = st.form_submit_button("Submit")

    if submit:
        item = {
            "name": name,
            "description": description,
            "location": location,
            "status": "lost",
            "date": datetime.now()
        }
        collection.insert_one(item)
        st.success("✅ Item reported successfully!")

# Search functionality
st.subheader("Search Found Items")
search_query = st.text_input("Search by item name or location")
if search_query:
    results = collection.find({
        "$or": [
            {"name": {"$regex": search_query, "$options": "i"}},
            {"location": {"$regex": search_query, "$options": "i"}}
        ]
    })
    for item in results:
        st.write(f"""
        **Item:** {item['name']}  
        **Description:** {item['description']}  
        **Location:** {item['location']}  
        **Date:** {item['date'].strftime("%Y-%m-%d")}
        """)