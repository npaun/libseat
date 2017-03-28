print "\033[1;36mLoading Darkflow YOLO.... please wait (~10 seconds)\033[0m"
from net.build import TFNet
import cv2
import sys
import imutils
import subprocess

options = {"model": "darkflow/cfg/yolo-voc.cfg", "load": "darkflow/bin/yolo-voc.weights"}

tfnet = TFNet(options)
print "\033[1;36mSetting up camera.... please wait (green light should shortly appear)\033[0m"
camera = cv2.VideoCapture(int(sys.argv[1]))

p = subprocess.Popen(["/Users/npaunl/intersect-acct.py",sys.argv[2]], stdin=subprocess.PIPE,stdout=sys.stdout,stderr=sys.stderr)

print "\033[1;36mReady to detect peeples\033[0m"

while True:
    grabbed,frame = camera.read()
    if not grabbed:
        sys.stderr.write("Failed to grab frame.\n")
        continue

    frame = imutils.resize(frame,width=500)
    results = tfnet.return_predict(frame)
    i = 0

    for result in results:
        if result['label'] != 'person':
            continue # No elephants in this library

        p.stdin.write("CV%d %d %d %d %d %f\n" % (i,result['topleft']['x'],result['topleft']['y'],result['bottomright']['x'],result['bottomright']['y'],result['confidence']))
        i += 1
    
    p.stdin.write("*\n")
