import cv2
import numpy as np
import matplotlib.pyplot as plt

def find_dominent_color(img_box, top_k):
  criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
  flags = cv2.KMEANS_RANDOM_CENTERS
  data = np.reshape(img_box, (-1,3))
  #data = img_box
  print("data ", data.shape)
  data = np.float32(data)
  compactness,labels,centers = cv2.kmeans(data,top_k,None,criteria,10,flags)
  #print('Dominant color is: bgr({})'.format(centers[0].astype(np.int32)))

  # Now separate the data, Note the flatten()
  size_list = [ (l, data[labels.ravel()==l].shape[0]) for l in range(top_k) ]

  #size_list2 = []
  #print ("label" , labels.shape)
  #for l in range(top_k):
  #  tmp = data[labels.ravel()==l]
  #  print ("lable %d " %l, tmp.shape)
  #  size_list2.append(tmp.shape[0])
  #print (size_list, size_list2)
  size_list = sorted(size_list, key = lambda v: v[1], reverse=True)
  #print (size_list)
  sorted_centers = [centers[i[0]] for i in size_list]
  return sorted_centers, size_list



if __name__ == "__main__":
  img = cv2.imread("/home/ccj/shoes_white.png")
  box = [
          [ # box1 
          {
              "x": 0.45544755,
              "y": 0.83132535
            },
            {
              "x": 0.6050424,
              "y": 0.83132535
            },
            {
              "x": 0.6050424,
              "y": 0.9597957
            },
            {
              "x": 0.45544755,
              "y": 0.9597957
            }
          ],

          [ # box 2
            {
              "x": 0.5977876,
              "y": 0.8656526
            },
            {
              "x": 0.82404524,
              "y": 0.8656526
            },
            {
              "x": 0.82404524,
              "y": 0.99006724
            },
            {
              "x": 0.5977876,
              "y": 0.99006724
            }

          ]
          # box 3 and so on;
      ]

  H, W = img.shape[0:2]
    
  # Window name in which image is displayed 
  window_name = 'Image Shoe'

  for bx in range(len(box)):
    print (bx)
    # Start coordinate, here (5, 5) 
    # # represents the top left corner of rectangle 
    i = 0
    start_point_x, start_point_y = int (box[bx][i]["x"]*W), int(box[bx][i]["y"]*H)
    print (start_point_x, start_point_y)
    
    # Ending coordinate, here (220, 220) 
    # represents the bottom right corner of rectangle 
    i = 2
    end_point_x, end_point_y = int (box[bx][i]["x"]*W), int(box[bx][i]["y"]*H)
    
    # given the boudnig boxs from the json file, to extract the target object region;
    img_box = img[start_point_y:end_point_y, start_point_x:end_point_x, :]
    # this is a hyper-perrameter you can tune for KMeans (for # of clusters) 
    top_k = 5
    top_k_colors, size_list = find_dominent_color(img_box, top_k)
    print('Top-{} Dominant color are:\n'.format(top_k))
    
    col_box_list = [img_box[:,:,::-1]]
    for i in range(0, top_k):
      print('idx {} dominant color is: rgb({}), has {} pixels'.format(
      i,
      top_k_colors[i][::-1].astype(np.int32),
      size_list[i]
      ))

      col_box = np.ones(img_box.shape)*top_k_colors[i][::-1]
      col_box_list.append(col_box)
    tmp_img = np.concatenate(col_box_list, axis = 1)
    plt.imshow(tmp_img.astype(np.uint8))
    plt.show()



    #hist_dominent_color(img_box, BINS = 20)
    
    # Blue color in BGR 
    #color = (255, 0, 0) 
      
    # Line thickness of 2 px 
    #thickness = 2
      
    # Using cv2.rectangle() method 
    # Draw a rectangle with blue line borders of thickness of 2 px 
    #image = cv2.rectangle(img, (start_point_x, start_point_y), (end_point_x, end_point_y), color, thickness) 
      
    # Displaying the image  
    #cv2.imshow(window_name, img)  
    #cv2.imwrite("/home/ccj/shoe_box.png", image)
