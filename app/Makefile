
help:
	@echo "Available tasks:"
	@echo "\t get_data_by_week             : run sample API call to select data for projID=1"
	@echo "\t get_data_by_week_and_form    : run sample API call to select data for projID=1"

get_data_by_week:
	@curl http://127.0.0.1:5000/api/site_data/by_week/1 | python -m json.tool

get_data_by_week_and_form:
	@curl http://127.0.0.1:5000/api/site_data/by_week_and_form/1 | python -m json.tool

clean:
	rm -f *.pyc
