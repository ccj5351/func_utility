import os
import glob
import rawpy
import imageio

def convert_nef_to_jpg(input_file, output_file, quality=90):
    with rawpy.imread(input_file) as raw:
        rgb_image = raw.postprocess()
    imageio.imwrite(output_file, rgb_image, format='JPEG', quality=quality)

def batch_convert_nef_to_jpg(input_dir, output_dir, quality=90):
    input_files = glob.glob(os.path.join(input_dir, '*.NEF'))
    print (f"found {len(input_files)} nef raw images")
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    for input_file in input_files:
        file_name = os.path.splitext(os.path.basename(input_file))[0]
        output_file = os.path.join(output_dir, f'{file_name}.jpg')
        if not os.path.exists(output_file):
            convert_nef_to_jpg(input_file, output_file, quality)
            print(f'Converted {input_file} to {output_file}')

if __name__ == "__main__":
    # Usage example
    input_dir = '/home/ccj/tmp'
    #quality = 85  # An integer between 1 and 100
    quality = 95  # An integer between 1 and 100
    output_dir = f'/home/ccj/tmp_jpeg_cq{quality}'

    batch_convert_nef_to_jpg(input_dir, output_dir, quality)
