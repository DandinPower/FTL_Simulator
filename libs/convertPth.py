import torch

def convert_checkpoint(input_path, output_path):
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    checkpoint = torch.load(input_path, map_location={'cuda:1': 'cuda:0'})
    torch.save(checkpoint, output_path)

# Usage example
input_file = 'path/to/your/input_model.pth'
output_file = 'path/to/your/output_model.pth'

for i in range(91):
    path = f'ftl/pretrain/weight/scratch_wdev_0/scratch_wdev_0_{i}.pth'
    convert_checkpoint(path, path)