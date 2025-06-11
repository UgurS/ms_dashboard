from dataclasses import dataclass

@dataclass
class ModelInfo:
    model_name: str
    display_name: str
    model_path: str
    train_set: str
    test_set: str
    threshold: float
    loader_class: type
