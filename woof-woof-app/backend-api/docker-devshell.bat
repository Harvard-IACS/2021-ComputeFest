call ./environment.bat
docker build -t %IMAGE_NAME% -f Dockerfile .
docker run --rm --name %IMAGE_NAME% -ti -v "%cd%:/app/" -v "%EXT_DATASTORE%:/datastore/" -p 9000:9000 -e DEV=1 %IMAGE_NAME%