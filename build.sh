poetry export -f requirements.txt --output requirements.txt --without-hashes
sudo docker build -t muse-stream .
docker run -p 6553:5000/udp -v /Users/ferguscurrie/data/muse:/data/muse -d muse-stream