import numpy as np
import matplotlib
#matplotlib.use("TkAgg") #required in MacOS, otherwise ignore
import matplotlib.pyplot as plt

#------------------ INPUT PARAMETERS OF THE CAVITY -------------------------# (Sample parameters are given in the input.py file, simply copy, and replace the ones below or write your own!)

# 4-mirror Tetrahedral

# ------------- USER INPUT FOR g_var ---------------------------------------#
#put the coords inside this function and add the g_var however you want it varied
#in the plotting function at the end, change the units and name of your geometric variable as you want


def get_coords(g_var):
    return [
    [5, 0, 5*np.tan(g_var/2)],
    [5, 5, 0],
    [0, 0, 0],
    [0, 5, 5*np.tan(g_var/2)]
]

g_var_min = 0.0
g_var_max = 90.0
n_g = 400

g_vars = np.linspace(np.deg2rad(g_var_min), np.deg2rad(g_var_max), n_g)
coords = get_coords(g_vars[0])

start_mirror = 2   # the starting mirror aka the section you want access to
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
    kin = normalize(np.array(coords[i]) - np.array(coords[i-1]))
    kout = normalize(np.array(coords[(i+1)%n_mirrors]) - np.array(coords[i]))
    nvec = kin + kout
    svec = normalize(np.cross(nvec, kin))
    pvec = normalize(np.cross(kin, svec))
    return pvec, svec, kin

def rotation_angle(i):
    _, svec_i, _ = local_basis(i)
    _, svec_next, _ = local_basis((i+1)%n_mirrors)
    cos_a = np.clip(np.dot(svec_i,svec_next),-1,1)
    return np.degrees(np.arccos(cos_a))


def angle_of_incidence(i):
    kin = normalize(np.array(coords[i])-np.array(coords[i-1]))
    kout = normalize(np.array(coords[(i+1)%n_mirrors])-np.array(coords[i]))
    nvec = -kin+kout
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


deltas = np.linspace(0, np.pi*2, 400)
circ_map = np.zeros((len(g_vars), len(deltas)))

for ig, g in enumerate(g_vars):
    coords = get_coords(g)
    for id, delta in enumerate(deltas):
        circ_map[ig,id]=circularity(delta)

print("\n===== ANGLES OF INCIDENCE (AOI) =====")
for i in range(n_mirrors):
    aoi = angle_of_incidence(i)
    print(f"AOI at mirror {i+1}: {aoi:.4f} degrees")

print("\n===== ROTATION ANGLES (α) =====")
for i in range(n_mirrors):
    ang = rotation_angle(i)
    print(f"Rotation angle between mirrors {i+1} → {(i+2)%n_mirrors}: {ang:.4f} degrees")


plt.figure(figsize=(8,6))


plt.imshow(
    circ_map,
    cmap="RdBu_r",
    origin="lower",
    aspect="auto",
    extent = [ deltas[0]*180/np.pi, deltas[-1]*180/np.pi, g_vars[0]*180/np.pi, g_vars[-1]*180/np.pi],
    vmin=0,
    vmax=1
)


plt.colorbar(label="Degree of circularity |S3/S0|")
plt.xlabel("Dephasing Δϕ (deg)")
plt.ylabel("geometric variable (unit)")
plt.title("Circulqrity vs Dephasing and g_var")

plt.show()


# --------------------- PRINTING SOME VALUES -------------#
specific_g_deg = [2,71,90]
specific_delta_deg = [30,90,180]


print("\nCircularity values:")

for g_deg in specific_g_deg:
    g_rad = np.deg2rad(g_deg)
    coords = get_coords(g_rad)

    for delta_deg in specific_delta_deg:
        delta_rad = np.deg2rad(delta_deg)
        circ_val = circularity(delta_rad)

    print(f"g_var = {g_deg:6.2f}°  | "f"Δϕ = {delta_deg:6.1f}°  → "f"Circularity = {circ_val:.4f}")
