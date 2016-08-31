""" Adgnosco: Nest API """
import os
import requests
import json
import urllib
import dateutil.parser
import datetime

def get_nest_api():
    access_token = os.environ['ACCESS_TOKEN']
    camera = os.environ['CAMERA']
    result = requests.get('https://developer-api.nest.com/?auth='+access_token, 
                           stream=True,
                           headers={"Accept":"text/event-stream"})

    for chunk in result.iter_lines():
        print chunk[:6]
        if len(chunk) > 100:
            data_chunk = json.loads(chunk[6:])
            data = data_chunk['data']
            devices = data['devices']
            camera_data = devices['cameras']
            camera_used = camera_data[camera]
            last_event = camera_used['last_event']
            animated_image = last_event['animated_image_url']
            still_image = last_event['image_url']    
            timestampy = last_event['start_time']
            current_datetime = (dateutil.parser.parse(timestampy)) - datetime.timedelta(hours=7)
            current_datetime_str = current_datetime.strftime('%Y-%m-%d-%H-%M-%S')
            print "animated:", animated_image
            print "still: ", still_image
            print "when: ", timestampy        

            # --- This is for the demo, where we only display the .gifs to see that the Nest API works ---
            # os.chdir('/home/vagrant/src/fr_project/thing/stillCaptured')
            # urllib.urlretrieve(still_image, current_datetime_str+'.jpg')
            os.chdir('/home/vagrant/src/fr_project/thing/static/demoAPI')
            urllib.urlretrieve(animated_image, current_datetime_str+'.gif')

            imgs_to_del=[]
            for img_file in os.listdir('/home/vagrant/src/fr_project/thing/static/demoAPI'):
                if img_file.endswith('.jpg'):
                    imgs_to_del.append(img_file)

            for each_img in imgs_to_del[:11]:
                os.chdir('/home/vagrant/src/fr_project/thing/static/demoAPI')
                os.system("python -rm " + each_img)

get_nest_api()
            