import streamlit as st
import pandas as pd
import streamlit_authenticator as stauth
from datetime import datetime

# Initialize Data
barbers = []
appointments = []

# Function to simulate payment processing
def process_payment(user, amount):
    st.write(f"Payment of ${amount} processed for {user}.")

# User Authentication
def authenticate_user():
    users = {'barber1': 'password123', 'barber2': 'password456'}
    usernames = list(users.keys())
    passwords = list(users.values())
    
    hashed_passwords = stauth.Hasher(passwords).generate()

    authenticator = stauth.Authenticate(usernames, usernames, hashed_passwords, 'app_home', 'random_key')
    name, authentication_status, username = authenticator.login('Login', 'main')

    return name, authentication_status, username, authenticator

# Main App
def main():
    st.title("Barber Booking Service")

    # Authenticate user
    name, authentication_status, username, authenticator = authenticate_user()

    if authentication_status:
        st.sidebar.title(f"Welcome, {name}")

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
                        'user': name,
                        'date': appointment_date,
                        'time': appointment_time,
                        'amount': barber['pricing']
                    }
                    appointments.append(appointment)
                    st.success(f"Appointment booked with {selected_barber} on {appointment_date} at {appointment_time}")
                    process_payment(name, barber['pricing'])

        # Option for Barbers to view appointments
        if st.sidebar.button("View Appointments"):
            st.subheader("My Appointments")
            for appointment in appointments:
                if appointment['barber'] == name:
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
            authenticator.logout('Logout', 'sidebar')
            st.success("Logged out successfully.")
    elif authentication_status == False:
        st.error("Username/password is incorrect")
    elif authentication_status == None:
        st.warning("Please enter your username and password")

if __name__ == '__main__':
    main()
