# Patient Management System

## Description

This repository contains the source code for a Patient Management System designed for a local medium clinic. The system is built using Django framework for the backend, Bootstrap for styling, and Vanilla JavaScript for frontend functionalities.

## Functionalities

### Receptionist

- **Patient Registration**: Receptionists can register new patients by entering their details including name, age, contact details, and reason for visit.
- **Appointment Scheduling**: After registering the patient, receptionists can schedule appointments for them with available doctors.
- **Patient Search**: Receptionists can search for existing patients using their first name, last name, or phone number to retrieve their information quickly.

### Doctor

- **Patient Diagnosis**: Doctors can view the list of patients assigned to them and diagnose their medical condition.
- **Lab Test Ordering**: Doctors can order lab tests for patients based on their diagnosis.
- **View Patient Results**: After lab tests are completed, doctors can view the results and prescribe medication accordingly.

### Lab Technician

- **Sample Collection**: Lab technicians can collect samples from patients based on the lab test orders assigned to them.
- **QR Code Generation**: Once the sample is collected, lab technicians generate a QR code that is attached to the sample for identification.
- **Upload Test Results**: After conducting tests, lab technicians upload the results to the system.

### Telegram Bot

- **Payment Notifications**: When a patient makes a payment, the payment information is sent to the clinic's Telegram channel to notify the staff.
- **Lab Order Status**: Patients can interact with the Telegram bot to inquire about their pending and completed lab orders by providing their card number.

### Admin

- **User Management**: Admin can manage user accounts, including creating, updating, and deleting user profiles.
- **Role Assignment**: Admin can assign roles to users and manage their permissions within the system.
- **System Configuration**: Admin has access to system configuration settings such as database management and application settings.

## Demo Access

- The demo version of the system is deployed on PythonAnywhere for demonstration purposes.
- You can access the system using the following credentials:
  - **Receptionist**: Username: `reception`, Password: `yakob@123`
  - **Doctor**: Username: `doctor`, Password: `yakob@123`
  - **Lab Technician**: Username: `lab`, Password: `yakob@123`
- Visit the demo site at [Demo Patient Management System](https://yakob.pythonanywhere.com/)

## Installation

1. Clone the repository: `git clone https://github.com/yourusername/patient-management-system.git`
2. Install dependencies: `pip install -r requirements.txt`
3. Apply database migrations: `python manage.py migrate`
4. Run the server: `python manage.py runserver`
5. Access the application through a web browser at `http://localhost:8000`

## Usage

1. Access the application using the provided URL.
2. Log in with the demo user credentials based on your role (Receptionist, Doctor, or Lab Technician).
3. Explore the functionalities of the system and familiarize yourself with its features.

## Database

- The backend of the system uses PostgreSQL as the relational database.

## Contributing

If you'd like to contribute to this project, please follow these steps:

1. Fork the repository
2. Create a new branch (`git checkout -b feature/new-feature`)
3. Make your changes
4. Commit your changes (`git commit -am 'Add new feature'`)
5. Push to the branch (`git push origin feature/new-feature`)
6. Create a new Pull Request

## License

This project is licensed under the ACT As my School project
