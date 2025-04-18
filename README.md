# PatientPal-backend
## Steps to run:
1. Clone the repo
2. Create a virtual environment <code>python -m venv virtualEnvName</code> then activate it <code>./virtualEnvName/Scripts/activate</code>.
3. Install dependencies: 
    3.1 <code>pip install pip-tools</code>
    3.2 <code>pip-compile requirements.in</code>
    3.3 <code>pip install -r requirements.txt</code>
4. Create logs directory <code>mkdir logs</code>
5. Run the app <code>flask run</code> (add <code>--debug</code> to run in debug mode)
### Important Notes:
1. Please put your virtual environment in the .gitignore file.

