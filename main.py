from typing import Dict
from PIL import Image as PillowImage
import subprocess
from flet import *
import shutil
import os


test_images_folder = "test_images"
input_images_sizes = {}


def resize_images(filenames: list):
    global input_images_sizes

    save_path = f"./yolov5/data/{test_images_folder}"
    os.makedirs(save_path, exist_ok=True)
    input_images_sizes = {}

    for filename in filenames:
        shutil.move(f"./uploads/{filename}", "./assets/input_images")

        img = PillowImage.open(f"./assets/input_images/{filename}")
        input_images_sizes[f"{filename}"] = img.size

        resized_img = img.resize((640, 480))
        resized_img.save(f"{save_path}/{filename}")

    print("input_images_sizes: ", input_images_sizes)


def resize_images_to_original():
    global input_images_sizes

    print(">>>> in resize_images_to_original")
    print("input_images_sizes = ", input_images_sizes)

    save_path = "./assets/result_images"

    for filename in input_images_sizes.keys():
        print(f"processing {filename}")
        image = PillowImage.open(f"./yolov5/runs/detect/expTestImage/{filename}")

        original_size = input_images_sizes[f"{filename}"]
        original_size_image = image.resize(original_size)
        original_size_image.save(f"{save_path}/{filename}")

    print(">>>> out resize_images_to_original")


def clear_assets_folder():
    shutil.rmtree("./assets/input_images", ignore_errors=True)
    shutil.rmtree("./assets/result_images", ignore_errors=True)
    os.makedirs("./assets/input_images", exist_ok=True)
    os.makedirs("./assets/result_images", exist_ok=True)


def main(page: Page):
    global input_images_sizes

    prog_bars: Dict[str, ProgressRing] = {}
    files = Ref[Column]()
    upload_button = Ref[ElevatedButton]()

    def file_picker_result(e: FilePickerResultEvent):
        upload_button.current.disabled = True if e.files is None else False
        prog_bars.clear()
        files.current.controls.clear()
        if e.files is not None:
            for f in e.files:
                prog = ProgressRing(value=0, bgcolor="#eeeeee", width=20, height=20)
                prog_bars[f.name] = prog
                files.current.controls.append(Row([prog, Text(f.name)]))
        page.update()

    def on_upload_progress(e: FilePickerUploadEvent):
        prog_bars[e.file_name].value = e.progress
        prog_bars[e.file_name].update()

    input_images_container = Ref[Row]()
    output_images_container = Ref[Row]()

    def fill_input_images_conteiner():
        global input_images_sizes

        input_images_container.current.controls.clear()
        output_images_container.current.controls.clear()

        for filename in input_images_sizes.keys():
            input_image_object = Image(
                src=f"./assets/input_images/{filename}",
                width=400,
                # height=400,
                fit=ImageFit.CONTAIN,
                repeat=ImageRepeat.NO_REPEAT,
                border_radius=border_radius.all(10),
            )

            input_images_container.current.controls.append(input_image_object)

    def fill_output_images_conteiner():
        global input_images_sizes

        output_images_container.current.controls.clear()

        for filename in input_images_sizes.keys():
            output_image_object = Image(
                src=f"./assets/result_images/{filename}",
                width=400,
                # height=400,
                fit=ImageFit.CONTAIN,
                repeat=ImageRepeat.NO_REPEAT,
                border_radius=border_radius.all(10),
            )

            output_images_container.current.controls.append(output_image_object)

    file_picker = FilePicker(on_result=file_picker_result, on_upload=on_upload_progress)

    def upload_files(e):
        uf = []

        if file_picker.result is not None and file_picker.result.files is not None:
            filenames = [fileinfo.name for fileinfo in file_picker.result.files]

            for f in file_picker.result.files:
                uf.append(
                    FilePickerUploadFile(
                        f.name,
                        upload_url=page.get_upload_url(f.name, 600),
                    )
                )

            file_picker.upload(uf)

            # удаляем старые данные
            clear_assets_folder()

            # ресайзим и сохраняем в ./yolov5/data/test_images
            resize_images(filenames)

            # заполняем картинками результирующую табличку
            fill_input_images_conteiner()
            page.update()

    def run_detect():
        shutil.rmtree("./yolov5/runs/detect", ignore_errors=True)
        command = "python3 ./yolov5/detect.py --source ./yolov5/data/test_images/ --weight ./yolov5_weights/yolov5_mask_detection.onnx --name expTestImage --conf 0.4"
        result = subprocess.run(command.split(), stderr=subprocess.PIPE, text=True)
        print("subprocess.run stderr: ", result.stderr)

        # ресайзим картинки обратно
        resize_images_to_original()

        # заполняем картинками результирующую табличку
        fill_output_images_conteiner()
        page.update()

    # hide dialog in a overlay
    page.overlay.append(file_picker)

    page.add(
        ElevatedButton(
            "Select files...",
            icon=icons.FOLDER_OPEN,
            on_click=lambda _: file_picker.pick_files(allow_multiple=True),
        ),
        Column(ref=files),
        ElevatedButton(
            "Upload",
            ref=upload_button,
            icon=icons.UPLOAD,
            on_click=upload_files,
            disabled=True,
        ),
        ElevatedButton(
            "Run detect.py",
            on_click=lambda _: run_detect(),
        ),
        Text(value=f"input images ({len(input_images_sizes)}):"),
        Row(ref=input_images_container),
        Text(value=f"output images ({len(input_images_sizes)}):"),
        Row(ref=output_images_container),
    )

    # imageContainer.current.controls.clear()
    # imageContainer.current.controls.append(Text(value="123"))
    # page.update()


app(target=main, upload_dir="uploads", assets_dir="assets", view=WEB_BROWSER)
