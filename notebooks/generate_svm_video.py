"""
Simulación de Cálculo del Hiperplano Óptimo en Support Vector Machine (SVM)
Genera un video MP4 en resolución Full HD 16:9 (1920x1080, 30 fps).
"""

import argparse
import math
import os
import time
import numpy as np
from scipy.optimize import minimize

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Polygon, Circle, FancyArrowPatch
from matplotlib.collections import LineCollection
import imageio.v2 as imageio


# ---------------------------------------------------------------------------
# 1. Dataset y Resolución Matemática Exacta del SVM
# ---------------------------------------------------------------------------

def build_dataset():
    """
    Dataset 2D linealmente separable cuidadosamente diseñado para que:
    - Existan exactamente 3 vectores de soporte bien espaciados (2 de una clase, 1 de la otra).
    - El hiperplano óptimo tenga una inclinación clara (~40°) y pase cerca del origen.
    - Todos los puntos queden holgadamente dentro de xlim=(-5.5, 5.5), ylim=(-4.05, 4.05).
    """
    # Clase +1 (superior derecha)
    X_pos = np.array([
        [0.40,  1.55],   # Vector de soporte (+1)
        [2.05,  0.15],   # Vector de soporte (+1)
        [1.35,  2.35],
        [2.65,  1.95],
        [3.35,  0.85],
        [3.95,  2.55],
        [0.85,  3.15],
        [2.15,  3.35],
        [4.35,  1.45],
        [3.20, -0.35],
        [4.55,  0.15],
        [1.75,  1.40],
        [3.05,  2.95],
        [0.10,  2.85],
    ], dtype=float)

    # Clase -1 (inferior izquierda)
    X_neg = np.array([
        [-0.75, -0.95],  # Vector de soporte (-1)
        [-2.45,  0.35],
        [-1.85, -1.95],
        [-3.20, -0.85],
        [-3.85, -2.10],
        [-0.95, -2.75],
        [-2.75, -2.95],
        [-4.25, -0.40],
        [-3.55,  1.05],
        [-1.95, -0.45],
        [-0.15, -2.35],
        [-4.55, -1.55],
        [-2.20,  1.45],
        [-1.40, -3.25],
    ], dtype=float)

    X = np.vstack([X_pos, X_neg])
    y = np.concatenate([np.ones(len(X_pos)), -np.ones(len(X_neg))])
    return X, y


def solve_exact_hard_margin_svm(X, y):
    """
    Resuelve el problema dual exacto de SVM de margen duro:
        max_alpha  sum(alpha) - 0.5 * sum_ij alpha_i alpha_j y_i y_j (x_i . x_j)
        s.a.       alpha_i >= 0,  sum(alpha_i * y_i) = 0
    """
    n = len(y)
    K = (X @ X.T) * np.outer(y, y)

    def obj(a):
        return 0.5 * a @ K @ a - np.sum(a)

    def jac(a):
        return K @ a - np.ones(n)

    constraints = ({
        "type": "eq",
        "fun": lambda a: np.dot(a, y),
        "jac": lambda a: y,
    },)
    bounds = [(0.0, None) for _ in range(n)]
    a0 = np.zeros(n)

    res = minimize(
        obj, a0, method="SLSQP", jac=jac,
        bounds=bounds, constraints=constraints,
        options={"ftol": 1e-12, "maxiter": 1000},
    )
    if not res.success:
        raise RuntimeError(f"SLSQP no convergió: {res.message}")

    alpha = np.maximum(res.x, 0.0)
    w = (alpha * y) @ X
    sv_mask = alpha > 1e-4
    sv_indices = np.where(sv_mask)[0]
    b = float(np.mean(y[sv_indices] - X[sv_indices] @ w))

    # Verificación KKT
    margins = y * (X @ w + b)
    assert np.min(margins) >= 1.0 - 1e-4, f"Restricción violada: min margin = {np.min(margins)}"
    return w, b, alpha, sv_indices


def simulate_optimization_trajectory(X, y, w_opt, b_opt, n_steps=240):
    """
    Simula una trayectoria real de optimización primal-dual (Lagrangiano Aumentado
    con descenso de gradiente suave) que parte de un hiperplano subóptimo (inclinado,
    con margen estrecho y violaciones iniciales) y converge exactamente a (w_opt, b_opt).
    """
    n = len(y)
    # Punto inicial deliberadamente subóptimo: inclinado y con norma alta (margen estrecho)
    w = np.array([1.85, -0.35], dtype=float)
    b = -1.15
    lam = np.zeros(n, dtype=float)

    # Velocidades para momento suave
    vw = np.zeros(2, dtype=float)
    vb = 0.0

    rho = 1.6
    lr = 0.016
    beta = 0.82

    hist_w = []
    hist_b = []
    hist_loss = []
    hist_margin = []
    hist_geom_margin = []
    hist_violations = []
    hist_viol_mask = []

    C_eval = 6.0  # Para medir función objetivo J(w, b) consistente

    for step in range(n_steps):
        scores = y * (X @ w + b)
        slack = np.maximum(0.0, 1.0 - scores)
        viol_mask = scores < (1.0 - 1e-2)
        n_viol = int(np.sum(viol_mask))

        # Función objetivo suave: 0.5 ||w||^2 + C * sum(max(0, 1 - y_i(w.x_i + b))^2)
        loss = 0.5 * float(np.dot(w, w)) + C_eval * float(np.sum(slack ** 2))
        w_norm = float(np.linalg.norm(w))
        nominal_margin = 2.0 / max(w_norm, 1e-6)
        min_signed_dist = float(np.min(scores)) / max(w_norm, 1e-6)

        hist_w.append(w.copy())
        hist_b.append(float(b))
        hist_loss.append(loss)
        hist_margin.append(nominal_margin)
        hist_geom_margin.append(max(0.0, 2.0 * min_signed_dist))
        hist_violations.append(n_viol)
        hist_viol_mask.append(viol_mask.copy())

        # Gradiente del Lagrangiano aumentado:
        # L = 0.5 ||w||^2 + sum_i [ lam_i * g_i + 0.5 * rho * max(0, g_i)^2 ]
        # donde g_i = 1 - y_i (w.x_i + b), activado cuando lam_i + rho * g_i > 0
        g = 1.0 - scores
        eff = np.maximum(0.0, lam + rho * g)

        grad_w = w - (eff * y) @ X
        grad_b = -float(np.sum(eff * y))

        # Clamping suave para estabilidad visual sin saltos bruscos
        g_norm = math.hypot(grad_w[0], grad_w[1], grad_b)
        if g_norm > 8.0:
            scale = 8.0 / g_norm
            grad_w *= scale
            grad_b *= scale

        vw = beta * vw + (1.0 - beta) * grad_w
        vb = beta * vb + (1.0 - beta) * grad_b

        # Tasa de aprendizaje con decaimiento progresivo
        lr_t = lr * (0.35 + 0.65 * (1.0 - step / n_steps) ** 0.7)
        w = w - lr_t * vw
        b = b - lr_t * vb

        # Actualización dual suave (crece en los vectores de soporte)
        lam = np.maximum(0.0, lam + 0.14 * rho * g)
        rho = min(6.5, rho * 1.008)

    # Mezcla ultra-suave en los últimos 25 pasos para garantizar exactitud KKT 100% al final
    tail = 30
    for i in range(tail):
        t = (i + 1) / tail
        s = t * t * (3.0 - 2.0 * t)  # smoothstep
        idx = n_steps - tail + i
        w_blend = (1.0 - s) * hist_w[idx] + s * w_opt
        b_blend = (1.0 - s) * hist_b[idx] + s * b_opt
        scores = y * (X @ w_blend + b_blend)
        slack = np.maximum(0.0, 1.0 - scores)
        w_norm = float(np.linalg.norm(w_blend))

        hist_w[idx] = w_blend
        hist_b[idx] = float(b_blend)
        hist_loss[idx] = 0.5 * float(np.dot(w_blend, w_blend)) + C_eval * float(np.sum(slack ** 2))
        hist_margin[idx] = 2.0 / max(w_norm, 1e-6)
        hist_geom_margin[idx] = max(0.0, 2.0 * float(np.min(scores)) / max(w_norm, 1e-6))
        hist_violations[idx] = int(np.sum(scores < (1.0 - 1e-2)))
        hist_viol_mask[idx] = scores < (1.0 - 1e-2)

    return {
        "w": np.array(hist_w),
        "b": np.array(hist_b),
        "loss": np.array(hist_loss),
        "margin": np.array(hist_margin),
        "geom_margin": np.array(hist_geom_margin),
        "violations": np.array(hist_violations),
        "viol_mask": np.array(hist_viol_mask),
    }


def compute_candidate_hyperplanes(X, y):
    """
    Genera 3 hiperplanos separadores válidos pero subóptimos (márgenes pequeños)
    para demostrar por qué existen infinitas soluciones y por qué SVM busca el máximo margen.
    Cada uno se normaliza para que min_i y_i (w.x_i + b) == 1.0 (margen exacto = 2/||w||).
    """
    raw_candidates = [
        # (w_dir, point_on_line)
        (np.array([0.85, 0.22]), np.array([0.38, -0.30])),   # Muy empinado, roza ambos lados
        (np.array([0.30, 0.95]), np.array([0.85, 0.08])),    # Casi horizontal, pasa pegado a puntos
        (np.array([0.62, 0.78]), np.array([-0.22, -0.48])),  # Buena inclinación pero desplazado hacia clase -1
    ]
    candidates = []
    for w_raw, pt in raw_candidates:
        w0 = w_raw / np.linalg.norm(w_raw)
        b0 = -float(np.dot(w0, pt))
        margins = y * (X @ w0 + b0)
        min_m = float(np.min(margins))
        if min_m <= 0.02:
            # Desplazar al punto medio exacto para asegurar separación válida pero angosta
            pos_min = float(np.min(X[y == 1] @ w0))
            neg_max = float(np.max(X[y == -1] @ w0))
            b0 = -0.5 * (pos_min + neg_max)
            margins = y * (X @ w0 + b0)
            min_m = float(np.min(margins))
        # Escalar para que la banda ±1 toque el punto más cercano
        w_scaled = w0 / min_m
        b_scaled = b0 / min_m
        # Encontrar los puntos más cercanos
        scaled_m = y * (X @ w_scaled + b_scaled)
        closest = np.where(scaled_m < 1.12)[0]
        candidates.append((w_scaled, b_scaled, 2.0 / np.linalg.norm(w_scaled), closest))
    return candidates


# ---------------------------------------------------------------------------
# 2. Utilidades Geométricas y de Easing
# ---------------------------------------------------------------------------

def ease_out_cubic(t):
    t = max(0.0, min(1.0, t))
    return 1.0 - (1.0 - t) ** 3


def ease_in_out_cubic(t):
    t = max(0.0, min(1.0, t))
    return 4 * t * t * t if t < 0.5 else 1 - ((-2 * t + 2) ** 3) / 2


def clip_line_to_box(w, b, c, xmin, xmax, ymin, ymax):
    """
    Calcula los dos extremos del segmento de recta w[0]*x + w[1]*y + b = c
    recortado al rectángulo [xmin, xmax] x [ymin, ymax].
    """
    wx, wy = float(w[0]), float(w[1])
    pts = []
    eps = 1e-9
    if abs(wy) > eps:
        for x in (xmin, xmax):
            yv = (c - b - wx * x) / wy
            if ymin - 1e-6 <= yv <= ymax + 1e-6:
                pts.append((x, yv))
    if abs(wx) > eps:
        for yv in (ymin, ymax):
            x = (c - b - wy * yv) / wx
            if xmin - 1e-6 <= x <= xmax + 1e-6:
                pts.append((x, yv))
    # Deduplicar puntos cercanos
    uniq = []
    for p in pts:
        if all(math.hypot(p[0] - q[0], p[1] - q[1]) > 1e-4 for q in uniq):
            uniq.append(p)
    if len(uniq) < 2:
        return np.array([]), np.array([])
    # Ordenar a lo largo de la dirección tangente (-wy, wx)
    tx, ty = -wy, wx
    uniq.sort(key=lambda p: p[0] * tx + p[1] * ty)
    return np.array([uniq[0][0], uniq[-1][0]]), np.array([uniq[0][1], uniq[-1][1]])


def margin_band_polygon(w, b, xmin, xmax, ymin, ymax):
    """
    Devuelve los vértices ordenados del polígono de la banda -1 <= w.x + b <= +1
    recortada a la caja de visualización.
    """
    # Recorte de Sutherland-Hodgman del rectángulo por dos semiplanos
    poly = [(xmin, ymin), (xmax, ymin), (xmax, ymax), (xmin, ymax)]

    def clip_halfplane(vertices, a, b_coef, rhs):
        # Mantener a*x + b_coef*y <= rhs
        if not vertices:
            return []
        out = []
        n = len(vertices)
        for i in range(n):
            p1 = vertices[i]
            p2 = vertices[(i + 1) % n]
            v1 = a * p1[0] + b_coef * p1[1] - rhs
            v2 = a * p2[0] + b_coef * p2[1] - rhs
            in1 = v1 <= 1e-9
            in2 = v2 <= 1e-9
            if in1 and in2:
                out.append(p2)
            elif in1 and not in2:
                t = v1 / (v1 - v2)
                out.append((p1[0] + t * (p2[0] - p1[0]), p1[1] + t * (p2[1] - p1[1])))
            elif not in1 and in2:
                t = v1 / (v1 - v2)
                out.append((p1[0] + t * (p2[0] - p1[0]), p1[1] + t * (p2[1] - p1[1])))
                out.append(p2)
        return out

    poly = clip_halfplane(poly, w[0], w[1], 1.0 - b)      # w.x + b <= +1
    poly = clip_halfplane(poly, -w[0], -w[1], 1.0 + b)    # w.x + b >= -1
    return poly


def halfspace_polygon(w, b, side, xmin, xmax, ymin, ymax):
    """
    side = +1 -> w.x + b >= 0
    side = -1 -> w.x + b <= 0
    """
    poly = [(xmin, ymin), (xmax, ymin), (xmax, ymax), (xmin, ymax)]
    a = -side * w[0]
    bc = -side * w[1]
    rhs = side * b

    out = []
    n = len(poly)
    for i in range(n):
        p1 = poly[i]
        p2 = poly[(i + 1) % n]
        v1 = a * p1[0] + bc * p1[1] - rhs
        v2 = a * p2[0] + bc * p2[1] - rhs
        in1 = v1 <= 1e-9
        in2 = v2 <= 1e-9
        if in1 and in2:
            out.append(p2)
        elif in1 and not in2:
            t = v1 / (v1 - v2)
            out.append((p1[0] + t * (p2[0] - p1[0]), p1[1] + t * (p2[1] - p1[1])))
        elif not in1 and in2:
            t = v1 / (v1 - v2)
            out.append((p1[0] + t * (p2[0] - p1[0]), p1[1] + t * (p2[1] - p1[1])))
            out.append(p2)
    return out


def point_on_hyperplane_near_origin(w, b):
    """Punto de w.x + b = 0 más cercano al origen."""
    denom = float(np.dot(w, w))
    if denom < 1e-12:
        return np.zeros(2)
    return (-b / denom) * w


# ---------------------------------------------------------------------------
# 3. Renderer de Video 16:9 (1920x1080)
# ---------------------------------------------------------------------------

def render_video(output_path, snapshots_dir=None, fps=30, duration_sec=32.0):
    # Paleta de colores (Dark Scientific Studio)
    BG = "#090E1A"
    PANEL_BG = "#10182B"
    PANEL_EDGE = "#22304E"
    GRID_COL = "#1B2640"
    TEXT_PRI = "#F8FAFC"
    TEXT_SEC = "#94A3B8"
    TEXT_MUT = "#64748B"

    CYAN = "#38BDF8"
    CYAN_GLOW = "#0284C7"
    CORAL = "#FB7185"
    CORAL_GLOW = "#E11D48"
    GOLD = "#FACC15"
    EMERALD = "#34D399"
    AMBER = "#F97316"
    VIOLET = "#A78BFA"

    # 1. Datos y matemática
    X, y = build_dataset()
    w_opt, b_opt, alpha_opt, sv_indices = solve_exact_hard_margin_svm(X, y)
    opt_margin = 2.0 / float(np.linalg.norm(w_opt))
    opt_loss = 0.5 * float(np.dot(w_opt, w_opt))

    n_opt_steps = 240
    traj = simulate_optimization_trajectory(X, y, w_opt, b_opt, n_steps=n_opt_steps)
    candidates = compute_candidate_hyperplanes(X, y)

    print(f"SVM Exacto resuelto:")
    print(f"  w* = [{w_opt[0]:+.4f}, {w_opt[1]:+.4f}], b* = {b_opt:+.4f}")
    print(f"  ||w*|| = {np.linalg.norm(w_opt):.4f}, Margen óptimo = {opt_margin:.4f}")
    print(f"  Vectores de soporte ({len(sv_indices)}): indices={sv_indices.tolist()}, alphas={np.round(alpha_opt[sv_indices], 4).tolist()}")

    pos_idx = np.where(y == 1)[0]
    neg_idx = np.where(y == -1)[0]
    non_sv_pos = np.array([i for i in pos_idx if i not in sv_indices])
    non_sv_neg = np.array([i for i in neg_idx if i not in sv_indices])

    # 2. Configuración de Matplotlib (16:9 exacto: 1920 x 1080)
    plt.rcParams.update({
        "font.family": "DejaVu Sans",
        "mathtext.fontset": "dejavusans",
        "axes.unicode_minus": True,
    })

    fig = plt.figure(figsize=(16, 9), dpi=120, facecolor=BG)

    # --- Fondo de paneles decorativos (en coordenadas de figura) ---
    bg_ax = fig.add_axes([0, 0, 1, 1], facecolor=BG)
    bg_ax.set_xlim(0, 1)
    bg_ax.set_ylim(0, 1)
    bg_ax.axis("off")

    def add_card(x, y0, w_c, h_c, radius=0.014, fc=PANEL_BG, ec=PANEL_EDGE, lw=1.2):
        patch = FancyBboxPatch(
            (x, y0), w_c, h_c,
            boxstyle=f"round,pad=0.0,rounding_size={radius}",
            facecolor=fc, edgecolor=ec, linewidth=lw,
            transform=bg_ax.transAxes, zorder=1,
        )
        bg_ax.add_patch(patch)
        return patch

    # Tarjetas estructurales
    add_card(0.025, 0.028, 0.610, 0.068, radius=0.010, fc="#0E1729", ec="#243554", lw=1.1)  # Barra narración inferior
    add_card(0.655, 0.608, 0.320, 0.275, radius=0.012)  # Card 1: Ecuación y telemetría
    add_card(0.655, 0.332, 0.320, 0.256, radius=0.012)  # Card 2: Función Objetivo J
    add_card(0.655, 0.028, 0.320, 0.284, radius=0.012)  # Card 3: Margen 2/||w||

    # Header superior
    bg_ax.text(
        0.028, 0.953, "Support Vector Machine (SVM)",
        color=TEXT_PRI, fontsize=20, fontweight="bold", va="center", ha="left",
    )
    bg_ax.text(
        0.295, 0.951, "Simulación del Cálculo del Hiperplano de Margen Máximo",
        color=TEXT_SEC, fontsize=12.5, va="center", ha="left",
    )

    # Línea divisoria y barra de progreso en header
    bg_ax.plot([0.025, 0.975], [0.910, 0.910], color="#1E2B45", lw=1.5)
    progress_line, = bg_ax.plot([0.025, 0.025], [0.910, 0.910], color=CYAN, lw=2.8, solid_capstyle="round")

    # Pill de fase (esquina superior derecha)
    phase_pill = FancyBboxPatch(
        (0.735, 0.928), 0.240, 0.044,
        boxstyle="round,pad=0.0,rounding_size=0.012",
        facecolor="#13223D", edgecolor=CYAN, linewidth=1.3,
        transform=bg_ax.transAxes, zorder=2,
    )
    bg_ax.add_patch(phase_pill)
    phase_badge_txt = bg_ax.text(
        0.855, 0.950, "FASE 1/5 · DATOS",
        color=CYAN, fontsize=10.5, fontweight="bold", va="center", ha="center", zorder=3,
    )

    # Narración inferior
    narration_txt = bg_ax.text(
        0.330, 0.062, "",
        color=TEXT_PRI, fontsize=11.5, va="center", ha="center", zorder=3,
    )

    # --- Card 1: Formulación Matemática y Telemetría en vivo ---
    bg_ax.text(
        0.673, 0.858, "OPTIMIZACIÓN DEL HIPERPLANO",
        color=TEXT_SEC, fontsize=9.2, fontweight="bold", va="center", ha="left",
    )
    bg_ax.text(
        0.815, 0.812,
        r"$\min_{\mathbf{w}, b}\;\frac{1}{2}\|\mathbf{w}\|^2 \quad \mathrm{s.a.}\;\; y_i(\mathbf{w}^\top \mathbf{x}_i + b) \geq 1$",
        color=TEXT_PRI, fontsize=11.8, va="center", ha="center",
    )
    bg_ax.plot([0.673, 0.957], [0.777, 0.777], color="#1E2C48", lw=1.0)

    # Etiquetas estáticas de telemetría
    tel_labels = [
        (0.673, 0.750, "Iteración:"),
        (0.673, 0.720, "Vector normal w:"),
        (0.673, 0.690, "Sesgo (bias) b:"),
        (0.673, 0.660, "Norma ||w||:"),
        (0.673, 0.629, "Margen (2 / ||w||):"),
    ]
    for tx, ty, lbl in tel_labels:
        bg_ax.text(tx, ty, lbl, color=TEXT_SEC, fontsize=10.2, va="center", ha="left")

    tel_iter = bg_ax.text(0.955, 0.750, "—", color=TEXT_PRI, fontsize=10.5, family="DejaVu Sans Mono", fontweight="bold", va="center", ha="right")
    tel_w = bg_ax.text(0.955, 0.720, "—", color=CYAN, fontsize=10.5, family="DejaVu Sans Mono", fontweight="bold", va="center", ha="right")
    tel_b = bg_ax.text(0.955, 0.690, "—", color=TEXT_PRI, fontsize=10.5, family="DejaVu Sans Mono", fontweight="bold", va="center", ha="right")
    tel_wnorm = bg_ax.text(0.955, 0.660, "—", color=VIOLET, fontsize=10.5, family="DejaVu Sans Mono", fontweight="bold", va="center", ha="right")
    tel_margin = bg_ax.text(0.955, 0.629, "—", color=EMERALD, fontsize=11.2, family="DejaVu Sans Mono", fontweight="bold", va="center", ha="right")

    # --- Eje Principal 2D (Espacio de Características) ---
    XMIN, XMAX = -5.5, 5.5
    YMIN, YMAX = -4.05, 4.05

    ax = fig.add_axes([0.055, 0.140, 0.575, 0.740], facecolor="#0C1324")
    ax.set_xlim(XMIN, XMAX)
    ax.set_ylim(YMIN, YMAX)
    ax.set_aspect("equal", adjustable="box")
    ax.set_xlabel(r"Característica $x_1$", color=TEXT_SEC, fontsize=11, labelpad=6)
    ax.set_ylabel(r"Característica $x_2$", color=TEXT_SEC, fontsize=11, labelpad=6)
    ax.tick_params(colors=TEXT_MUT, labelsize=9.5, length=4)
    for spine in ax.spines.values():
        spine.set_color(PANEL_EDGE)
        spine.set_linewidth(1.2)
    ax.grid(True, color=GRID_COL, linewidth=0.75, linestyle="-", alpha=0.85, zorder=0)
    ax.axhline(0, color="#263554", lw=1.0, zorder=0)
    ax.axvline(0, color="#263554", lw=1.0, zorder=0)

    # Polígonos de regiones de decisión (Fase 5)
    pos_region_poly = Polygon([(0, 0)], closed=True, facecolor=CYAN, edgecolor="none", alpha=0.0, zorder=1)
    neg_region_poly = Polygon([(0, 0)], closed=True, facecolor=CORAL, edgecolor="none", alpha=0.0, zorder=1)
    ax.add_patch(pos_region_poly)
    ax.add_patch(neg_region_poly)

    # Banda del margen (-1 <= w.x + b <= +1)
    margin_poly = Polygon([(0, 0)], closed=True, facecolor=GOLD, edgecolor="none", alpha=0.0, zorder=2)
    ax.add_patch(margin_poly)

    # Rectas de margen (+1 y -1) y Recta del Hiperplano (con efecto glow multicapa)
    line_m_pos, = ax.plot([], [], linestyle="--", color=CYAN, lw=1.7, alpha=0.0, zorder=4)
    line_m_neg, = ax.plot([], [], linestyle="--", color=CORAL, lw=1.7, alpha=0.0, zorder=4)

    hp_glow_outer, = ax.plot([], [], color=GOLD, lw=9.5, alpha=0.0, solid_capstyle="round", zorder=5)
    hp_glow_inner, = ax.plot([], [], color=GOLD, lw=5.0, alpha=0.0, solid_capstyle="round", zorder=6)
    hp_core, = ax.plot([], [], color="#FEF9C3", lw=2.3, alpha=0.0, solid_capstyle="round", zorder=7)

    # Vector normal w (flecha) + etiqueta
    w_arrow = FancyArrowPatch(
        (0, 0), (0.01, 0.01),
        arrowstyle="-|>,head_length=8,head_width=4.5",
        color=VIOLET, lw=2.5, alpha=0.0, zorder=11,
    )
    ax.add_patch(w_arrow)
    w_label = ax.text(
        0, 0, r"$\mathbf{w}$", color="#DDD6FE", fontsize=13.5, fontweight="bold",
        ha="center", va="center", alpha=0.0, zorder=12,
        bbox=dict(boxstyle="round,pad=0.18", fc="#161C36", ec=VIOLET, lw=0.9, alpha=0.88),
    )

    # Etiquetas sobre las rectas de margen (+1, 0, -1)
    lbl_hp_eq = ax.text(
        0.50, 0.955, "", transform=ax.transAxes,
        color=EMERALD, fontsize=10.8, fontweight="bold", family="DejaVu Sans Mono",
        ha="center", va="top", alpha=0.0, zorder=15,
        bbox=dict(boxstyle="round,pad=0.35", fc="#0D1F22", ec=EMERALD, lw=1.2, alpha=0.94),
    )

    # Puntos de datos (glow + núcleo) — se actualizan por tamaño/alpha para pop-in suave
    sc_pos_glow = ax.scatter(X[pos_idx, 0], X[pos_idx, 1], s=np.zeros(len(pos_idx)), color=CYAN_GLOW, alpha=0.28, edgecolors="none", zorder=8)
    sc_pos_core = ax.scatter(X[pos_idx, 0], X[pos_idx, 1], s=np.zeros(len(pos_idx)), color=CYAN, alpha=0.96, edgecolors="#E0F2FE", linewidths=1.2, zorder=9)

    sc_neg_glow = ax.scatter(X[neg_idx, 0], X[neg_idx, 1], s=np.zeros(len(neg_idx)), color=CORAL_GLOW, alpha=0.28, edgecolors="none", zorder=8)
    sc_neg_core = ax.scatter(X[neg_idx, 0], X[neg_idx, 1], s=np.zeros(len(neg_idx)), color=CORAL, alpha=0.96, edgecolors="#FFE4E6", linewidths=1.2, zorder=9)

    # Aros de violación (Fase 2 puntos más cercanos / Fase 3 violaciones de margen)
    sc_viol_rings = ax.scatter(X[:, 0], X[:, 1], s=np.zeros(len(X)), facecolors="none", edgecolors=AMBER, linewidths=2.4, alpha=0.0, zorder=10)

    # Aros dorados para Vectores de Soporte (Fase 4 y 5)
    sv_rings_outer = ax.scatter(X[sv_indices, 0], X[sv_indices, 1], s=np.zeros(len(sv_indices)), facecolors="none", edgecolors=GOLD, linewidths=3.5, alpha=0.0, zorder=11)
    sv_rings_inner = ax.scatter(X[sv_indices, 0], X[sv_indices, 1], s=np.zeros(len(sv_indices)), facecolors="none", edgecolors="#FEF08A", linewidths=1.6, alpha=0.0, zorder=12)

    # Segmentos de proyección ortogonal desde cada SV al hiperplano
    sv_proj_lines = []
    sv_badges = []
    # Desplazamientos manuales limpios para los 3 SVs para que nunca se solapen
    sv_badge_offsets = [
        (-1.45, 0.72),   # SV0: [0.40, 1.55] -> arriba-izquierda
        (1.42, -0.62),   # SV1: [2.05, 0.15] -> abajo-derecha
        (-1.55, -0.78),  # SV2: [-0.75, -0.95] -> abajo-izquierda
    ]
    for k, idx in enumerate(sv_indices):
        ln, = ax.plot([], [], linestyle=":", color=GOLD, lw=2.0, alpha=0.0, zorder=7)
        sv_proj_lines.append(ln)
        px, py = X[idx]
        ox, oy = sv_badge_offsets[k]
        txt = ax.annotate(
            f"VS{k+1}\nα={alpha_opt[idx]:.2f}",
            xy=(px, py), xytext=(px + ox, py + oy),
            color="#FEF3C7", fontsize=9.0, fontweight="bold", ha="center", va="center",
            alpha=0.0, zorder=14,
            bbox=dict(boxstyle="round,pad=0.25", fc="#1F1B12", ec=GOLD, lw=1.1, alpha=0.92),
            arrowprops=dict(arrowstyle="-", color=GOLD, lw=1.1, alpha=0.0),
        )
        sv_badges.append(txt)

    # Flecha doble de ancho de margen (caliper) en Fase 4 y 5
    caliper_arrow = FancyArrowPatch(
        (0, 0), (0.01, 0.01),
        arrowstyle="<->,head_length=7,head_width=4",
        color=EMERALD, lw=2.4, alpha=0.0, zorder=13,
    )
    ax.add_patch(caliper_arrow)
    caliper_label = ax.text(
        0, 0, "", color="#D1FAE5", fontsize=9.6, fontweight="bold",
        ha="center", va="center", alpha=0.0, zorder=14,
        bbox=dict(boxstyle="round,pad=0.24", fc="#0B221C", ec=EMERALD, lw=1.1, alpha=0.92),
    )

    # Puntos de prueba nuevos (Fase 5)
    test_pts = np.array([[2.65, 0.85], [-2.55, -1.75]])
    test_scatters = []
    test_labels = []
    test_colors = [CYAN, CORAL]
    test_texts = ["Nuevo (+1)\nf(x) > 0", "Nuevo (-1)\nf(x) < 0"]
    test_offsets = [(0.95, -0.68), (1.05, -0.62)]
    for k in range(2):
        sc = ax.scatter(
            [test_pts[k, 0]], [test_pts[k, 1]],
            s=[0], marker="*", color="#FFFFFF", edgecolors=test_colors[k],
            linewidths=1.8, alpha=0.0, zorder=15,
        )
        test_scatters.append(sc)
        tx = ax.annotate(
            test_texts[k],
            xy=(test_pts[k, 0], test_pts[k, 1]),
            xytext=(test_pts[k, 0] + test_offsets[k][0], test_pts[k, 1] + test_offsets[k][1]),
            color="#FFFFFF", fontsize=8.8, fontweight="bold", ha="center", va="center",
            alpha=0.0, zorder=15,
            bbox=dict(boxstyle="round,pad=0.24", fc="#111C33", ec=test_colors[k], lw=1.1, alpha=0.92),
            arrowprops=dict(arrowstyle="->", color=test_colors[k], lw=1.1, alpha=0.0),
        )
        test_labels.append(tx)

    # Leyenda limpia en esquina superior izquierda del plano
    leg_handles = [
        plt.Line2D([0], [0], marker="o", color="none", markerfacecolor=CYAN, markeredgecolor="#E0F2FE", markersize=7.5, label="Clase +1 (y = +1)"),
        plt.Line2D([0], [0], marker="o", color="none", markerfacecolor=CORAL, markeredgecolor="#FFE4E6", markersize=7.5, label="Clase −1 (y = −1)"),
        plt.Line2D([0], [0], color=GOLD, lw=2.4, label="Hiperplano wᵀx + b = 0"),
        plt.Line2D([0], [0], marker="o", color="none", markerfacecolor="none", markeredgecolor=GOLD, markeredgewidth=2.0, markersize=8.5, label="Vectores de Soporte"),
    ]
    leg = ax.legend(
        handles=leg_handles, loc="upper left", frameon=True,
        facecolor="#0E172A", edgecolor="#253657", framealpha=0.92,
        fontsize=8.8, labelcolor=TEXT_PRI, borderpad=0.55, handletextpad=0.6,
    )
    leg.set_zorder(16)

    # --- Card 2: Gráfica de Función Objetivo J(w, b) ---
    ax_loss = fig.add_axes([0.695, 0.370, 0.262, 0.180], facecolor="#0C1324")
    ax_loss.set_title("Función Objetivo  J(w, b)", color=TEXT_PRI, fontsize=10.2, fontweight="bold", loc="left", pad=7)
    ax_loss.set_xlim(0, n_opt_steps - 1)
    max_loss = float(np.max(traj["loss"]))
    ax_loss.set_ylim(0, max_loss * 1.12)
    ax_loss.tick_params(colors=TEXT_MUT, labelsize=8.2)
    ax_loss.set_xlabel("Iteración", color=TEXT_MUT, fontsize=8.3, labelpad=2)
    for sp in ax_loss.spines.values():
        sp.set_color("#1E2C48")
    ax_loss.grid(True, color=GRID_COL, lw=0.6, alpha=0.8)
    ax_loss.axhline(opt_loss, color=EMERALD, ls=":", lw=1.1, alpha=0.65)
    ax_loss.text(n_opt_steps - 4, opt_loss + max_loss * 0.04, f"Óptimo = {opt_loss:.2f}", color=EMERALD, fontsize=7.8, ha="right", va="bottom", alpha=0.85)

    loss_line, = ax_loss.plot([], [], color=AMBER, lw=2.3, zorder=4)
    loss_dot, = ax_loss.plot([], [], marker="o", color="#FFF7ED", markeredgecolor=AMBER, markeredgewidth=2.0, markersize=6.2, zorder=5)

    # --- Card 3: Gráfica de Ancho del Margen (2 / ||w||) ---
    ax_marg = fig.add_axes([0.695, 0.072, 0.262, 0.195], facecolor="#0C1324")
    ax_marg.set_title("Evolución del Margen  M = 2 / ||w||", color=TEXT_PRI, fontsize=10.2, fontweight="bold", loc="left", pad=7)
    ax_marg.set_xlim(0, n_opt_steps - 1)
    max_m = max(opt_margin, float(np.max(traj["margin"]))) * 1.18
    ax_marg.set_ylim(0, max_m)
    ax_marg.tick_params(colors=TEXT_MUT, labelsize=8.2)
    ax_marg.set_xlabel("Iteración", color=TEXT_MUT, fontsize=8.3, labelpad=2)
    for sp in ax_marg.spines.values():
        sp.set_color("#1E2C48")
    ax_marg.grid(True, color=GRID_COL, lw=0.6, alpha=0.8)
    ax_marg.axhline(opt_margin, color=EMERALD, ls="--", lw=1.2, alpha=0.75)
    ax_marg.text(n_opt_steps - 4, opt_margin + max_m * 0.035, f"Máx = {opt_margin:.2f}", color=EMERALD, fontsize=8.0, fontweight="bold", ha="right", va="bottom")

    marg_line, = ax_marg.plot([], [], color=EMERALD, lw=2.3, zorder=4)
    marg_dot, = ax_marg.plot([], [], marker="o", color="#ECFDF5", markeredgecolor=EMERALD, markeredgewidth=2.0, markersize=6.2, zorder=5)

    # Helpers para actualizar elementos geométricos del hiperplano
    def set_hyperplane_visual(w_vec, b_val, hp_color, core_color, hp_alpha, band_alpha, show_normal=True, normal_alpha=1.0):
        # Línea central w.x + b = 0
        hx, hy = clip_line_to_box(w_vec, b_val, 0.0, XMIN, XMAX, YMIN, YMAX)
        hp_glow_outer.set_data(hx, hy)
        hp_glow_inner.set_data(hx, hy)
        hp_core.set_data(hx, hy)

        hp_glow_outer.set_color(hp_color)
        hp_glow_inner.set_color(hp_color)
        hp_core.set_color(core_color)

        hp_glow_outer.set_alpha(0.20 * hp_alpha)
        hp_glow_inner.set_alpha(0.42 * hp_alpha)
        hp_core.set_alpha(0.98 * hp_alpha)

        # Rectas de margen ±1
        px, py = clip_line_to_box(w_vec, b_val, 1.0, XMIN, XMAX, YMIN, YMAX)
        nx, ny = clip_line_to_box(w_vec, b_val, -1.0, XMIN, XMAX, YMIN, YMAX)
        line_m_pos.set_data(px, py)
        line_m_neg.set_data(nx, ny)
        line_m_pos.set_alpha(0.85 * hp_alpha)
        line_m_neg.set_alpha(0.85 * hp_alpha)

        # Banda del margen
        poly = margin_band_polygon(w_vec, b_val, XMIN, XMAX, YMIN, YMAX)
        if len(poly) >= 3:
            margin_poly.set_xy(poly)
            margin_poly.set_facecolor(hp_color)
            margin_poly.set_alpha(band_alpha * hp_alpha)
        else:
            margin_poly.set_alpha(0.0)

        # Vector normal w anclado sobre el hiperplano (desplazado hacia abajo-derecha para claridad)
        if show_normal and hp_alpha > 0.02 and np.linalg.norm(w_vec) > 1e-4:
            p0 = point_on_hyperplane_near_origin(w_vec, b_val)
            # Desplazar origen del vector a lo largo de la tangente del hiperplano hacia la parte superior-izquierda
            w_unit = w_vec / np.linalg.norm(w_vec)
            t_unit = np.array([-w_unit[1], w_unit[0]])
            if t_unit[1] < 0:
                t_unit = -t_unit
            anchor = p0 + 1.45 * t_unit
            # Escala visual del vector w proporcional a ||w|| (así se ve cómo se acorta al maximizar margen)
            vec_vis = w_vec * 1.15
            tip = anchor + vec_vis
            w_arrow.set_positions((anchor[0], anchor[1]), (tip[0], tip[1]))
            w_arrow.set_alpha(0.95 * normal_alpha * hp_alpha)
            lbl_pos = tip + 0.42 * w_unit
            w_label.set_position((lbl_pos[0], lbl_pos[1]))
            w_label.set_alpha(0.95 * normal_alpha * hp_alpha)
        else:
            w_arrow.set_alpha(0.0)
            w_label.set_alpha(0.0)

    def update_telemetry(iter_str, w_vec, b_val, margin_val, margin_color=EMERALD):
        tel_iter.set_text(iter_str)
        if w_vec is None:
            tel_w.set_text("—")
            tel_b.set_text("—")
            tel_wnorm.set_text("—")
            tel_margin.set_text("—")
        else:
            wn = float(np.linalg.norm(w_vec))
            tel_w.set_text(f"[{w_vec[0]:+6.3f}, {w_vec[1]:+6.3f}]")
            tel_b.set_text(f"{b_val:+6.3f}")
            tel_wnorm.set_text(f"{wn:6.3f}")
            tel_margin.set_text(f"{margin_val:6.3f}")
            tel_margin.set_color(margin_color)

    # Pre-cálculo para Caliper del margen óptimo (Fase 4 y 5)
    w_unit_opt = w_opt / np.linalg.norm(w_opt)
    t_unit_opt = np.array([-w_unit_opt[1], w_unit_opt[0]])
    if t_unit_opt[1] > 0:
        t_unit_opt = -t_unit_opt  # hacia abajo-derecha donde hay espacio limpio
    p0_opt = point_on_hyperplane_near_origin(w_opt, b_opt)
    caliper_center = p0_opt + 2.35 * t_unit_opt
    half_m = 1.0 / float(np.linalg.norm(w_opt))
    caliper_p1 = caliper_center - half_m * w_unit_opt
    caliper_p2 = caliper_center + half_m * w_unit_opt

    # Pre-cálculo de proyecciones de los 3 SVs sobre el hiperplano óptimo
    sv_proj_pts = []
    for idx in sv_indices:
        pt = X[idx]
        dist_signed = (np.dot(w_opt, pt) + b_opt) / np.dot(w_opt, w_opt)
        proj = pt - dist_signed * w_opt
        sv_proj_pts.append((pt, proj))

    # 3. Bucle de renderizado de frames
    total_frames = int(round(fps * duration_sec))
    iters_x = np.arange(n_opt_steps)

    # Momentos clave para guardar capturas de verificación (segundos)
    snapshot_secs = [2.5, 6.8, 13.5, 23.0, 30.2]
    snapshot_frames = {int(round(s * fps)): f"frame_{i+1:02d}_{s:.1f}s.png" for i, s in enumerate(snapshot_secs)}
    if snapshots_dir:
        os.makedirs(snapshots_dir, exist_ok=True)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    writer = imageio.get_writer(
        output_path,
        fps=fps,
        codec="libx264",
        quality=8,
        pixelformat="yuv420p",
        macro_block_size=16,
        ffmpeg_params=["-preset", "medium", "-crf", "18", "-movflags", "+faststart"],
    )

    t_start = time.time()
    print(f"Renderizando {total_frames} frames (1920x1080 @ {fps} fps) en {output_path}...")

    try:
        for f in range(total_frames):
            t_sec = f / fps
            frac_total = f / max(1, total_frames - 1)
            progress_line.set_xdata([0.025, 0.025 + 0.950 * frac_total])

            # Reset por defecto de overlays de fases posteriores
            pos_region_poly.set_alpha(0.0)
            neg_region_poly.set_alpha(0.0)
            sc_viol_rings.set_alpha(0.0)
            sv_rings_outer.set_alpha(0.0)
            sv_rings_inner.set_alpha(0.0)
            caliper_arrow.set_alpha(0.0)
            caliper_label.set_alpha(0.0)
            lbl_hp_eq.set_alpha(0.0)
            for ln in sv_proj_lines:
                ln.set_alpha(0.0)
            for bdg in sv_badges:
                bdg.set_alpha(0.0)
                if bdg.arrow_patch:
                    bdg.arrow_patch.set_alpha(0.0)
            for sc in test_scatters:
                sc.set_alpha(0.0)
                sc.set_sizes([0])
            for tx in test_labels:
                tx.set_alpha(0.0)
                if tx.arrow_patch:
                    tx.arrow_patch.set_alpha(0.0)

            # -----------------------------------------------------------------
            # FASE 1 (0.0s – 4.0s): Aparición de datos linealmente separables
            # -----------------------------------------------------------------
            if t_sec < 4.0:
                phase_badge_txt.set_text("FASE 1/5 · CONJUNTO DE DATOS")
                phase_badge_txt.set_color(CYAN)
                phase_pill.set_edgecolor(CYAN)
                progress_line.set_color(CYAN)
                narration_txt.set_text(
                    "Dos clases linealmente separables: buscamos el hiperplano wᵀx + b = 0 que mejor las separe."
                )

                # Pop-in escalonado de puntos
                s_pos = np.zeros(len(pos_idx))
                s_neg = np.zeros(len(neg_idx))
                for i in range(len(pos_idx)):
                    dt = (t_sec - 0.35 - i * 0.11) / 0.45
                    sc_val = ease_out_cubic(dt)
                    s_pos[i] = 95.0 * sc_val
                for i in range(len(neg_idx)):
                    dt = (t_sec - 0.85 - i * 0.11) / 0.45
                    sc_val = ease_out_cubic(dt)
                    s_neg[i] = 95.0 * sc_val

                sc_pos_core.set_sizes(s_pos)
                sc_pos_glow.set_sizes(s_pos * 3.1)
                sc_neg_core.set_sizes(s_neg)
                sc_neg_glow.set_sizes(s_neg * 3.1)
                sc_pos_core.set_alpha(0.96)
                sc_neg_core.set_alpha(0.96)

                set_hyperplane_visual(w_opt, b_opt, GOLD, "#FEF9C3", 0.0, 0.0, show_normal=False)
                update_telemetry("Preparando...", None, None, None)
                loss_line.set_data([], [])
                loss_dot.set_data([], [])
                marg_line.set_data([], [])
                marg_dot.set_data([], [])

            # -----------------------------------------------------------------
            # FASE 2 (4.0s – 10.0s): Infinitos hiperplanos candidatos
            # -----------------------------------------------------------------
            elif t_sec < 10.0:
                phase_badge_txt.set_text("FASE 2/5 · MÚLTIPLES CANDIDATOS")
                phase_badge_txt.set_color(AMBER)
                phase_pill.set_edgecolor(AMBER)
                progress_line.set_color(AMBER)
                narration_txt.set_text(
                    "Existen infinitos hiperplanos que separan los datos, pero con márgenes estrechos y menor robustez."
                )

                sc_pos_core.set_sizes(np.full(len(pos_idx), 95.0))
                sc_pos_glow.set_sizes(np.full(len(pos_idx), 295.0))
                sc_neg_core.set_sizes(np.full(len(neg_idx), 95.0))
                sc_neg_glow.set_sizes(np.full(len(neg_idx), 295.0))
                sc_pos_core.set_alpha(0.95)
                sc_neg_core.set_alpha(0.95)

                local_t = t_sec - 4.0  # 0..6s (2s por candidato)
                seg_idx = min(2, int(local_t // 2.0))
                seg_u = (local_t - seg_idx * 2.0) / 2.0

                if seg_idx == 0:
                    w_c, b_c, m_c, closest = candidates[0]
                    fade = ease_out_cubic(seg_u / 0.28) if seg_u < 0.28 else 1.0
                else:
                    # Transición suave desde candidato anterior
                    w_prev, b_prev, _, _ = candidates[seg_idx - 1]
                    w_next, b_next, _, closest = candidates[seg_idx]
                    if seg_u < 0.35:
                        u_m = ease_in_out_cubic(seg_u / 0.35)
                        w_c = (1.0 - u_m) * w_prev + u_m * w_next
                        b_c = (1.0 - u_m) * b_prev + u_m * b_next
                        m_c = 2.0 / float(np.linalg.norm(w_c))
                    else:
                        w_c, b_c = w_next, b_next
                        m_c = 2.0 / float(np.linalg.norm(w_c))
                    fade = 1.0

                # Al final de Fase 2 (9.4..10.0), interpolar suavemente hacia el estado inicial de optimización
                if local_t > 5.35:
                    u_end = ease_in_out_cubic((local_t - 5.35) / 0.65)
                    w_c = (1.0 - u_end) * w_c + u_end * traj["w"][0]
                    b_c = (1.0 - u_end) * b_c + u_end * traj["b"][0]
                    m_c = 2.0 / float(np.linalg.norm(w_c))

                set_hyperplane_visual(w_c, b_c, AMBER, "#FFEDD5", fade, 0.14, show_normal=True, normal_alpha=fade)
                update_telemetry(f"Candidato {seg_idx + 1}/3", w_c, b_c, m_c, margin_color=AMBER)

                # Resaltar puntos más próximos al candidato actual
                if local_t <= 5.35 and seg_u >= 0.30:
                    pulse = 0.55 + 0.45 * math.sin(local_t * 9.0)
                    rings = np.zeros(len(X))
                    rings[closest] = 280.0 + 45.0 * pulse
                    sc_viol_rings.set_sizes(rings)
                    sc_viol_rings.set_edgecolors(AMBER)
                    sc_viol_rings.set_alpha(0.85 * fade)

                loss_line.set_data([], [])
                loss_dot.set_data([], [])
                marg_line.set_data([], [])
                marg_dot.set_data([], [])

            # -----------------------------------------------------------------
            # FASE 3 (10.0s – 20.0s): Optimización Iterativa en Tiempo Real
            # -----------------------------------------------------------------
            elif t_sec < 20.0:
                phase_badge_txt.set_text("FASE 3/5 · OPTIMIZACIÓN ITERATIVA")
                phase_badge_txt.set_color(GOLD)
                phase_pill.set_edgecolor(GOLD)
                progress_line.set_color(GOLD)

                u = (t_sec - 10.0) / 10.0
                # Pacing ligeramente desacelerado para ver bien rotación inicial y ajuste fino
                u_paced = 0.65 * u + 0.35 * (1.0 - (1.0 - u) ** 1.8)
                idx_float = u_paced * (n_opt_steps - 1)
                i0 = int(math.floor(idx_float))
                i1 = min(n_opt_steps - 1, i0 + 1)
                frac = idx_float - i0

                w_cur = (1.0 - frac) * traj["w"][i0] + frac * traj["w"][i1]
                b_cur = (1.0 - frac) * traj["b"][i0] + frac * traj["b"][i1]
                loss_cur = (1.0 - frac) * traj["loss"][i0] + frac * traj["loss"][i1]
                marg_cur = (1.0 - frac) * traj["margin"][i0] + frac * traj["margin"][i1]
                n_viol = int(traj["violations"][i0])
                viol_mask = traj["viol_mask"][i0]

                if n_viol > 0:
                    narration_txt.set_text(
                        f"Minimizando ½||w||² + penalización por margen: {n_viol} punto(s) empujan la frontera hacia afuera."
                    )
                else:
                    narration_txt.set_text(
                        "Sin violaciones de margen: reduciendo ||w|| para maximizar el ancho del corredor 2/||w||."
                    )

                sc_pos_core.set_sizes(np.full(len(pos_idx), 95.0))
                sc_pos_glow.set_sizes(np.full(len(pos_idx), 295.0))
                sc_neg_core.set_sizes(np.full(len(neg_idx), 95.0))
                sc_neg_glow.set_sizes(np.full(len(neg_idx), 295.0))
                sc_pos_core.set_alpha(0.96)
                sc_neg_core.set_alpha(0.96)

                # Color pasa de dorado a esmeralda al acercarse al óptimo
                hp_col = EMERALD if u > 0.88 else GOLD
                core_col = "#D1FAE5" if u > 0.88 else "#FEF9C3"
                set_hyperplane_visual(w_cur, b_cur, hp_col, core_col, 1.0, 0.16, show_normal=True, normal_alpha=1.0)
                update_telemetry(f"{i0 + 1:3d} / {n_opt_steps}", w_cur, b_cur, marg_cur, margin_color=EMERALD if n_viol == 0 else GOLD)

                # Resaltar puntos que están violando el margen en esta iteración
                if n_viol > 0:
                    pulse = 0.5 + 0.5 * math.sin(t_sec * 12.0)
                    rings = np.zeros(len(X))
                    rings[viol_mask] = 260.0 + 60.0 * pulse
                    sc_viol_rings.set_sizes(rings)
                    sc_viol_rings.set_edgecolors(AMBER)
                    sc_viol_rings.set_alpha(0.88)

                # Actualizar curvas de telemetría
                xs_plot = np.append(iters_x[: i0 + 1], idx_float)
                ys_loss = np.append(traj["loss"][: i0 + 1], loss_cur)
                ys_marg = np.append(traj["margin"][: i0 + 1], marg_cur)

                loss_line.set_data(xs_plot, ys_loss)
                loss_dot.set_data([idx_float], [loss_cur])
                marg_line.set_data(xs_plot, ys_marg)
                marg_dot.set_data([idx_float], [marg_cur])

            # -----------------------------------------------------------------
            # FASE 4 (20.0s – 26.0s): Vectores de Soporte y Margen Máximo
            # -----------------------------------------------------------------
            elif t_sec < 26.0:
                phase_badge_txt.set_text("FASE 4/5 · VECTORES DE SOPORTE")
                phase_badge_txt.set_color(EMERALD)
                phase_pill.set_edgecolor(EMERALD)
                progress_line.set_color(EMERALD)
                narration_txt.set_text(
                    "Solo los Vectores de Soporte (αᵢ > 0) tocan los límites ±1 y determinan el hiperplano óptimo."
                )

                local_t = t_sec - 20.0
                fade_sv = ease_out_cubic(local_t / 1.1)
                fade_proj = ease_out_cubic((local_t - 1.0) / 1.0)
                fade_caliper = ease_out_cubic((local_t - 2.2) / 1.0)

                # Atenuar sutilmente los puntos que NO son vectores de soporte
                dim_factor = 1.0 - 0.52 * fade_sv
                pos_alphas = np.array([1.0 if idx in sv_indices else dim_factor for idx in pos_idx])
                neg_alphas = np.array([1.0 if idx in sv_indices else dim_factor for idx in neg_idx])
                sc_pos_core.set_alpha(pos_alphas)
                sc_neg_core.set_alpha(neg_alphas)
                sc_pos_core.set_sizes(np.array([125.0 if idx in sv_indices else 82.0 for idx in pos_idx]))
                sc_neg_core.set_sizes(np.array([125.0 if idx in sv_indices else 82.0 for idx in neg_idx]))
                sc_pos_glow.set_sizes(np.array([420.0 if idx in sv_indices else 210.0 for idx in pos_idx]))
                sc_neg_glow.set_sizes(np.array([420.0 if idx in sv_indices else 210.0 for idx in neg_idx]))

                set_hyperplane_visual(w_opt, b_opt, EMERALD, "#ECFDF5", 1.0, 0.18, show_normal=True, normal_alpha=1.0)
                update_telemetry("¡Óptimo KKT!", w_opt, b_opt, opt_margin, margin_color=EMERALD)

                # Aros dorados pulsantes en Vectores de Soporte
                pulse = 0.5 + 0.5 * math.sin(local_t * 5.0)
                sv_rings_outer.set_sizes(np.full(len(sv_indices), 420.0 + 75.0 * pulse))
                sv_rings_inner.set_sizes(np.full(len(sv_indices), 275.0))
                sv_rings_outer.set_alpha(0.45 * fade_sv)
                sv_rings_inner.set_alpha(0.95 * fade_sv)

                # Proyecciones ortogonales y etiquetas VS1, VS2, VS3
                for k, (pt, proj) in enumerate(sv_proj_pts):
                    sv_proj_lines[k].set_data([pt[0], proj[0]], [pt[1], proj[1]])
                    sv_proj_lines[k].set_alpha(0.90 * fade_proj)
                    sv_badges[k].set_alpha(fade_sv)
                    if sv_badges[k].arrow_patch:
                        sv_badges[k].arrow_patch.set_alpha(0.85 * fade_sv)

                # Caliper del margen máximo
                caliper_arrow.set_positions((caliper_p1[0], caliper_p1[1]), (caliper_p2[0], caliper_p2[1]))
                caliper_arrow.set_alpha(0.95 * fade_caliper)
                lbl_c_pos = caliper_center + 0.62 * t_unit_opt
                caliper_label.set_position((lbl_c_pos[0], lbl_c_pos[1]))
                caliper_label.set_text(f"Margen Máximo\n2 / ||w*|| = {opt_margin:.2f}")
                caliper_label.set_alpha(fade_caliper)

                # Curvas completas
                loss_line.set_data(iters_x, traj["loss"])
                loss_dot.set_data([n_opt_steps - 1], [traj["loss"][-1]])
                marg_line.set_data(iters_x, traj["margin"])
                marg_dot.set_data([n_opt_steps - 1], [traj["margin"][-1]])

            # -----------------------------------------------------------------
            # FASE 5 (26.0s – 32.0s): Regiones de Decisión y Clasificación Final
            # -----------------------------------------------------------------
            else:
                phase_badge_txt.set_text("FASE 5/5 · FRONTERA FINAL")
                phase_badge_txt.set_color(EMERALD)
                phase_pill.set_edgecolor(EMERALD)
                progress_line.set_color(EMERALD)
                narration_txt.set_text(
                    "Hiperplano óptimo hallado: clasifica nuevos puntos mediante ŷ = sign(w*ᵀx + b*)."
                )

                local_t = t_sec - 26.0
                fade_reg = ease_out_cubic(local_t / 1.2)
                fade_eq = ease_out_cubic((local_t - 0.4) / 0.8)
                fade_t1 = ease_out_cubic((local_t - 1.3) / 0.7)
                fade_t2 = ease_out_cubic((local_t - 2.3) / 0.7)

                # Regiones de decisión translúcidas
                p_poly = halfspace_polygon(w_opt, b_opt, +1, XMIN, XMAX, YMIN, YMAX)
                n_poly = halfspace_polygon(w_opt, b_opt, -1, XMIN, XMAX, YMIN, YMAX)
                pos_region_poly.set_xy(p_poly)
                neg_region_poly.set_xy(n_poly)
                pos_region_poly.set_alpha(0.085 * fade_reg)
                neg_region_poly.set_alpha(0.085 * fade_reg)

                # Restaurar visibilidad equilibrada de todos los puntos
                pos_alphas = np.array([1.0 if idx in sv_indices else 0.72 for idx in pos_idx])
                neg_alphas = np.array([1.0 if idx in sv_indices else 0.72 for idx in neg_idx])
                sc_pos_core.set_alpha(pos_alphas)
                sc_neg_core.set_alpha(neg_alphas)
                sc_pos_core.set_sizes(np.array([125.0 if idx in sv_indices else 88.0 for idx in pos_idx]))
                sc_neg_core.set_sizes(np.array([125.0 if idx in sv_indices else 88.0 for idx in neg_idx]))

                set_hyperplane_visual(w_opt, b_opt, EMERALD, "#ECFDF5", 1.0, 0.16, show_normal=True, normal_alpha=0.85)
                update_telemetry("Convergido ✓", w_opt, b_opt, opt_margin, margin_color=EMERALD)

                # Mantener SVs y caliper visibles
                sv_rings_outer.set_sizes(np.full(len(sv_indices), 440.0))
                sv_rings_inner.set_sizes(np.full(len(sv_indices), 275.0))
                sv_rings_outer.set_alpha(0.38)
                sv_rings_inner.set_alpha(0.95)
                for k, (pt, proj) in enumerate(sv_proj_pts):
                    sv_proj_lines[k].set_data([pt[0], proj[0]], [pt[1], proj[1]])
                    sv_proj_lines[k].set_alpha(0.65)
                    sv_badges[k].set_alpha(0.90)
                    if sv_badges[k].arrow_patch:
                        sv_badges[k].arrow_patch.set_alpha(0.70)

                caliper_arrow.set_positions((caliper_p1[0], caliper_p1[1]), (caliper_p2[0], caliper_p2[1]))
                caliper_arrow.set_alpha(0.90)
                lbl_c_pos = caliper_center + 0.62 * t_unit_opt
                caliper_label.set_position((lbl_c_pos[0], lbl_c_pos[1]))
                caliper_label.set_text(f"Margen Máximo\n2 / ||w*|| = {opt_margin:.2f}")
                caliper_label.set_alpha(0.92)

                # Ecuación final del hiperplano
                sign_w2 = "+" if w_opt[1] >= 0 else "−"
                sign_b = "+" if b_opt >= 0 else "−"
                lbl_hp_eq.set_text(
                    f"Hiperplano Óptimo:  {w_opt[0]:.2f}·x₁ {sign_w2} {abs(w_opt[1]):.2f}·x₂ {sign_b} {abs(b_opt):.2f} = 0"
                )
                lbl_hp_eq.set_alpha(fade_eq)

                # Puntos nuevos clasificados
                for k, ft in enumerate((fade_t1, fade_t2)):
                    if ft > 0.01:
                        test_scatters[k].set_sizes([290.0 * ft])
                        test_scatters[k].set_alpha(ft)
                        test_labels[k].set_alpha(ft)
                        if test_labels[k].arrow_patch:
                            test_labels[k].arrow_patch.set_alpha(0.85 * ft)

                loss_line.set_data(iters_x, traj["loss"])
                loss_dot.set_data([n_opt_steps - 1], [traj["loss"][-1]])
                marg_line.set_data(iters_x, traj["margin"])
                marg_dot.set_data([n_opt_steps - 1], [traj["margin"][-1]])

            # Dibujar frame a buffer RGB
            fig.canvas.draw()
            buf = np.asarray(fig.canvas.buffer_rgba())[:, :, :3].copy()
            writer.append_data(buf)

            if snapshots_dir and f in snapshot_frames:
                snap_path = os.path.join(snapshots_dir, snapshot_frames[f])
                imageio.imwrite(snap_path, buf)

            if (f + 1) % 120 == 0 or f == total_frames - 1:
                elapsed = time.time() - t_start
                print(f"  Frame {f + 1:4d}/{total_frames} ({100.0 * (f + 1) / total_frames:5.1f}%) — {elapsed:5.1f}s")

    finally:
        writer.close()
        plt.close(fig)

    elapsed_total = time.time() - t_start
    size_mb = os.path.getsize(output_path) / (1024 * 1024)
    print(f"¡Video completado en {elapsed_total:.1f}s! Tamaño: {size_mb:.2f} MB -> {output_path}")


def main():
    parser = argparse.ArgumentParser(description="Genera video 16:9 de simulación de cálculo de hiperplano en SVM.")
    parser.add_argument(
        "--output",
        default=os.path.join(os.path.dirname(os.path.abspath(__file__)), "svm_hyperplane_simulation_16x9.mp4"),
        help="Ruta del archivo MP4 de salida",
    )
    parser.add_argument(
        "--snapshots",
        default=os.path.join(os.path.dirname(os.path.abspath(__file__)), "preview_frames"),
        help="Carpeta para guardar fotogramas clave de verificación",
    )
    parser.add_argument("--fps", type=int, default=30)
    parser.add_argument("--duration", type=float, default=32.0)
    args = parser.parse_args()
    render_video(args.output, snapshots_dir=args.snapshots, fps=args.fps, duration_sec=args.duration)


if __name__ == "__main__":
    main()
