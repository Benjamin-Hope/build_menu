import tkinter as tk
from pathlib import Path
from tkinter import ttk


class BuildGUI(tk.Tk):
    def __init__(self, tool_root_path):
        super().__init__()
        self.title("Build GUI")
        self.geometry("400x300")
        self.tool_root_path = tool_root_path

        self.__create_widgets()
        self.__create_menu()

        self.process_pool = []
        self.status = []

    def __create_menu(self):
        self.menu_bar = tk.Menu(self)
        self.config(menu=self.menu_bar)

    def __create_widgets(self):
        self.profile_table = ttk.Treeview(
            self,
            columns=("profile", "status"),
            show="headings",
            height=10
        )
        self.profile_table.heading("profile", text="Profile")
        self.profile_table.heading("status", text="Status")
        self.profile_table.column("profile", width=230, anchor="w")
        self.profile_table.column("status", width=90, anchor="center")
        self.profile_table.pack(pady=10, fill=tk.BOTH, expand=True)

        self.profile_rows = {}   # profile -> row_id
        self.process_rows = {}   # process -> row_id

        profiles = self.__load_profiles(
            Path(self.tool_root_path) / "build_profiles")

        for profile in profiles:
            row_id = self.profile_table.insert(
                "", tk.END, values=(profile, "Idle"))
            self.profile_rows[profile] = row_id

    def __load_profiles(self, profiles_path):
        profiles = [str(path.name.replace(".ini", ""))
                    for path in Path(profiles_path).glob("*.ini")]
        return profiles

    def get_selected_profile(self):
        selection = self.profile_table.selection()

        if not selection:
            return None

        return self.profile_table.item(selection[0], "values")[0]

    def fill_menu_items(self, label, cls_method):
        self.menu_bar.add_command(label=label, command=cls_method)

    def start_build(self):
        selection = self.profile_listbox.curselection()
        if selection:
            selected_profile = self.profile_listbox.get(selection[0])
            print(f"Selected profile: {selected_profile}")
        else:
            print("No profile selected")

    def register_process(self, profile, process):
        self.process_pool.append(process)
        row_id = self.profile_rows[profile]
        self.process_rows[process] = row_id
        self.profile_table.set(row_id, "status", "Starting")

    def check_process_output(self):
        for process in self.process_pool:
            row_id = self.process_rows[process]
            if process.poll() is None:
                self.profile_table.set(row_id, "status", "Running")
            else:
                self.profile_table.set(
                    row_id,
                    "status",
                    "Failed" if process.returncode != 0 else "Finished"
                )

        if self.process_pool:
            self.after(100, self.check_process_output)


if __name__ == "__main__":
    app = BuildGUI()
    app.mainloop()
