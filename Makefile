clean:
	rm -rf raw_data
	mkdir raw_data
	rm statsbomb.db

tar:
	tar -zcvf raw_data.tar.gz raw_data