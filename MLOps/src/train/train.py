import numpy as np
from tqdm import tqdm


def train(model, train_loader):

    total_loss = 0
    for features, labels in tqdm(train_loader):
        predictions = model.forward(features)
        labels = labels.reshape(-1, 1)
        loss = np.mean((predictions - labels) ** 2)

        model.backward(features, labels, predictions)

        total_loss += loss

    return total_loss / len(train_loader)