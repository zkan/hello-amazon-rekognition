import unittest
from unittest.mock import patch

from detect_smiles import detect_faces


class DetectSmilesTest(unittest.TestCase):
    @patch('detect_smiles.boto3.client')
    def test_detect_faces_should_call_rekognition_functions_property(
        self,
        mock_boto3,
    ):
        bucket = 'amazon-rekognition'
        key = 'capture.jpg'
        rekognition = mock_boto3.return_value
        detect_faces(bucket, key)

        mock_boto3.assert_called_once_with(
            'rekognition',
            'eu-west-1',
            aws_access_key_id='',
            aws_secret_access_key='',
        )
        rekognition.detect_faces.assert_called_once_with(
            Image={
                'S3Object': {
                    'Bucket': bucket,
                    'Name': key
                }
            },
            Attributes=['ALL'],
        )


if __name__ == '__main__':
    unittest.main()
