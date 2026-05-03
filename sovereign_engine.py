import math

try:
    import rhinoscriptsyntax as rs
except ImportError:
    # Mocking rs for environments outside of Rhino
    rs = None

class RhinoSovereignEngine:
    def __init__(self):
        # Universal Constants (Validated Geometric Parameters)
        # phi = 2 * cos(36 degrees)
        self.PHI = 2 * math.cos(math.radians(36))
        self.WATER_BOND_ANGLE = 104.5
        self.MODULO_LOCK = 61
        self.DANA_CONSTANT = 1.1517     # The Non-Static Love Glue (Z-Axis)
        self.BASE_33 = 33
        self.ACTIVE_STATE = 34

        # Origin - Point E (The Universal Truth Intersection)
        self.origin = [0, 0, 0]

    def construct_dodecreation_plane(self):
        """
        Creates the base observation plane where data is evaluated.
        This represents the Alpha/Beta/Gamma Tri-Axial Threading.
        """
        if rs is None: return

        size = 100 * self.PHI

        # Create corner points for the plane
        pt1 = [-size, -size, 0]
        pt2 = [size, -size, 0]
        pt3 = [size, size, 0]
        pt4 = [-size, size, 0]

        # Create the surface in Rhino
        plane_id = rs.AddSrfPt([pt1, pt2, pt3, pt4])
        rs.ObjectName(plane_id, "DODECA_OBSERVATION_PLANE")
        rs.ObjectColor(plane_id, [0, 0, 128]) # Deep blue
        return plane_id

    def render_point_e(self):
        """
        Renders the singular point of connection (11^2, 314, etc.)
        """
        if rs is None: return

        pt_id = rs.AddPoint(self.origin)
        rs.ObjectName(pt_id, "POINT_E_SINGULARITY")
        rs.ObjectColor(pt_id, [255, 215, 0]) # Gold

        # Add a sphere to make it visible
        sphere_id = rs.AddSphere(self.origin, self.DANA_CONSTANT * 5)
        rs.ObjectColor(sphere_id, [255, 215, 0])
        return pt_id

    def evaluate_data_query(self, query_seed):
        """
        The Filter: Acts as an automatic drive. Feeds data through the geometry.
        If it hits the Modulo 61 lock, it collapses to the center (Point E).
        If not, it scatters as 'Imagination/Torsion'.
        """
        # Convergence Lock check (Modulo 61)
        is_sovereign_lock = (query_seed % self.MODULO_LOCK) == 0

        # Calculate where this data point lands visually
        if is_sovereign_lock:
            # It collapses to Point E (Z-axis lifted by Dana's Constant)
            target_pt = [0, 0, self.DANA_CONSTANT * 10]
            color = [0, 255, 0] # Green for 1:1 Parity
            name = f"LOCKED_DATA_{query_seed}"
        else:
            # It scatters into the lattice (Torsion)
            # Using math to create a spiraling scatter effect based on the seed
            x_scatter = math.cos(query_seed) * (query_seed % 50)
            y_scatter = math.sin(query_seed) * (query_seed % 50)
            target_pt = [x_scatter, y_scatter, 0]
            color = [255, 0, 0] # Red for Torsion/Noise
            name = f"TORSION_DATA_{query_seed}"

        if rs is not None:
            # Draw the point in Rhino
            data_pt_id = rs.AddPoint(target_pt)
            rs.ObjectName(data_pt_id, name)
            rs.ObjectColor(data_pt_id, color)

            # Draw a line connecting the data to the origin (Point E) to show the relationship
            line_id = rs.AddLine(target_pt, self.origin)
            rs.ObjectColor(line_id, color)

        return is_sovereign_lock, target_pt

    def generate_nilchi_lattice(self, node_count=144):
        """
        Generates nodes of the Nilchi Lattice around the plane.
        """
        nodes = []
        for i in range(node_count):
            # Example propagation logic using PHI and Modulo 61
            angle = i * self.PHI * 10
            radius = (i % self.MODULO_LOCK) * self.PHI * 2

            # Use water bond angle for Z-axis influence
            z = math.sin(math.radians(i * self.WATER_BOND_ANGLE)) * 10

            x = math.cos(angle) * radius
            y = math.sin(angle) * radius

            pt = [x, y, z]
            nodes.append(pt)

            if rs is not None:
                pt_id = rs.AddPoint(pt)
                rs.ObjectColor(pt_id, [150, 150, 150]) # Grey for lattice nodes

        return nodes

# --- Implementation Instructions ---
# 1. Open Rhino 8.
# 2. Type `EditPythonScript` into the command line to open the editor.
# 3. Paste this entire code block into the editor.
# 4. Click the green "Play" button to run the engine.

if __name__ == "__main__":
    # Initialize the Engine
    engine = RhinoSovereignEngine()

    if rs is not None:
        # 1. Build the structure
        engine.construct_dodecreation_plane()
        engine.render_point_e()

        # 2. Generate Lattice
        engine.generate_nilchi_lattice(144)

        # 3. Feed it Data Queries (Testing the Filter)

        # Noise
        engine.evaluate_data_query(500.0)
        engine.evaluate_data_query(144.0)

        # Universal Truth (Multiple of 61)
        engine.evaluate_data_query(366.0)
        engine.evaluate_data_query(610.0)
    else:
        print("Sovereign Engine initialized in headless mode (Rhino not detected).")
        print(f"PHI: {engine.PHI}")
        print(f"Testing lock for 366: {engine.evaluate_data_query(366.0)[0]}")
        print(f"Testing lock for 500: {engine.evaluate_data_query(500.0)[0]}")
