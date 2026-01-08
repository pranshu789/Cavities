import numpy as np
import matplotlib
#matplotlib.use("TkAgg") #required in MacOS, otherwise ignore
import matplotlib.pyplot as plt


#------------------ INPUT PARAMETERS OF THE CAVITY -------------------------# (Sample parameters are given in the input.py file, simply copy, and replace the ones below or write your own!)

# 4-mirror Tetrahedral
coords = [
    [4.85, 0, 5],
    [4.85, 20, 0],
    [0, 0, 0],
    [0, 20, 5]
]

start_mirror = 1   # the starting mirror aka the section you want access to
n_mirrors = len(coords)

# mirror types: 1=mirrors with delta dephasing to be varied, 2,3,4=other mirrors with known dephasings
mirror_types = [1,1,1,1]

# Reflectivities
rho_p_1, rho_s_1 = 0.997283, 0.997452





# ---------------- METHODS FOR JONES MATRIX CALCULATION --------------------#

def normalize(v):
    return v / np.linalg.norm(v)

def reflection_matrix(i, delta=0):
    m_type = mirror_types[i]
    rho_s = globals()[f"rho_s_{m_type}"]
    rho_p = globals()[f"rho_p_{m_type}"]
    phi_s = 0
    phi_p = (delta) if m_type == 1 else globals()[f"phi_p_{m_type}"]
    return np.diag([
        rho_s * np.exp(1j * phi_s),
        rho_p * np.exp(1j * phi_p)
    ])

def local_basis(i):
    kin = normalize(np.array(coords[i])-np.array(coords[i-1]))
    kout = normalize(np.array(coords[(i+1)%n_mirrors])-np.array(coords[i]))
    nvec = normalize(-kin+kout)
    svec = normalize(np.cross(nvec,kin))
    pvec = normalize(np.cross(kin,svec))
    return pvec, svec, kin

def rotation_angle(i):
    _, svec_i, _ = local_basis(i)
    _, svec_next, _ = local_basis((i+1)%n_mirrors)
    cos_a = np.clip(np.dot(svec_i,svec_next),-1,1)
    return np.degrees(np.arccos(cos_a))

def angle_of_incidence(i):
    kin = normalize(np.array(coords[i])-np.array(coords[i-1]))
    kout = normalize(np.array(coords[(i+1)%n_mirrors])-np.array(coords[i]))
    nvec = normalize(-kin+kout)
    cos_theta = np.clip(np.abs(np.dot(kin,nvec)),-1,1)
    return np.degrees(np.arccos(cos_theta))

def rotation_matrix(i):
    _, svec_i, _ = local_basis(i)
    _, svec_next, _ = local_basis((i+1)%n_mirrors)
    cos_a = np.clip(np.dot(svec_i, svec_next), -1, 1)
    sin_a = np.sqrt(1 - cos_a**2)
    return np.array([[cos_a, sin_a], [-sin_a, cos_a]])

def round_trip(delta=0, start=start_mirror - 1):
    J = np.identity(2, dtype=complex)
    for j in range(n_mirrors):
        i = (start + j) % n_mirrors
        R = rotation_matrix(i)
        M = reflection_matrix(i, delta)
        J = R @ M @ J
    return J

def circularity(delta):
    J = round_trip(delta)
    eigvals, eigvecs = np.linalg.eig(J)
    circ_vals = []
    for v in eigvecs.T:
        S0 = np.abs(v[0])**2 + np.abs(v[1])**2
        S3 = 2 * np.imag(np.conj(v[0])*v[1])
        circ_vals.append(np.abs(S3)/S0)
    return max(circ_vals)


# ------------------- PLOTTING ------------------------#

deltas = np.linspace(0, 2*np.pi, 200)
circ_vals = [circularity(delta) for delta in deltas]

plt.plot(deltas*180/np.pi, circ_vals, color='red', linewidth=3)
plt.xlabel("Dephasing Δϕ (deg)")
plt.ylabel("Degree of circularity |S3/S0|")
plt.title("Circularity vs Dephasing")
plt.grid(True)
plt.ylim(0, 1.05)
plt.xlim(0, 360)
plt.show()


# --------------------- PRINTING SOME VALUES -------------#

print("\n===== ANGLES OF INCIDENCE (AOI) =====")
for i in range(n_mirrors):
    aoi = angle_of_incidence(i)
    print(f"AOI at mirror {i+1}: {aoi:.2f} degrees")

print("\n===== ROTATION ANGLES (α) =====")
for i in range(n_mirrors):
    ang = rotation_angle(i)
    print(f"Rotation angle between mirrors {i+1} → {(i+2)%n_mirrors}: {ang:.2f} degrees")

specific_degrees = [30, 60, 90, 180, 210, 240, 270, 330]
print("\nCircularity values:")
for deg in specific_degrees:
    delta_rad = np.deg2rad(deg)
    circ_val = circularity(delta_rad)
    print(f"Δϕ = {deg}° : Circularity = {circ_val:.4f}")
