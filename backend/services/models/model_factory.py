from backend.models.model_info import ModelInfo
from backend.services.models.mobilenet_v2_model import MobileNetV2Model
from backend.services.models.resnet_mil_model import ResNetMILModel


class ModelFactory:
    _models = {
        "mobilenetv2-standard-full-v1.0.0": ModelInfo(
            model_name="mobilenetv2-standard-full-v1.0.0",
            display_name="MobileNetV2 (224x224 samples)",
            model_path="trained_models/mobilenetv2-standard-full-v1.0.0.keras",
            train_set="HC J04, HC J07, HC J23, HC J25, MSp J34, MSp J35, MSp J36, MSp J41",
            test_set="HC J01, MSp J38",
            threshold=0.5,
            loader_class=MobileNetV2Model
        ),
        "resnet18-mil-fold1-v1.0.0": ModelInfo(
            model_name="resnet18-mil-fold1-v1.0.0",
            display_name="ResNet18 MIL (Fold 1)",
            model_path="trained_models/resnet18-mil-fold1-v1.0.0.pt",
            train_set="HC J01, HC J23, HC J24, MSp J40, MSp J41",
            test_set="HC J04, HC J07, HC J25, MSp J34, MSp J35, MSp J36, MSp J38, MSp J42",
            threshold=0.59,
            loader_class=ResNetMILModel
        ),
        "resnet18-mil-fold2-v1.0.0": ModelInfo(
            model_name="resnet18-mil-fold2-v1.0.0",
            display_name="ResNet18 MIL (Fold 2)",
            model_path="trained_models/resnet18-mil-fold2-v1.0.0.pt",
            train_set="HC J01, HC J07, HC J24, MSp J25, MSp J34, MSp J36, MSp J40, MSp J42",
            test_set="HC J04, HC J23, MSp J35, MSp J38, MSp J41",
            threshold=0.39,
            loader_class=ResNetMILModel
        ),
        "resnet18-mil-fold3-v1.0.0": ModelInfo(
            model_name="resnet18-mil-fold3-v1.0.0",
            display_name="ResNet18 MIL (Fold 3)",
            model_path="trained_models/resnet18-mil-fold3-v1.0.0.pt",
            train_set="HC J04, HC J07, HC J23, HC J24, MSp J34, MSp J35, MSp J38, MSp J41, MSp J42",
            test_set="HC J01, HC J25, MSp J36, MSp J40",
            threshold=0.30,
            loader_class=ResNetMILModel
        )
    }

    @staticmethod
    def get_model(model_name):
        if model_name in ModelFactory._models:
            info = ModelFactory._models[model_name]
            threshold = info.threshold if hasattr(info, 'threshold') else 0.5
            return info.loader_class(model_path=info.model_path, threshold=threshold)
        raise ValueError(f"Unknown model: {model_name}")

    @staticmethod
    def get_all_model_info():
        return list(ModelFactory._models.values())
