clean:
	 rm statsbomb.db | true

tar:
	tar -zcvf raw_data.tar.gz raw_data

decompress:
	tar -xf raw_data.tar.gz

run:
	rm -rf new_data | true
	mkdir new_data
	make clean
	python statsbomb_demo/cli.py --threads=6 
	docker-compose up