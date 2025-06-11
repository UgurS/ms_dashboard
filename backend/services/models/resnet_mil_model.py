import torch
import torch.nn as nn
import numpy as np
import cv2
from PIL import Image
from torchvision import transforms, models
from backend.services.models.base_model import BaseModel
from PIL import ImageOps

class AttentionMIL(nn.Module):
    def __init__(self, feature_dim=512):
        super().__init__()
        self.attn = nn.Sequential(
            nn.LayerNorm(feature_dim),
            nn.Linear(feature_dim, 128),
            nn.Tanh(),
            nn.Dropout(0.3),
            nn.Linear(128, 1),
        )

    def forward(self, x):
        a = self.attn(x)
        w = torch.softmax(a, dim=0)
        return w


class ResNetMILModel(BaseModel):
    def load_model(self):
        checkpoint = torch.load(self.model_path, map_location=self.device)

        self.net = models.resnet18(weights=None)
        self.net.fc = nn.Identity()
        self.net.load_state_dict(checkpoint['net_state_dict'])
        self.net.to(self.device).eval()

        self.attn = AttentionMIL()
        self.attn.load_state_dict(checkpoint['attn_state_dict'])
        self.attn.to(self.device).eval()

        self.clf = nn.Sequential(nn.Dropout(0.3), nn.Linear(512, 1))
        self.clf.load_state_dict(checkpoint['clf_state_dict'])
        self.clf.to(self.device).eval()

        return {
            'backbone': self.net,
            'attention': self.attn,
            'classifier': self.clf
        }

    def __init__(self, model_path, threshold=0.5):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        super().__init__(model_path, threshold)
        self.resize_size = (224, 224)
        self.patch_size = (448, 448)
        self.transform = transforms.Compose([
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406],
                                 [0.229, 0.224, 0.225])
        ])

    def extract_patches(self, img_np):
        img_h, img_w, _ = img_np.shape
        ph, pw = self.patch_size

        num_h = int(np.ceil(img_h / ph))
        num_w = int(np.ceil(img_w / pw))

        oh = ((num_h * ph) - img_h) // (num_h - 1) if num_h > 1 else 0
        ow = ((num_w * pw) - img_w) // (num_w - 1) if num_w > 1 else 0

        stride_h = ph - oh
        stride_w = pw - ow

        patches = []
        positions = []

        for x in range(0, img_w - pw + 1, stride_w):  # ← column-first
            for y in range(0, img_h - ph + 1, stride_h):
                patch = img_np[y:y + ph, x:x + pw]
                resized = cv2.resize(patch, self.resize_size)
                patches.append(self.transform(resized))
                positions.append((y, x))

        patch_tensor = torch.stack(patches)

        return patch_tensor, list(positions), img_h, img_w

    def generate_heatmap(self, patches_tensor, attention_weights, positions, canvas_height, canvas_width):
        attn = attention_weights.squeeze().cpu().numpy()
        attn = (attn - attn.min()) / (attn.max() - attn.min() + 1e-8)

        # Unnormalize patches
        mean = torch.tensor([0.485, 0.456, 0.406]).view(3, 1, 1)
        std = torch.tensor([0.229, 0.224, 0.225]).view(3, 1, 1)
        patches = patches_tensor.clone().cpu() * std + mean
        patches = torch.clamp(patches, 0, 1).permute(0, 2, 3, 1).numpy()
        patches = (patches * 255).astype(np.uint8)

        # Pair patches, attn, positions
        combined = list(zip(patches, attn, positions))

        # Sort to draw back-to-front (top-left to bottom-right)
        combined.sort(key=lambda item: (item[2][0], item[2][1]))

        # Prepare canvas
        canvas = np.zeros((canvas_height, canvas_width, 3), dtype=np.uint8)
        ph, pw = self.patch_size

        for patch, attn_val, (y, x) in combined:
            patch = cv2.resize(patch, self.patch_size)
            gray_val = int(attn_val * 255)
            heatmap = cv2.applyColorMap(np.full(self.patch_size, gray_val, np.uint8), cv2.COLORMAP_JET)
            blended = cv2.addWeighted(patch, 0.6, heatmap, 0.4, 0)

            label = f"{int(attn_val * 100)}%"
            cv2.putText(blended, label, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)
            canvas[y:y+ph, x:x+pw] = blended

        _, buffer = cv2.imencode('.jpg', canvas)
        return buffer.tobytes()

    def predict(self, image_bytes):
        image = ImageOps.exif_transpose(Image.open(image_bytes).convert("RGB"))
        img_np = np.array(image)

        patches_tensor, positions, h, w = self.extract_patches(img_np)
        patches_tensor = patches_tensor.to(self.device)

        with torch.no_grad():
            feats = self.model['backbone'](patches_tensor)
            attn_weights = self.model['attention'](feats)
            bag_repr = torch.sum(attn_weights * feats, dim=0)
            logit = self.model['classifier'](bag_repr.unsqueeze(0))
            prob = torch.sigmoid(logit).item()

        label = "MSP" if prob >= self.threshold else "HC"
        confidence = prob if prob >= self.threshold else 1.0 - prob

        heatmap = self.generate_heatmap(patches_tensor, attn_weights, positions, h, w)

        return {
            "prediction": label,
            "confidence": float(confidence),
            "heatmap": heatmap
        }

