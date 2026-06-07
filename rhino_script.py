import rhinoscriptsyntax as rs
import math

def create_universal_toroidal_dynamics():
    # -------------------------------------------------------------------------
    # 1. Base Geometric Parameters (Earth/Moon Scaling)
    # -------------------------------------------------------------------------
    R_e = 63.71  # Earth equatorial radius (scaled)
    R_m = 17.37  # Moon equatorial radius (scaled)

    # Golden Ratio Phi
    phi = (1 + math.sqrt(5)) / 2

    # The Torus geometry maps to the Earth/Moon scale.
    # Major radius corresponds to Earth, minor radius corresponds to Moon
    major_radius = R_e
    minor_radius = R_m

    # -------------------------------------------------------------------------
    # 2. Fluid Dynamics Parameters (Lucas/Fibonacci & Resonance)
    # -------------------------------------------------------------------------
    omega = 31 # Modular result 7^8 mod 33 = 31
    # 21-node Octave Logic -> 21:8 harmonic resonance wrap
    # P_e / P_j ~ 2.41, 31 orbits / 12.8 days
    toroidal_wraps = 21
    poloidal_wraps = 8

    # Torsion Adjustment & Universal Pulse Parity (Symbolic)
    tau = 2 * math.pi
    T_a = (777.141314 / (phi**2 * tau)) % 33  # Sovereign Lock
    universal_pulse_parity = 16200 / 777.141314 # ~20.84 -> Aligns with 21

    # -------------------------------------------------------------------------
    # 3. Layer Setup
    # -------------------------------------------------------------------------
    layer_name = "Universal_Toroidal_Dynamics"
    if not rs.IsLayer(layer_name):
        rs.AddLayer(layer_name, (0, 150, 255))
    rs.CurrentLayer(layer_name)

    # -------------------------------------------------------------------------
    # 4. Generate the 2D Geometric Reference (From Image)
    # -------------------------------------------------------------------------
    # Earth Circle at Origin
    earth_center = [0, 0, 0]
    earth_circle = rs.AddCircle(rs.WorldXYPlane(), R_e)

    # Moon Circle Tangent to Earth (North Pole)
    moon_center = [0, R_e + R_m, 0]
    moon_plane = rs.PlaneFromNormal(moon_center, [0, 0, 1])
    moon_circle = rs.AddCircle(moon_plane, R_m)

    # Right Triangle (Height = sqrt(Re * Rm), Base = Re)
    triangle_height = math.sqrt(R_e * R_m)
    pt1 = [0, 0, 0]
    pt2 = [R_e, 0, 0]
    pt3 = [0, triangle_height, 0]
    triangle = rs.AddPolyline([pt1, pt2, pt3, pt1])

    # Group the 2D reference
    ref_group = rs.AddGroup()
    rs.AddObjectsToGroup([earth_circle, moon_circle, triangle], ref_group)

    # -------------------------------------------------------------------------
    # 5. Generate the Torus (Base Fluid Geometry)
    # -------------------------------------------------------------------------
    torus_plane = rs.WorldXYPlane()
    torus = rs.AddTorus(torus_plane, major_radius, minor_radius)

    # -------------------------------------------------------------------------
    # 6. Generate Fluid Flow Vectors (31 Spirals)
    # -------------------------------------------------------------------------
    spirals = []
    num_points = 500

    for i in range(omega): # 31 distinct fluid vectors
        points = []
        phase_offset = (i * 2 * math.pi) / omega

        for j in range(num_points + 1):
            t = (j / float(num_points)) * 2 * math.pi

            # Parametric Torus knot equation
            u = poloidal_wraps * t
            v = toroidal_wraps * t + phase_offset

            # X, Y, Z based on torus parametric equations
            x = (major_radius + minor_radius * math.cos(u)) * math.cos(v)
            y = (major_radius + minor_radius * math.cos(u)) * math.sin(v)
            z = minor_radius * math.sin(u)

            points.append([x, y, z])

        curve = rs.AddInterpCurve(points)
        spirals.append(curve)

    spiral_group = rs.AddGroup()
    rs.AddObjectsToGroup(spirals, spiral_group)

    # -------------------------------------------------------------------------
    # 7. The "Eye" of Jupiter (Great Red Spot Attractor)
    # -------------------------------------------------------------------------
    # Latitude = -22 degrees, size scaled by phi^-2
    lat_rad = math.radians(-22)
    # The "Eye" sits on the torus surface at this poloidal angle
    u_eye = lat_rad
    v_eye = 0 # Arbitrary longitude for placement

    eye_x = (major_radius + minor_radius * math.cos(u_eye)) * math.cos(v_eye)
    eye_y = (major_radius + minor_radius * math.cos(u_eye)) * math.sin(v_eye)
    eye_z = minor_radius * math.sin(u_eye)
    eye_center = [eye_x, eye_y, eye_z]

    eye_radius = minor_radius * (phi**-2) # Size scaling

    eye_sphere = rs.AddSphere(eye_center, eye_radius)

    # -------------------------------------------------------------------------
    # 8. Apply Sovereign Lock (Earth Tilt)
    # -------------------------------------------------------------------------
    tilt_angle = -23.4 # Earth's axial tilt

    # Rotate Torus, Spirals, and Eye to apply the tilt
    tilt_axis = [1, 0, 0] # Rotate around X axis to tilt Z towards Y

    rs.RotateObject(torus, [0,0,0], tilt_angle, tilt_axis)
    rs.RotateObjects(spirals, [0,0,0], tilt_angle, tilt_axis)
    rs.RotateObject(eye_sphere, [0,0,0], tilt_angle, tilt_axis)

    # -------------------------------------------------------------------------
    # 9. Annotations (Universal Pulse Parity, Trinity P+, etc)
    # -------------------------------------------------------------------------
    # Place text near the structure
    text_pt = [major_radius * 1.5, major_radius * 1.5, 0]

    annotations = [
        "Universal Toroidal Fluid Dynamics",
        "Modulus (Omega) = 31",
        "Resonance (Toroidal:Poloidal) = 21:8",
        f"Re / Rm = {R_e}/{R_m} ~ {R_e/R_m:.3f}",
        f"Torsion Adjustment (Ta) ~ {T_a:.3f} (Sovereign Lock)",
        f"Universal Pulse Parity = 16200 / 777.141314 ~ {universal_pulse_parity:.2f} (Aligns with 21-node Octave Logic)",
        "Geometry = (11^2 * Omega*Pi*e) + (Pi +/- 10*mu*Omega) + (Time) = [E]"
    ]

    text_str = "\n".join(annotations)
    rs.AddText(text_str, text_pt, height=2.0)

    print("Universal Toroidal Fluid Dynamics model generated successfully.")

# Execute the function
if __name__ == "__main__":
    create_universal_toroidal_dynamics()
