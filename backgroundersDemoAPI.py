""" Adgnosco: Nest API """
import os
import requests
import json
import urllib
import dateutil.parser
import datetime
# from flask import Flask, render_template, request, flash, redirect, session, jsonify
# from flask_debugtoolbar import DebugToolbarExtension

# app = Flask(__name__)

# app.secret_key = "some secret"


# stop_me = False
# @app.route('/')
# def index():
#     """Homepage."""

#     return render_template("homepage.html")


# @app.route('/start')
def get_nest_api():

    global stop_me
    access_token = os.environ['ACCESS_TOKEN']
    camera = os.environ['CAMERA']
    result = requests.get('https://developer-api.nest.com/?auth='+access_token, 
                           stream=True,
                           headers={"Accept":"text/event-stream"})



    for chunk in result.iter_lines():
        print chunk[:6]
        imgs_to_del=[]
        for img_file in os.listdir('/home/vagrant/src/fr_project/thing/static/demoAPI'):
            if img_file.endswith('.gif'):
                imgs_to_del.append(img_file)
        if len(imgs_to_del) > 10:
            for each_img in imgs_to_del[:-10]:
                print each_img   
                os.chdir('/home/vagrant/src/fr_project/thing/static/demoAPI')
                os.system("rm " + each_img)

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

get_nest_api()
# @app.route('/stop')
# def stop_nesting():
#     global stop_me
#     stop_me = True


# if __name__ == "__main__":
#     # We have to set debug=True here, since it has to be True at the point
#     # that we invoke the DebugToolbarExtension

#     # Do not debug for demo
#     app.debug = True
#     DebugToolbarExtension(app)
#     app.run(host='0.0.0.0', port=5000)
#             