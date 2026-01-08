import numpy as np
import matplotlib
#matplotlib.use("TkAgg") #required in MacOS, otherwise ignore
import matplotlib.pyplot as plt


#------------------ INPUT PARAMETERS OF THE CAVITY -------------------------# (Sample parameters are given in the input.py file, simply copy, and replace the ones below (be careful: need to modify somethings here) or write your own!)

# 4-mirror Tetrahedral

# ------- USER INPUT FOR g_var ---------#
#put the coords inside this function and add the g_var however you want it varied
#in the plotting function at the end, change the units and name of your geometric variable as you want


def get_coords(g_var):
    return [
    [5, 0, 5*np.tan(g_var/2)],
    [5, 20, 0],
    [0, 0, 0],
    [0, 20, 5*np.tan(g_var/2)]
]

g_var_min = 0.0
g_var_max = 90.0
n_g = 100

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

def local_basis(i):
    kin = normalize(np.array(coords[i]) - np.array(coords[i-1]))
    kout = normalize(np.array(coords[(i+1)%n_mirrors]) - np.array(coords[i]))
    nvec = normalize(-kin + kout)
    svec = normalize(np.cross(nvec, kin))
    pvec = normalize(np.cross(kin, svec))
    return pvec, svec, kin

def rotation_angle(i):
    _, svec_i, _ = local_basis(i)
    _, svec_next, _ = local_basis((i+1)%n_mirrors)
    cos_a = np.clip(np.dot(svec_i,svec_next),-1,1)
    return np.degrees(np.arccos(cos_a))

def angle_of_incidence(i):
    global coords
    kin = normalize(np.array(coords[i])-np.array(coords[i-1]))
    kout = normalize(np.array(coords[(i+1)%n_mirrors])-np.array(coords[i]))
    nvec = normalize(-kin+kout)
    cos_theta = np.clip(np.abs(np.dot(kin,nvec)),-1,1)
    return np.degrees(np.arccos(cos_theta))


# ------------------- PLOTTING 1D GRAPHS ------------------------#

rotation_angles_all = np.zeros((n_mirrors, n_g))
aoi_all = np.zeros((n_mirrors, n_g))

for ig, g in enumerate(g_vars):
    coords = get_coords(g)
    for i in range(n_mirrors):
        rotation_angles_all[i, ig] = rotation_angle(i)
        aoi_all[i, ig] = angle_of_incidence(i)

plt.figure(figsize=(8,5))
line_styles = ['-', '--', ':', '-.']
for i in range(n_mirrors):
    plt.plot(np.rad2deg(g_vars), rotation_angles_all[i], linestyle=line_styles[i % len(line_styles)], linewidth=2, label=f'Mirror {i+1}')
plt.xlabel("Geometric variable g_var (deg)")
plt.ylabel("Rotation angle α (deg)")
plt.title("Rotation Angles vs Geometric Variable")
plt.legend()
plt.grid(True)
plt.show()

plt.figure(figsize=(8,5))
for i in range(n_mirrors):
    plt.plot(np.rad2deg(g_vars), aoi_all[i], linestyle=line_styles[i % len(line_styles)], linewidth=2, label=f'Mirror {i+1}')
plt.xlabel("Geometric variable g_var (deg)")
plt.ylabel("Angle of incidence AOI (deg)")
plt.title("AOI vs Geometric Variable")
plt.legend()
plt.grid(True)
plt.show()


# --------------------- PRINTING SOME VALUES -------------#

def print_angles(g_deg):

    global coords
    g_rad = np.deg2rad(g_deg)
    coords = get_coords(g_rad)

    print("\n")
    print(f"\nParameters for g_var = {g_deg:.2f}°")
    print("=" * 60)

    print("Mirror | AOI (deg) | Rotation Angle α (deg) ")
    print("-" * 60)
    for i in range(n_mirrors):
        aoi = angle_of_incidence(i)
        rot = rotation_angle(i)
        print(f"{i+1:6d} | {aoi:9.2f} | {rot:18.2f}")

specific_g_deg = [2,71,90]

for g in specific_g_deg:
    print_angles(g)

