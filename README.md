# **mercure-decompressor**

Mercure module to decompress DICOM images. It uses the decoding plugins provided in the [Pydicom](https://pydicom.github.io/pydicom/dev/guides/plugin_table.html) package to decompress the files having different compressed transfer syntaxes.

## **Installation**

### Add module to existing mercure installation
Follow instructions on [mercure website](https://mercure-imaging.org) on how to add a new module. Use the docker tag `mercureimaging/mercure-decompressor`.

### Build module for local testing, modification and development
1. Clone repo.
2. Build Docker container locally by running make (modify makefile with new docker tag as needed).
3. Test container :\
`docker run -it -v /input_data:/input -v /output_data:/output --env MERCURE_IN_DIR=/input  --env MERCURE_OUT_DIR=/output mercureimaging/mercure-decompressor`

## **Configuration**

The mercure-decompressor module requires no additional configuration in mercure. A rule should be configured to receive the images with this module as a processing step. More information on mercure rule configuration can be found [here.](https://mercure-imaging.org/docs/usage.html)

By default, the decoding plugins for the incoming files will be tried in the below order. If you want to change the order or fix one plugin; settings can be configured in the mercure user interface.
<pre>
  {
      "decoding_plugins": ['gdcm', 'pylibjpeg', 'pydicom']
  }
</pre>

If the received series/study has multiple transfer syntaxes, a mapping between `tranfer_uid_name -> decoding_plugin_used` would be created and printed in the logs to avoid confusion. The above plugin order can be changed or fixed to one to satisfy the use case.
