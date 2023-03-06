import lab as B
from matrix import AbstractMatrix
from plum import convert, parametric

from . import _dispatch
from .. import Kernel

__all__ = ["PosteriorKernel"]


@parametric
class PosteriorKernel(Kernel):
    """Posterior kernel.

    Args:
        k_ij (:class:`.kernel.Kernel`): Kernel between processes corresponding to the
            left input and the right input respectively.
        k_zi (:class:`.kernel.Kernel`): Kernel between processes corresponding to the
            data and the left input respectively.
        k_zj (:class:`.kernel.Kernel`): Kernel between processes corresponding to the
            data and the right input respectively.
        z (input): Locations of data.
        K_z (matrix): Kernel matrix of data.
    """

    @classmethod
    def __infer_type_parameter__(cls, k_ij, k_zi, k_zj, *args):
        return type(k_ij), type(k_zi), type(k_zj)

    def __init__(self, k_ij, k_zi, k_zj, z, K_z):
        self.k_ij = k_ij
        self.k_zi = k_zi
        self.k_zj = k_zj
        self.z = z
        self.K_z = convert(K_z, AbstractMatrix)


def _K_zi_K_zj(k_zi, k_zj, z, x, y):
    K_zi = k_zi(z, x)
    if k_zi == k_zj and x is y:
        K_zj = K_zi
    else:
        K_zj = k_zj(z, y)
    return K_zi, K_zj


@_dispatch
def pairwise(k: PosteriorKernel, x, y):
    return _pairwise_posteriorkernel(k, x, y, *_K_zi_K_zj(k.k_zi, k.k_zj, k.z, x, y))


@_dispatch
def _pairwise_posteriorkernel(k: PosteriorKernel, x, y, K_zi, K_zj):
    return B.subtract(k.k_ij(x, y), B.iqf(k.K_z, K_zi, K_zj))


@_dispatch
def elwise(k: PosteriorKernel, x, y):
    return _elwise_posteriorkernel(k, x, y, *_K_zi_K_zj(k.k_zi, k.k_zj, k.z, x, y))


@_dispatch
def _elwise_posteriorkernel(k: PosteriorKernel, x, y, K_zi, K_zj):
    iqf_diag = B.iqf_diag(k.K_z, K_zi, K_zj)
    return B.subtract(k.k_ij.elwise(x, y), B.expand_dims(iqf_diag, axis=-1))
