from backend.services.models.model_factory import ModelFactory


class DiagnosisService:
    def __init__(self, model_name="resnet18-mil-fold1-v1.0.0"):
        self.model = ModelFactory.get_model(model_name)

    def predict(self, image_bytes):
        return self.model.predict(image_bytes)