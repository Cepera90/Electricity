enter to conteiner:
docker exec -it 151c3ad3b0ab bash
copy file to conteiner:
docker cp wheater_RUS.csv 151c3ad3b0ab:/home/jovyan/wheater_RUS.csv

docker run -v E:/Учеба/github/Electricity:/home/jovyan/ -p 8888:8888 jupyter/scipy-notebook:2c80cf3537ca

docker build -t my_notebook .

docker run -v E:/Учеба/github/Electricity:/home/jovyan/ -p 8888:8888 my_notebook

docker-compose up