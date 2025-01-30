Dataset **AAU-PD-T** can be downloaded in [Supervisely format](https://developer.supervisely.com/api-references/supervisely-annotation-json-format):

 [Download](https://assets.supervisely.com/remote/eyJsaW5rIjogImZzOi8vYXNzZXRzLzMxMTBfQUFVLVBELVQvYWF1cGR0LURhdGFzZXROaW5qYS50YXIiLCAic2lnIjogIlE0bENCSjJTajNObzZXcVc0b0xpWUNUVlFDT25BaTBUbW0xMTdBb1JybkU9In0=)

As an alternative, it can be downloaded with *dataset-tools* package:
``` bash
pip install --upgrade dataset-tools
```

... using following python code:
``` python
import dataset_tools as dtools

dtools.download(dataset='AAU-PD-T', dst_dir='~/dataset-ninja/')
```
Make sure not to overlook the [python code example](https://developer.supervisely.com/getting-started/python-sdk-tutorials/iterate-over-a-local-project) available on the Supervisely Developer Portal. It will give you a clear idea of how to effortlessly work with the downloaded dataset.

The data in original format can be [downloaded here](https://www.kaggle.com/datasets/noorulhuda90/aaupdt/download?datasetVersionNumber=3).