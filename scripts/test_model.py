from classifier_engine import AgriculturePestClassifier
from classifier_engine import WheatDiseaseClassifier

pest_classifier = AgriculturePestClassifier()
wheat_disease_classifier = WheatDiseaseClassifier()

predicted_class, confidence = wheat_disease_classifier.predict("datasets/wheat_disease_dataset/test/Brown Rust/brown_rust_test_3.png")
print(predicted_class, confidence)

predicted_class, confidence = wheat_disease_classifier.predict("datasets/wheat_disease_dataset/test/Common Root Rot/common_root_rot_127.png")
print(predicted_class, confidence)

predicted_class, confidence = wheat_disease_classifier.predict("datasets/wheat_disease_dataset/test/Mite/mite_29.png")
print(predicted_class, confidence)