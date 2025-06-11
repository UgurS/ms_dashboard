import abc
from pathlib import Path

class BaseModel(abc.ABC):
    def __init__(self, model_path, threshold=0.5):
        current_file = Path(__file__).resolve()
        backend_dir = current_file.parents[2]
        self.model_path = backend_dir / model_path

        self.model = self.load_model()
        self.threshold = threshold

    @abc.abstractmethod
    def load_model(self):
        pass

    @abc.abstractmethod
    def predict(self, image_bytes):
        pass
