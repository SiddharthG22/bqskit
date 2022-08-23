from __future__ import annotations

import pytest
import qiskit.quantum_info as qi
from qiskit import QuantumCircuit
from qiskit import transpile

from bqskit.compiler.compile import compile
from bqskit.ext import bqskit_to_qiskit
from bqskit.ext import qiskit_to_bqskit
from bqskit.ir.circuit import Circuit
from bqskit.ir.gates import CNOTGate
from bqskit.ir.gates import U3Gate
from bqskit.qis import UnitaryMatrix


class TestTranslate:

    @pytest.fixture
    def bqskit_circuit(self) -> Circuit:
        circuit = Circuit(3)
        circuit.append_gate(CNOTGate(), (0, 1))
        circuit.append_gate(U3Gate(), 0, [1, 2, 3])
        circuit.append_gate(U3Gate(), 1, [1, 2, 3])
        circuit.append_gate(U3Gate(), 2, [1, 2, 3])
        circuit.append_gate(CNOTGate(), (0, 1))
        circuit.append_gate(CNOTGate(), (0, 2))
        circuit.append_gate(CNOTGate(), (0, 2))
        circuit.append_gate(U3Gate(), 0, [1, 2.4, 3])
        circuit.append_gate(U3Gate(), 1, [1, 2.2, 3])
        circuit.append_gate(U3Gate(), 2, [1, 2.1, 3])
        circuit.append_gate(U3Gate(), 2, [1, 2.1, 3])
        circuit.append_gate(CNOTGate(), (0, 2))
        circuit.append_gate(CNOTGate(), (0, 2))
        circuit.append_gate(CNOTGate(), (0, 1))
        circuit.append_gate(CNOTGate(), (0, 2))
        circuit.append_gate(U3Gate(), 0, [1, 2.4, 3])
        circuit.append_gate(U3Gate(), 1, [1, 2.2, 3])
        circuit.append_gate(U3Gate(), 2, [1, 2.1, 3])
        return circuit

    @pytest.fixture
    def qiskit_circuit(self) -> QuantumCircuit:
        circuit = QuantumCircuit(3)
        circuit.cnot(0, 1)
        circuit.u(1, 2, 3, 0)
        circuit.u(1, 2, 3, 1)
        circuit.u(1, 2, 3, 2)
        circuit.cnot(0, 1)
        circuit.cnot(0, 2)
        circuit.cnot(0, 2)
        circuit.u3(1, 2.4, 3, 0)
        circuit.u(1, 2.2, 3, 1)
        circuit.u(1, 2.1, 3, 2)
        circuit.u(1, 2.1, 3, 2)
        circuit.cnot(0, 2)
        circuit.cnot(0, 2)
        circuit.cnot(0, 1)
        circuit.cnot(0, 2)
        circuit.u(1, 2.4, 3, 0)
        circuit.u(1, 2.2, 3, 1)
        circuit.u(1, 2.1, 3, 2)
        return circuit

    def test_bqskit_to_bqskit(self, bqskit_circuit: Circuit) -> None:
        in_utry = bqskit_circuit.get_unitary()
        out_circuit = qiskit_to_bqskit(bqskit_to_qiskit(bqskit_circuit))
        out_utry = out_circuit.get_unitary()
        assert in_utry.get_distance_from(out_utry) < 1e-7

    def test_qiskit_to_qiskit(self, qiskit_circuit: QuantumCircuit) -> None:
        qc = qiskit_circuit
        in_utry = UnitaryMatrix(qi.Operator(qc).data)
        out_circuit = bqskit_to_qiskit(qiskit_to_bqskit(qc))
        out_utry = UnitaryMatrix(qi.Operator(out_circuit).data)
        assert in_utry.get_distance_from(out_utry) < 1e-7

    def test_compile_bqskit(self, qiskit_circuit: QuantumCircuit) -> None:
        qc = qiskit_circuit
        in_utry = UnitaryMatrix(qi.Operator(qc).data)
        bqskit_circuit = qiskit_to_bqskit(qc)
        bqskit_out_circuit = compile(
            bqskit_circuit, block_size=2, max_synthesis_size=2,
        )
        out_circuit = bqskit_to_qiskit(bqskit_out_circuit)
        out_utry = UnitaryMatrix(qi.Operator(out_circuit).data)
        assert in_utry.get_distance_from(out_utry) < 1e-5

    def test_synthesis_bqskit(self, qiskit_circuit: QuantumCircuit) -> None:
        qc = qiskit_circuit
        in_utry = UnitaryMatrix(qi.Operator(qc).data)
        bqskit_circuit = qiskit_to_bqskit(qc)
        bqskit_out_circuit = compile(bqskit_circuit)
        out_circuit = bqskit_to_qiskit(bqskit_out_circuit)
        out_utry = UnitaryMatrix(qi.Operator(out_circuit).data)
        assert in_utry.get_distance_from(out_utry) < 1e-5

    def test_compile_qiskit(self, bqskit_circuit: Circuit) -> None:
        in_utry = bqskit_circuit.get_unitary()
        qiskit_circuit = bqskit_to_qiskit(bqskit_circuit)
        qc_out = transpile(qiskit_circuit, optimization_level=3)
        bqskit_out_circuit = qiskit_to_bqskit(qc_out)
        out_utry = bqskit_out_circuit.get_unitary()
        assert in_utry.get_distance_from(out_utry) < 1e-5
