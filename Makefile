clean:
	 rm statsbomb.db

tar:
	tar -zcvf raw_data.tar.gz raw_data

decompress:
	tar -xf raw_data.tar.gz