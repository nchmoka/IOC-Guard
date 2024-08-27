# IOC-Guard

IoC-Guard is a Django-based application that automates the process of analyzing IoC's using external threat intelligence services like VirusTotal and AbuseCH. The application provides a RESTful API for submitting IoCs and generates detailed PDF reports that include analysis results.

## Installation

```bash

1. Clone the Repository
git clone https://github.com/your-username/IoC-Guard.git
cd IoC-Guard
cd IoC-Guard

2. Create a Virtual Environment
python -m venv venv

3. Activate the Virtual Environment
On Windows:
venv\Scripts\activate
On Linux:
source venv/bin/activate

4. Install Dependencies
pip install -r requirements.txt

5. Set Up Environment Variables
copy the env file into the folder where manage.py exists

6. Apply Database Migrations
python manage.py makemigrations ioc_guard
python manage.py migrate

7. Create a Superuser (Admin)
python manage.py createsuperuser

8. Run the Development Server
python manage.py runserver

9. Access the Admin Panel
Visit http://127.0.0.1:8000/admin/ in your browser and log in with the superuser credentials.

Usage
API Endpoints
Check Domain:
POST /ioc_guard/api/check-domain/
Body: { "domain": "example.com" }
Check IP:
POST /ioc_guard/api/check-ip/
Body: { "ip": "8.8.8.8" }
Check Hash:
POST /ioc_guard/api/check-hash/
Body: { "hash": "44d88612fea8a8f36de82e1278abb02f" }
```

## Testing

To run the automated tests:

```
python manage.py test
```
