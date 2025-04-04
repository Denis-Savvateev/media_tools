import os
import shutil
from tkinter import filedialog

from PIL import Image, ExifTags

from settings import (
    photo_files,
    video_files,
)


def copy_file(in_file, out_file):
    if os.path.exists(out_file):
        index: int = 2
        busy_name: bool = True
        while busy_name:
            dir_name = os.path.dirname(out_file)
            short_name, ext = os.path.splitext(
                os.path.basename(out_file)
            )
            short_name += f' ({str(index)})'
            new_out_file = os.path.join(
                dir_name,
                f'{short_name}{ext}'
            )
            if not os.path.exists(new_out_file):
                out_file = new_out_file
                busy_name = False
                continue
            index += 1
    try:
        shutil.copy2(in_file, out_file)
    except Exception as e:
        print(f'Ошибка копирования: {e}')


def find_copy_files(start_path, path_out):
    for path, dirs, files in os.walk(start_path):
        for f in files:
            file_path = os.path.join(path, f)
            short_name, ext = os.path.splitext(
                os.path.basename(file_path)
            )
            ext = ext.lstrip('.')
            if ext in photo_files:
                image = Image.open(file_path)
                try:
                    exif = {
                        ExifTags.TAGS[k]: v
                        for k, v in image._getexif().items()
                        if k in ExifTags.TAGS
                    }
                    if 'Make' in exif:
                        time: str = exif['DateTime']
                        time_in_name = time.replace(':', '-')
                        camera = exif['Make'].rstrip('\\x00').rstrip()
                        model = exif['Model'].rstrip('\\x00').rstrip()
                        new_name = f'{time_in_name}.{ext}'
                        new_dir = os.path.join(path_out, f'{camera}_{model}')
                        new_full_path = os.path.join(new_dir, new_name)
                        if not os.path.exists(new_dir):
                            os.makedirs(
                                new_dir,
                                exist_ok=True
                            )
                        copy_file(file_path, new_full_path)
                except Exception:
                    continue
            elif ext in video_files:
                new_full_path = os.path.join(
                    path_out,
                    os.path.basename(file_path)
                )
                copy_file(file_path, new_full_path)


def main():
    path = filedialog.askdirectory(
        title="Выберите папку для поиска файлов."
    )
    path_out = filedialog.askdirectory(
        title="Выберите папку для сохранения фотографий."
    )
    find_copy_files(path, path_out)


if __name__ == '__main__':
    main()
