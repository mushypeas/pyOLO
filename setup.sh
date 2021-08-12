cd darknet
make
cd ..
FILE=darknet53.conv.74
if [ -f "$FILE" ]; then
    echo "$FILE already exists."
else
    wget https://pjreddie.com/media/files/darknet53.conv.74
fi