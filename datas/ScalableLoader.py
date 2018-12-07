import random
import torch
from torch.utils.data import DataLoader

import torchvision.transforms as transforms
from torchvision.datasets import ImageFolder

from config import resl_to_batch

class ScalableLoader:
    def __init__(self, path, shuffle=True, drop_last=False, num_workers=4, shuffled_cycle=True):
        self.path = path
        self.shuffle = shuffle
        self.drop_last = drop_last
        self.num_workers = num_workers
        self.shuffled_cycle = shuffled_cycle
        
    def __call__(self, resl):
        batch = resl_to_batch[resl]

        transform = transforms.Compose([transforms.Resize(size=(resl, resl)),
                                        transforms.ToTensor()])

        fullpath = self.path % max(64, resl)
        dataset = ImageFolder(root=fullpath, transform=transform)
        print("Data path: %s" % fullpath)
        loader = DataLoader(
            dataset=dataset,
            batch_size=batch,
            shuffle=self.shuffle,
            drop_last=self.drop_last,
            num_workers=self.num_workers
        )

        loader = self._cycle(loader, self.shuffled_cycle)

        return loader

    def _cycle(self, loader, shuffled_cycle=True):
        while True:
            for element in loader:
                yield element
            if self.shuffled_cycle:
                random.shuffle(loader.dataset.imgs)
            
    
if __name__ == "__main__":
    
    from itertools import cycle
    sl = ScalableLoader("../dataset", shuffled_cycle=False)
    loader = sl(4)
    len_loader = 520
    for idx, item in enumerate(loader):
        print(idx, item)
        if idx % len_loader == 0:
            input()