cd darknet
make
FILE=darknet19_448.conv.23
if [ ! -f "$FILE" ]; then
    wget http://pjreddie.com/media/files/darknet19_448.conv.23
fi
cd ..