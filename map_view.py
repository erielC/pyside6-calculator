# 1. Check data service directly
python -c "from src.data import data_service; s=data_service.get_locations()[0]; print(f'Direct: lat={s.get(\"Lattitude\")}, lon={s.get(\"Longitude\")}')"

# 2. Check if stores work
python -c "import json; from src.data import data_service; s=data_service.get_locations()[0]; print('Before JSON:', type(s.get('Longitude'))); j=json.dumps(s); d=json.loads(j); print('After JSON:', type(d.get('Longitude')))"