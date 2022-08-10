import numpy as np
from collections import OrderedDict

from batchgenerators.utilities.file_and_folder_operations import *
from nnunet.paths import nnUNet_raw_data
import SimpleITK as sitk
import shutil


if __name__ == "__main__":
    """
    use  data
    """

    task_name = "Task504_singleT1c"
    downloaded_data_dir = "/media/fengjie/FJ4T/3_breast_data/cui_copy/breast_data5_sample"

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
        t1c = join(patdir, "90S.nii.gz")
        seg = join(patdir, "label.nii.gz")

        assert all([
            isfile(t1c),
            isfile(seg)
        ]), "%s" % patient_name

        shutil.copy(t1c, join(target_imagesTr, patient_name + "_0000.nii.gz"))
        shutil.copy(seg, join(target_labelsTr, patient_name + ".nii.gz"))

    json_dict = OrderedDict()
    json_dict['name'] = "BreastTumorSeg"
    json_dict['description'] = "BreastTumorSegmentation_single_t1c_data"
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
















