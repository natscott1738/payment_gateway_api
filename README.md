💳 Django Payment Gateway API
A simple RESTful API using Django REST Framework that allows businesses to initiate and track payments using Paystack.

✅ Features
Initiate a payment via Paystack
Retrieve payment status
Versioned API (/api/v1/)
Automated tests
GitHub Actions CI/CD
Docker support
🔧 Getting Started
paystack key is hidden in the settings.py
Option 1: Run Locally with Python
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name

python3 -m venv env
source env/bin/activate

pip install -r requirements.txt

python manage.py migrate
python manage.py runserver
