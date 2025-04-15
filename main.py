import os
import pydicom
import sys
import glob
import json
from pathlib import Path


def decompress_dicom_file(input_file, output_file, decoding_plugins, transfer_uid_to_plugin):
    ds = pydicom.dcmread(input_file)
    transfer_uid_name = ds.file_meta.TransferSyntaxUID.name

    if ds.file_meta.TransferSyntaxUID.is_compressed:
        if transfer_uid_name in transfer_uid_to_plugin:
            plugin = transfer_uid_to_plugin[transfer_uid_name]
            try:
                ds.decompress(decoding_plugin=plugin)
            except Exception as e:
                print(f"Failed to decompress DICOM file {input_file}: {e}")
        else:
            for plugin in decoding_plugins:
                try:
                    ds.decompress(decoding_plugin=plugin)
                    if ds.file_meta.TransferSyntaxUID.is_compressed:
                        continue # if still compressed, try next plugin.
                    transfer_uid_to_plugin[transfer_uid_name] = plugin
                    break
                except Exception as e:
                    print(f"Failed to decompress DICOM file {input_file}: {e} using {plugin} plugin")
    else:
        print(f"DICOM file {input_file} is not compressed")

    # Ensure the pixel data is in bytes format
    if isinstance(ds.PixelData, str):
        ds.PixelData = ds.PixelData.encode('utf-8')

    ds.save_as(output_file)


def decompress_dicom_folder(input_folder, output_folder, decoding_plugins, transfer_uid_to_plugin):
   # Get all DICOM files in the input folder
    dicom_files = glob.glob(os.path.join(input_folder, '*.dcm'))

    # Decompress each DICOM file
    for input_file in dicom_files:
        output_file = os.path.join(output_folder, os.path.basename(input_file))
        decompress_dicom_file(input_file, output_file, decoding_plugins, transfer_uid_to_plugin)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Abort! Input folder and output folder should be specified.")
        print("Usage: python main.py <input_folder> <output_folder>")
        sys.exit(1)

    input_folder = Path(sys.argv[1])
    output_folder = Path(sys.argv[2])

    decoding_plugins = ['gdcm', 'pylibjpeg', 'pydicom']
    transfer_uid_to_plugin = {}

    # Check if the user provided plugins to use
    try:
        with open(input_folder / "task.json", "r") as json_file:
            task = json.load(json_file)
    except Exception:
        print("Error: Task file task.json not found")
        sys.exit(1)
    # Overwrite default values with settings from the task file (if present)
    settings =  task.get("process", "").get("settings", "")
    val = settings.get("decoding_plugins", "")
    if val and isinstance(val, str):
        decoding_plugins = [val]
    elif val and isinstance(val, list):
        decoding_plugins = val

    decompress_dicom_folder(input_folder, output_folder, decoding_plugins, transfer_uid_to_plugin)

    print("Available decompression plugins: ", decoding_plugins)
    print("Decompression plugins used: ", transfer_uid_to_plugin)