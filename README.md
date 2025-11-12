# gifters-backend

Add columns to exisiting tables.
alembic revision --autogenerate -m "Add hashed password column to users table"
alembic upgrade head
#alembic stamp head --> to reset between migartion

Host Database in AWS
Go to aws console
RDS
Create a database with require specifics
Copy the host url, port etc
Connect the url from your backend

Host backedn in AWS
Got to aws console > EC2
Launch Instance
Key pair config -- > When you connect to your EC2 instance via SSH (for Linux) or RDP (for Windows), AWS uses this key pair to authenticate that you are the authorized user.
Security group config --> virtual firewall, controls which network traffic is allowed to enter or leave the instance  
“Inbound rules” = who can connect to your instance.
“Outbound rules” = where your instance can connect out to.

Connect to your EC2 instance via git bash
Go to your ec2-key file path and connect to your ubuntu 

ssh -i my-ec2-key.pem ubuntu@13.48.58.135 ==> Public IP from created instance
And install dependencies in your EC2 terminal
sudo apt update
sudo apt install python3-pip python3-venv git nginx -y

apt update → updates package list
python3-pip → installs Python’s package manager
python3-venv → lets you create isolated environments
git → allows cloning from GitHub (if you store code there)
nginx → production web server to forward traffic to your backend later

Clone your repo in server
cd repo

Create a isolated virtual env to install repo related dependencies
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000

http://13.48.58.135:8000
 