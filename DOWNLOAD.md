Dataset **AAU-PD-T** can be downloaded in [Supervisely format](https://developer.supervisely.com/api-references/supervisely-annotation-json-format):

 [Download](https://assets.supervisely.com/supervisely-supervisely-assets-public/teams_storage/L/C/xW/QIS8KnSN2IJA7da9BynS4APzl4qgMdINY8iOTw6fTNmFqT3GIO3HntuWbdr1m5cfRBM3MVy0c3OiBVJIDzzJM0wLwPFUdILAsEdkzvl1QX64v3gP0o8SDmABVvVA.tar)

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