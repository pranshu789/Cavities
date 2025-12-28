#SAMPLE INPUTS (this file is not executable, simply a database for commonly used cavity geometries

# ----------------- 4 MIRROR Tetrahedral --------------------- #

coords = [
    [3.5, 0, 5],
    [3.5, 5, 0],
    [0, 0, 0],
    [0, 5, 5]
]

n_mirrors = len(coords)
start_mirror = 2   

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





