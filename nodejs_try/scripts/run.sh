# echo "2 from sh script:"
# echo $1

cd ./scripts

# output.json --> jsonGraphData.js
python3 json2js.py output.json ../public/algoviewCodeCopy/data/jsonGraphData.js

echo "done!"
