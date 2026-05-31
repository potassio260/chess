# Imports
import torch

print(torch.cuda.is_available())
print(torch.cuda.device_count())
print(torch.cuda.current_device())

# Bot class
class Bot():
    def __init__(self):
        EPOCHS = 0
        LEARNING_RATE = 0

    def generate_move(self, possible_moves):
        pass

    def evaluate_move(self):
        pass

    def loss_function(self):
        pass
    
    def cross_entropy(self):
        pass

