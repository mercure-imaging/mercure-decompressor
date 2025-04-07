import os
import pydicom
import sys
import glob


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
    dicom_files = glob.glob(os.path.join(input_folder, '*'))

    # Decompress each DICOM file
    for input_file in dicom_files:
        output_file = os.path.join(output_folder, os.path.basename(input_file))
        decompress_dicom_file(input_file, output_file, decoding_plugins, transfer_uid_to_plugin)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Abort! Input folder and output folder should be specified.")
        print("Usage: python main.py <input_folder> <output_folder>")
        sys.exit(1)

    input_folder = sys.argv[1]
    output_folder = sys.argv[2]

    decoding_plugins = ['gdcm', 'pylibjpeg', 'pydicom']
    transfer_uid_to_plugin = {}

    decompress_dicom_folder(input_folder, output_folder, decoding_plugins, transfer_uid_to_plugin)

    print("Available decompression plugins: ", decoding_plugins)
    print("Decompression plugins used: ", transfer_uid_to_plugin)