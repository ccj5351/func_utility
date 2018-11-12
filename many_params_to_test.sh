#!/bin/bash
#echo "Hi, I'm sleeping for 13000 seconds..."
#sleep 13000s
#echo "all Done."

# case 1:
for i in $(seq 200 1 300) # sequence [200, 300], with step = 1 (the default step, could be removed)

# case 2:
for i in $(seq 200 300) # sequence [200, 300], with step = 1 (the default step, could be removed)

# case 3:
for i in 213 263 # array = [213, 263]
do 
	tmp=$(printf "%05d" "$i") #04 pad to length of 4
  predSaveDir='results/gcnet-sf-epo6-kt15-ft/disp-epo-'$(printf "%03d" "$i")'/'
  weight_file='./model/saved/cbmvnet-gc-regu-sf-epo6-kt15-ft/model-kt15-epoch300-epoch-'$tmp'.hdf5'
	#echo $predSaveDir
  python ./main_cbmv_keras.py --featuredata=$featuredata --f_imgset=$f_imgset --data=$data --upw=$upw --bs=$bs --bs_in_img=$bs_in_img_flag \
		--isTest=$isTest --predsavedir=$predSaveDir \
	  --weight_file=$weight_file 
done


declare -a disps=(
"disp0-iter-0" "disp0-iter-1"
)
for d in "${disps[@]}"
do
	#something you want to do;
	echo 'something'
done



