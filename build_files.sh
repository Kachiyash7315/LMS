## build_files.sh
#pip install -r requirements.txt
#python manage.py collectstatic

echo " BUILD START"
python3.9  -m pip install -r requirements.txt
python3.9 manage.py collectstatic  --noinput --clear
echo " BUILD END"