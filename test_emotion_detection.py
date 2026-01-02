import unittest
from EmotionDetection.emotion_detection import emotion_predictor

class TestEmotionPredictor(unittest.TestCase):
    def test_emotion_predictor(self):
        result_1 = emotion_predictor("I am glad this happened")
        self.assertEqual(result_1['dominant_emotion'], 'joy')
        
        result_2 = emotion_predictor("I am really mad about this")
        self.assertEqual(result_2['dominant_emotion'], 'anger')

if __name__ == '__main__':
    unittest.main()