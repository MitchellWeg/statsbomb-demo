clean:
	 rm statsbomb.db | true

tar:
	tar -zcvf raw_data.tar.gz raw_data

decompress:
	tar -xf raw_data.tar.gz

run:
	make clean
	python statsbomb_demo/cli.py
	docker-compose up