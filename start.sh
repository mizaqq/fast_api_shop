source ./env/scripts/activate

uvicorn  --app-dir=./api main:app --reload
