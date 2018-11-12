cd /home/ccj/GCNet/model/cbmvnet-gc-regu-sf-epo2-kt15-ft/
a=13
for i in *.hdf5; do
	new=$(printf "%05d.hdf5" "$a") #04 pad to length of 4
	mv -i -- "$i" "${i:0:14}-$new"
	let a=a+1
done
exit

#https://unix.stackexchange.com/questions/121570/rename-multiples-files-using-bash-scripting
#That simply matches the first 4 numbers and swaps them for the ones you specified, here '2503'.
rename 's/\d{4}/2503/' file*

