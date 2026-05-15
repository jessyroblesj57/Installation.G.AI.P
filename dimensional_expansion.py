import rhinoscriptsyntax as rs
import math

def generate_dimensional_expansion():
    """
    Generates a recursive dimensional expansion starting from a 3-4-5 right triangle.
    It creates "triangle pipes" by extending points and scaling geometry
    based on the user's defined electrical/scalar vectors.
    """

    # Core Mathematical Variables
    iterations = 7 # Number of recursive dimensional expansions
    scaling_vector = 0.70714 # Defined extension vector

    # 1. Define the base 3-4-5 right triangle at origin
    # Adjacent = 3, Opposite = 4, Hypotenuse = 5
    p1 = [0, 0, 0]
    p2 = [3, 0, 0]
    p3 = [3, 4, 0]

    base_points = [p1, p2, p3]

    # Group to hold all generated geometry
    cloud_group = rs.AddGroup("DIMENSIONAL_EXPANSION_LATTICE")
    rs.EnableRedraw(False)

    # Create the base triangle curve
    base_triangle = rs.AddPolyline([p1, p2, p3, p1])
    rs.ObjectColor(base_triangle, [0, 255, 0]) # Green base
    rs.AddObjectsToGroup([base_triangle], cloud_group)

    current_triangle = base_points

    # 2. Recursive Dimensional Expansion
    for i in range(1, iterations + 1):
        # Calculate the center (electrical observation point) of current triangle
        center_x = sum([pt[0] for pt in current_triangle]) / 3.0
        center_y = sum([pt[1] for pt in current_triangle]) / 3.0
        center_z = sum([pt[2] for pt in current_triangle]) / 3.0
        center_pt = [center_x, center_y, center_z]

        # Add observer point
        obs_pt = rs.AddPoint(center_pt)
        rs.ObjectColor(obs_pt, [255, 255, 0]) # Yellow observer
        rs.AddObjectsToGroup([obs_pt], cloud_group)

        # 3. Extend definitions to a new point (Z-axis translation & scalar expansion)
        # We project outward using the scaling_vector logic to form the "pipe"
        z_offset = (5 * i) * scaling_vector # Scale Z depth
        expansion_scale = 1 + (i * scaling_vector) # Scale triangle size up

        next_triangle = []
        for pt in current_triangle:
            # Scale point relative to center, then push to next dimension (Z)
            nx = center_x + (pt[0] - center_x) * expansion_scale
            ny = center_y + (pt[1] - center_y) * expansion_scale
            nz = pt[2] + z_offset
            next_triangle.append([nx, ny, nz])

        # Draw the next dimensional triangle
        next_curve = rs.AddPolyline([next_triangle[0], next_triangle[1], next_triangle[2], next_triangle[0]])

        # Color gradient based on iteration
        r = min(255, int(50 * i))
        g = min(255, int(255 - (20 * i)))
        b = min(255, int(100 + (25 * i)))
        rs.ObjectColor(next_curve, [r, g, b])
        rs.AddObjectsToGroup([next_curve], cloud_group)

        # 4. Create the "Triangle Pipe" (Dimensional Plane connecting the instances)
        pipe_lines = []
        for j in range(3):
            # Connect corresponding vertices between current and next triangle
            line = rs.AddLine(current_triangle[j], next_triangle[j])
            rs.ObjectColor(line, [0, 255, 255]) # Cyan connecting pipes
            pipe_lines.append(line)

        rs.AddObjectsToGroup(pipe_lines, cloud_group)

        # Update current triangle for next recursive iteration
        current_triangle = next_triangle

    rs.EnableRedraw(True)
    rs.ZoomExtents()

    print("DIMENSIONAL EXPANSION COMPLETE")
    print(f"Base Geometry: 3-4-5 Triangle")
    print(f"Iterations: {iterations}")
    print(f"Scaling Vector Applied: {scaling_vector}")
    print("Status: Dimensional Triangle Pipe Lattice Generated")

if __name__ == "__main__":
    generate_dimensional_expansion()
