# echo "2 from sh script:"
# echo $1

cd ./scripts

# input.xml --> output.json
./main $1

# output.json --> jsonGraphData.js
python3 json2js.py output.json ../public/algoviewCodeCopy/data/jsonGraphData.js

echo "done!"
