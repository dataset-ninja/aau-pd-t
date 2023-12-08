# https://www.kaggle.com/datasets/noorulhuda90/aaupdt

import os, glob
import numpy as np
import supervisely as sly
from supervisely.io.fs import (
    get_file_name_with_ext,
    get_file_name,
    get_file_ext,
    file_exists,
    get_file_size,
)
from dotenv import load_dotenv
import supervisely as sly
import os
from dataset_tools.convert import unpack_if_archive
import src.settings as s
from urllib.parse import unquote, urlparse
from supervisely.io.fs import get_file_name, get_file_size
import shutil

from tqdm import tqdm


def download_dataset(teamfiles_dir: str) -> str:
    """Use it for large datasets to convert them on the instance"""
    api = sly.Api.from_env()
    team_id = sly.env.team_id()
    storage_dir = sly.app.get_data_dir()

    if isinstance(s.DOWNLOAD_ORIGINAL_URL, str):
        parsed_url = urlparse(s.DOWNLOAD_ORIGINAL_URL)
        file_name_with_ext = os.path.basename(parsed_url.path)
        file_name_with_ext = unquote(file_name_with_ext)

        sly.logger.info(f"Start unpacking archive '{file_name_with_ext}'...")
        local_path = os.path.join(storage_dir, file_name_with_ext)
        teamfiles_path = os.path.join(teamfiles_dir, file_name_with_ext)

        fsize = api.file.get_directory_size(team_id, teamfiles_dir)
        with tqdm(
            desc=f"Downloading '{file_name_with_ext}' to buffer...",
            total=fsize,
            unit="B",
            unit_scale=True,
        ) as pbar:
            api.file.download(team_id, teamfiles_path, local_path, progress_cb=pbar)
        dataset_path = unpack_if_archive(local_path)

    if isinstance(s.DOWNLOAD_ORIGINAL_URL, dict):
        for file_name_with_ext, url in s.DOWNLOAD_ORIGINAL_URL.items():
            local_path = os.path.join(storage_dir, file_name_with_ext)
            teamfiles_path = os.path.join(teamfiles_dir, file_name_with_ext)

            if not os.path.exists(get_file_name(local_path)):
                fsize = api.file.get_directory_size(team_id, teamfiles_dir)
                with tqdm(
                    desc=f"Downloading '{file_name_with_ext}' to buffer...",
                    total=fsize,
                    unit="B",
                    unit_scale=True,
                ) as pbar:
                    api.file.download(team_id, teamfiles_path, local_path, progress_cb=pbar)

                sly.logger.info(f"Start unpacking archive '{file_name_with_ext}'...")
                unpack_if_archive(local_path)
            else:
                sly.logger.info(
                    f"Archive '{file_name_with_ext}' was already unpacked to '{os.path.join(storage_dir, get_file_name(file_name_with_ext))}'. Skipping..."
                )

        dataset_path = storage_dir
    return dataset_path


def count_files(path, extension):
    count = 0
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(extension):
                count += 1
    return count


def convert_and_upload_supervisely_project(
    api: sly.Api, workspace_id: int, project_name: str
) -> sly.ProjectInfo:
    # project_name = "Thermal Person Detection"
    train_path = "/home/grokhi/rawdata/aau-pd-t/Data/Data/Train"
    test_path = "/home/grokhi/rawdata/aau-pd-t/Data/Data/Test"
    batch_size = 30
    images_folder = "/Images/"
    anns_folder = "/Annotations/"
    images_ext = ".jpg"
    ann_ext = ".txt"

    ds_name_to_images = {"train": train_path, "test": test_path}

    def create_ann(image_path):
        labels = []
        tags = []

        image_np = sly.imaging.image.read(image_path)[:, :, 0]
        img_height = image_np.shape[0]
        img_wight = image_np.shape[1]

        if ds_name == "train":
            tag_name = image_path.split("/")[-3].lower()
            tags = [sly.Tag(tag_meta) for tag_meta in tag_metas if tag_meta.name == tag_name]

        ann_path = image_path.replace(images_folder, anns_folder).replace(images_ext, ann_ext)

        if file_exists(ann_path):
            with open(ann_path) as f:
                content = f.read().split("\n")

                for curr_data in content:
                    if len(curr_data) != 0:
                        idx = 1
                        curr_data = list(map(float, curr_data.rstrip().split(" ")))
                        if len(curr_data) == 4:  # no class data in ann
                            idx = 0

                        left = int((curr_data[idx] - curr_data[idx + 2] / 2) * img_wight)
                        right = int((curr_data[idx] + curr_data[idx + 2] / 2) * img_wight)
                        top = int((curr_data[idx + 1] - curr_data[idx + 3] / 2) * img_height)
                        bottom = int((curr_data[idx + 1] + curr_data[idx + 3] / 2) * img_height)
                        rectangle = sly.Rectangle(top=top, left=left, bottom=bottom, right=right)
                        label = sly.Label(rectangle, obj_class)
                        labels.append(label)

        return sly.Annotation(img_size=(img_height, img_wight), labels=labels, img_tags=tags)

    obj_class = sly.ObjClass("person", sly.Rectangle)
    # subfolder_meta = sly.TagMeta("subfolder", sly.TagValueType.ANY_STRING)
    tag_names = [
        "far_viewpoint",
        "good_condition",
        "low_resolution",
        "occlusion",
        "opposite_temperature",
        "shadow",
        "similar_temperature",
        "snow",
        "wind",
    ]
    tag_metas = [sly.TagMeta(name, sly.TagValueType.NONE) for name in tag_names]

    project = api.project.create(workspace_id, project_name, change_name_if_conflict=True)
    meta = sly.ProjectMeta(obj_classes=[obj_class], tag_metas=tag_metas)
    api.project.update_meta(project.id, meta.to_json())

    for ds_name, ds_data in ds_name_to_images.items():
        dataset = api.dataset.create(project.id, ds_name, change_name_if_conflict=True)

        images_pathes = glob.glob(ds_data + "/*/*/*.jpg")
        if len(images_pathes) == 0:
            images_pathes = glob.glob(ds_data + "/*/*.jpg")

        progress = sly.Progress("Create dataset {}".format(ds_name), len(images_pathes))

        for img_pathes_batch in sly.batched(images_pathes, batch_size=batch_size):
            img_names_batch = [
                im_path.split("/")[-3] + "_" + get_file_name_with_ext(im_path)
                for im_path in img_pathes_batch
            ]

            img_infos = api.image.upload_paths(dataset.id, img_names_batch, img_pathes_batch)
            img_ids = [im_info.id for im_info in img_infos]

            anns = [create_ann(image_path) for image_path in img_pathes_batch]
            api.annotation.upload_anns(img_ids, anns)

            progress.iters_done_report(len(img_names_batch))
    return project
