import customtkinter as ctk

class VariableRow(ctk.CTkFrame):
    """
    Rappresenta una singola riga nell'interfaccia per una variabile.
    """
    def __init__(self, master, var_data, on_modify, on_plot_toggle, is_plotted=False, **kwargs):
        super().__init__(master, **kwargs)
        self.var_data = var_data
        self.on_modify = on_modify
        self.on_plot_toggle = on_plot_toggle
        self.plot_cb_visible = False # Traccia se la checkbox è visualizzata
        
        # Etichetta Nome: anchor="w" allinea il testo a sinistra (West)
        self.name_label = ctk.CTkLabel(self, text=var_data['name'], width=300, anchor="w", 
                                      font=ctk.CTkFont(weight="bold" if var_data['step_type'] == '0' else "normal"))
        self.name_label.pack(side="left", padx=10, pady=1)
        
        # Etichetta Valore: anchor="e" allinea il testo a dastra (East)
        self.value_label = ctk.CTkLabel(self, text="--", width=200, anchor="e")
        self.value_label.pack(side="left", padx=10, pady=1)
        
        # Se la variabile è modificabile (step_type '1' o '2'), aggiunge i pulsanti di controllo
        if var_data['step_type'] in ['1', '2']:
            self.min_btn = ctk.CTkButton(self, text="-", width=30, command=lambda: self.on_modify(var_data['index'], '-'))
            self.min_btn.pack(side="right", padx=2)
            
            self.plus_btn = ctk.CTkButton(self, text="+", width=30, command=lambda: self.on_modify(var_data['index'], '+'))
            self.plus_btn.pack(side="right", padx=2)
            
            self.dmin_btn = ctk.CTkButton(self, text="--", width=30, command=lambda: self.on_modify(var_data['index'], '/'))
            self.dmin_btn.pack(side="right", padx=2)
            
            self.dplus_btn = ctk.CTkButton(self, text="++", width=30, command=lambda: self.on_modify(var_data['index'], '*'))
            self.dplus_btn.pack(side="right", padx=2)

        # Checkbox per il plotting
        self.plot_cb = ctk.CTkCheckBox(self, text="Plot", text_color="#aaaaaa", border_width=1,width=10, height=10, corner_radius=5, fg_color="#40A040", hover_color="#308030",
                                      command=lambda: self.on_plot_toggle(var_data['index'], self.plot_cb.get()))
        
        if is_plotted or var_data['step_type'] in ['1', '2']:
            if is_plotted:
                self.plot_cb.select()
            self._show_plot_checkbox()

    def _show_plot_checkbox(self):
        """Rende visibile la checkbox del grafico se non lo è già."""
        if not self.plot_cb_visible:
            self.plot_cb.pack(side="right", padx=10)
            self.plot_cb_visible = True

    def update_value(self, new_value):
        """Aggiorna il testo visualizzato nell'etichetta del valore."""
        try:
            if self.winfo_exists():
                self.value_label.configure(text=new_value)
                
                if not self.plot_cb_visible and new_value.strip() and new_value != "--":
                    try:
                        clean_val = "".join(c for c in new_value if c.isdigit() or c in '.-')
                        if clean_val:
                            float(clean_val)
                            self._show_plot_checkbox()
                    except:
                        pass
        except:
            pass
