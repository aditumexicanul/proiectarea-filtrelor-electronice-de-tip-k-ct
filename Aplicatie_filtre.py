import customtkinter as ctk
from PIL import Image
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

# ----------------- SETARI APLICATIE -----------------

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("Proiectarea filtrelor electrice de tip K-constant")
app.state("zoomed")
app.configure(fg_color="#EAEAEA")

app.grid_columnconfigure(0, weight=1)
app.grid_rowconfigure(0, weight=1)

main_frame = ctk.CTkFrame(app, fg_color="white", corner_radius=20)
main_frame.grid(row=0, column=0, padx=40, pady=40, sticky="nsew")

main_frame.grid_columnconfigure(0, weight=0)
main_frame.grid_columnconfigure(1, weight=1)
main_frame.grid_columnconfigure(2, weight=1)

title_label = ctk.CTkLabel(
    main_frame,
    text="Proiectarea filtrelor electrice de tip K-constant",
    text_color="#222222",
    font=("Arial", 24, "bold")
)
title_label.grid(row=0, column=0, columnspan=3, padx=30, pady=(25, 25))

# ----------------- CONSTANTE SURSA/SARCINA -----------------

RS = 50.0
RL = 50.0

# ----------------- WIDGETURI DINAMICE (PARAM + REZULTATE) -----------------

dynamic_widgets = []

entry_fc = None
entry_fc1 = None
entry_fc2 = None
entry_R0 = None

result_value_labels = {}   # {"L1": label_val, ...}
result_unit_boxes = {}     # {"L1": combobox_unit, ...}

def clear_dynamic_widgets():
    for w in dynamic_widgets:
        w.destroy()
    dynamic_widgets.clear()
    result_value_labels.clear()
    result_unit_boxes.clear()

def add_parameters_title(row):
    label = ctk.CTkLabel(
        main_frame,
        text="Parametrii:",
        text_color="#222222",
        font=("Arial", 18, "bold")
    )
    label.grid(row=row, column=0, padx=(30, 15), pady=(0, 5), sticky="w")
    dynamic_widgets.append(label)

def add_field(row, text, var_name):
    global entry_fc, entry_fc1, entry_fc2, entry_R0

    label = ctk.CTkLabel(
        main_frame,
        text=text,
        text_color="#222222",
        font=("Arial", 16, "bold")
    )
    label.grid(row=row, column=0, padx=(30, 15), pady=4, sticky="w")

    entry = ctk.CTkEntry(
        main_frame,
        placeholder_text="Introduceți valoarea",
        width=260,
        height=34,
        fg_color="#F8F8F8",
        border_color="#C8C8C8",
        text_color="#222222",
        placeholder_text_color="#888888"
    )
    entry.grid(row=row, column=1, padx=(0, 30), pady=4, sticky="w")

    dynamic_widgets.append(label)
    dynamic_widgets.append(entry)

    if var_name == "fc":
        entry_fc = entry
    elif var_name == "fc1":
        entry_fc1 = entry
    elif var_name == "fc2":
        entry_fc2 = entry
    elif var_name == "R0":
        entry_R0 = entry

def add_results(start_row, symbols):
    """
    Creează blocul 'Rezultate:' și liniile L1/C1/L2/C2 una sub alta,
    cu spacing egal pe verticală, indiferent de filtru.
    """
    result_title = ctk.CTkLabel(
        main_frame,
        text="Rezultate:",
        text_color="#222222",
        font=("Arial", 18, "bold")
    )
    result_title.grid(row=start_row, column=0, padx=(30, 15), pady=(10, 4), sticky="w")
    dynamic_widgets.append(result_title)

    row = start_row + 1
    result_value_labels.clear()
    result_unit_boxes.clear()

    for sym in symbols:
        # Nume
        label_name = ctk.CTkLabel(
            main_frame,
            text=f"{sym} =",
            text_color="#222222",
            font=("Arial", 16)
        )
        label_name.grid(row=row, column=0, padx=(30, 5), pady=2, sticky="w")

        # Valoare numerică
        label_val = ctk.CTkLabel(
            main_frame,
            text="",
            text_color="#222222",
            font=("Arial", 16)
        )
        label_val.grid(row=row, column=1, padx=(0, 10), pady=2, sticky="w")

        # Unități: L -> mH / μH ; C -> μF / nF
        if sym.startswith("L"):
            units = ["mH", "μH"]
            default_unit = "mH"
        else:
            units = ["μF", "nF"]
            default_unit = "μF"

        unit_box = ctk.CTkComboBox(
            main_frame,
            values=units,
            width=70,
            state="readonly"
        )
        unit_box.set(default_unit)
        unit_box.grid(row=row, column=1, padx=(220, 30), pady=2, sticky="w")

        dynamic_widgets.extend([label_name, label_val, unit_box])

        result_value_labels[sym] = label_val
        result_unit_boxes[sym] = unit_box

        row += 1

def update_results_labels(results):
    """
    results: dict cu valori în SI; afișăm în unitățile alese pentru
    L1/L2 (mH/μH) și C1/C2 (μF/nF).
    """
    for sym, val in results.items():
        if sym not in result_value_labels:
            continue

        unit = result_unit_boxes.get(sym).get() if sym in result_unit_boxes else ""

        if sym.startswith("L"):
            if unit == "mH":
                shown = val * 1e3
                text = f"{shown:.6f} mH"
            elif unit == "μH":
                shown = val * 1e6
                text = f"{shown:.6f} μH"
            else:
                text = f"{val:.6e} H"
        else:
            if unit == "μF":
                shown = val * 1e6
                text = f"{shown:.6f} μF"
            elif unit == "nF":
                shown = val * 1e9
                text = f"{shown:.6f} nF"
            else:
                text = f"{val:.6e} F"

        result_value_labels[sym].configure(text=text)

# ----------------- IMAGINE FILTRU (DREAPTA SUS) -----------------

image_label = ctk.CTkLabel(main_frame, text="", fg_color="transparent")
image_label.grid(row=2, column=2, rowspan=4, padx=(40, 30), pady=(20, 10), sticky="n")

def set_filter_image(path):
    try:
        img = ctk.CTkImage(
            light_image=Image.open(path),
            dark_image=Image.open(path),
            size=(420, 260)
        )
        image_label.configure(image=img, text="")
        image_label.image = img
    except Exception:
        image_label.configure(image=None, text="(Imagine indisponibilă)")

# ----------------- GRAFIC (DREAPTA JOS) -----------------

graph_frame = ctk.CTkFrame(main_frame, fg_color="white", corner_radius=10)
graph_frame.grid(row=7, column=2, rowspan=8, padx=(40, 30), pady=(10, 20), sticky="nsew")
main_frame.grid_rowconfigure(7, weight=1)
main_frame.grid_rowconfigure(8, weight=1)
main_frame.grid_rowconfigure(9, weight=1)

def draw_graph(f, A_dB, meta):
    for child in graph_frame.winfo_children():
        child.destroy()

    fig = Figure(figsize=(4.8, 3.0), dpi=100)
    ax = fig.add_subplot(111)
    ax.semilogx(f, A_dB, label='|Vout/Vin| [dB]')

    ct = meta["ct"]
    fc = meta["fc"]
    fc1 = meta["fc1"]
    fc2 = meta["fc2"]

    if ct == 1:
        ax.axvline(fc, color='red', linestyle='--', label=f'fc = {fc:.0f} Hz')
        ax.set_title('Filtru trece-jos k constant, T')
    elif ct == 2:
        ax.axvline(fc, color='red', linestyle='--', label=f'fc = {fc:.0f} Hz')
        ax.set_title('Filtru trece-sus k constant, T')
    elif ct == 3:
        ax.axvline(fc1, color='red', linestyle='--', label=f'fc1 = {fc1:.0f} Hz')
        ax.axvline(fc2, color='red', linestyle='--', label=f'fc2 = {fc2:.0f} Hz')
        ax.set_title('Filtru trece-banda k constant, T')
    elif ct == 4:
        ax.axvline(fc1, color='red', linestyle='--', label=f'fc1 = {fc1:.0f} Hz')
        ax.axvline(fc2, color='red', linestyle='--', label=f'fc2 = {fc2:.0f} Hz')
        ax.set_title('Filtru opreste-banda k constant, T')

    ax.grid(True, which='both', linestyle='--', alpha=0.6)
    ax.set_xlabel('Frecventa [Hz]')
    ax.set_ylabel('Amplitudine [dB]')
    ax.legend()

    canvas = FigureCanvasTkAgg(fig, master=graph_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True)

# ----------------- FUNCTII DE CALCUL -----------------

def calc_ftj(fc, R0, Rs=RS, RL_=RL):
    L1 = R0 / (np.pi * fc)
    C2 = 1 / (np.pi * fc * R0)

    f = np.logspace(1, 6, 2000)
    w = 2 * np.pi * f
    Vin = 1.0

    Z1 = 1j * w * (L1 / 2)
    Z2 = 1 / (1j * w * C2)

    Z_right = Z1 + RL_
    Z_parallel = (Z2 * Z_right) / (Z2 + Z_right)
    Zin = Rs + Z1 + Z_parallel

    Iin = Vin / Zin
    Vmid = Iin * Z_parallel
    Iright = Vmid / Z_right
    Vout = Iright * RL_

    H = Vout / Vin
    A_dB = 20 * np.log10(np.abs(H))

    results = {"L1": L1, "C2": C2}
    meta = {"ct": 1, "fc": fc, "fc1": 0, "fc2": 0}
    return results, f, A_dB, meta

def calc_fts(fc, R0, Rs=RS, RL_=RL):
    C1 = 1 / (4 * np.pi * R0 * fc)
    L2 = R0 / (4 * np.pi * fc)

    f = np.logspace(1, 6, 2000)
    w = 2 * np.pi * f
    Vin = 1.0

    Z1 = 1 / (1j * w * 2 * C1)
    Z2 = 1j * w * L2

    Z_right = Z1 + RL_
    Z_parallel = (Z2 * Z_right) / (Z2 + Z_right)
    Zin = Rs + Z1 + Z_parallel

    Iin = Vin / Zin
    Vmid = Iin * Z_parallel
    Iright = Vmid / Z_right
    Vout = Iright * RL_

    H = Vout / Vin
    A_dB = 20 * np.log10(np.abs(H))

    results = {"C1": C1, "L2": L2}
    meta = {"ct": 2, "fc": fc, "fc1": 0, "fc2": 0}
    return results, f, A_dB, meta

def calc_ftb(fc1, fc2, R0, Rs=RS, RL_=RL):
    dF = fc2 - fc1
    pF = fc1 * fc2

    L1 = R0 / (np.pi * dF)
    C1 = dF / (4 * np.pi * R0 * pF)
    L2 = (R0 * dF) / (4 * np.pi * pF)
    C2 = 1 / (np.pi * R0 * dF)

    f = np.logspace(1, 7, 2000)
    w = 2 * np.pi * f
    Vin = 1.0

    Zl1 = 1j * w * (L1 / 2)
    Zc1 = 1 / (1j * w * 2 * C1)
    Zl2 = 1j * w * L2
    Zc2 = 1 / (1j * w * C2)

    Z1 = Zl1 + Zc1
    Z2 = (Zl2 * Zc2) / (Zl2 + Zc2)

    Z_right = Z1 + RL_
    Z_parallel = (Z2 * Z_right) / (Z2 + Z_right)
    Zin = Rs + Z1 + Z_parallel

    Iin = Vin / Zin
    Vmid = Iin * Z_parallel
    Iright = Vmid / Z_right
    Vout = Iright * RL_

    H = Vout / Vin
    A_dB = 20 * np.log10(np.abs(H))

    results = {"L1": L1, "C1": C1, "L2": L2, "C2": C2}
    meta = {"ct": 3, "fc": 0, "fc1": fc1, "fc2": fc2}
    return results, f, A_dB, meta

def calc_fob(fc1, fc2, R0, Rs=RS, RL_=RL):
    dF = fc2 - fc1
    pF = fc1 * fc2

    L1 = (R0 * dF) / (np.pi * pF)
    C1 = 1 / (4 * np.pi * R0 * dF)
    L2 = R0 / (4 * np.pi * dF)
    C2 = dF / (np.pi * R0 * pF)

    f = np.logspace(1, 7, 2000)
    w = 2 * np.pi * f
    Vin = 1.0

    Zl1 = 1j * w * (L1 / 2)
    Zc1 = 1 / (1j * w * 2 * C1)
    Zl2 = 1j * w * L2
    Zc2 = 1 / (1j * w * C2)

    Z1 = (Zl1 * Zc1) / (Zl1 + Zc1)
    Z2 = Zl2 + Zc2

    Z_right = Z1 + RL_
    Z_parallel = (Z2 * Z_right) / (Z2 + Z_right)
    Zin = Rs + Z1 + Z_parallel

    Iin = Vin / Zin
    Vmid = Iin * Z_parallel
    Iright = Vmid / Z_right
    Vout = Iright * RL_

    H = Vout / Vin
    A_dB = 20 * np.log10(np.abs(H))

    results = {"L1": L1, "C1": C1, "L2": L2, "C2": C2}
    meta = {"ct": 4, "fc": 0, "fc1": fc1, "fc2": fc2}
    return results, f, A_dB, meta

# ----------------- CALLBACK SEGMENTED BUTTON + BUTON CALCUL -----------------

def segmented_button_callback(choice):
    clear_dynamic_widgets()

    params_title_row = 2
    add_parameters_title(params_title_row)
    first_param_row = params_title_row + 1

    if choice == "Filtru trece jos":
        add_field(first_param_row,     "Frecventa de taiere fc [Hz]", "fc")
        add_field(first_param_row + 1, "Impedanta caracteristica R0 [Ω]", "R0")
        results_start_row = first_param_row + 3
        add_results(results_start_row, ["L1", "C2"])
        set_filter_image("FTJ.png")

    elif choice == "Filtru trece sus":
        add_field(first_param_row,     "Frecventa de taiere fc [Hz]", "fc")
        add_field(first_param_row + 1, "Impedanta caracteristica R0 [Ω]", "R0")
        results_start_row = first_param_row + 3
        add_results(results_start_row, ["C1", "L2"])
        set_filter_image("FTS.png")

    elif choice == "Filtru trece banda":
        add_field(first_param_row,     "Frecventa de taiere inferioara fc1 [Hz]", "fc1")
        add_field(first_param_row + 1, "Frecventa de taiere superioara fc2 [Hz]", "fc2")
        add_field(first_param_row + 2, "Impedanta caracteristica R0 [Ω]", "R0")
        results_start_row = first_param_row + 4
        add_results(results_start_row, ["L1", "C1", "L2", "C2"])
        set_filter_image("FTB.png")

    elif choice == "Filtru opreste banda":
        add_field(first_param_row,     "Frecventa de taiere inferioara fc1 [Hz]", "fc1")
        add_field(first_param_row + 1, "Frecventa de taiere superioara fc2 [Hz]", "fc2")
        add_field(first_param_row + 2, "Impedanta caracteristica R0 [Ω]", "R0")
        results_start_row = first_param_row + 4
        add_results(results_start_row, ["L1", "C1", "L2", "C2"])
        set_filter_image("FOB.png")
    else:
        return

    # buton Calculează imediat sub parametri, înainte de blocul de rezultate
    calc_row = results_start_row - 1
    calc_button = ctk.CTkButton(
        main_frame,
        text="Calculează",
        command=on_calculate,
        fg_color="#2F6DB3",
        hover_color="#245A95",
        text_color="white"
    )
    calc_button.grid(row=calc_row, column=1, padx=(0, 30), pady=(6, 6), sticky="e")
    dynamic_widgets.append(calc_button)

def on_calculate():
    choice = combobox.get()
    try:
        if choice == "Filtru trece jos":
            fc = float(entry_fc.get())
            R0 = float(entry_R0.get())
            results, f, A_dB, meta = calc_ftj(fc, R0)

        elif choice == "Filtru trece sus":
            fc = float(entry_fc.get())
            R0 = float(entry_R0.get())
            results, f, A_dB, meta = calc_fts(fc, R0)

        elif choice == "Filtru trece banda":
            fc1 = float(entry_fc1.get())
            fc2 = float(entry_fc2.get())
            R0 = float(entry_R0.get())
            results, f, A_dB, meta = calc_ftb(fc1, fc2, R0)

        elif choice == "Filtru opreste banda":
            fc1 = float(entry_fc1.get())
            fc2 = float(entry_fc2.get())
            R0 = float(entry_R0.get())
            results, f, A_dB, meta = calc_fob(fc1, fc2, R0)
        else:
            return
    except (TypeError, ValueError):
        return

    update_results_labels(results)
    draw_graph(f, A_dB, meta)

# ----------------- SEGMENTED BUTTON (ALEGERE FILTRU) -----------------

combobox = ctk.CTkSegmentedButton(
    main_frame,
    values=[
        "Filtru trece jos",
        "Filtru trece sus",
        "Filtru trece banda",
        "Filtru opreste banda"
    ],
    command=segmented_button_callback,
    fg_color="#D9D9D9",
    selected_color="#2F6DB3",
    selected_hover_color="#245A95",
    unselected_color="#EFEFEF",
    unselected_hover_color="#DDDDDD",
    text_color="#222222",
    font=("Arial", 14, "bold"),
    height=40
)
combobox.grid(row=1, column=0, columnspan=3, padx=30, pady=(0, 30), sticky="ew")
combobox.set("Filtru trece jos")
segmented_button_callback(combobox.get())

app.mainloop()