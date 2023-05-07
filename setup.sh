git clone https://github.com/ultralytics/yolov5.git

python3 -m venv flet_venv
. ./flet_venv/bin/activate


pip3 install -r ./yolov5/requirements.txt

pip3 install flet
pip3 install torch
pip3 install Pillow
pip3 install pytest-shutil
