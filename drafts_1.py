# myList = ["Bran", 11, 22, 33, "Stark", 22, 33, 11]
#
# a = myList.pop(0)
# print(myList)
import torch
use_cuda = torch.cuda.is_available()
print(f"Using CUDA: {use_cuda}")
print()