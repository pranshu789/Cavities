#SAMPLE INPUTS (this file is not executable, simply a database for commonly used cavity geometries

# ----------------- 4 MIRROR Tetrahedral --------------------- #

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


# ------------------ 10 MIRROR Spacecraft --------------------#

coords = [
    [13, 0, 6],
    [9, -36, 6],
    [6, -15, 9],
    [6, -48, 13],
    [6, -48, 17],
    [6, 0, 13],
    [6, -36, 9],
    [9, -15, 6],
    [13, -48, 6],
    [17, -48, 6]
]

n_mirrors = len(coords)
start_mirror = 5  


mirror_types = [2,2,2,1,1,2,2,2,1,1]

# Reflectivities
rho_p_2, rho_s_2 = 0.997283, 0.997452
rho_p_1, rho_s_1 = 0.9990, 0.9995

phi_p_2 = 0


# -------------------- 6 MIRROR Manta ----------------------#

coords = [
    [1, 0, -1],
    [-1, -600, 1],
    [-1, -300, 520],
    [-1, 0, 1],
    [1, -600, -1],
    [520, -300, -1]
]

n_mirrors = len(coords)
start_mirror = 3    # the starting mirror aka the section you want access to

# mirror types: 1=mirrors with delta dephasing to be varied, 2,3,4=other mirrors with known dephasings
mirror_types = [1,1,1,1,1,1]

# Reflectivities
rho_p_1, rho_s_1 = 0.9990, 0.9995

#known dephasings
phi_p_2 = 0



