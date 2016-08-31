import glob
import os

img_files = []

for img_file in os.listdir('/home/vagrant/src/fr_project/thing/static/demoFaces'):
    if img_file.endswith('.jpg'):
        img_files.append(img_file)

for each_img in img_files:
    os.chdir('/home/vagrant/src/fr_project')
    os.system("python -m thing.openface-master.demos.classifier infer thing/openface-master/classifier0823.pkl thing/static/demoFaces/"+each_img)