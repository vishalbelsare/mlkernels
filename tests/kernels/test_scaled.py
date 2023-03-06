from mlkernels import EQ, Matern12, ScaledKernel
from ..util import standard_kernel_tests


def test_scaled():
    k = 2 * EQ()

    # Test parametric type.
    assert type(k) == ScaledKernel[EQ]

    # Verify that the kernel has the right properties.
    assert k.stationary

    # Test equality.
    assert 2 * EQ() == 2 * EQ()
    assert 2 * EQ() != 3 * EQ()
    assert 2 * EQ() != 2 * Matern12()

    # Standard tests:
    standard_kernel_tests(
        k,
        f1=lambda *xs: (5 * EQ())(*xs),
        f2=lambda *xs: 5 * EQ()(*xs),
    )
