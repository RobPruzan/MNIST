# -*- coding: utf-8 -*-
"""FFNMNIST.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1EXmeBn54lpO5L7c_NgNVBy0zYrTVl7jT
"""

import torch
import torch.nn as nn
import torchvision
import torchvision.transforms as transforms
import matplotlib.pyplot as plt


device = torch.device('cuda' if torch.cuda.is_available else 'cpu')
input_size = 28*28
hidden_size = 100 
num_classes = 10
EPOCHS = 8
BATCH_SIZE = 100
learning_rate = 0.001

#MNIST
train_dataset = torchvision.datasets.MNIST(root='/content/sample_data', train=True,
                                           transform=transforms.ToTensor(), download=True)

test_dataset = torchvision.datasets.MNIST(root='/content/sample_data', train=False,
                                           transform=transforms.ToTensor())

train_loader = torch.utils.data.DataLoader(dataset=train_dataset, batch_size=BATCH_SIZE, shuffle=True)

test_loader = torch.utils.data.DataLoader(dataset=test_dataset, batch_size=BATCH_SIZE, shuffle=False)

examples = iter(train_loader)
samples, labels = examples.next()
print(samples.shape, labels.shape)
for i in range(6):
  plt.subplot(2, 3, i+1)
  plt.imshow(samples[i][0], cmap='gray')
  print(labels[i])
plt.show()

class NeuralNet(nn.Module):
  def __init__(self, input_size, hidden_size, output_size):
    super(NeuralNet, self).__init__()
    self.l1 = nn.Linear(input_size, hidden_size)
    self.relu = nn.ReLU()
    self.l2 = nn.Linear(hidden_size, num_classes)
  def forward(self, x):
    out = self.l1(x)
    out = self.relu(out)
    out = self.l2(out)
    return out

model = NeuralNet(input_size, hidden_size, num_classes)

criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)

n_total_steps = len(train_loader)

for epoch in range(EPOCHS):
  for i, (images, labels) in enumerate(train_loader):
    #100, 1, 28, 28
    #100, 784
    images = images.reshape(-1,28*28)
    labels = labels

    output = model(images)

    loss = criterion(output, labels)

    optimizer.zero_grad()

    loss.backward()

    optimizer.step()

    if (i+1) % 100 == 0:
      print(f'epoch: {epoch+1} / {EPOCHS}, step {i+1} / {n_total_steps}, loss = {loss.item():.4f}')
with torch.no_grad():
  n_correct = 0
  n_samples = 0
  for images, labels in test_loader:
    images = images.reshape(-1, 28*28)
    labels = labels
    outputs = model(images)
    
    _, predictions = torch.max(outputs, 1)
    n_samples += labels.shape[0]
    n_correct += (predictions == labels).sum().item()

  acc = 100.0 * n_correct / n_samples
  print(f'accuracy = {acc}')