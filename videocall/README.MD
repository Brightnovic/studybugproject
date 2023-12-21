			BIGSON  AYO
THIS APP HAS BEEN COMPLETED YOU CAN MAKE VIDEO  CALL WITH THIS APP 
INCASE YOU WANT TO ADD THIS VIDEO CALL TO YOUR ALREAD BUILT APP  WITH DJANGO HERE ARE SOME STEPS TO FOLLOW:

cd mychat
pip install -r requirements.txt
```

#### 3 - Update Agora credentals
In order to use this project you will need to replace the agora credentials in `views.py` and `streams.js`.

Create an account at agora.io and create an `app`. Once you create your app, you will want to copy the `appid` & `appCertificate` to update `views.py` and `streams.js`. If you have questions about where to get your app I'd recommend referencing this link `https://youtu.be/HX6AM_1-jNM?t=88`

###### views.py
```
def getToken(request):
    appId = "YOUR APP ID"
    appCertificate = "YOUR APPS CERTIFICATE"
    ......
```

###### streams.js
```
....
const APP_ID = 'YOUR APP ID'
....
```


#### 4 - Start server
```
python manage.py runserver

 * GO TO THE ROOT FOLDER WHERE MANAGE.PY IS  LOCATED 
*MOVE INTO STATIC FOLDER 
YOU WILL FIND ASSEST AND JS FOLDER
* MOVE INTO ASSEST FOLDER  AND GRAB THE FILE NAMED "AgoraRTC_N-4.8.0"
GO BACK INTO JS FOLDER AND GRAB THE FILE NAMED  "STREAM.JS"
! MAKE SURE YOU LINK "AgoraRTC_N-4.8.0" BEFORE "STREAM.JS" INSIDE YOUR DJANGO PROJECT

DO YOU WISH TO USE THIS VIDEO CALL WITH THE OTHER APPS?
FOLLOW THIS STEPS:
#### 2 - Install requirements
```
cd mychat
pip install -r requirements.txt
```

#### 3 - Update Agora credentals
In order to use this project you will need to replace the agora credentials in `views.py` and `streams.js`.

Create an account at agora.io and create an `app`. Once you create your app, you will want to copy the `appid` & `appCertificate` to update `views.py` and `streams.js`. If you have questions about where to get your app I'd recommend referencing this link `https://youtu.be/HX6AM_1-jNM?t=88`

###### views.py
```
def getToken(request):
    appId = "YOUR APP ID"
    appCertificate = "YOUR APPS CERTIFICATE"
    ......
```

###### streams.js
```
....
const APP_ID = 'YOUR APP ID'
....
```


#### 4 - Start server
```
python manage.py runserver
```


