import os
import numpy as np
import SimpleITK as sitk
from medpy import metric


folds = 2
pred_dir1 = '/data1/FJ/nnUNet_raw_data_base/nnUNet_raw_data/Task503_BreastSeg/predict_final'
gt_dir = '/data1/FJ/nnUNet_raw_data_base/nnUNet_raw_data/Task503_BreastSeg/labelsTs'

pred_dir = pred_dir1 + '/' + 'fold_' + str(folds) + '/'
gt_dir = gt_dir + '/' + 'fold_' + str(folds) + '/'
method = 'result_fold_' + str(folds)
image_list = os.listdir(gt_dir)
image_list.sort()


def inference():
    total_metric = np.zeros((1, 6))
    print("Testing start")
    with open(pred_dir1 + "/{}.txt".format(method), "a") as f:
        for ids in range(len(image_list)):
            image_path = image_list[ids]
            save_name = image_path.split('.')[0]

            gt_path = gt_dir + image_path
            pred_path = pred_dir + image_path
            gt = sitk.ReadImage(gt_path)
            pred = sitk.ReadImage(pred_path)
            gt = sitk.GetArrayFromImage(gt)
            pred = sitk.GetArrayFromImage(pred)
            # print(gt.min(), gt.max(), pred.min(), pred.max())

            metric = calculate_metric_percase(gt == 1, pred == 1)
            total_metric[0, :] += metric
            print("{},{},{},{},{},{},{},{}\n".format(ids, save_name, metric[0], metric[1], metric[2], metric[3], metric[4], metric[5]))

            f.writelines("{},{},{},{},{},{},{},{}\n".format(
                ids, save_name, metric[0], metric[1], metric[2], metric[3], metric[4], metric[5]))

        f.writelines("Mean metrics,{},{},{},{},{},{}".format(total_metric[0, 0] / len(image_list), total_metric[0, 1] / len(
            image_list), total_metric[0, 2] / len(image_list), total_metric[0, 3] / len(image_list), total_metric[0, 4]
                                                       / len(image_list), total_metric[0, 5] / len(image_list)))
    f.close()
    print("Testing end")


def calculate_metric_percase(pred, gt):
    if pred.sum() > 0 and gt.sum() > 0:
        dice = metric.binary.dc(pred, gt)
        ravd = abs(metric.binary.ravd(pred, gt))
        hd = metric.binary.hd95(pred, gt)
        asd = metric.binary.asd(pred, gt)
        ppv = metric.binary.positive_predictive_value(pred, gt)
        sen = metric.binary.sensitivity(pred, gt)
        recall = metric.binary.recall(pred, gt)
        precising = metric.binary.precision(pred, gt)
        # return np.array([dice, ppv, sen, hd, recall, precising])
        return np.array([dice, ppv, sen, asd, ravd, hd])
    else:
        print('000000000000000000000000000000000000')
        return np.zeros(6)


if __name__ == "__main__":
    inference()


