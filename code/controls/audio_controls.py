import os
import pygame
import re

from tkinter import *
from tkinter import messagebox
from tkinter import ttk

from controls.file_handler import *
from controls.sort_functions import *

from window.window_components import WindowComponents

from common_data import *

class AudioControls:
    pygame.mixer.init()

    def play_audio(audio_file: str) -> None:
        audio_parts: list[str] = audio_file.split('\\')

        if len(audio_parts) == 0:
            messagebox.showerror("Empty Audio File", "No Audio File Provided")
            return 0

        if not AudioControls.valid_audio_file(audio_parts[-1]):
            messagebox.showerror("Audio File Error", "Something is Wrong with the Audio File, please ensure that the File Exists and is properly named, before trying again.\nThat or its the wrong file type, this can only play MP3's, MIDI's or WAV's.")
            return 0

        if len(audio_parts) == 1: audio_file = os.path.join(CommonData.audio_folder, audio_parts[-1])
        if not AudioControls.valid_audio_file(audio_file): audio_file = os.path.join(CommonData.audio_folder, audio_parts[-1])
        
        if not os.path.exists(audio_file):
            messagebox.showerror("Audio File Doesn't Exist", "Audio File Can't Be Played, It Doesn't Exist")
        else:
            pygame.mixer.music.load(audio_file)
            pygame.mixer.music.play(loops = 0)

    def valid_audio_file(audio_file: str) -> bool:
        valid_file_name: bool = not re.findall("[/*-+<>;'#@~,`¬!£$%^&*()=]", audio_file)
        valid_file_type: bool = audio_file.lower().endswith((".wav", ".mp3", ".midi"))

        return valid_file_name and valid_file_type
    
    def update_audio_file() -> None:
        audio_data: str = f"{CommonData.audio_list[0].audio_id},{CommonData.audio_list[0].audio_name},{CommonData.audio_list[0].audio_file}"

        for i in range(1, len(CommonData.audio_list)):
            audio_data += f"\n{CommonData.audio_list[i].audio_id},{CommonData.audio_list[i].audio_name},{CommonData.audio_list[i].audio_file}"

        write_file(CommonData.audio_file, audio_data)

    def select_audio() -> None:
        id_sort_audios(CommonData.audio_list)
        WindowComponents.current_edit_audio = CommonData.audio_list[WindowComponents.audios_listbox.curselection()[0]]
        AudioControls.load_audio_details()

    def create_audio() -> None:
        audio_file: str = WindowComponents.audio_file_entry.get()

        audio_parts: list[str] = audio_file.split('\\')

        if len(audio_parts) == 1: audio_file = os.path.join(CommonData.audio_folder, audio_parts[-1])
        if not AudioControls.valid_audio_file(audio_file): audio_file = os.path.join(CommonData.audio_folder, audio_parts[-1])

        if AudioControls.valid_audio("Create", audio_file):
            if not file_in_folder(CommonData.audio_folder, audio_parts[-1], ["mp3", "midi", "wav"]): relocate_file(audio_file, os.path.join(CommonData.audio_folder, audio_parts[-1]))

            CommonData.audio_list.append(Audio([AudioControls.generate_audio_id(), WindowComponents.audio_name_entry.get(), audio_parts[-1]], os.path.join(CommonData.audio_folder, audio_parts[-1])))

            AudioControls.update_audio_list()
            AudioControls.update_audio_file()
        else:
            messagebox.showerror("Error Creating Audio", "Something has gone wrong creating the Audio, please ensure all details are correct and try again")

    def update_audio() -> None:
        audio_file: str = WindowComponents.audio_file_entry.get()

        audio_parts: list[str] = audio_file.split('\\')

        if len(audio_parts) == 1: audio_file = os.path.join(CommonData.audio_folder, audio_parts[-1])
        if not AudioControls.valid_audio_file(audio_file): audio_file = os.path.join(CommonData.audio_folder, audio_parts[-1])

        if AudioControls.valid_audio("Update", audio_file):
            if not file_in_folder(CommonData.audio_folder, audio_parts[-1], ["mp3", "midi", "wav"]): relocate_file(audio_file, os.path.join(CommonData.audio_folder, audio_parts[-1]))

            WindowComponents.current_edit_audio.audio_name = WindowComponents.audio_name_entry.get()
            WindowComponents.current_edit_audio.audio_file = audio_parts[-1]
            WindowComponents.current_edit_audio.full_file = audio_file

            AudioControls.update_audio_list()
            AudioControls.update_audio_file()
        else: messagebox.showerror("Error Updating Audio", "Something has gone wrong updating the Audio, please ensure all details are correct and try again")

    def revert_audio() -> None:
        if WindowComponents.current_edit_audio != None: WindowComponents.load_audio_details()

    def load_audio_details() -> None:
        AudioControls.clear_edit_audios_page()

        WindowComponents.audio_name_entry.insert(0, WindowComponents.current_edit_audio.audio_name)
        WindowComponents.audio_file_entry.insert(0, WindowComponents.current_edit_audio.audio_file)

    def valid_audio(check_type: str, audio_file: str) -> bool:
        check_name: str = ""
        if check_type == "Update": check_name = WindowComponents.audio_name_entry.get()

        if not AudioControls.unique_audio_name(check_name): return False
        if not AudioControls.unique_audio_file(audio_file): return False
        return True
    
    def unique_audio_name(compare_name: str) -> bool:
        for audio in CommonData.audio_list:
            if compare_name == audio.audio_name and audio != WindowComponents.current_edit_audio:
                return False
        return True
    
    def unique_audio_file(compare_file: str) -> bool:
        for audio in CommonData.audio_list:
            if open(compare_file, "rb") == open(audio.full_file, "rb") and audio != WindowComponents.current_edit_audio:
                return False
        return True

    def generate_audio_id() -> str:
        if len(CommonData.audio_list) == 0: return "A0001"
        id_sort_audios(CommonData.audio_list)
        return f"A{str(int(CommonData.audio_list[-1].audio_id.replace("A", "")) + 1).rjust(4, "0")}"

    def update_audio_list() -> None:
        id_sort_audios(CommonData.audio_list)
        WindowComponents.audios_listbox.delete(0, END)

        for audio in CommonData.audio_list:
            WindowComponents.audios_listbox.insert('end', f"{audio.audio_id} - {audio.audio_name}")

    def preview_audio() -> None:
        AudioControls.play_audio(WindowComponents.audio_file_entry.get())

    def clear_audio() -> None:
        WindowComponents.current_edit_audio = None
        AudioControls.clear_edit_audios_page()
    
    def clear_edit_audios_page() -> None:
        WindowComponents.audio_name_entry.delete(0, len(WindowComponents.audio_name_entry.get()))
        WindowComponents.audio_file_entry.delete(0, len(WindowComponents.audio_file_entry.get()))
