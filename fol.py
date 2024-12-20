import cv2
from flask import Flask, Response

app = Flask(__name__)


camera = cv2.VideoCapture(0)


def generate_frames():
    while True:
        
        success, frame = camera.read()
        if not success:
            break
        else:
            
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()

            
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/')
def index():
    
    return '''
        <html>
            <head>
                <title>Live Stream</title>
            </head>
            <body>
                <h1>Live Streaming</h1>
                <img src="/video_feed" width="640" height="480" />
            </body>
        </html>
    '''



if __name__ == '__main__':
    app.run(debug=True, threaded=True)