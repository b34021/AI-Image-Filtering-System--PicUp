import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import datasets, transforms, models
from torch.utils.data import DataLoader
import os
import shutil

# --- 1. נתיבי הנתונים ---
train_dir = r"O:\share\project miri and brachy\chassid"
validation_dir = r"O:\share\project miri and brachy\validations"
output_dir = r"O:\share\project miri and brachy\sorted_images"

# --- 2. טרנספורמציות ---
train_transforms = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.RandomHorizontalFlip(),
    transforms.RandomRotation(20),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
])

val_transforms = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
])

# --- 3. Datasets ו-DataLoaders ---
train_dataset = datasets.ImageFolder(train_dir, transform=train_transforms)
val_dataset = datasets.ImageFolder(validation_dir, transform=val_transforms)

train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)
val_loader = DataLoader(val_dataset, batch_size=32, shuffle=False)

# --- 4. שימוש ב-Transfer Learning (ResNet18) ---
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
num_classes = 8  # כמות הקטגוריות שלך

model = models.resnet18(pretrained=True)
# החלפת ה-classifier האחרון
model.fc = nn.Linear(model.fc.in_features, num_classes)
model = model.to(device)

# --- 5. Loss ו-Optimizer ---
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.0001)

# --- 6. אימון המודל ---
epochs = 10
for epoch in range(epochs):
    model.train()
    running_loss = 0.0
    correct = 0
    total = 0

    for inputs, labels in train_loader:
        inputs, labels = inputs.to(device), labels.to(device)

        optimizer.zero_grad()
        outputs = model(inputs)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()

        running_loss += loss.item()
        _, predicted = torch.max(outputs, 1)
        total += labels.size(0)
        correct += (predicted == labels).sum().item()

    train_acc = correct / total
    print(f"Epoch {epoch + 1}/{epochs} | Loss: {running_loss:.4f} | Train Acc: {train_acc:.4f}")

    # אימות
    model.eval()
    val_correct = 0
    val_total = 0
    with torch.no_grad():
        for inputs, labels in val_loader:
            inputs, labels = inputs.to(device), labels.to(device)
            outputs = model(inputs)
            _, predicted = torch.max(outputs, 1)
            val_total += labels.size(0)
            val_correct += (predicted == labels).sum().item()
    val_acc = val_correct / val_total
    print(f"Validation Accuracy: {val_acc:.4f}")

# --- 7. שמירת המודל ---
torch.save(model.state_dict(), 'wedding_image_classifier_resnet.pth')

# --- 8. סקריפט לחלוקת התמונות לפי קטגוריות ---
class_names = train_dataset.classes  # ['כיסא כלה', 'תמונות חוץ', ...]


def sort_images(input_folder, model, device, output_folder):
    transform = val_transforms
    model.eval()

    for root, _, files in os.walk(input_folder):
        for file in files:
            if file.lower().endswith(('png', 'jpg', 'jpeg')):
                img_path = os.path.join(root, file)
                from PIL import Image
                img = Image.open(img_path).convert('RGB')
                img_tensor = transform(img).unsqueeze(0).to(device)

                with torch.no_grad():
                    outputs = model(img_tensor)
                    _, pred = torch.max(outputs, 1)
                    category = class_names[pred.item()]

                # יצירת תיקייה אם לא קיימת
                os.makedirs(os.path.join(output_folder, category), exist_ok=True)
                shutil.copy(img_path, os.path.join(output_folder, category, file))

# דוגמה לשימוש:
# sort_images('path_to_unsorted_images', model, device, output_dir)
# #llm
# import torch
# import torch.nn as nn
# import torch.optim as optim
# from torchvision import datasets, transforms
# from torch.utils.data import DataLoader
#
# # הגדרת נתיב לתמונות
# train_dir = 'path_to_train_data'
# validation_dir = 'path_to_validation_data'
#
# # טרנספורמציות לתמונות
# train_transforms = transforms.Compose([
#     transforms.Resize((150, 150)),
#     transforms.RandomHorizontalFlip(),
#     transforms.RandomRotation(20),
#     transforms.ToTensor(),
#     transforms.Normalize([0.5, 0.5, 0.5], [0.5, 0.5, 0.5])
# ])
#
# val_transforms = transforms.Compose([
#     transforms.Resize((150, 150)),
#     transforms.ToTensor(),
#     transforms.Normalize([0.5, 0.5, 0.5], [0.5, 0.5, 0.5])
# ])
#
# # יצירת Dataset ו-DataLoader
# train_dataset = datasets.ImageFolder(train_dir, transform=train_transforms)
# val_dataset = datasets.ImageFolder(validation_dir, transform=val_transforms)
#
# train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)
# val_loader = DataLoader(val_dataset, batch_size=32, shuffle=False)
#
# # הגדרת מודל CNN
# class CNNModel(nn.Module):
#     def __init__(self, num_classes=5):
#         super(CNNModel, self).__init__()
#         self.features = nn.Sequential(
#             nn.Conv2d(3, 32, kernel_size=3, padding=1),
#             nn.ReLU(),
#             nn.MaxPool2d(2, 2),
#
#             nn.Conv2d(32, 64, kernel_size=3, padding=1),
#             nn.ReLU(),
#             nn.MaxPool2d(2, 2),
#
#             nn.Conv2d(64, 128, kernel_size=3, padding=1),
#             nn.ReLU(),
#             nn.MaxPool2d(2, 2)
#         )
#         self.classifier = nn.Sequential(
#             nn.Flatten(),
#             nn.Linear(128 * 18 * 18, 512),  # 150x150 -> 18x18 אחרי 3 שכבות Pooling
#             nn.ReLU(),
#             nn.Dropout(0.5),
#             nn.Linear(512, num_classes)
#         )
#
#     def forward(self, x):
#         x = self.features(x)
#         x = self.classifier(x)
#         return x
#
# device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
# model = CNNModel(num_classes=5).to(device)
#
# # הגדרת loss ו-optimizer
# criterion = nn.CrossEntropyLoss()
# optimizer = optim.Adam(model.parameters(), lr=0.001)
#
# # אימון המודל
# epochs = 10
# for epoch in range(epochs):
#     model.train()
#     running_loss = 0.0
#     correct = 0
#     total = 0
#     for inputs, labels in train_loader:
#         inputs, labels = inputs.to(device), labels.to(device)
#
#         optimizer.zero_grad()
#         outputs = model(inputs)
#         loss = criterion(outputs, labels)
#         loss.backward()
#         optimizer.step()
#
#         running_loss += loss.item()
#         _, predicted = torch.max(outputs, 1)
#         total += labels.size(0)
#         correct += (predicted == labels).sum().item()
#
#     train_acc = correct / total
#     print(f"Epoch {epoch+1}/{epochs}, Loss: {running_loss:.4f}, Accuracy: {train_acc:.4f}")
#
#     # אימות
#     model.eval()
#     val_correct = 0
#     val_total = 0
#     with torch.no_grad():
#         for inputs, labels in val_loader:
#             inputs, labels = inputs.to(device), labels.to(device)
#             outputs = model(inputs)
#             _, predicted = torch.max(outputs, 1)
#             val_total += labels.size(0)
#             val_correct += (predicted == labels).sum().item()
#     val_acc = val_correct / val_total
#     print(f"Validation Accuracy: {val_acc:.4f}")
#
# # שמירת המודל
# torch.save(model.state_dict(), 'wedding_image_classifier.pth')