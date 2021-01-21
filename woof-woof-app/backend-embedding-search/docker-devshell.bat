call ./environment.bat
docker build -t %IMAGE_NAME% -f Dockerfile .
docker run --rm --name %IMAGE_NAME% -ti -v "%cd%:/app/" -v "%EXT_DATASTORE%:/datastore/" -p 9010:9010 -e DEV=1 %IMAGE_NAME%