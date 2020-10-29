# import the necessary packages 
import cv2 
import argparse 
import os
import yaml

# now let's initialize the list of reference point 
ref_point = [] 
crop = False

door = 0
door_list = []

def shape_selection(event, x, y, flags, param): 
	# grab references to the global variables 
	global ref_point, crop, door 

	# if the left mouse button was clicked, record the starting 
	# (x, y) coordinates and indicate that cropping is being performed 
	if event == cv2.EVENT_LBUTTONDOWN: 
		ref_point = [(x, y)] 

	# check to see if the left mouse button was released 
	elif event == cv2.EVENT_LBUTTONUP: 
		# record the ending (x, y) coordinates and indicate that 
		# the cropping operation is finished 
		ref_point.append((x, y)) 

		# draw a rectangle around the region of interest 
		cv2.rectangle(image, ref_point[0], ref_point[1], (0, 255, 0), 2)

		door_list.append([ref_point[0][1], ref_point[1][1], ref_point[0][0], ref_point[1][0]])
		cv2.imshow("image", image) 

# construct the argument parser and parse the arguments 
ap = argparse.ArgumentParser() 
ap.add_argument("-i", "--video", required = True, help ="Path to the video") 
args = vars(ap.parse_args()) 

# grab the video file and read the first frame
vidcap = cv2.VideoCapture(args["video"])
success, frame = vidcap.read()

# load the frame, clone it, and setup the mouse callback function 
image = frame 
clone = image.copy() 
cv2.namedWindow("image") 
cv2.setMouseCallback("image", shape_selection) 


# keep looping until the 'q' key is pressed 
while True: 
	# display the image and wait for a keypress 
	cv2.imshow("image", image) 
	key = cv2.waitKey(1) & 0xFF

	# press 'r' to reset the window 
	if key == ord("r"): 
		image = clone.copy() 
    
	# if the 'q' key is pressed, break from the loop 
	elif key == ord("q"): 
		break
	
'''
if len(ref_point) == 2: 
	crop_img = clone[ref_point[0][1]:ref_point[1][1], ref_point[0][0]: 
														ref_point[1][0]] 
	cv2.imshow("crop_img", crop_img) 
	cv2.waitKey(0) 
'''

# close all open windows 
cv2.destroyAllWindows() 
#os.remove("tmp.jpg")
#print(ref_point)
#print(door_list)
door_dict = {}
count = 0
for i in range(0, len(door_list), 2):
	tmp = {}
	tmp["firstcheckpoint"] = door_list[i]
	tmp["secondcheckpoint"] = door_list[i+1]
	door_dict["Door"+str(count)] = tmp
	count += 1

#print(door_dict)
with open("door.yaml", 'w') as file:
	doc = yaml.dump(door_dict, file)