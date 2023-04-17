color a
echo "Cheking for librares\n"
timeout /t 2 /nobreak > NUL
color
pip install -r requirements.txt
color a
timeout /t 2 /nobreak > NUL
echo "Starting database\n"
color
timeout /t 2 /nobreak > NUL
python DB.py
color a
timeout /t 2 /nobreak > NUL
echo "Starting server"
timeout /t 2 /nobreak > NUL
start python MainServer.py
timeout /t 2 /nobreak > NUL
start ngrok http 5000
timeout /t 2 /nobreak > NUL
color