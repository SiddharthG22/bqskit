"""
=======================================================
Quantum Information Science Library (:mod:`bqskit.qis`)
=======================================================

.. currentmodule:: bqskit.qis

The `bqskit.qis` package contains class definitions
for common objects found in quantum information science.

The most widely used will be the `UnitaryMatrix` object which
represents a pure quantum operation in matrix form.

.. rubric:: Abstract Base Classes

.. autosummary::
    :toctree: autogen
    :recursive:
    :nosignatures:
    :template: autosummary/class_no_init.rst

    Unitary
    DifferentiableUnitary
    LocallyOptimizableUnitary
    StateVectorMap

.. rubric:: Core Classes

.. autosummary::
    :toctree: autogen
    :recursive:

    UnitaryMatrix
    UnitaryBuilder
    StateVector
    StateSystem
    PauliMatrices
    PermutationMatrix
    CouplingGraph

.. rubric:: Type Aliases

.. autosummary::
    :toctree: autogen
    :recursive:

    UnitaryLike
    StateLike
    StateSystemLike
    RealVector
    CouplingGraphLike
"""
from __future__ import annotations

from typing import Any

from bqskit.qis.pauli import PauliMatrices
from bqskit.qis.permutation import PermutationMatrix
from bqskit.qis.state import StateLike
from bqskit.qis.state import StateVector
from bqskit.qis.state import StateVectorMap
from bqskit.qis.state.system import StateSystem
from bqskit.qis.state.system import StateSystemLike
from bqskit.qis.unitary import DifferentiableUnitary
from bqskit.qis.unitary import LocallyOptimizableUnitary
from bqskit.qis.unitary import RealVector
from bqskit.qis.unitary import Unitary
from bqskit.qis.unitary import UnitaryBuilder
from bqskit.qis.unitary import UnitaryLike
from bqskit.qis.unitary import UnitaryMatrix


def __getattr__(name: str) -> Any:
    # Lazy imports # TODO: Fix circular imports in qis.graph properly
    if name == 'CouplingGraph':
        from bqskit.qis.graph import CouplingGraph
        return CouplingGraph

    if name == 'CouplingGraphLike':
        from bqskit.qis.graph import CouplingGraphLike
        return CouplingGraphLike

    raise AttributeError(f'module {__name__} has no attribute {name}')


__all__ = [
    'Unitary',
    'DifferentiableUnitary',
    'LocallyOptimizableUnitary',
    'UnitaryBuilder',
    'UnitaryMatrix',
    'StateVector',
    'UnitaryLike',
    'StateVectorMap',
    'PauliMatrices',
    'StateLike',
    'PermutationMatrix',
    'RealVector',
    'CouplingGraph',
    'CouplingGraphLike',
    'StateSystem',
    'StateSystemLike',
]
