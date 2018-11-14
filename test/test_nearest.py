from itertools import product

import pytest
import torch
from torch_cluster import nearest

from .utils import tensor

devices = [torch.device('cuda')]
grad_dtypes = [torch.float]


@pytest.mark.skipif(not torch.cuda.is_available(), reason='CUDA not available')
@pytest.mark.parametrize('dtype,device', product(grad_dtypes, devices))
def test_nearest(dtype, device):
    x = tensor([
        [-1, -1],
        [-1, +1],
        [+1, +1],
        [+1, -1],
        [-2, -2],
        [-2, +2],
        [+2, +2],
        [+2, -2],
    ], dtype, device)
    y = tensor([
        [-1, 0],
        [+1, 0],
        [-2, 0],
        [+2, 0],
    ], dtype, device)

    batch_x = tensor([0, 0, 0, 0, 1, 1, 1, 1], torch.long, device)
    batch_y = tensor([0, 0, 1, 1], torch.long, device)

    print()
    out = nearest(x, y, batch_x, batch_y)
    print()
    print('out', out)
    print('expected', [0, 0, 1, 1, 2, 2, 3, 3])
