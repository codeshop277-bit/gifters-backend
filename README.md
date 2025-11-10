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

 