import numpy as np
import pyqtgraph as pg
import pyqtgraph.opengl as gl
from PyQt5 import QtWidgets, QtCore


# ==========================================================
# december 1ST 2025 — Modified for QWP Input
# ==========================================================

class PolarizationWaveWithSliderLabels(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Polarization Eigenmode Coupling - Visualizer")

        # Master layout
        main_layout = QtWidgets.QVBoxLayout()
        self.setLayout(main_layout)

        views_layout = QtWidgets.QHBoxLayout()
        main_layout.addLayout(views_layout, 1)

        # ==========================================================
        # LEFT SIDE: INPUT VIEW WITH QWP
        # ==========================================================
        left_layout = QtWidgets.QVBoxLayout()
        views_layout.addLayout(left_layout, 2)

        input_title = QtWidgets.QLabel("Input Polarization (S-pol → QWP)")
        input_title.setAlignment(QtCore.Qt.AlignCenter)
        input_title.setStyleSheet("font-weight: bold; font-size: 16px; margin-bottom: 5px;")
        left_layout.addWidget(input_title)

        self.input_view = gl.GLViewWidget()
        self.input_view.setMinimumWidth(300)
        self.input_view.setMinimumHeight(600)
        self.input_view.opts['distance'] = 8
        self.input_view.opts['elevation'] = 15
        self.input_view.opts['azimuth'] = 45
        self.input_view.setBackgroundColor('w')
        left_layout.addWidget(self.input_view)

        axis_in = gl.GLAxisItem()
        axis_in.setSize(12, 5, 5)
        self.input_view.addItem(axis_in)

        # input curves
        self.input_p_curve = gl.GLLinePlotItem(width=1, antialias=True, color=(255, 0, 0, 50))
        self.input_s_curve = gl.GLLinePlotItem(width=1, antialias=True, color=(0, 0, 255, 50))
        self.input_result_curve = gl.GLLinePlotItem(width=4, antialias=True, color=(0, 0, 0, 255))
        self.input_view.addItem(self.input_p_curve)
        self.input_view.addItem(self.input_s_curve)
        self.input_view.addItem(self.input_result_curve)

        # input vectors
        self.input_p_vectors = gl.GLLinePlotItem(width=1, antialias=True, color=(255, 0, 0, 100), mode='lines')
        self.input_s_vectors = gl.GLLinePlotItem(width=1, antialias=True, color=(0, 0, 255, 100), mode='lines')
        self.input_result_vectors = gl.GLLinePlotItem(width=1, antialias=True, color=(0, 0, 0, 255), mode='lines')
        self.input_view.addItem(self.input_p_vectors)
        self.input_view.addItem(self.input_s_vectors)
        self.input_view.addItem(self.input_result_vectors)

        # ==========================================================
        # RIGHT SIDE: EIGEN VIEW
        # ==========================================================
        right_layout = QtWidgets.QVBoxLayout()
        views_layout.addLayout(right_layout, 2)

        eigen_title = QtWidgets.QLabel("Cavity Eigenmodes")
        eigen_title.setAlignment(QtCore.Qt.AlignCenter)
        eigen_title.setStyleSheet("font-weight: bold; font-size: 16px; margin-bottom: 5px;")
        right_layout.addWidget(eigen_title)

        self.eigen_view = gl.GLViewWidget()
        self.eigen_view.setMinimumWidth(300)
        self.eigen_view.setMinimumHeight(600)
        self.eigen_view.opts['distance'] = 15
        self.eigen_view.opts['elevation'] = 15
        self.eigen_view.opts['azimuth'] = 90
        self.eigen_view.setBackgroundColor('w')
        right_layout.addWidget(self.eigen_view)

        axis_eig = gl.GLAxisItem()
        axis_eig.setSize(12, 5, 5)
        self.eigen_view.addItem(axis_eig)

        # mirrors
        self.eigen_view.addItem(self.create_mirror(-5))
        self.eigen_view.addItem(self.create_mirror(5))

        # eigen curves
        self.eigen_p_curve = gl.GLLinePlotItem(width=1, antialias=True, color=(255, 0, 0, 50))
        self.eigen_s_curve = gl.GLLinePlotItem(width=1, antialias=True, color=(0, 0, 255, 50))
        self.eigen_result_curve = gl.GLLinePlotItem(width=4, antialias=True, color=(0, 0, 0, 255))
        self.eigen_view.addItem(self.eigen_p_curve)
        self.eigen_view.addItem(self.eigen_s_curve)
        self.eigen_view.addItem(self.eigen_result_curve)

        # eigen vectors
        self.eigen_p_vectors = gl.GLLinePlotItem(width=1, antialias=True, color=(255, 0, 0, 100), mode='lines')
        self.eigen_s_vectors = gl.GLLinePlotItem(width=1, antialias=True, color=(0, 0, 255, 100), mode='lines')
        self.eigen_result_vectors = gl.GLLinePlotItem(width=1, antialias=True, color=(0, 0, 0, 255), mode='lines')
        self.eigen_view.addItem(self.eigen_p_vectors)
        self.eigen_view.addItem(self.eigen_s_vectors)
        self.eigen_view.addItem(self.eigen_result_vectors)

        # ==========================================================
        # COUPLING BAR CHART
        # ==========================================================
        coupling_layout = QtWidgets.QVBoxLayout()
        views_layout.addLayout(coupling_layout, 1)

        coupling_title = QtWidgets.QLabel("Coupling")
        coupling_title.setAlignment(QtCore.Qt.AlignCenter)
        coupling_title.setStyleSheet("font-weight: bold; font-size: 16px; margin-bottom: 5px;")
        coupling_layout.addWidget(coupling_title)

        self.coupling_plot = pg.PlotWidget()
        self.coupling_plot.setBackground('w')
        self.coupling_plot.setYRange(0, 1.1)
        self.coupling_plot.setMouseEnabled(x=False, y=False)
        self.coupling_plot.hideButtons()
        ax_bottom = self.coupling_plot.getAxis('bottom')
        ax_bottom.setTicks([[(1, 'Eigenmode A'), (2, 'Eigenmode B')]])
        self.coupling_bar_item = pg.BarGraphItem(x=[1, 2], height=[0, 0],
                                                 width=0.6,
                                                 brush=(107, 142, 35), pen='k')
        self.coupling_plot.addItem(self.coupling_bar_item)
        coupling_layout.addWidget(self.coupling_plot)

        # ==========================================================
        # CONTROL SLIDERS
        # ==========================================================
        controls_layout = QtWidgets.QHBoxLayout()
        main_layout.addLayout(controls_layout, 0)

        # -------------- INPUT CONTROLS (Now only QWP slider) --------------
        left_controls = QtWidgets.QVBoxLayout()
        controls_layout.addLayout(left_controls, 2)

        self.qwp_slider, _ = self.create_slider(
            "QWP Angle", 0, -180, 180,
            left_controls,
            self.update_input_from_qwp,
            self.renderInputCircularity
        )

        self.input_circularity = self.create_styled_label("Input Circularity: -", left_controls)

        # -------------- EIGENMODE CONTROLS --------------------
        right_controls = QtWidgets.QVBoxLayout()
        controls_layout.addLayout(right_controls, 2)

        self.eigen_pAmp_slider, _ = self.create_slider(
            "Eigen P Amp", 1, 0, 1, right_controls,
            self.update_eigen_from_sliders, self.renderEigenCircularity)

        self.eigen_sAmp_slider, _ = self.create_slider(
            "Eigen S Amp", 1, 0, 1, right_controls,
            self.update_eigen_from_sliders, self.renderEigenCircularity)

        self.eigen_phase_slider, _ = self.create_slider(
            "Eigen Phase", 0, 0, 360, right_controls,
            self.update_eigen_from_sliders, self.renderEigenCircularity)

        self.eigen_circularity = self.create_styled_label("Eigen Circularity: -", right_controls)

        controls_layout.addStretch(1)

        # Initialize
        self.update_input_from_qwp()
        self.renderInputCircularity()
        self.update_eigen_from_sliders()
        self.renderEigenCircularity()
        self.renderCoupling()

    # ==========================================================
    # GEOMETRY HELPERS
    # ==========================================================
    def create_mirror(self, x_pos, radius=1.5, height=0.2, color=pg.mkColor(120, 120, 120, 120)):
        md = gl.MeshData.cylinder(rows=10, cols=20, radius=[radius, radius], length=height)
        mirror = gl.GLMeshItem(meshdata=md, smooth=True, color=color,
                               shader='shaded', drawEdges=False, drawFaces=True,
                               glOptions='opaque')
        mirror.rotate(90, 0, 1, 0)
        mirror.translate(x_pos, 0, 0)
        return mirror

    # ==========================================================
    # UI HELPERS
    # ==========================================================
    def create_styled_label(self, text, layout):
        label = QtWidgets.QLabel(text)
        label.setAlignment(QtCore.Qt.AlignCenter)
        label.setStyleSheet("""
            font-weight: bold; 
            font-size: 14px; 
            margin-top: 10px; 
            color: black; 
            background-color: #f0f0f0; 
            border: 1px solid #ccc; 
            padding: 5px;
        """)
        layout.addWidget(label)
        return label

    def create_slider(self, name, val, vmin, vmax, layout, update_func, circ_func):
        row = QtWidgets.QHBoxLayout()
        label = QtWidgets.QLabel(name)
        label.setFixedWidth(100)
        row.addWidget(label)

        slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        slider.setRange(0, 722)
        slider.setValue(int((val - vmin) / (vmax - vmin) * 722))
        slider.min_val = vmin
        slider.max_val = vmax

        value_label = QtWidgets.QLabel(f"{val:.2f}")
        value_label.setFixedWidth(60)
        value_label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)

        row.addWidget(slider)
        row.addWidget(value_label)
        layout.addLayout(row)

        slider.valueChanged.connect(update_func)
        slider.valueChanged.connect(lambda: self.update_label(slider, value_label, name))
        slider.valueChanged.connect(circ_func)
        slider.valueChanged.connect(self.renderCoupling)

        return slider, value_label

    def update_label(self, slider, label, name):
        val = slider.min_val + (slider.value() / 722) * (slider.max_val - slider.min_val)
        if "Phase" in name or "Angle" in name:
            label.setText(f"{val:.0f}°")
        else:
            label.setText(f"{val:.2f}")

    def slider_value(self, slider, name):
        val = slider.min_val + (slider.value() / 722) * (slider.max_val - slider.min_val)
        if "Phase" in name or "Angle" in name:
            return np.round(val) * np.pi / 180
        return val

    # ==========================================================
    # QWP INPUT POLARIZATION COMPUTATION
    # ==========================================================
    def update_input_from_qwp(self):
        # angle in radians
        theta = self.slider_value(self.qwp_slider, "QWP Angle")

        # S-polarized input field
        Ein = np.array([0, 1], dtype=complex)

        # Rotation matrices
        R = np.array([[np.cos(theta), -np.sin(theta)],
                      [np.sin(theta),  np.cos(theta)]], dtype=complex)
        Rm = np.array([[np.cos(theta), np.sin(theta)],
                       [-np.sin(theta), np.cos(theta)]], dtype=complex)

        # QWP matrix
        Jqwp = Rm @ np.array([[1, 0],
                              [0, 1j]], dtype=complex) @ R

        # Output field
        Eout = Jqwp @ Ein
        Ep, Es = Eout

        # extract p, s, phase
        p = np.abs(Ep)
        s = np.abs(Es)
        phase = np.angle(Es) - np.angle(Ep)

        # store for coupling
        self.input_p_val = p
        self.input_s_val = s
        self.input_phase_val = phase

        # update visualization using generic renderer
        self.update_wave_generic(p, s, phase,
                                 self.input_p_curve, self.input_s_curve, self.input_result_curve,
                                 self.input_p_vectors, self.input_s_vectors, self.input_result_vectors)

    # ==========================================================
    # CIRCULARITY
    # ==========================================================
    def renderInputCircularity(self):
        p = getattr(self, 'input_p_val', 0)
        s = getattr(self, 'input_s_val', 0)
        ph = getattr(self, 'input_phase_val', 0)
        S0 = p ** 2 + s ** 2
        S3 = 2 * p * s * np.sin(ph)
        val = 0 if S0 == 0 else np.abs(S3) / S0
        self.input_circularity.setText(f"Input Circularity: {val:.4f}")

    def renderEigenCircularity(self):
        p = self.slider_value(self.eigen_pAmp_slider, "Eigen P Amp")
        s = self.slider_value(self.eigen_sAmp_slider, "Eigen S Amp")
        ph = self.slider_value(self.eigen_phase_slider, "Eigen Phase")
        S0 = p ** 2 + s ** 2
        S3 = 2 * p * s * np.sin(ph)
        val = 0 if S0 == 0 else np.abs(S3) / S0
        self.eigen_circularity.setText(f"Eigen Circularity: {val:.4f}")

    # ==========================================================
    # WAVE UPDATE
    # ==========================================================
    def update_eigen_from_sliders(self):
        p = self.slider_value(self.eigen_pAmp_slider, "Eigen P Amp")
        s = self.slider_value(self.eigen_sAmp_slider, "Eigen S Amp")
        ph = self.slider_value(self.eigen_phase_slider, "Eigen Phase")

        # update the eigenmode visualization
        self.update_wave_generic(
            p, s, ph,
            self.eigen_p_curve, self.eigen_s_curve, self.eigen_result_curve,
            self.eigen_p_vectors, self.eigen_s_vectors, self.eigen_result_vectors
        )

    def update_wave_generic(self, p, s, ph,
                            p_curve, s_curve, r_curve,
                            p_vec, s_vec, r_vec):

        x = np.linspace(-5, 5, 1500)
        k = 2.0

        yp = p * np.cos(k * x)
        zp = np.zeros_like(x)

        zs = s * np.cos(k * x + ph)
        ys = np.zeros_like(x)

        yr = yp
        zr = zs

        p_curve.setData(pos=np.vstack([x, yp, zp]).T)
        s_curve.setData(pos=np.vstack([x, ys, zs]).T)
        r_curve.setData(pos=np.vstack([x, yr, zr]).T)

        idx = np.arange(0, len(x), 10)

        def create_vectors(X, Y, Z):
            pts = []
            for i in idx:
                pts.append([X[i], 0, 0])
                pts.append([X[i], Y[i], Z[i]])
                pts.append([np.nan, np.nan, np.nan])
            return np.array(pts)

        p_vec.setData(pos=create_vectors(x, yp, zp))
        s_vec.setData(pos=create_vectors(x, ys, zs))
        r_vec.setData(pos=create_vectors(x, yr, zr))

    # ==========================================================
    # COUPLING
    # ==========================================================
    def renderCoupling(self):
        input_p = getattr(self, 'input_p_val', 0)
        input_s = getattr(self, 'input_s_val', 0)
        input_ph = getattr(self, 'input_phase_val', 0)

        eigen_p = self.slider_value(self.eigen_pAmp_slider, "Eigen P Amp")
        eigen_s = self.slider_value(self.eigen_sAmp_slider, "Eigen S Amp")
        eigen_ph = self.slider_value(self.eigen_phase_slider, "Eigen Phase")

        proj_A, proj_B = self.calculateCoupling(
            input_p, input_s, input_ph,
            eigen_p, eigen_s, eigen_ph
        )

        self.coupling_bar_item.setOpts(height=[proj_A, proj_B])

    def calculateCoupling(self, input_p, input_s, input_ph, eigen_p, eigen_s, eigen_ph):
        norm_in = np.sqrt(input_p ** 2 + input_s ** 2)
        norm_eig = np.sqrt(eigen_p ** 2 + eigen_s ** 2)

        if norm_in == 0 or norm_eig == 0:
            return 0.0, 0.0

        input_vector = np.array([input_p,
                                 input_s * np.exp(1j * input_ph)]) / norm_in

        eigen_vector = np.array([eigen_p,
                                 eigen_s * np.exp(1j * eigen_ph)]) / norm_eig

        proj_A = np.abs(np.vdot(eigen_vector, input_vector)) ** 2
        proj_B = 1 - proj_A

        return proj_A, proj_B


# ==========================================================
# MAIN
# ==========================================================
def main():
    app = QtWidgets.QApplication([])
    win = PolarizationWaveWithSliderLabels()
    win.resize(1400, 800)
    win.show()
    app.exec_()


if __name__ == "__main__":
    main()
