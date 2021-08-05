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
PATH_TO_LEFT_IMAGES="/data/ccjData/datasets/kitti-raw/2011_10_03_drive_0034_sync/image_02/data"
# right rgb images
PATH_TO_RIGHT_IMAGES="/data/ccjData/datasets/kitti-raw/2011_10_03_drive_0034_sync/image_03/data"
# gcnet-disparity
PATH_TO_PSM_IMAGES="/home/ccj/GCNet/results/gcnet-F8-RMSp-sf-epo30-4dsConv-k5-testKTRaw/disp-epo-030" 
# cbmv-gcnet disparity
PATH_TO_CBMV_IMAGES="/home/ccj/GCNet/results/cbmvnet-gc-F8-RMSp-sf-epo26Based-epo30-4dsConv-k5-testKTRaw/disp-epo-023"

print (PATH_TO_LEFT_IMAGES + '/0%09d.png'%(0))
left = cv2.imread(PATH_TO_LEFT_IMAGES+'/0%09d.png'%(0),-1)

for i in range(101, 199):
#for i in range(240, 300):
#for i in range(370, 400):
#for i in range(503, 504):
#for i in range(990, 1100):
#for i in range(1115, 1161):
#for i in range(0, 400):
#for i in range(599):
        src_limg_name = PATH_TO_LEFT_IMAGES+'/0%09d.png'%i
        left = cv2.imread(src_limg_name)[:,:,::-1]
        dst_limg_name = 'results/msnet-supp-figs/left/0%09d_L.png'%i
        os.system("cp {} {}".format(src_limg_name, dst_limg_name))
        
        src_rimg_name = PATH_TO_RIGHT_IMAGES+'/0%09d.png'%i
        right = cv2.imread(src_rimg_name)[:,:,::-1]
        dst_rimg_name = 'results/msnet-supp-figs/right/0%09d_R.png'%i
        os.system("cp {} {}".format(src_rimg_name, dst_rimg_name))
        # here we directly read the pfm disparity
	disp0 = kitti_colormap( pfm.load(PATH_TO_PSM_IMAGES+'/0%09d.pfm'%i) )
	disp1 = kitti_colormap( pfm.load(PATH_TO_CBMV_IMAGES+'/0%09d.pfm'%i) )
        w = disp0.shape[1]
        
        cv2.imwrite('results/msnet-supp-figs/disp_gc/0%06d_gc.png'%i, disp0[:,:,[2,1,0]])
        cv2.imwrite('results/msnet-supp-figs/disp_msgc/0%06d_msgc.png'%i, disp1[:,:,[2,1,0]])
        
        board_tmp = np.zeros((10, w, 3))
        collage = np.concatenate((left, board_tmp, right, board_tmp, disp0, board_tmp, disp1),0)
        cv2.imwrite('results/msnet-supp-figs/concat/0%06d_all.png'%i, collage[:,:,[2,1,0]])
sys.exit()



if 0:
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    #fourcc = cv2.VideoWriter_fourcc(*'MP4V')
    scale = 1
    #scale = 2
    out = cv2.VideoWriter('results/cbmv-gcnet-ndisp192-scl1.avi',fourcc,
            10.0,# fps 
            #20.0,# fps 
            #(left.shape[1]/2,left.shape[0]/2*3) # frameSize
            (left.shape[1]/scale,left.shape[0]/scale*3) # frameSize
            #(left.shape[1]/4,left.shape[0]/4*3) # frameSize
            )

    for i in range(0, 1150):
    #for i in range(0, 400):
    #for i in range(599):
            left = cv2.imread(PATH_TO_LEFT_IMAGES+'/0%09d.png'%i,-1)

            # disparities need to be saved in KITTI format (disp*256. as uint16)
            #disp0 = kitti_colormap( cv2.imread(PATH_TO_PSM_IMAGES+'/0%09d.png'%i,-1)/256.)
            #disp1 = kitti_colormap( cv2.imread(PATH_TO_CBMV_IMAGES+'/0%09d.png'%i,-1)/256.)
            # here we directly read the pfm disparity
            disp0 = kitti_colormap( pfm.load(PATH_TO_PSM_IMAGES+'/0%09d.pfm'%i) )
            disp1 = kitti_colormap( pfm.load(PATH_TO_CBMV_IMAGES+'/0%09d.pfm'%i) )
            
            #cv2.imwrite('results/0%06d_gcnet.png'%i, disp0[:,:,[2,1,0]])
            #cv2.imwrite('results/0%06d_cbmvgcnet.png'%i, disp1[:,:,[2,1,0]])

            collage = np.concatenate((left,disp0,disp1),0)
            collage = cv2.resize(collage, (left.shape[1]/scale, left.shape[0]/scale*3))
            #collage = cv2.resize(collage, (left.shape[1]/4, left.shape[0]/4*3))
            out.write(collage)
            if i % 20 == 0:
                print ('processing frame 0%09d.png'%i )
            # show image for debug only
            #cv2.imshow('disp', collage)
            #cv2.waitKey(1)

    out.release()
