call conda create --name test python=3.8
call conda activate test
call pip install -r requirements.txt
call python -m pytest
