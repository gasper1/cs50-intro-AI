model 1:
    Conv2D - 6 filters, kernel: 3x3, relu
    Pooling 2x2
    Flatten
    Dense 128
    Dropout 0.5
    Dense NUM_CATEGORIES
    ==> Accuracy: 0.33, loss: 2.502

model 2:
    Conv2D - 10 filters, kernel: 3x3, relu
    Pooling 2x2
    Flatten
    Dense 128
    Dropout 0.5
    Dense NUM_CATEGORIES
    ==> Accuracy: 0.0552, loss: 3.5010
