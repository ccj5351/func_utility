#!/bin/bash
#echo "Hi, I'm sleeping for 13000 seconds..."
#sleep 13000s
#echo "all Done."

# constantly check file exists or not, if exists, then do some experiments;
weight_file='./model/cbmvnet-gc-regu-sf-epo5-F8/model-sf-epoch5-epoch-00005.hdf5'
while [ ! -f $weight_file ]
do
  echo "File ${weight_file} not found!"
  echo  "sleep 1200s"
  sleep 1200
done
#---------
# do whatever you do, once found the above file;
#---------

#for i in $(seq 200 300)
for i in 213 263
do 
  tmp=$(printf "%05d" "$i") #04 pad to length of 4
  predSaveDir='results/gcnet-sf-epo6-kt15-ft/disp-epo-'$(printf "%03d" "$i")'/'
  weight_file='./model/saved/cbmvnet-gc-regu-sf-epo6-kt15-ft/model-kt15-epoch300-epoch-'$tmp'.hdf5'
  #echo $predSaveDir
  python ./main_cbmv_keras.py --featuredata=$featuredata --f_imgset=$f_imgset --data=$data --upw=$upw --bs=$bs --bs_in_img=$bs_in_img_flag \
    --isTest=$isTest --predsavedir=$predSaveDir \
    --weight_file=$weight_file	 
done
