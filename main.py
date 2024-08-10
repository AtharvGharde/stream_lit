import streamlit as st
import pandas as pd
from datetime import datetime

# Initialize Data
barbers = []
appointments = []
# Users dictionary with a hardcoded developer profile
users = {
    "barber1": "password123", 
    "barber2": "password456",
    "developer": "devpassword"  # Hardcoded developer profile
}

# User Authentication Function
def authenticate_user(username, password):
    if username in users and users[username] == password:
        return True
    return False

# Function to simulate payment processing
def process_payment(user, amount):
    st.write(f"Payment of ${amount} processed for {user}.")

# Main App
def main():
    st.title("Barbur.com - Uber for Barbers")

    # Simple Login Form
    st.sidebar.title("Login")
    username = st.sidebar.text_input("Username")
    password = st.sidebar.text_input("Password", type="password")
    login_button = st.sidebar.button("Login")
    
    if login_button:
        if authenticate_user(username, password):
            st.sidebar.success(f"Welcome, {username}")
            st.session_state['authenticated'] = True
            st.session_state['username'] = username
        else:
            st.sidebar.error("Invalid username or password")

    if 'authenticated' in st.session_state and st.session_state['authenticated']:
        username = st.session_state['username']

        # Option for Barbers to register
        if st.sidebar.button("Register as a Barber"):
            st.subheader("Register as a Barber")
            with st.form("barber_registration"):
                barber_name = st.text_input("Full Name")
                experience = st.number_input("Years of Experience", 1, 50)
                services = st.text_area("Services Offered")
                pricing = st.number_input("Base Price ($)", 10, 500)
                availability = st.text_input("Availability (e.g., Mon-Fri, 9am-5pm)")
                submitted = st.form_submit_button("Register")
                if submitted:
                    barber = {
                        'name': barber_name,
                        'experience': experience,
                        'services': services,
                        'pricing': pricing,
                        'availability': availability,
                        'ratings': [],
                        'profile_id': len(barbers) + 1
                    }
                    barbers.append(barber)
                    st.success("Barber registered successfully!")
        
        # Option for Users to book appointments
        if st.sidebar.button("Book a Barber"):
            st.subheader("Book a Barber")
            if len(barbers) == 0:
                st.write("No barbers available. Please check back later.")
            else:
                selected_barber = st.selectbox("Select Barber", [barber['name'] for barber in barbers])
                for barber in barbers:
                    if barber['name'] == selected_barber:
                        st.write(f"Experience: {barber['experience']} years")
                        st.write(f"Services: {barber['services']}")
                        st.write(f"Pricing: ${barber['pricing']}")
                        st.write(f"Availability: {barber['availability']}")
                        break
                appointment_date = st.date_input("Select Date", min_value=datetime.now().date())
                appointment_time = st.time_input("Select Time")
                confirm = st.button("Confirm Booking")
                if confirm:
                    appointment = {
                        'barber': selected_barber,
                        'user': username,
                        'date': appointment_date,
                        'time': appointment_time,
                        'amount': barber['pricing']
                    }
                    appointments.append(appointment)
                    st.success(f"Appointment booked with {selected_barber} on {appointment_date} at {appointment_time}")
                    process_payment(username, barber['pricing'])

        # Option for Barbers to view appointments
        if st.sidebar.button("View Appointments"):
            st.subheader("My Appointments")
            for appointment in appointments:
                if appointment['barber'] == username:
                    st.write(f"User: {appointment['user']}")
                    st.write(f"Date: {appointment['date']}")
                    st.write(f"Time: {appointment['time']}")
                    st.write("---")
        
        # Option to rate barbers
        if st.sidebar.button("Rate a Barber"):
            st.subheader("Rate a Barber")
            rated_barber = st.selectbox("Select Barber to Rate", [barber['name'] for barber in barbers])
            rating = st.slider("Rate out of 5", 1, 5)
            review = st.text_area("Leave a review")
            submit_rating = st.button("Submit Rating")
            if submit_rating:
                for barber in barbers:
                    if barber['name'] == rated_barber:
                        barber['ratings'].append({'rating': rating, 'review': review})
                        st.success("Rating submitted successfully!")

        # Logout option
        if st.sidebar.button("Logout"):
            st.session_state['authenticated'] = False
            st.session_state['username'] = ""
            st.success("Logged out successfully.")
    else:
        st.warning("Please log in to access the app features.")

if __name__ == '__main__':
    main()
