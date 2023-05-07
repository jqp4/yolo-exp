from typing import Dict
from PIL import Image as PillowImage
from flet import *
import os


test_images_folder = "test_images"


def resize_images(filenames: list, source_folder: str, save_folder: str):
    save_path = f"./yolov5/data/{test_images_folder}"
    os.makedirs(save_path, exist_ok=True)

    for image in filenames:
        img = PillowImage.open(f"{source_folder}/{image}")
        resized_img = img.resize((640, 480))
        # resized_img.save(
        #     source_folder + "/yolov5/data/" + save_folder + "/images/" + image
        # )
        resized_img.save(f"{save_path}/{image}")


def main(page: Page):
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

    file_picker = FilePicker(on_result=file_picker_result, on_upload=on_upload_progress)
    imageContainer = Ref[Row]()

    def upload_files(e):
        uf = []

        if file_picker.result is not None and file_picker.result.files is not None:
            filename = file_picker.result.files[0].name
            filenames = [fileinfo.name for fileinfo in file_picker.result.files]

            for f in file_picker.result.files:
                uf.append(
                    FilePickerUploadFile(
                        f.name,
                        upload_url=page.get_upload_url(f.name, 600),
                    )
                )
            file_picker.upload(uf)

            img = Image(
                src=filename,
                width=400,
                height=400,
                fit=ImageFit.CONTAIN,
                repeat=ImageRepeat.NO_REPEAT,
                border_radius=border_radius.all(10),
            )

            print(filenames)

            # ресайзим
            resize_images(filenames, "uploads", "")

            imageContainer.current.controls.clear()
            imageContainer.current.controls.append(img)
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
        Row(ref=imageContainer),
    )

    # imageContainer.current.controls.clear()
    # imageContainer.current.controls.append(Text(value="123"))
    # page.update()


app(target=main, upload_dir="uploads", assets_dir="uploads", view=WEB_BROWSER)
