docker stop test
docker rm test
docker build -t test .
docker run --name test -p 41061:22 -p 41062:80 -d -v "%cd%/my_web_pages":/www  -v ~/my_apache_conf:/opt/lampp/apache2/conf.d tomsik68/xampp
pause