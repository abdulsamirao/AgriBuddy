#from classifier_engine import AgriculturePestClassifier
from classifier_engine import WheatDiseaseClassifier
from classifier_engine import MangoDiseaseClassifier
from classifier_engine import CottonDiseaseClassifier

#pest_classifier = AgriculturePestClassifier()

def test_wheat():
    wheat_disease_classifier = WheatDiseaseClassifier()
    
    predicted_class, confidence = wheat_disease_classifier.predict("datasets/wheat_disease_dataset/test/Brown Rust/brown_rust_test_3.png")
    print(predicted_class, confidence)

    predicted_class, confidence = wheat_disease_classifier.predict("datasets/wheat_disease_dataset/test/Common Root Rot/common_root_rot_127.png")
    print(predicted_class, confidence)

    predicted_class, confidence = wheat_disease_classifier.predict("datasets/wheat_disease_dataset/test/Mite/mite_29.png")
    print(predicted_class, confidence)

    predicted_class, confidence = wheat_disease_classifier.predict("datasets/wheat_disease_dataset/test/Mildew/mildew_test_41.png")
    print(predicted_class, confidence)

    predicted_class, confidence = wheat_disease_classifier.predict("datasets/wheat_disease_dataset/test/Septoria/septoria_19.png")
    print(predicted_class, confidence)

def test_mango():
    mango_disease_classifier = MangoDiseaseClassifier()
    
    predicted_class, confidence = mango_disease_classifier.predict("test.png")
    print(predicted_class, confidence)

def test_cotton():
    cotton_disease_classifier = CottonDiseaseClassifier()
    
    predicted_class, confidence = cotton_disease_classifier.predict("test.jpg")
    print(predicted_class, confidence)

test_cotton()