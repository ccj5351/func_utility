import cv2
import numpy as np
import sys
import os
sys.path.append('src')
import pfmutil as pfm 

def kitti_colormap(disparity, maxval=-1):
	"""
	A utility function to reproduce KITTI fake colormap
	Arguments:
	- disparity: numpy float32 array of dimension HxW
	- maxval: maximum disparity value for normalization (if equal to -1, the maximum value in disparity will be used)
	
	Returns a numpy uint8 array of shape HxWx3.
	"""
	if maxval < 0:
		maxval = np.max(disparity)
                #print ('maxval = %f' % maxval)

	colormap = np.asarray([[0,0,0,114],[0,0,1,185],[1,0,0,114],[1,0,1,174],[0,1,0,114],[0,1,1,185],[1,1,0,114],[1,1,1,0]])
	weights = np.asarray([8.771929824561404,5.405405405405405,8.771929824561404,5.747126436781609,8.771929824561404,5.405405405405405,8.771929824561404,0])
	cumsum = np.asarray([0,0.114,0.299,0.413,0.587,0.701,0.8859999999999999,0.9999999999999999])

	colored_disp = np.zeros([disparity.shape[0], disparity.shape[1], 3])
	values = np.expand_dims(np.minimum(np.maximum(disparity/maxval, 0.), 1.), -1)
	bins = np.repeat(np.repeat(np.expand_dims(np.expand_dims(cumsum,axis=0),axis=0), disparity.shape[1], axis=1), disparity.shape[0], axis=0)
	diffs = np.where((np.repeat(values, 8, axis=-1) - bins) > 0, -1000, (np.repeat(values, 8, axis=-1) - bins))
	index = np.argmax(diffs, axis=-1)-1

	w = 1-(values[:,:,0]-cumsum[index])*np.asarray(weights)[index]


	colored_disp[:,:,2] = (w*colormap[index][:,:,0] + (1.-w)*colormap[index+1][:,:,0])
	colored_disp[:,:,1] = (w*colormap[index][:,:,1] + (1.-w)*colormap[index+1][:,:,1])
	colored_disp[:,:,0] = (w*colormap[index][:,:,2] + (1.-w)*colormap[index+1][:,:,2])

	return (colored_disp*np.expand_dims((disparity>0),-1)*255).astype(np.uint8)



# left rgb images
PATH_TO_LEFT_IMAGES="/media/ccjData2/datasets/KITTI-2015/training/left"
PATH_TO_LEFT_DISP_GT="/media/ccjData2/datasets/KITTI-2015/training/disp_occ_0_pfm"
# right rgb images
PATH_TO_RIGHT_IMAGES="/media/ccjData2/datasets/KITTI-2015/training/right"
# gcnet-disparity
PATH_TO_DISP_CBMV_IMAGES="/media/ccjData2/research-projects/kitti-devkit/results/cbmvnet-gc-F8-RMSp-sf-epo26Based-epo30-4dsConv-k5-testKT15/result_disp_img_0" 
# cbmv-gcnet disparity
PATH_TO_DISP_GC_IMAGES="/media/ccjData2/research-projects/kitti-devkit/results/gcnet-F8-RMSp-sf-epo30-4dsConv-k5-testKT15/result_disp_img_0"

# error gcnet-disparity
PATH_TO_ERR_CBMV_IMAGES="/media/ccjData2/research-projects/kitti-devkit/results/cbmvnet-gc-F8-RMSp-sf-epo26Based-epo30-4dsConv-k5-testKT15/errors_disp_img_0" 
# error cbmv-gcnet disparity
PATH_TO_ERR_GC_IMAGES="/media/ccjData2/research-projects/kitti-devkit/results/gcnet-F8-RMSp-sf-epo30-4dsConv-k5-testKT15/errors_disp_img_0"

if 0:
    for i in range(0, 200):
        src_limg_name = PATH_TO_LEFT_IMAGES+'/%06d_10.png'%i
        dst_limg_name = 'results/msnet-supp-figs/kt15/left/%06d_L_10.png'%i
        os.system("cp {} {}".format(src_limg_name, dst_limg_name))
        
        src_rimg_name = PATH_TO_RIGHT_IMAGES+'/%06d_10.png'%i
        dst_rimg_name = 'results/msnet-supp-figs/kt15/right/%06d_R_10.png'%i
        os.system("cp {} {}".format(src_rimg_name, dst_rimg_name))
        
        dispGT = pfm.load(PATH_TO_LEFT_DISP_GT+'/%06d_10.pfm'%i)
        dispGT[dispGT == np.inf] = .0
        dispGT = kitti_colormap( dispGT)
        # here we directly read the pfm disparity
        #disp0 = kitti_colormap( pfm.load(PATH_TO_DISP_GC_IMAGES+'/%06d.pfm'%i) )
        #disp1 = kitti_colormap( pfm.load(PATH_TO_DISP_CBMV_IMAGES+'/0%09d.pfm'%i) )
        disp0 = cv2.imread(PATH_TO_DISP_GC_IMAGES + '/%06d_10.png'%i)
        print (PATH_TO_DISP_GC_IMAGES + '/%06d.png'%i)
        disp1 = cv2.imread(PATH_TO_DISP_CBMV_IMAGES+'/%06d_10.png'%i)
        w = disp0.shape[1]
        
        disp0_err = cv2.imread(PATH_TO_ERR_GC_IMAGES+'/%06d_10.png'%i)
        disp1_err = cv2.imread(PATH_TO_ERR_CBMV_IMAGES+'/%06d_10.png'%i)
        
        cv2.imwrite('results/msnet-supp-figs/kt15/disp_gc/%06d_10_gc.png'%i, disp0)
        cv2.imwrite('results/msnet-supp-figs/kt15/disp_msgc/%06d_10_msgc.png'%i, disp1)
        cv2.imwrite('results/msnet-supp-figs/kt15/disp_GT/%06d_10_gt.png'%i, dispGT[:,:,::-1])
        
        board_tmp = np.zeros((10, w, 3))
        collage = np.concatenate((disp0, board_tmp, disp1, board_tmp, disp0_err, board_tmp, disp1_err),0)
        cv2.imwrite('results/msnet-supp-figs/kt15/concat/%06d_10_all.png'%i, collage)

if 1: #KT15
    for i in [2, 54, 100, 104, 128, 136, 150, 166, 199]:
    #for i in [2]:
        tmp_src_root = './results/msnet-supp-figs/kt15/'
        tmp_dst_root = './results/msnet-supp-figs/kt15/'
        src_lists = [
                tmp_src_root + 'disp_gc/%06d_10_gc.png'%i, 
                tmp_src_root + 'disp_msgc/%06d_10_msgc.png'%i, 
                tmp_src_root + 'disp_GT/%06d_10_gt.png'%i,
                PATH_TO_LEFT_IMAGES+'/%06d_10.png'%i,
                PATH_TO_RIGHT_IMAGES+'/%06d_10.png'%i,
                PATH_TO_ERR_GC_IMAGES+'/%06d_10.png'%i,
                PATH_TO_ERR_CBMV_IMAGES+'/%06d_10.png'%i,
                ]
        dst_lists = [
                tmp_dst_root + '%06d_10_gc.png'%i, 
                tmp_dst_root + '%06d_10_msgc.png'%i, 
                tmp_dst_root + '%06d_10_gt.png'%i,
                tmp_dst_root + '%06d_L_10.png'%i,
                tmp_dst_root + '%06d_R_10.png'%i,
                tmp_dst_root + '%06d_10_gc_err.png'%i,
                tmp_dst_root + '%06d_10_msgc_err.png'%i,
                ]
        for t in range(len(src_lists)):
            #print("cp {} {}".format(src_lists[t], dst_lists[t]))
            tmp_in = cv2.imread(src_lists[t])
            h, w = tmp_in.shape[0:2]
            #print (h,w)
            scale = 4
            resized = cv2.resize(tmp_in, (w//scale, h//scale), interpolation = cv2.INTER_AREA)
            #print (resized.shape)
            cv2.imwrite(dst_lists[t], resized)
            print ('save ', dst_lists[t])
            #os.system("cp {} {}".format(src_lists[t], dst_lists[t]))

if 0:   # Middlebury
        from os import listdir
        from os.path import isfile, join
        tmp_src_root = './results/msnet-supp-figs/mbv3/'
        tmp_dst_root = './results/msnet-supp-figs/mbv3/resized'
        imgs_lists = [f for f in listdir(tmp_src_root) if isfile(join(tmp_src_root, f))]
        
        H_size = {'Jadeplant': 248,  'Piano': 240, 'Pipes':242, 
                'PlaytableP': 231, 'Recycle': 243, 'Teddy': 187
                }
        for img in imgs_lists:
            for i in ['Jadeplant', 'Piano', 'Pipes', 'PlaytableP', 'Recycle', 'Teddy']:
                if i in img:
                    print("reading {}".format(join(tmp_src_root, img)))
                    tmp_in = cv2.imread(join(tmp_src_root, img))
                    h, w = tmp_in.shape[0:2]
                    print (h,w)
                    scale = h // H_size[i]
                    resized = cv2.resize(tmp_in, (w//scale, h//scale), interpolation = cv2.INTER_AREA)
                    print (resized.shape)
                    cv2.imwrite(join(tmp_dst_root, img), resized)
                    print ('save ', join(tmp_dst_root, img))
                    #os.system("cp {} {}".format(src_lists[t], dst_lists[t]))
                else:
                    pass

if 0:   # KT Raw
        from os import listdir
        from os.path import isfile, join
        tmp_src_root = './results/msnet-supp-figs/kt-raw/'
        tmp_dst_root = './results/msnet-supp-figs/kt-raw/resized-quart'
        imgs_lists = [f for f in listdir(tmp_src_root) if isfile(join(tmp_src_root, f))]
        
        for img in imgs_lists:
            print("reading {}".format(join(tmp_src_root, img)))
            tmp_in = cv2.imread(join(tmp_src_root, img))
            h, w = tmp_in.shape[0:2]
            print (h,w)
            scale = 4
            resized = cv2.resize(tmp_in, (w//scale, h//scale), interpolation = cv2.INTER_AREA)
            print (resized.shape)
            cv2.imwrite(join(tmp_dst_root, img), resized)
            print ('save ', join(tmp_dst_root, img))
