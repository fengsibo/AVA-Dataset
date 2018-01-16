# encoding=utf-8
import cv2
import pandas as pd
import os
import time
import math
from PIL import Image
import numpy as np

# TYPE = 'train'
TYPE = 'test'
AVA_folder_path = "G:/AVA/" + TYPE
sava_path = "new_image"
# ISOTIMEFORMAT='%

def getFrame(row):
    if row['status'] == 0:
        return
    image_foler = os.path.join("image/"+TYPE+'/'+str(row['action_id']))
    if not os.path.isdir(image_foler):
        os.mkdir(image_foler)
    video_path = os.path.join(AVA_folder_path, row['video_id'], row['video_id'] + '.mp4')
    print(video_path)
    imagename = row['video_id']
    second = row['middle_frame_timestamp']
    videoCapture = cv2.VideoCapture(video_path)
    fps = videoCapture.get(cv2.CAP_PROP_FPS)
    size = (int(videoCapture.get(cv2.CAP_PROP_FRAME_HEIGHT)),
            int(videoCapture.get(cv2.CAP_PROP_FRAME_WIDTH)))
    numFrame = videoCapture.get(cv2.CAP_PROP_FRAME_COUNT)
    print(fps, size, numFrame)
    flag, frame = videoCapture.read()
    i = 1
    middel_frame = int(fps)*int(second) - int(fps/2)
    print("middel_frame:", middel_frame)
    while flag:
        if i == middel_frame:
            image_path = image_foler + '/' + imagename + '_' + str(second) + '_' + str(time.time()) + '.jpg'
            cv2.imwrite(image_path, frame)
            print("save image to " + image_path)
            videoCapture.release()
            return
        i = i + 1
        flag, frame = videoCapture.read()
    videoCapture.release()

def getFrames2(data_block):
    # 判断status(该视频是否存在)
    index_list = list(data_block.index)
    index = index_list[0]
    if data_block.status[index] == 0:
        return
    image_num, _ = data_block.shape
    video_id = data_block.video_id[index]  # get the video id
    video_path = os.path.normpath(os.path.join(AVA_folder_path, video_id, video_id + '.mp4'))
    print("found {} path at {}".format(video_id, video_path))

    # 打开视频， 获取视频的基本信息
    videoCapture = cv2.VideoCapture(video_path)
    video_fps = int(math.ceil(videoCapture.get(cv2.CAP_PROP_FPS)))
    video_size = (int(videoCapture.get(cv2.CAP_PROP_FRAME_HEIGHT)),
                  int(videoCapture.get(cv2.CAP_PROP_FRAME_WIDTH)))
    numFrame = int(videoCapture.get(cv2.CAP_PROP_FRAME_COUNT))
    print("[INFO VIDEO {}] video_fps:{} video_size:{} video _frames:{}".format(video_id, video_fps, video_size, numFrame))

    middel_frame_list = []
    for i in index_list:
        middel_frame = video_fps * int(data_block.ix[i]['middle_frame_timestamp']) - math.ceil(video_fps / 2)
        middel_frame_list.append(middel_frame)


    video_flag, video_frame = videoCapture.read()
    frame = 0
    current_num = 0
    while video_flag:
        if frame in middel_frame_list:
            for i in index_list:
                middel_frame = video_fps * int(data_block.ix[i]['middle_frame_timestamp']) - math.ceil(video_fps / 2)
                if frame == middel_frame:
                    video_id = data_block.ix[i]['video_id']
                    second = str(data_block.ix[i]['middle_frame_timestamp'])
                    x1 = data_block.ix[i]['x1']
                    y1 = data_block.ix[i]['y1']
                    x2 = data_block.ix[i]['x2']
                    y2 = data_block.ix[i]['y2']
                    action_id = str(data_block.ix[i]['action_id'])
                    image_folder = os.path.join(sava_path, TYPE, video_id) # 保存文件路径
                    if not os.path.isdir(image_folder):
                        os.makedirs(image_folder)
                    str_list = [video_id, second, str(middel_frame), str(x1), str(y1), str(x2), str(y2),
                                action_id + ".jpg"]
                    image_path = os.path.join(image_folder, '='.join(str_list))
                    cv2.imwrite(image_path, video_frame)
                    print("save image to " + image_path, "middle frame:", middel_frame, "middle_frame_timestamp",
                          second)
                    current_num += 1
        if current_num == image_num:
            break

        frame+=1
        video_flag, video_frame = videoCapture.read()
    videoCapture.release()



if __name__ == "__main__" :
    if not os.path.isdir(sava_path):
        os.mkdir(sava_path)
        os.mkdir(os.path.join(sava_path, 'train'))
        os.mkdir(os.path.join(sava_path, 'test'))

    csvfile = pd.read_csv("csv/ava_" + TYPE + "_v1.0.csv")
    m, n = csvfile.shape
    # file = pd.DataFrame(csvfile)
    video_id_set = list(set(list(csvfile['video_id'])))
    video_id_set.sort()
    video_id_num = video_id_set.__len__()

    # print(video_id_set)
    # video_id_list = ['-5KQ66BBWC4', '0f39OWEqJ24', '20TAGRElvfE', '26V9UzqSguo', '2PpxiG0WU18', '2XeFK-DTSZk', '2bxKkUgcqpk',
    #  '2fwni_Kjf2M', '32HR3MnDZ8g', '4gVsDd8PV9U', '4trIFq61-lk', '55Ihr6uVIDA', '5BDj0ow5hnA', '5YPjcdLbs5g',
    #  '6d5u6FHvz7Q', '7nHkh4sP5Ks', '8aMv-ZGD4ic', '914yZXz-iRs', '9F2voT6QWvQ', '9Y_l9NsnYE0', '9bK05eBt1GM',
    #  '9mLYmkonWZQ', 'AN07xQokfiE', 'AYebXQ8eUkM', 'Ag-pXiLrd48', 'B1MAUxpKaV8', 'BY3sZmvUp-0', 'CZ2NP8UsPuE',
    #  'CrlfWnsS7ac', 'D-BJTU6NxZ8', 'Db19rWN5BGo', 'Di1MG6auDYo', 'E7JcKooKVsM', 'EQZWzLyx-GM', 'Ecivp8t3MdY',
    #  'Ekwy7wzLfjc', 'F3dPH6Xqf5M', 'F_-zE1dQsso', 'G3nRbyu0gMs', 'G5Yr20A5z_Q', 'Gvp-cj3bmIY', 'HJzgJ9ZjvJk',
    #  'Hi8QeP_VPu0', 'HymKCzQJbB8', 'J1jDc2rTJlg', 'J4bt4y9ShTA', 'K--hW14uzA0', 'KVq6If6ozMY', 'KWoSGtglCms',
    #  'K_SpqDJnlps', 'Kb1fduj-jdY', 'Ksd1JQFHYWA', 'Ma2hgTmveKQ', 'N0Dt9i9IUNg', 'N1K2bEZLL_A', 'N5UD8FGzDek',
    #  'N7baJsMszJ0', 'NEQ7Wpf-EtI', 'OGNnUvJq9RI', 'O_NYCUhZ9zw', 'OfMdakd4bHI', 'Ov0za6Xb1LM', 'P90hF2S1JzA',
    #  'PNZQ2UJfyQE', 'QCLQYnt3aMo', 'QMwT7DFA5O4', 'Riu4ZKk4YdQ', 'RvdxDMfMtiA', 'S0tkhGJjwLA', 'T-Fc9ctuNVI',
    #  'TcT4TxCxn_Q', 'TzaVHtLXOzY', 'U6m3kNFjdTs', 'UIy730JrFIc', 'UOyyTUX5Vo4', 'U_WzY2k8IBM', 'UgZFdrNT6W0',
    #  'VMNmRlhFT-o', 'VsYPP2I0aUQ', 'WKqbLbU68wU', 'WVde9pyaHg4', 'WlgxRNCHQzw', 'WwoTG3_OjUg', 'XV_FF3WC7kA',
    #  'YYWdB7h1INo', 'ZFQ3lF6yq_E', '_2Isct32Msg', '_a9SWtcaNj8', '_dBTTYDRdRQ', '_mAfwH6i90E', 'aDEYi1OG0vU',
    #  'b5pRYl_djbs', 'bhlFavrh7WU', 'c9pEMjPT16M', 'cKA-qeZuH_w', 'cWYJHb25EVs', 'er7eeiJB6dI', 'fD6VkIRlIRI',
    #  'fNcxxBjEOgw', 'fpprSy6AzKk', 'gjdgj04FzR0', 'hHgg9WI8dTk', 'hbYvDvJrpNk', 'iK4Y-JKRRAc', 'iSlDMboCSao',
    #  'issue-FaXLcSFjUI', 'issue-IELREHX_js', 'jgAwJ0RqmYg', 'jqZpiHlJUig', 'l-jxh8gpxuY', 'l2XO3tQk8lI', 'lDmLcWWBp1E',
    #  'lSCEt_mCHlM', 'lT1zdTL-3SM', 'lWXhqIAvarw', 'ly1upu2FNTs', 'mfsbYdLx9wE', 'nxL0yqWP3H0', 'o4xQ-BEa3Ss',
    #  'oD_wxyTHJ2I', 'oq_bufAhyl8', 'pLJ7bC5Vcqw', 'phVLLTMzmKk', 'phrYEKv0rmw', 'plkJ45_-pMk', 'qBUu7cy-5Iw',
    #  'qx2vAO5ofmo', 'r2llOyS-BmE', 'rFgb2ECMcrY', 'rUYsoIIE37A', 'rXFlJbXyZyc', 'rk8Xm0EAOWs', 'sADELCyj10I',
    #  'sUVhd0YTKgw', 'skiZueh4lfY', 't0V4drbYDnc', 't1LXrJOvPDg', 'tNpZtigMc4g', 'tghXjom3120', 'tjqCzVjojCo',
    #  'tt0t_a1EDCE', 'u1ltv6r14KQ', 'uNT6HrrnqPU', 'uPJPNPbWMFk', 'uwW0ejeosmk', 'uzPI7FcF79U', 'vfjywN5CN0Y',
    #  'x-6CtPWVi6E', 'xO4ABy2iOQA', 'xmqSaQPzL1E', 'xp67EC-Hvwk', 'y7ncweROe9U', 'yMtGmGa8KZ0', 'yo-Kg2YxlZs']

    # # for id in video_id_set:
    for i in range(video_id_num):
        data_block = csvfile[csvfile.video_id == video_id_set[i]]
        getFrames2(data_block)

    # video_id = '0f39OWEqJ24'
    # data_block = csvfile[csvfile.video_id == video_id]
    # data_block = pd.DataFrame(data_block)
    # getFrames2(data_block)
    # # print(data_block.index)
