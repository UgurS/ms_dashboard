import os
import numpy as np
import cv2
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras import backend as K


class DiagnosisService:
    def __init__(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        model_path = os.path.join(current_dir, '../trained_models/MobileNetV2.keras')
        self.model = load_model(model_path)
        self.img_size = (224, 224)

    def preprocess(self, image_bytes):
        # Decode input image from bytes (as color BGR)
        np_img = np.frombuffer(image_bytes.read(), np.uint8)
        image = cv2.imdecode(np_img, cv2.IMREAD_COLOR)

        if image is None:
            raise ValueError("Could not decode input image")

        # Resize keeping height = 224
        h, w, _ = image.shape
        new_height = 224
        new_width = int((w / h) * new_height)
        resized = cv2.resize(image, (new_width, new_height), interpolation=cv2.INTER_AREA)

        # Pad width to 224
        delta_w = 224 - new_width
        left = delta_w // 2
        right = delta_w - left
        padded = cv2.copyMakeBorder(resized, 0, 0, left, right, cv2.BORDER_CONSTANT, value=[0, 0, 0])

        # Apply CLAHE to each channel
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        channels = cv2.split(padded)
        clahe_channels = [clahe.apply(c) for c in channels]
        enhanced = cv2.merge(clahe_channels)

        # Convert BGR to RGB and normalize
        rgb_img = cv2.cvtColor(enhanced, cv2.COLOR_BGR2RGB)
        img_array = rgb_img.astype('float32') / 255.0
        img_array = np.expand_dims(img_array, axis=0)

        return img_array, rgb_img

    def predict(self, image_bytes):
        input_tensor, rgb_img = self.preprocess(image_bytes)
        pred = self.model.predict(input_tensor)[0][0]
        label = "MSP" if pred > 0.5 else "HC"
        confidence = float(pred if pred > 0.5 else 1.0 - pred)

        heatmap = self.generate_gradcam(input_tensor, rgb_img)

        return {
            "prediction": label,
            "confidence": confidence,
            "heatmap": heatmap
        }

    def generate_gradcam(self, input_tensor, original_image):
        # Automatically find last conv layer
        def get_last_conv_layer(model):
            for layer in reversed(model.layers):
                try:
                    if len(layer.output.shape) == 4:
                        return layer.name
                except Exception:
                    continue
            raise ValueError("No valid 4D conv layer found.")

        # Get correct layer name
        last_conv_layer_name = get_last_conv_layer(self.model)

        # Build grad model
        grad_model = tf.keras.models.Model(
            inputs=self.model.input,
            outputs=[self.model.get_layer(last_conv_layer_name).output, self.model.output]
        )

        with tf.GradientTape() as tape:
            conv_outputs, predictions = grad_model(input_tensor)
            loss = predictions[:, 0]  # targeting the predicted class

        grads = tape.gradient(loss, conv_outputs)[0]  # shape: (H, W, C)
        pooled_grads = tf.reduce_mean(grads, axis=(0, 1))  # shape: (C,)
        pooled_grads = tf.reshape(pooled_grads, [1, 1, -1])

        conv_outputs = conv_outputs[0]  # shape: (H, W, C)
        weighted_output = conv_outputs * pooled_grads

        heatmap = tf.reduce_mean(weighted_output, axis=-1)  # shape: (H, W)
        heatmap = np.maximum(heatmap, 0)

        if np.max(heatmap) != 0:
            heatmap /= np.max(heatmap)

        heatmap = cv2.resize(heatmap, (224, 224))
        heatmap_img = np.uint8(255 * heatmap)
        heatmap_img = cv2.applyColorMap(heatmap_img, cv2.COLORMAP_JET)
        superimposed = cv2.addWeighted(original_image, 0.6, heatmap_img, 0.4, 0)

        _, buffer = cv2.imencode('.jpg', superimposed)
        return buffer.tobytes()

