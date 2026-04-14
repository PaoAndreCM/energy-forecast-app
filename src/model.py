import torch
from PatchTST import Model
import config

def load_model():
    configs = config.get_configs(name='inference')
    device = torch.device("mps" if torch.backends.mps.is_available() else "cpu")
    model = Model(configs)
    checkpoint = torch.load("models/best_checkpoint.pth", map_location=device)
    model.load_state_dict(checkpoint)
    model.to(device)
    model.eval()
    return model, device

if __name__ == "__main__":
    model, device = load_model()
    print(f"Model loaded successfully!")
    print(f"Device: {device}")
    print(f"Model type: {type(model)}")
    print(f"Model is in eval mode: {not model.training}")