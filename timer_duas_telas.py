import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from visor_flutuante import FloatingTimer
import sys
import os
from PyQt5 import QtWidgets
import webbrowser

def resource_path(relative_path):
    """Retorna o caminho absoluto, mesmo quando empacotado com PyInstaller."""
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class TimerApp:
    def __init__(self, root):
        self.root = root
        self.root.iconbitmap(resource_path("clock.ico"))
        self.root.title("Timer Screen")
        self.timer_running = False
        self.remaining_seconds = 0
        self.fullscreen_window = None
        self.floating_window = None
        self.floating_label = None
        self._drag_data = {"x": 0, "y": 0}
        self.floating_default_pos = None  # Posição padrão do visor flutuante

        # Inicializa o visor flutuante
        self.qt_app = QtWidgets.QApplication(sys.argv)
        self.floating_timer = FloatingTimer()
        self.floating_timer.show()
        self.floating_timer.hide()  # Começa escondido

        self.create_widgets()
        self.bind_shortcuts()

        root.resizable(False, False)

    def create_widgets(self):
        # Entrada de tempo
        time_frame = ttk.Frame(self.root)
        time_frame.pack(padx=10, pady=10)

        ttk.Label(time_frame, text="Horas:").grid(row=0, column=0, padx=5)
        self.hours_var = tk.StringVar(value="0")
        self.hours_entry = ttk.Entry(time_frame, textvariable=self.hours_var, width=5)
        self.hours_entry.grid(row=0, column=1)

        ttk.Label(time_frame, text="Minutos:").grid(row=0, column=2, padx=5)
        self.minutes_var = tk.StringVar(value="0")
        self.minutes_entry = ttk.Entry(time_frame, textvariable=self.minutes_var, width=5)
        self.minutes_entry.grid(row=0, column=3)

        ttk.Label(time_frame, text="Segundos:").grid(row=0, column=4, padx=5)
        self.seconds_var = tk.StringVar(value="0")
        self.seconds_entry = ttk.Entry(time_frame, textvariable=self.seconds_var, width=5)
        self.seconds_entry.grid(row=0, column=5)

        # Botões
        button_frame = ttk.Frame(self.root)
        button_frame.pack(pady=10)

        self.start_button = ttk.Button(button_frame, text="Iniciar", command=self.start_timer)
        self.start_button.grid(row=0, column=0, padx=5)

        self.stop_button = ttk.Button(button_frame, text="Parar", command=self.stop_timer, state="disabled")
        self.stop_button.grid(row=0, column=1, padx=5)

        self.reset_button = ttk.Button(button_frame, text="Resetar", command=self.reset_timer)
        self.reset_button.grid(row=0, column=2, padx=5)

        self.toggle_fs_button = ttk.Button(button_frame, text="Tela Cheia", command=self.toggle_fullscreen)
        self.toggle_fs_button.grid(row=0, column=3, padx=5)

        self.toggle_floating_button = ttk.Button(button_frame, text="Visor Flutuante", command=self.toggle_floating_timer)
        self.toggle_floating_button.grid(row=0, column=4, padx=5)

        # Frame para botões de cor do visor flutuante
        color_frame = ttk.LabelFrame(self.root, text="Cores do Visor Flutuante")
        color_frame.pack(pady=5)

        # Botões de cor
        colors = {
            "white": "Branco",
            "red": "Vermelho",
            "green": "Verde",
            "black": "Preto",
            "yellow": "Amarelo"
        }

        for i, (color, name) in enumerate(colors.items()):
            btn = tk.Button(
                color_frame,
                text=name,
                bg=color,
                fg="black" if color != "black" else "white",
                command=lambda c=color: self.change_floating_color(c)
            )
            btn.grid(row=0, column=i, padx=5, pady=5)

        # Botões de ajuste de fonte do visor flutuante
        font_plus = tk.Button(color_frame, text="+", width=2, command=self.increase_floating_font)
        font_plus.grid(row=0, column=len(colors), padx=5, pady=5)
        font_minus = tk.Button(color_frame, text="-", width=2, command=self.decrease_floating_font)
        font_minus.grid(row=0, column=len(colors)+1, padx=5, pady=5)

        # Tempo na tela principal
        self.timer_label = ttk.Label(self.root, text="00:00:00", font=("Helvetica", 36))
        self.timer_label.pack(pady=10)

        # Adiciona o rodapé com o link do desenvolvedor
        footer_frame = tk.Frame(self.root)
        footer_frame.pack(side="bottom", fill="x", anchor="se")
        footer_frame.grid_columnconfigure(1, weight=1)
        dev_text = tk.Label(footer_frame, text="Desenvolvido por ", fg="gray", font=("Arial", 8))
        dev_text.grid(row=0, column=0, sticky="e", padx=0, pady=0)
        dev_link = tk.Label(footer_frame, text="Victor Hugo dos S. Silva", fg="blue", cursor="hand2", font=("Arial", 8))
        dev_link.grid(row=0, column=1, sticky="w", padx=0, pady=0)
        dev_link.bind("<Button-1>", lambda e: webbrowser.open_new("https://www.linkedin.com/in/victorhugosantossilva/"))

    def bind_shortcuts(self):
        self.root.bind("<F11>", lambda event: self.toggle_fullscreen())

    def start_timer(self):
        try:
            hours = int(self.hours_var.get())
            minutes = int(self.minutes_var.get())
            seconds = int(self.seconds_var.get())
            self.remaining_seconds = hours * 3600 + minutes * 60 + seconds

            if self.remaining_seconds <= 0:
                raise ValueError

        except ValueError:
            messagebox.showerror("Erro", "Insira um tempo válido.")
            return

        self.timer_running = True
        self.start_button.config(state="disabled")
        self.stop_button.config(state="normal")

        self.update_timer()

    def stop_timer(self):
        self.timer_running = False
        self.start_button.config(state="normal")
        self.stop_button.config(state="disabled")

    def reset_timer(self):
        try:
            hours = int(self.hours_var.get())
            minutes = int(self.minutes_var.get())
            seconds = int(self.seconds_var.get())
            self.remaining_seconds = hours * 3600 + minutes * 60 + seconds
        except ValueError:
            self.remaining_seconds = 0

        self.timer_running = False
        self.update_timer_label(self.remaining_seconds)
        self.start_button.config(state="normal")
        self.stop_button.config(state="disabled")
        # Atualiza imediatamente o label da tela cheia, se estiver aberta
        if self.fullscreen_window:
            hours = self.remaining_seconds // 3600
            minutes = (self.remaining_seconds % 3600) // 60
            seconds = self.remaining_seconds % 60
            time_str = f"{hours:02}:{minutes:02}:{seconds:02}"
            self.fullscreen_label.config(text=time_str, font=("Helvetica", 160))

    def update_timer(self):
        if self.timer_running and self.remaining_seconds > 0:
            self.update_timer_label(self.remaining_seconds)
            self.remaining_seconds -= 1
            self.root.after(1000, self.update_timer)
        elif self.remaining_seconds == 0:
            self.update_timer_label(0)
            self.stop_timer()
            self.exibir_mensagem_fim()

    def exibir_mensagem_fim(self):
        if self.fullscreen_window:
            self.fullscreen_label.config(text="TEMPO ESGOTADO", font=("Helvetica", 110))
        else:
            self.timer_label.config(text="TEMPO ESGOTADO")
        
        # Atualiza o visor flutuante
        if self.floating_timer.isVisible():
            self.floating_timer.set_time("TEMPO ESGOTADO")

    def update_timer_label(self, total_seconds):
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60
        time_str = f"{hours:02}:{minutes:02}:{seconds:02}"
        self.timer_label.config(text=time_str)

        if self.fullscreen_window:
            # Sempre usa o tamanho fixo, não altera fonte
            if self.fullscreen_label.cget("text") != "TEMPO ESGOTADO":
                self.fullscreen_label.config(text=time_str, font=("Helvetica", 160))
        
        # Atualiza o visor flutuante
        if self.floating_timer.isVisible():
            self.floating_timer.set_time(time_str)

    def toggle_fullscreen(self):
        if self.fullscreen_window:
            self.close_fullscreen_timer()
        else:
            self.show_fullscreen_timer()

    def show_fullscreen_timer(self):
        if self.fullscreen_window:
            return  # já está aberta

        self.fullscreen_window = tk.Toplevel(self.root)
        self.fullscreen_window.attributes("-fullscreen", True)
        self.fullscreen_window.configure(bg="black")
        self.fullscreen_window.bind("<Escape>", lambda e: self.close_fullscreen_timer())

        self.fullscreen_label = tk.Label(
            self.fullscreen_window,
            text="",
            font=("Helvetica", 220),  # Aumente aqui
            fg="white",
            bg="black"
        )
        self.fullscreen_label.pack(expand=True)

        self.update_timer_label(self.remaining_seconds)
        self.toggle_fs_button.config(text="Esconder Tela Cheia")

    def close_fullscreen_timer(self):
        if self.fullscreen_window:
            self.fullscreen_window.destroy()
            self.fullscreen_window = None
            self.toggle_fs_button.config(text="Tela Cheia")

    def toggle_floating_timer(self):
        if self.floating_timer.isVisible():
            # Salva a posição atual como padrão ao esconder
            self.floating_default_pos = self.floating_timer.pos()
            self.floating_timer.hide()
            self.toggle_floating_button.config(text="Contador Flutuante")
        else:
            self.floating_timer.show()
            # Reposiciona para a posição padrão, se existir
            if self.floating_default_pos:
                self.floating_timer.move(self.floating_default_pos)
            # Atualiza o visor flutuante com o tempo atual no formato HH:MM:SS
            hours = self.remaining_seconds // 3600
            minutes = (self.remaining_seconds % 3600) // 60
            seconds = self.remaining_seconds % 60
            time_str = f"{hours:02}:{minutes:02}:{seconds:02}"
            self.floating_timer.set_time(time_str)
            self.toggle_floating_button.config(text="Esconder Contador")

    def start_move_floating(self, event):
        self._drag_data["x"] = event.x
        self._drag_data["y"] = event.y

    def do_move_floating(self, event):
        x = self.floating_window.winfo_x() + event.x - self._drag_data["x"]
        y = self.floating_window.winfo_y() + event.y - self._drag_data["y"]
        self.floating_window.geometry(f"+{x}+{y}")

    def change_floating_color(self, color):
        # Muda a cor do visor flutuante, se visível
        if self.floating_timer.isVisible():
            self.floating_timer.set_color(color)
        # Muda a cor do contador da tela cheia, se visível
        if self.fullscreen_window:
            self.fullscreen_label.config(fg=color)

    def increase_floating_font(self):
        if self.floating_timer.isVisible():
            self.floating_timer.increase_font_size()

    def decrease_floating_font(self):
        if self.floating_timer.isVisible():
            self.floating_timer.decrease_font_size()

if __name__ == "__main__":
    root = tk.Tk()
    root.resizable(False, False)
    app = TimerApp(root)
    root.mainloop()
