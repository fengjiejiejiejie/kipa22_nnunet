#    Copyright 2020 Division of Medical Image Computing, German Cancer Research Center (DKFZ), Heidelberg, Germany
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.


import numpy as np
from collections import OrderedDict

from batchgenerators.utilities.file_and_folder_operations import *
from nnunet.paths import nnUNet_raw_data
import SimpleITK as sitk
import shutil


if __name__ == "__main__":
    """
    use NAC data
    """

    task_name = "Task501_Breast"
    downloaded_data_dir = "/media/milab/FJ4T/3_breast_data/peng_copy/NACdata2"

    target_base = join(nnUNet_raw_data, task_name)
    target_imagesTr = join(target_base, "imagesTr")
    target_imagesVal = join(target_base, "imagesVal")
    target_imagesTs = join(target_base, "imagesTs")
    target_labelsTr = join(target_base, "labelsTr")

    maybe_mkdir_p(target_imagesTr)
    maybe_mkdir_p(target_imagesVal)
    maybe_mkdir_p(target_imagesTs)
    maybe_mkdir_p(target_labelsTr)

    patient_names = []
    for p in subdirs(downloaded_data_dir, join=False):
        patdir = join(downloaded_data_dir, p)
        patient_name = p
        patient_names.append(patient_name)
        t1c = join(patdir, "90.nii.gz")
        seg = join(patdir, "90S.nii.gz")

        assert all([
            isfile(t1c),
            isfile(seg)
        ]), "%s" % patient_name

        shutil.copy(t1c, join(target_imagesTr, patient_name + "_0000.nii.gz"))
        shutil.copy(seg, join(target_labelsTr, patient_name + ".nii.gz"))

    json_dict = OrderedDict()
    json_dict['name'] = "BreastTumorSeg"
    json_dict['description'] = "BreastTumorSegmentation_NACdata"
    json_dict['tensorImageSize'] = "3D"
    json_dict['reference'] = "nothing"
    json_dict['licence'] = "nothing"
    json_dict['release'] = "0.0"
    json_dict['modality'] = {
        "0": "T1c",
    }
    json_dict['labels'] = {
        "0": "background",
        "1": "tumor",
    }
    json_dict['numTraining'] = len(patient_names)
    json_dict['numTest'] = 0
    json_dict['training'] = [{'image': "./imagesTr/%s.nii.gz" % i, "label": "./labelsTr/%s.nii.gz" % i} for i in
                             patient_names]
    json_dict['test'] = []

    save_json(json_dict, join(target_base, "dataset.json"))

    # downloaded_data_dir = "/home/sdp/MLPERF/Brats2019_DATA/MICCAI_BraTS_2019_Data_Validation"
    #
    # for p in subdirs(downloaded_data_dir, join=False):
    #     patdir = join(downloaded_data_dir, p)
    #     patient_name = p
    #     t1 = join(patdir, p + "_t1.nii.gz")
    #     t1c = join(patdir, p + "_t1ce.nii.gz")
    #     t2 = join(patdir, p + "_t2.nii.gz")
    #     flair = join(patdir, p + "_flair.nii.gz")
    #
    #     assert all([
    #         isfile(t1),
    #         isfile(t1c),
    #         isfile(t2),
    #         isfile(flair),
    #     ]), "%s" % patient_name
    #
    #     shutil.copy(t1, join(target_imagesVal, patient_name + "_0000.nii.gz"))
    #     shutil.copy(t1c, join(target_imagesVal, patient_name + "_0001.nii.gz"))
    #     shutil.copy(t2, join(target_imagesVal, patient_name + "_0002.nii.gz"))
    #     shutil.copy(flair, join(target_imagesVal, patient_name + "_0003.nii.gz"))

    """
    #I dont have the testing data
    downloaded_data_dir = "/home/fabian/Downloads/BraTS2018_train_val_test_data/MICCAI_BraTS_2018_Data_Testing_FIsensee"

    for p in subdirs(downloaded_data_dir, join=False):
        patdir = join(downloaded_data_dir, p)
        patient_name = p
        t1 = join(patdir, p + "_t1.nii.gz")
        t1c = join(patdir, p + "_t1ce.nii.gz")
        t2 = join(patdir, p + "_t2.nii.gz")
        flair = join(patdir, p + "_flair.nii.gz")

        assert all([
            isfile(t1),
            isfile(t1c),
            isfile(t2),
            isfile(flair),
        ]), "%s" % patient_name

        shutil.copy(t1, join(target_imagesTs, patient_name + "_0000.nii.gz"))
        shutil.copy(t1c, join(target_imagesTs, patient_name + "_0001.nii.gz"))
        shutil.copy(t2, join(target_imagesTs, patient_name + "_0002.nii.gz"))
        shutil.copy(flair, join(target_imagesTs, patient_name + "_0003.nii.gz"))"""
