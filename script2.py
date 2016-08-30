import glob
import os

img_files = []

for img_file in os.listdir('/home/vagrant/src/fr_project/thing/stillCaptured'):
    if img_file.endswith('.jpg'):
        img_files.append(img_file)
        
# shows the list of files that are going to be sent over to OpenFace
print img_files

for each_img in img_files:
    os.chdir('/home/vagrant/src/fr_project')
    os.system("python -m thing.openface-master.demos.classifier infer thing/openface-master/classifier0823.pkl thing/stillCaptured/"+each_img)