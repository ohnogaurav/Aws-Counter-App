# AWS Counter App

A simple multi-user counter app built with Flask and SQLite.  
Each user can log in, increment their own counter, and reset it.

## Features
- User authentication (register/login/logout)
- Persistent counter storage
- Responsive UI with Bootstrap

## Installation
```bash
git clone https://github.com/yourusername/aws-counter-app.git
cd aws-counter-app
pip install -r requirements.txt
python app.py
```

## Running on AWS EC2
1. Launch Ubuntu EC2 instance.
2. Install Python & pip:
   ```bash
   sudo apt update
   sudo apt install python3 python3-pip -y
   ```
3. Upload project files (via SCP or Git clone).
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
5. Run app:
   ```bash
   python3 app.py
   ```
6. Access via: `http://<your-ec2-public-ip>:5000`
