import matplotlib.pyplot as plt

from PIL import Image

from torchvision import transforms

image = Image.open(
    r"D:\uir 4eme annee\s8\deep learning\project\AI_Medical_Assistant\data\chest_xray\train\NORMAL\IM-0115-0001.jpeg"
)

transform = transforms.Compose([

    transforms.Resize((224,224)),

    transforms.RandomHorizontalFlip(p=1),

    transforms.RandomRotation(15)

])

augmented = transform(image)

plt.imshow(augmented)

plt.axis("off")

plt.show()