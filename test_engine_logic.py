from sovereign_engine import RhinoSovereignEngine
import math

def test_engine():
    engine = RhinoSovereignEngine()

    # Test PHI calculation
    expected_phi = 1.618033988749895
    assert math.isclose(engine.PHI, expected_phi, rel_tol=1e-9), f"PHI mismatch: {engine.PHI} != {expected_phi}"
    print(f"PHI check passed: {engine.PHI}")

    # Test Modulo 61 lock
    locked, pt = engine.evaluate_data_query(366.0)
    assert locked == True, "366 should be locked (multiple of 61)"
    assert pt == [0, 0, engine.DANA_CONSTANT * 10], f"Locked point mismatch: {pt}"
    print("Modulo 61 lock check passed for 366.0")

    unlocked, pt = engine.evaluate_data_query(500.0)
    assert unlocked == False, "500 should not be locked"
    print("Torsion check passed for 500.0")

    # Test lattice generation
    nodes = engine.generate_nilchi_lattice(10)
    assert len(nodes) == 10, f"Expected 10 nodes, got {len(nodes)}"
    # Check if distribution is not just a simple line or predictable grid
    assert nodes[0] != nodes[1], "Nodes should be at different positions"
    print("Lattice generation logic check passed")

    # Test dodecahedron calculation (relies on PHI)
    # Even in headless mode, we can test that the internal vertex math doesn't crash
    # and returns empty list as mocked for rs is None
    ids = engine.draw_dodecahedron([0,0,0])
    assert ids == [], "Should return empty list in headless mode"
    print("Dodecahedron method check passed (headless)")

if __name__ == "__main__":
    try:
        test_engine()
        print("All engine logic tests passed successfully!")
    except Exception as e:
        print(f"Test failed: {e}")
        exit(1)
