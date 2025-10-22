from classifier_engine import AgriculturePestClassifier

pest_classifier = AgriculturePestClassifier()

predicted_class, confidence = pest_classifier.predict("fas.webp")

print(predicted_class, confidence)