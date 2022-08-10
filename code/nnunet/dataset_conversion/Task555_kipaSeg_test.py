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
    use data
    """

    task_name = "Task555_kipa"
    downloaded_data_dir = "/media/milab-2080ti/ProgrammerOfCyz/kipa2022/nnUNet_raw_data_base/nnUNet_raw_data/Task555_kipa/imagesTs_orig"

    target_base = join(nnUNet_raw_data, task_name)
    target_imagesTs = join(target_base, "imagesTs")

    maybe_mkdir_p(target_imagesTs)

    patient_names = []
    # for p in subdirs(downloaded_data_dir, join=False):
    for p in range(30):
        img = downloaded_data_dir + '/' + str(p+70) + '.nii.gz'

        patient_name = str(p+70)
        patient_names.append(patient_name)

        assert all([
            isfile(img)
        ]), "%s" % patient_name

        shutil.copy(img, join(target_imagesTs, patient_name + "_0000.nii.gz"))
