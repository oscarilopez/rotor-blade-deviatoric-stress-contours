import os
import numpy as np
import matplotlib.pyplot as plt

# -----------------------------
# Parameters (from project table)
# -----------------------------
L = 0.3
w = 0.1
t = 0.025

Rr = 1.0
Ro = 1.3

rho1 = 4500.0
rho2 = 8908.0
v1_const = 0.7
v2_const = 0.3
rho = v1_const * rho1 + v2_const * rho2

Nx = 60
Ny = 200

omega_list = np.array([0, 40, 160, 350, 625, 975, 1400, 1900], dtype=float)
alpha_list = np.array([0, 2250, 9000, 20000, 40000, 63000, 90000, 165000], dtype=float)

# Section properties
A = w * t
Izz = t * w**3 / 12.0

# Output folder
OUTDIR = "figures"
os.makedirs(OUTDIR, exist_ok=True)


# -----------------------------
# Internal resultants along blade
# (consistent with beam relations using distributed inertial load ~ rho*A*(...) * r )
# -----------------------------
def resultants(r, omega, alpha):
    """
    r in [Rr, Ro]
    returns (F_r, V_r, M_r) at section r with free-end boundary conditions at r=Ro.
    """
    # distributed load magnitudes proportional to r
    # Use omega^2 for centrifugal contribution and alpha for tangential contribution
    q_omega = rho * A * (omega**2) * r
    q_alpha = rho * A * (alpha) * r

    # For q = c*r, with free end at Ro:
    # V(r) = ∫_r^Ro q(s) ds = c/2 (Ro^2 - r^2)
    # M(r) = ∫_r^Ro V(s) ds = c*( Ro^3/3 - Ro^2*r/2 + r^3/6 )
    c_omega = rho * A * (omega**2)
    c_alpha = rho * A * (alpha)

    V_omega = 0.5 * c_omega * (Ro**2 - r**2)
    M_omega = c_omega * (Ro**3 / 3.0 - (Ro**2) * r / 2.0 + r**3 / 6.0)

    V_alpha = 0.5 * c_alpha * (Ro**2 - r**2)

    # In this model we use:
    # - axial force from centrifugal scaling (same functional form as V_omega here)
    # - shear from alpha scaling
    # - bending moment from omega scaling
    F_r = V_omega
    V_r = V_alpha
    M_r = M_omega

    return F_r, V_r, M_r



# Deviatoric stress norm field

def deviatoric_norm_field(omega, alpha):
    x_edges = np.linspace(-w / 2.0, w / 2.0, Nx + 1)
    y_edges = np.linspace(0.0, L, Ny + 1)

    x_cent = 0.5 * (x_edges[:-1] + x_edges[1:])
    y_cent = 0.5 * (y_edges[:-1] + y_edges[1:])

    Xc, Yc = np.meshgrid(x_cent, y_cent)

    # Map blade coordinate y -> radius r
    r = Rr + Yc

    # Resultants (vectorized)
    F_r, V_r, M_r = resultants(r, omega, alpha)

    # Bending stress variation across x (neutral axis at x=0)
    sigma_xx = (F_r / A) - (M_r / Izz) * Xc

    # Rectangle shear formula uses Q(x) about neutral axis
    # Here x is measured from -w/2 to +w/2
    # Use x' = Xc (already centered)
    Q = t * (0.5 * w - np.abs(Xc)) * (0.25 * w + 0.5 * np.abs(Xc))
    tau_xy = (V_r * Q) / (Izz * t)

    # Plane stress deviatoric norm:
    # ||S_dev|| = sqrt( (2/3)*sigma^2 + 2*tau^2 )
    Sdev = np.sqrt((2.0 / 3.0) * sigma_xx**2 + 2.0 * tau_xy**2)

    return Xc, Yc, Sdev


# Main run: 8 plots total

def main():
    for i, (omega, alpha) in enumerate(zip(omega_list, alpha_list), start=1):
        Xc, Yc, Sdev = deviatoric_norm_field(omega, alpha)

        plt.figure(figsize=(6.5, 5))
        cf = plt.contourf(Xc, Yc, Sdev, levels=60)
        plt.colorbar(cf, label=r"$\|\mathbf{S}_{dev}\|$")

        plt.xlabel("x [m]")
        plt.ylabel("y [m]")
        plt.title(rf"$\|\mathbf{{S}}_{{dev}}\|$ at $\omega={omega:.0f}$ rad/s, $\alpha={alpha:.0f}$ rad/s$^2$")

        fname = f"Sdev_{i:02d}_omega_{int(omega)}_alpha_{int(alpha)}.png"
        plt.tight_layout()
        plt.savefig(os.path.join(OUTDIR, fname), dpi=250)
        plt.close()

    print(f"Done. Saved {len(omega_list)} plots to ./{OUTDIR}/")


if __name__ == "__main__":
    main()
    
