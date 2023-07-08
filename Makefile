install_requirements:
	pip3 install -r requirements.txt

run_dev_server:
	flask run --port=3001 --reload

run_server:
	flask run

init_db_tables:
	psql -h 0.0.0.0 -U root -d postgres -a -f ./db/tables.sql