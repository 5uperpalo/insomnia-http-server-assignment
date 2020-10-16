pause & ^
docker stop insomnia & ^
docker rm insomnia -f & ^
docker image remove -f insomnia & ^
docker build -t insomnia . && ^
docker run --restart unless-stopped -p 80:80 -p 9001:9001 --name insomnia insomnia & ^
pause