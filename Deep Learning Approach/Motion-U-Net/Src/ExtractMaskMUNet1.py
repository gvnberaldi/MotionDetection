###########################################################################
#
#  Program Name: Extract Mask MU-Net1
#                
#################################################################
#                
#  Author: Gani Rahmon & Kannappan Palaniappan
#  
#  Copyright(C)2020-2021. G. Rahmon, K. Palaniappan and      
#             Curators of the University of Missouri, a          
#             public corporation. All Rights Reserved.
#
#  Created by
#  Gani Rahmon & Kannappan Palaniappan
#  Department of Electrical Engineering and Computer Science,
#  University of Missouri-Columbia
#  For more information, contact:
#
#      Gani Rahmon
#      211 Naka Hall (EBW)  
#      University of Missouri-Columbia
#      Columbia, MO 65211
#      grzc7@mail.missouri.edu
# 
# or
#      Dr. K. Palaniappan
#      205 Naka Hall (EBW)
#      University of Missouri-Columbia
#      Columbia, MO 65211
#      palaniappank@missouri.edu
#
###########################################################################
#  
#  Script ExtractMaskMUNet1.py
#  Desc:
#        Main script used to extract mask using trained model of MU-Net1
#
#  Inputs:
#       Put your inputs inside data/testData/ folder
#       change extensions accordingly while loading the paths 
#             
#  Outputs: masks
#        
###########################################################################

import torch
import numpy as np
import glob
import os
import imageio
import torch.nn.functional as F
from tqdm import tqdm
from pythonCodes.testDataLoader import MU_Net1_TestDataLoader
from pythonCodes.MUNet import MUNet


def get_predicted_mask(dataset_path, chosen_dataset, video_path):
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    numClass = 1
    model = MUNet(numClass).to(device)

    # load trained model
    #model = torch.load('./models/MUNet1.pt')

    # load pre-trained weights
    model.load_state_dict(torch.load(os.path.join(os.path.dirname(__file__), '..\\weights\\MU_Net1_Weights.pt'), map_location='cpu'))
    model.eval()

    # path to the test image
    # change folder name and extension according to your test images
    folderTestData = sorted(glob.glob(os.path.join(dataset_path, video_path, 'input\\*.jpg')))
    testDataset = MU_Net1_TestDataLoader(folderTestData)
    testLoader = torch.utils.data.DataLoader(testDataset, batch_size=1, shuffle=False)

    # set mask path
    maskDir = os.path.join(os.path.join(os.path.dirname(__file__), f'outputMaskMUNet1\\{chosen_dataset}', video_path))

    # create path if not exist
    if not os.path.exists(maskDir):
        os.makedirs(maskDir)

    for i, inputs in tqdm(enumerate(testLoader), total=len(testLoader), desc="Processing Frames"):

        inputs = inputs.to(device)

        # Predict
        pred = model(inputs)

        # The loss functions include the sigmoid function.
        pred = F.sigmoid(pred)
        pred = pred.data.cpu().numpy()

        outPred = pred[0].squeeze()
        outPredNorm = 255 * outPred
        outPredUint8 = outPredNorm.astype(np.uint8)

        # get frame name from original frame and replace in with bin and extension of jpg to png
        # change accordingly replace functions for your test inputs
        fname = os.path.basename(folderTestData[i]).replace('in','gt').replace('jpg','png')
        imageio.imwrite(os.path.join(maskDir, fname), outPredUint8)

    print('Testing finished')
