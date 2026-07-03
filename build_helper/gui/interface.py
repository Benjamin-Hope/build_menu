import tkinter as tk
import os
from pathlib import Path


class BuildGUI(tk.Tk):
    def __init__(self, tool_root_path):
        super().__init__()
        self.title("Build GUI")
        self.geometry("400x300")
        self.tool_root_path = tool_root_path

        self.__create_widgets()
        self.__create_menu()

    def __create_menu(self):
        self.menu_bar = tk.Menu(self)
        self.config(menu=self.menu_bar)

    def __create_widgets(self):
        # ... existing widgets ...

        self.profile_listbox = tk.Listbox(
            self, selectmode=tk.SINGLE, height=10)
        self.profile_listbox.pack(pady=10, fill=tk.BOTH, expand=True)

        profiles = self.__load_profiles(
            Path(self.tool_root_path) / "build_profiles")

        for profile in profiles:
            self.profile_listbox.insert(tk.END, profile)

    def __load_profiles(self, profiles_path):
        profiles = [str(path.name.replace(".ini", ""))
                    for path in Path(profiles_path).glob("*.ini")]
        return profiles

    def get_selected_profile(self):
        selection = self.profile_listbox.curselection()
        if selection:
            return self.profile_listbox.get(selection[0])
        return None

    def fill_menu_items(self, label, cls_method):
        self.menu_bar.add_command(label=label, command=cls_method)

    def start_build(self):
        selection = self.profile_listbox.curselection()
        if selection:
            selected_profile = self.profile_listbox.get(selection[0])
            print(f"Selected profile: {selected_profile}")
        else:
            print("No profile selected")


if __name__ == "__main__":
    app = BuildGUI()
    app.mainloop()
