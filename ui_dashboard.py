import customtkinter as ctk # type: ignore
import psutil, os, sys, time, threading # type: ignore
from datetime import datetime

sys.path.append(os.path.dirname(os.path.abspath(__file__))) # env setup

class Nexusv7(ctk.CTk):
    def __init__(self, on_cmd=None):
        super().__init__()
        self.title("J.A.R.V.I.S. // NEXUS v7.2") # window title
        self.geometry("1100x700") # fixed size
        self.configure(fg_color="#050505") # deep black
        ctk.set_appearance_mode("dark") # force dark
        
        self.on_cmd = on_cmd # event hook
        self.accent = "#00FF88" # neon accent
        
        self.grid_columnconfigure(0, weight=1, minsize=220) # side bar
        self.grid_columnconfigure(1, weight=4) # main hub
        self.grid_rowconfigure(0, weight=1)

        self.side = ctk.CTkFrame(self, fg_color="#050505", corner_radius=0, border_width=1, border_color="#1A1A1A")
        self.side.grid(row=0, column=0, sticky="nsew") # sidebar grid
        
        ctk.CTkLabel(self.side, text="NEXUS COMMAND", font=("Consolas", 18, "bold"), text_color=self.accent).pack(pady=30)
        
        self.vitals = {} # vitals map
        for k in ["CPU", "RAM", "BAT"]:
            f = ctk.CTkFrame(self.side, fg_color="#0D0D0D", height=70, corner_radius=8, border_width=1, border_color="#1A1A1A")
            f.pack(fill="x", padx=15, pady=8); f.pack_propagate(False) # lock size
            ctk.CTkLabel(f, text=k, font=("Consolas", 10), text_color="#777777").pack(pady=(8, 0))
            lb = ctk.CTkLabel(f, text="--%", font=("Consolas", 18, "bold"))
            lb.pack(); self.vitals[k] = lb # store lb

        ctk.CTkLabel(self.side, text="NEURAL REGISTRY", font=("Consolas", 10), text_color="#777777").pack(pady=(20, 5))
        self.models = ["meta-llama/llama-3.3-70b-instruct:free", "google/gemma-3-27b-it:free", "z-ai/glm-4.5-air:free", "stepfun/step-3.5-flash:free", "openrouter/free"]
        self.sel = ctk.CTkOptionMenu(self.side, values=self.models, fg_color="#151515", button_color="#222222", command=self.set_mod)
        self.sel.pack(pady=10, padx=15, fill="x") # model selector

        self.foot = ctk.CTkLabel(self.side, text="SYSTEM READY", font=("Consolas", 10), text_color="#444444")
        self.foot.pack(side="bottom", pady=20) # footer status

        self.hub = ctk.CTkFrame(self, fg_color="#080808", corner_radius=12)
        self.hub.grid(row=0, column=1, sticky="nsew", padx=20, pady=20) # hub grid
        self.hub.grid_columnconfigure(0, weight=1); self.hub.grid_rowconfigure(1, weight=1)

        h = ctk.CTkFrame(self.hub, fg_color="transparent")
        h.grid(row=0, column=0, sticky="ew", padx=20, pady=20) # header
        self.head = ctk.CTkLabel(h, text="NEURAL LINK: SYNCED", font=("Consolas", 12), text_color=self.accent)
        self.head.pack(side="left") # status lbl
        self.mlbl = ctk.CTkLabel(h, text="ACTIVE NODE", font=("Consolas", 10), text_color="#444444")
        self.mlbl.pack(side="right") # model lbl

        self.log_box = ctk.CTkTextbox(self.hub, font=("Consolas", 13), fg_color="#0A0A0A", border_width=1, border_color="#151515")
        self.log_box.grid(row=1, column=0, sticky="nsew", padx=20, pady=10) # console
        
        in_f = ctk.CTkFrame(self.hub, fg_color="transparent")
        in_f.grid(row=2, column=0, sticky="ew", padx=20, pady=10) # input area
        self.entry = ctk.CTkEntry(in_f, placeholder_text="Neural input...", height=40, font=("Consolas", 13), fg_color="#0C0C0C")
        self.entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        self.entry.bind("<Return>", lambda e: self.fire()) # bind enter
        ctk.CTkButton(in_f, text="EXEC", width=80, height=40, fg_color=self.accent, text_color="#000", command=self.fire).pack(side="right")

        act_f = ctk.CTkFrame(self.hub, fg_color="transparent")
        act_f.grid(row=3, column=0, sticky="ew", padx=20, pady=(0, 20)) # actions
        for t, c in [("LOCK", "lock pc"), ("SNAP", "screenshot"), ("NEWS", "news"), ("WEATHER", "weather")]:
            ctk.CTkButton(act_f, text=t, width=70, height=28, fg_color="#121212", font=("Consolas", 9), command=lambda x=c: self.btn_act(x)).pack(side="left", padx=5)
        
        ctk.CTkButton(act_f, text="RELOAD", width=70, height=28, fg_color="#1A1A1A", text_color="#00FFCC", font=("Consolas", 9, "bold"), command=self.reload_cfg).pack(side="left", padx=20)
        ctk.CTkButton(act_f, text="POWER", width=70, height=28, fg_color="#330000", text_color="#FF4444", font=("Consolas", 9, "bold"), command=lambda: self.btn_act("shutdown")).pack(side="right", padx=5)

        threading.Thread(target=self.vitals_loop, daemon=True).start() # start loop

    def vitals_loop(self):
        while 1:
            try:
                c, r = psutil.cpu_percent(), psutil.virtual_memory().percent # poll hw
                b_sens = psutil.sensors_battery() # get bat
                b = f"{b_sens.percent}%" if b_sens else "A/C" # format bat
                self.after(0, lambda: self.upd_v(c, r, b)) # sync ui
            except: pass
            time.sleep(2)

    def upd_v(self, c, r, b): # refresh vitals
        self.vitals["CPU"].configure(text=f"{c}%", text_color=self.accent if c < 80 else "red")
        self.vitals["RAM"].configure(text=f"{r}%", text_color=self.accent if r < 85 else "red")
        self.vitals["BAT"].configure(text=b)

    def fire(self): # process input
        cmd = self.entry.get().strip()
        if not cmd: return # ignore empty
        self.add_log(f"> {cmd}") # log input
        self.entry.delete(0, 'end') # clear box
        if self.on_cmd: threading.Thread(target=self.on_cmd, args=(cmd,), daemon=True).start()

    def btn_act(self, c): # process buttons
        if self.on_cmd: threading.Thread(target=self.on_cmd, args=(c,), daemon=True).start()

    def set_mod(self, m): # switch brain
        import config # type: ignore
        config.OPENROUTER_MODEL = m # set global
        self.mlbl.configure(text=f"NODE: {m.split('/')[-1].upper()}")
        self.add_log(f"Neural Node -> {m}")

    def reload_cfg(self): # sync .env
        import config, importlib # type: ignore
        importlib.reload(config) # clear cache
        self.add_log("SYSTEM: Config reloaded from .env")

    def sync_status(self, sleep=False): # status toggle
        self.head.configure(text="STATUS: STANDBY" if sleep else "STATUS: ONLINE", text_color="#FFBB00" if sleep else self.accent)
        self.foot.configure(text="GHOST MODE" if sleep else "SYSTEM READY")

    def add_log(self, m): # push to console
        self.log_box.insert("end", f"[{datetime.now().strftime('%H:%M:%S')}] {m}\n")
        self.log_box.see("end") # scroll down

    def write(self, t): # terminal bridge
        if t.strip(): self.after(0, lambda: self.add_log(t.strip()))
    def flush(self): pass # terminal interface

if __name__ == "__main__": # local launching
    app = Nexusv7()
    sys.stdout = app # test redirect
    app.mainloop()
