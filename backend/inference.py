from model import DenseNetModel
import torch
from PIL import Image
from torchvision import transforms

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

model = DenseNetModel().to(device)
model.load_state_dict(torch.load("best_resnet_model.pth", map_location=device))
model.eval()

transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize([0.5]*3, [0.5]*3)
])

img = Image.open("data/chest_xray/test/PNEUMONIA/person1.jpeg").convert("RGB")
img = transform(img).unsqueeze(0).to(device)

with torch.no_grad():
    output = model(img)
    prob = torch.sigmoid(output).item()

print(f"Probability: {prob:.4f}")

if prob > 0.4:
    print("Prediction: Pneumonia")
else:
    print("Prediction: Normal") 