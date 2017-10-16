import os

import boto3
import cv2


BUCKET = 'amazon-rekognition'
KEY = 'capture.jpg'


def detect_faces(bucket, key, attributes=['ALL'], region='eu-west-1'):
    rekognition = boto3.client(
        'rekognition',
        region,
        aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID', ''),
        aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY', '')
    )
    response = rekognition.detect_faces(
        Image={
            'S3Object': {
                'Bucket': bucket,
                'Name': key,
            }
        },
        Attributes=attributes,
    )
    return response['FaceDetails']


if __name__ == '__main__':
    cap = cv2.VideoCapture(0)

    s3_client = boto3.client(
        's3',
        aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID', ''),
        aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY', '')
    )

    while(True):
        ret, frame = cap.read()
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2BGRA)

        cv2.imwrite(KEY, frame)
        s3_client.upload_file(KEY, BUCKET, KEY)
        for face in detect_faces(BUCKET, KEY):
            box = face.get('BoundingBox')
            smile = str(face.get('Smile').get('Value'))
            x1 = round(box.get('Left') * 1280)
            y1 = round(box.get('Top') * 720)
            x2 = round((box.get('Left') * 1280) + (box.get('Width') * 1280))
            y2 = round((box.get('Top') * 720) + (box.get('Height') * 720))
            cv2.rectangle(rgb, (x1, y1), (x2, y2), (255, 0, 0), 2)
            cv2.putText(rgb, smile, (x2 - 100, y2 + 30), 1, 1, (0, 255, 0), 1)

        cv2.imshow('frame', rgb)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
