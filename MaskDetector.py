
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.models import load_model
from imutils.video import VideoStream
import numpy as np
import argparse
import imutils
import time
import cv2
import os, threading
from time import sleep

class MaskDetector(object):

    def __init__(self, confidence=0.5 ,v_src=0, **kwargs):
        kwargs.setdefault('proto','./face_detector/deploy.prototxt')
        kwargs.setdefault('face','./face_detector/res10_300x300_ssd_iter_140000.caffemodel')
        kwargs.setdefault('model','./face_mask_detector.model')
        kwargs.setdefault('headless', True)
        prototxtPath = kwargs['proto']
        weightsPath = kwargs['face']
        model_path = kwargs['model']
        self.isHeadless = kwargs['headless']
        self.faceNet = cv2.dnn.readNet(prototxtPath, weightsPath)
        self.maskNet = load_model(model_path)
        self.videoStream = VideoStream(src=v_src)
        self.confidence = confidence
        self.videoOn = False
        if not self.isHeadless:
            self.displayThread = threading.Thread(target=self.video_stream)
            self.displayThread.start()

    def start_display(self):
        self.start_display = True
        return self.videoStream.start()

    def stop_display(self):
        self.videoOn = False
        return self.videoStream.stop()

    def video_stream(self):
        while True:
            while self.videoOn:
                self.detect_mask()
                sleep(0.2)
            sleep(1)

    def detect_mask(self):
        if self.videoStream.stopped:
            self.videoStream.start()
            print("""Warning, the video stream was stopped earlier but mask detection is asked.
            Attempting to start the video stream.""")

        # grab the dimensions of the frame and then construct a blob from it
        frame = imutils.resize( self.videoStream.read(), width=400)
        (h,w) = frame.shape[:2]
        blob = cv2.dnn.blobFromImage(frame, 1.0, (300, 300),(104.0, 177.0, 123.0))
        # pass the blob through the network and obtain the face detections
        faceNet.setInput(blob)
        detections = faceNet.forward()
        # initialize our list of faces, their corresponding locations,
        # and the list of predictions from our face mask network
        faces = []
        locs = []
        preds = []

        # loop over the detections
        for i in range(0, detections.shape[2]):
            # extract the confidence (i.e., probability) associated with
            # the detection
            confidence = detections[0, 0, i, 2]
            # filter out weak detections by ensuring the confidence is
            # greater than the minimum confidence
            if confidence > self.confidence:
                # compute the (x, y)-coordinates of the bounding box for
                # the object
                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                (startX, startY, endX, endY) = box.astype("int")
                # ensure the bounding boxes fall within the dimensions of
                # the frame
                (startX, startY) = (max(0, startX), max(0, startY))
                (endX, endY) = (min(w - 1, endX), min(h - 1, endY))
                # extract the face ROI, convert it from BGR to RGB channel
                # ordering, resize it to 224x224, and preprocess it
                face = frame[startY:endY, startX:endX]
                face = cv2.cvtColor(face, cv2.COLOR_BGR2RGB)
                face = cv2.resize(face, (224, 224))
                face = img_to_array(face)
                face = preprocess_input(face)
                # add the face and bounding boxes to their respective
                # lists
                faces.append(face)
                locs.append((startX, startY, endX, endY))

                # only make a predictions if at least one face was detected
        if len(faces) > 0:
            # for faster inference we'll make batch predictions on *all*
            # faces at the same time rather than one-by-one predictions
            # in the above `for` loop
            faces = np.array(faces, dtype="float32")
            preds = maskNet.predict(faces, batch_size=32)

        for (box, pred) in zip(locs, preds):
            # unpack the bounding box and predictions
            (startX, startY, endX, endY) = box
            (mask, maskImproper, withoutMask) = pred

            # determine the class label and color we'll use to draw
            # the bounding box and text
            #label = "Mask" if mask > withoutMask else "No Mask"
            #color = (0, 255, 0) if label == "Mask" else (0, 0, 255)

            if mask > withoutMask :
                if mask > maskImproper :
                    label = "Mask"
                else:
                    label = "Improper Mask"
            elif withoutMask > maskImproper :
                label = "No Mask"
            else :
                label = "Improper Mask"

            if label == "Mask" :
                color = (0, 255, 0)
            elif label == "Improper Mask" :
                color = (0, 127, 127)
            else :
                color = (0, 0, 255)
            # include the probability in the label
            labell = "{}: {:.2f}%".format(label, max(mask, maskImproper, withoutMask) * 100)
            if self.isHeadless:
                print(labell)
                return label
            else:
                # display the label and bounding box rectangle on the output
                # frame
                cv2.putText(frame, labell, (startX, startY - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.45, color, 2)
                cv2.rectangle(frame, (startX, startY), (endX, endY), color, 2)
                cv2.imshow("Frame", frame)
                return label
