from tkinter import END, Menu, filedialog, messagebox
from tkinter.scrolledtext import ScrolledText
from deep_translator import GoogleTranslator
from idlelib.tooltip import Hovertip
from collections import Counter
from threading import Timer
from typing import Any
from datetime import datetime, timedelta
from fisier import *
import tkinter as tk
import webbrowser
import subprocess
import random
import shutil
from pathlib import Path
import time
import zipfile
import re
import os
from pygments.lexers import get_lexer_for_filename

# define variables

version_number = "v0.9"
license_selected = ''
wordlist_big = []
dirname: str | bytes | Any = os.path.dirname(__file__)
allPath: list[str] = []
main_folder = "C:/Users/" + os.getlogin() + "/Downloads/test"
my_license = []
button_list = []
focus_btn = []
focus_buttons_nr = []
license_list = []
info_license = []
all_license = []
files_w = []
lic_click = ''
main_dictionary = {"Files": []}
list_buttons = []
mit_dict = []
culori = 'blue'
other_license = []
buttons_nr = []
Unknown_line = []
other_btn_list = []
focus_other = []
focus_other_nr = []
other_nr = []
tag_line = ''
copyright_store = []
language_list = []
time_list = []


# Clear all

def clear_other():
    destroy_focus_buttons()
    destroy_other_focus()
    destroy_other()

def clear_all():
    global lic_click
    try:
        language_label['text'] = ''
        license_label['text'] = ''
        file_label['text'] = ''
        release_label['text'] = ''
        lic_click = ''
        listbox.delete(0, tk.END)
        text_dialog.delete("1.0", tk.END)
        destroy_buttons()
        allPath.clear()
        wordlist_big.clear()
        files_w.clear()
        list_buttons.clear()
        license_list.clear()
        dic_MIT2.clear()
        main_dictionary.clear()
        clear_other()
    except:
        pass


# For open the folder path

def browse_button():
    """Button will open a window for directory selection"""
    global folder_path
    clear_all()
    selected_directory = filedialog.askdirectory()
    folder_path.set(selected_directory)
    window.title('-> ' + version_number + ' <--> LicenseDAC <-----< ' + selected_directory.split('/')[-1] + ' >--')


# For open the Archive path

def browse_zip():
    global folder_path, select_zip
    shutil.rmtree(main_folder, ignore_errors=True, onerror=None)
    select_zip = filedialog.askopenfilename(initialdir="C:/Users/" + os.getlogin() + "/Downloads", title="Select file",
                                            filetypes=(("tar.gz, .zip", "*"), ("all files", "*.*")))
    folder_path.set(main_folder)
    window.title('-> ' + version_number + ' <--> LicenseDAC <-----< ' + select_zip.split('/')[-1] + ' >--')
    listbox.insert(tk.END, "                    !!!!!! Start unzipped !!!!!!")
    print(select_zip.split('/')[-1])
    dezarhivare()


########################################## Open specific file

def open_file():
    global file_current
    select_file2 = filedialog.askopenfilename(initialdir="C:/Users/" + os.getlogin() + "/Downloads/test",
                                              title="Select file", filetypes=(("*.*, *.*", "*"), ("all files", "*.*")))
    if len(select_file2) >= 1:
        text_dialog.delete("1.0", tk.END)
        license_label['text'] = ''
        file_label['text'] = 'file: '+select_file2
        text_file = open(select_file2, encoding='utf-8')
        stuff = text_file.read()
        text_dialog.insert(END, stuff)
        file_current = select_file2
        try:
            clear_other()
        except:
            pass


# Click on the files in lisbox

def on_text_click(file_current):
    global other_btn_list, linie , text_dialog
    other_btn_list = []
    linie = []
    clear_other()
    text_dialog.delete("1.0", tk.END)
    str_file = file_current
    for aa in license_list:
        if str_file in aa:
            linie = eval(str(aa.split(lic_click+', ')[1]))

    def open_text():
        try:
            text_file = open(str_file, encoding='ANSI')
        except:
            text_file = open(str_file, encoding='utf-8')
        stuff = text_file.read()
        text_dialog.insert(END, stuff)
    open_text()
    text_dialog.tag_configure('highlighted', background='yellow')
    for element in linie:
        el1 = str(1 + int(element)) + '.0'
        el2 = str(1 + int(element)) + '.end'
        text_dialog.tag_add('highlighted', el1, el2)
        focus_btn.append(el1)

    def focus_on_line(line):
        text_dialog.see(line)

    def def_focus():
        global focus_bt
        for i, item in enumerate(focus_btn):
            if i >= 17:
                x = 785
                y = (i - 17) * 30 + 80
            else:
                x = 745
                y = i * 30 + 80
            culori = str("#" + ''.join([random.choice('ABCDEF0123456789') for i in range(6)]))
            focus_bt = tk.Button(window, text='  '+str(i+1)+'  ', command=lambda line=item: focus_on_line(line), bg=culori)
            focus_bt.pack()
            focus_bt.place(x=x, y=y)
            focus_buttons_nr.append(focus_bt)

    def_focus()
    linie.clear()


# Destroy buttons

def destroy_focus_buttons():
    global focus_buttons_nr
    for btn in focus_buttons_nr:
        btn.destroy()
    focus_buttons_nr = []


def destroy_buttons():
    global buttons_nr
    for btn in buttons_nr:
        btn.destroy()
    buttons_nr = []


def destroy_other():
    global other_nr
    for btn in other_nr:
        btn.destroy()
    other_nr = []


def destroy_other_focus():
    global focus_other_nr
    for btn in focus_other_nr:
        btn.destroy()
    focus_other_nr = []


# Search for all the files that contain licenses.

def search_all_license():
    language_list = []
    time_list = []
    global allPath
    clear_all()
    listbox.insert(tk.END, "           !!!!!! Start looking for licenses !!!!!!")
    with open(os.path.join(dirname, "license_txt/license_txt.txt")) as f:
        for line in f:
            license_txt = line.strip().split('|||')
    license_path = folder_path.get()

    # Loop through all files and search for licenses, line by line.
    for (path, directories, files) in os.walk(license_path, topdown=True):
        for file in files:
            filepath = os.path.join(path, file)
            try:
                for a in license_txt:
                    with open(filepath, 'r', encoding='utf-8') as currentfile:
                        for lineNum, line in enumerate(currentfile, 1):
                            line = line.strip()
                            match = re.search(a, line, re.IGNORECASE)
                            if match:
                                if len(line) >= 2000:
                                    word_big = f"{filepath}"
                                    wordlist_big.append(word_big)
                                else:
                                    word = f"{filepath}"
                                    allPath.append(word)

                mod_time = Path(filepath).stat().st_mtime
                time_mod = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(mod_time)).split(' ')[0]
                date = datetime.strptime(time_mod, '%Y-%m-%d')
                current_date = datetime.now()
                if (current_date - date) > timedelta(days=2):
                    time_list.append(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(mod_time)).split(' ')[0])
                else:
                    pass
                lexer = str(get_lexer_for_filename(file)).split('.')[-1].split('Lexer')[0]
                language_list.append(lexer)

            except IOError as ex:
                words = f"."
            except UnicodeDecodeError as ex:
                words = f"."
            except:
                words = f"."

    # Defain release date
    time_list1 = list(set(time_list))
    dates = [datetime.strptime(date_str, '%Y-%m-%d').date() for date_str in time_list1]
    try:
        max_date = max(dates).strftime('%Y-%m-%d')
        release_label['text'] = f" Release date: {max_date}"
    except:
        release_label['text'] = f" Release date: N/A"

    programming_language_list = Counter(language_list)
    language_label['text'] = f" Programming language: {programming_language_list.most_common(1)[0][0]}"

    allPath = list(set(allPath))
    for a in allPath:
        main_dictionary[a] = {}

    license_Public_Domain()
    license_MIT()
    license_Apache()
    license_BSL()
    license_BSD()
    license_LGPL()
    license_AGPL()
    license_GPL()
    license_ISC()
    license_EPL()
    license_MPL()
    license_EULA()
    license_CDDL()
    license_Artistic()
    license_Elastic()
    license_Python()
    license_OpenSSL()
    license_CCA()
    license_CC0()
    license_SSPL()
    license_Unknown()

# Create the license buttons.

def all_buttons2():
    for i, item in enumerate(list_buttons):
        if i >= 12:
            x = 140
            y = (i - 12) * 30 + 290
        else:
            x = 10
            y = i * 30 + 290
        button = tk.Button(window, text=item, command=lambda text=item: on_button_click(text), bg='#6ce3e5')
        button.pack()
        button.place(x=x, y=y)
        buttons_nr.append(button)


# Fill the ListBox.

def files_buttons2():
    for item in files_w:
        listbox.insert(tk.END, item)
    files_w.clear()


# On license buttons click.

def on_button_click(text):
    global lic_click
    clear_other()
    file_label['text'] = ''
    license_list.clear()
    listbox.delete(0, tk.END)
    lic_click = text
    for key, value in dic_MIT2.items():
        if lic_click in value:
            line = dic_MIT2[key][lic_click]
            word = f"{str(key)}, {lic_click}, {line}"
            file = key
            files_w.append(file)
            license_list.append(word)
    license_label['text'] = f"License: {lic_click} in {len(files_w)} files"
    files_buttons2()


# Other license in file; buttons, focus and print.

def on_other_click(text):
    destroy_other_focus()
    focus_other_nr = []
    focus_other = []
    all_lines = v2_other[text]
    for element in all_lines:
        focus_other.append(element)
    print(focus_other)
    def focus_on_other(line):
        global tag_line
        try:
            text_dialog.tag_remove('blue', tag_line + '.0', tag_line + '.end')
        except:
            pass
        text_dialog.tag_add('blue', str(1 + int(line)) + '.0', str(1 + int(line)) + '.end')
        text_dialog.tag_config("blue", foreground="blue")
        text_dialog.see(str(1 + int(line)) + '.0')
        tag_line = str(1 + int(line))

    def other_focus():
        global focus_other_nr
        for i, item in enumerate(focus_other):
            if i >= 20:
                x = (i - 20)*31 + 825
                y = 535
            else:
                x = i * 30 + 825
                y = 505
            culori = str("#" + ''.join([random.choice('ABCDEF0123456789') for i in range(6)]))
            focus_other_bt = tk.Button(window, text=' '+str(i+1)+' ', command=lambda line=item: focus_on_other(line), bg=culori)
            focus_other_bt.pack()
            focus_other_bt.place(x=x, y=y)
            focus_other_nr.append(focus_other_bt)
    other_focus()

# Build other license buttons.
def btn_others():
    other_btn_list.sort(key=len)
    for i, item in enumerate(other_btn_list):
        other_button = tk.Button(window, text=item, command=lambda text=item: on_other_click(text), bg='#6ce3e5')
        other_button.pack()
        other_button.place(x=i*45 + 825, y=475)
        other_nr.append(other_button)

# Check for other license in file.
def def_other_license(other_license):
    global v2_other
    v2_other = eval(str(other_license[0]))
    for key in v2_other:
        other_btn_list.append(key)
    btn_others()


# When click on one element in the list box

def on_item_doubleclick(event):
    global file_current
    other_license.clear()
    widget = event.widget
    selection = widget.curselection()
    value = widget.get(selection[0])
    focus_btn.clear()
    print(f"You double-clicked on {value}")
    file_current = value
    new_dict = {key: val for key, val in dic_MIT2[value].items() if key != lic_click}
    other_license.append(new_dict)
    print('mai exista si', other_license)
    if lic_click == 'Copyright':
        destroy_other_focus()
        destroy_other()
        destroy_focus_buttons()
        text_dialog.delete("1.0", tk.END)
        def open_text():
            try:
                text_file = open(file_current, encoding='ANSI')
            except:
                text_file = open(file_current, encoding='utf-8')
            stuff = text_file.read()
            text_dialog.insert(END, stuff)
        open_text()
        for element in copyright_store:
            if file_current in element:

                text_dialog.tag_configure('highlighted', background='yellow')
                text_dialog.tag_add('highlighted', f"{element.split('  ')[1]}.0", f"{element.split('  ')[1]}.end")
                text_dialog.see(f"{element.split('  ')[1]}.0")

    else:
        on_text_click(file_current)
        def_other_license(other_license)
        file_label['text'] = 'file: '+str(value).split("/")[-1]
    


def probe_v2(license1, key, exceptions, ignore_case):
    listbox.delete(0, tk.END)
    listbox.insert(tk.END, "           !!!!!! Check for " + license1 + " licenses !!!!!!")
    global main_dictionary, dic_MIT2
    for file_location in allPath:
        if os.path.exists(file_location):
            def encoding():
                for line_number, line in enumerate(file):
                    # if any(x in line for x in key) and (exceptions is None or not any(ex in line for ex in exceptions)):
                    if any(x in line for x in key):
                        if license1 == 'Unknown':
                            if line in Unknown_line:
                                pass
                            else:
                                if any(e in line for e in exceptions):
                                    pass
                                else:
                                    if license1 not in list_buttons:
                                        list_buttons.append(license1)
                                    if license1 not in main_dictionary[file_location]:
                                        main_dictionary[file_location][license1] = []
                                        main_dictionary[file_location][license1].append(line_number)
                                    else:
                                        main_dictionary[file_location][license1].append(line_number)
                        else:
                            if any(e in line for e in exceptions):
                                pass
                            else:
                                if license1 not in list_buttons:
                                    list_buttons.append(license1)
                                if license1 not in main_dictionary[file_location]:
                                    main_dictionary[file_location][license1] = []
                                    main_dictionary[file_location][license1].append(line_number)
                                else:
                                    main_dictionary[file_location][license1].append(line_number)
            try:
                with open(file_location, 'r', encoding='ANSI') as file:
                    encoding()
            except:
                with open(file_location, 'r', encoding='utf-8') as file:
                    encoding()

    dic_MIT2 = {k: v for k, v in main_dictionary.items() if v}
    list_buttons.sort(key=len)
    return dic_MIT2


dirname = os.path.dirname(__file__)


def license_MIT():
    with open(os.path.join(dirname, "license_txt/MIT_txt.txt")) as f:
        key = f.read().strip().split('|||')
    with open(os.path.join(dirname, "exceptions/MIT.txt")) as f:
        for line in f:
            exceptions = line.strip().split('|||')
    license1 = "MIT"
    ignore_case = False
    probe_v2(license1, key, exceptions, ignore_case)


def license_Apache():
    with open(os.path.join(dirname, "license_txt/Apache_txt.txt")) as f:
        for line in f:
            key = line.strip().split('|||')
    with open (os.path.join(dirname, "exceptions/Apache.txt")) as f:
        for line in f:
            exceptions = line.strip().split('|||')
    license1 = "Apache"
    ignore_case = True
    probe_v2(license1, key, exceptions, ignore_case)


def license_BSL():
    with open(os.path.join(dirname, "exceptions/Boost_Software_License.txt")) as f:
        for line in f:
            exceptions = line.strip().split('|||')
    with open (os.path.join(dirname, "license_txt/BSL_txt.txt")) as f:
        for line in f:
            key = line.strip().split('|||')
    license1 = "Boost_Software_License"
    ignore_case = False
    probe_v2(license1, key, exceptions, ignore_case)


def license_BSD():
    with open(os.path.join(dirname, "exceptions/BSD.txt")) as f:
        for line in f:
            exceptions = line.strip().split('|||')
    with open(os.path.join(dirname, "license_txt/BSD_txt.txt")) as f:
        for line in f:
            key = line.strip().split('|||')
    license1 = "BSD"
    ignore_case = False
    probe_v2(license1, key, exceptions, ignore_case)


def license_LGPL():
    with open(os.path.join(dirname, "exceptions/LGPL.txt")) as f:
        for line in f:
            exceptions = line.strip().split('|||')
    with open(os.path.join(dirname, "license_txt/LGPL_txt.txt")) as f:
        for line in f:
            key = line.strip().split('|||')
    license1 = "LGPL"
    ignore_case = True
    probe_v2(license1, key, exceptions, ignore_case)


def license_AGPL():
    with open(os.path.join(dirname, "exceptions/AGPL.txt")) as f:
        for line in f:
            exceptions = line.strip().split('|||')
    with open(os.path.join(dirname, "license_txt/AGPL_txt.txt")) as f:
        for line in f:
            key = line.strip().split('|||')
    license1 = "AGPL"
    ignore_case = True
    probe_v2(license1, key, exceptions, ignore_case)


def license_GPL():
    with open(os.path.join(dirname, "exceptions/GPL.txt")) as f:
        for line in f:
            exceptions = line.strip().split('|||')
    with open(os.path.join(dirname, "license_txt/GPL_txt.txt")) as f:
        for line in f:
            key = line.strip().split('|||')
    license1 = "GPL"
    ignore_case = True
    probe_v2(license1, key, exceptions, ignore_case)


def license_ISC():
    with open(os.path.join(dirname, "exceptions/ISC.txt")) as f:
        for line in f:
            exceptions = line.strip().split('|||')
    with open(os.path.join(dirname, "license_txt/ISC_txt.txt")) as f:
        for line in f:
            key = line.strip().split('|||')
    license1 = "ISC"
    ignore_case = False
    probe_v2(license1, key, exceptions, ignore_case)


def license_EPL():
    with open(os.path.join(dirname, "exceptions/EPL.txt")) as f:
        for line in f:
            exceptions = line.strip().split('|||')
    with open(os.path.join(dirname, "license_txt/EPL_txt.txt")) as f:
        for line in f:
            key = line.strip().split('|||')
    license1 = "EPL"
    ignore_case = True
    probe_v2(license1, key, exceptions, ignore_case)


def license_Public_Domain():
    with open(os.path.join(dirname, "exceptions/Public_Domain.txt")) as f:
        for line in f:
            exceptions = line.strip().split('|||')
    with open(os.path.join(dirname, "license_txt/Public_Domain_txt.txt")) as f:
        for line in f:
            key = line.strip().split('|||')
    license1 = "Public_Domain"
    ignore_case = True
    probe_v2(license1, key, exceptions, ignore_case)


def license_OpenSSL():
    with open(os.path.join(dirname, "exceptions/OpenSSL.txt")) as f:
        for line in f:
            exceptions = line.strip().split('|||')
    with open(os.path.join(dirname, "license_txt/OpenSSL_txt.txt")) as f:
        for line in f:
            key = line.strip().split('|||')
    license1 = "OpenSSL"
    ignore_case = True
    probe_v2(license1, key, exceptions, ignore_case)


def license_CCA():
    with open(os.path.join(dirname, "exceptions/CCA.txt")) as f:
        for line in f:
            exceptions = line.strip().split('|||')
    with open(os.path.join(dirname, "license_txt/CCA_txt.txt")) as f:
        for line in f:
            key = line.strip().split('|||')
    license1 = "CCA"
    ignore_case = True
    probe_v2(license1, key, exceptions, ignore_case)


def license_CC0():
    with open(os.path.join(dirname, "exceptions/CC0.txt")) as f:
        for line in f:
            exceptions = line.strip().split('|||')
    with open(os.path.join(dirname, "license_txt/CC0_txt.txt")) as f:
        for line in f:
            key = line.strip().split('|||')
    license1 = "CC0"
    ignore_case = True
    probe_v2(license1, key, exceptions, ignore_case)


def license_Python():
    with open(os.path.join(dirname, "exceptions/Python.txt")) as f:
        for line in f:
            exceptions = line.strip().split('|||')
    with open(os.path.join(dirname, "license_txt/Python_txt.txt")) as f:
        for line in f:
            key = line.strip().split('|||')
    license1 = "Python"
    ignore_case = True
    probe_v2(license1, key, exceptions, ignore_case)


def license_SSPL():
    with open(os.path.join(dirname, "exceptions/SSPL.txt")) as f:
        for line in f:
            exceptions = line.strip().split('|||')
    with open(os.path.join(dirname, "license_txt/SSPL_txt.txt")) as f:
        for line in f:
            key = line.strip().split('|||')
    license1 = "SSPL"
    ignore_case = True
    probe_v2(license1, key, exceptions, ignore_case)


def license_Elastic():
    with open(os.path.join(dirname, "exceptions/Elastic.txt")) as f:
        for line in f:
            exceptions = line.strip().split('|||')
    with open(os.path.join(dirname, "license_txt/Elastic_txt.txt")) as f:
        for line in f:
            key = line.strip().split('|||')
    license1 = "Elastic"
    ignore_case = True
    probe_v2(license1, key, exceptions, ignore_case)


def license_EULA():
    with open(os.path.join(dirname, "exceptions/EULA.txt")) as f:
        for line in f:
            exceptions = line.strip().split('|||')
    with open(os.path.join(dirname, "license_txt/EULA_txt.txt")) as f:
        for line in f:
            key = line.strip().split('|||')
    license1 = "EULA"
    ignore_case = True
    probe_v2(license1, key, exceptions, ignore_case)


def license_Artistic():
    with open(os.path.join(dirname, "exceptions/Artistic.txt")) as f:
        for line in f:
            exceptions = line.strip().split('|||')
    with open(os.path.join(dirname, "license_txt/Artistic_txt.txt")) as f:
        for line in f:
            key = line.strip().split('|||')
    license1 = "Artistic"
    ignore_case = True
    probe_v2(license1, key, exceptions, ignore_case)


def license_MPL():
    with open(os.path.join(dirname, "exceptions/MPL.txt")) as f:
        for line in f:
            exceptions = line.strip().split('|||')
    with open(os.path.join(dirname, "license_txt/MPL_txt.txt")) as f:
        for line in f:
            key = line.strip().split('|||')
    license1 = "MPL"
    ignore_case = False
    probe_v2(license1, key, exceptions, ignore_case)


def license_CDDL():
    with open(os.path.join(dirname, "exceptions/CDDL.txt")) as f:
        for line in f:
            exceptions = line.strip().split('|||')
    with open(os.path.join(dirname, "license_txt/CDDL_txt.txt")) as f:
        for line in f:
            key = line.strip().split('|||')
    license1 = "CDDL"
    ignore_case = False
    probe_v2(license1, key, exceptions, ignore_case)


def license_Unknown():
    global Unknown_line
    with open(os.path.join(dirname, "exceptions/Unknown.txt")) as f:
        for line in f:
            exceptions = line.strip().split('|||')
    with open(os.path.join(dirname, "exceptions/Unknown_line.txt")) as f:
        for line in f:
            Unknown_line = line.strip().split('|||')
    with open(os.path.join(dirname, "license_txt/Unknown_txt.txt")) as f:
        for line in f:
            key = line.strip().split('|||')
    license1 = "Unknown"
    ignore_case = True
    probe_v2(license1, key, exceptions, ignore_case)
    all_buttons2()
    listbox.delete(0, tk.END)
    listbox.insert(tk.END, "                !!!!!!         DONE          !!!!!!")
    listbox.insert(tk.END,f"                !!!!!!  Found: {len(allPath)} files  !!!!!! ")


# Copyright

def copyright_check():
    listbox.delete(0, tk.END)
    global lic_click, copyright_store
    copy = ['Copyright', '©']
    copyright_listbox = []
    copyright_store = []
    lic_click = 'Copyright'
    with open(os.path.join(dirname, "exceptions/Copyright.txt")) as f:
        for line in f:
            copyright_exception = line.strip().split('|||')
    for file_location in allPath:
        if os.path.exists(file_location):
            def encoding():
                for line_number, line in enumerate(file):
                    if any(x in line for x in copy):
                        if any(e in line for e in copyright_exception):
                            pass
                        else:
                            if str(file_location).count('\\') > 3:
                                pass
                            else:
                                copyright_store.append(f"{file_location}  {line_number + 1}")
            try:
                with open(file_location, 'r', encoding='ANSI') as file:
                    encoding()
            except:
                with open(file_location, 'r', encoding='utf-8') as file:
                    encoding()
    for element in copyright_store:
        listbox.insert(tk.END, element.split('  ')[0])
    license_label['text'] = 'License: '+lic_click
    print(copyright_listbox)


###################### manually_check2
def clear_page():
    text_dialog.delete("1.0", tk.END)

def print_to_textbox(wordlist):
    for lines in wordlist:
        text_dialog.insert("end", "\n"+lines)
    if len(wordlist) == 0:
        text_dialog.insert("1.0", "\n                !!!!!! Nothing To Display !!!!!!")
        window.bell()

def manually_check():
    global lic_click
    lic_click = ''
    file_label['text'] = ''
    license_label['text'] = ''
    manuallyPath = folder_path.get()
    manuallySearch = manually_entry.get()
    listbox.delete(0, tk.END)
    clear_page()
    if var1.get() == 1:
        IGNOREWORDCASE = True
    else:
        IGNOREWORDCASE = False
    wordlist = []

    for (path, directories, files) in os.walk(manuallyPath, topdown=True):
        for file in files:
            filepath = os.path.join(path, file)
            try:
                with open(filepath, 'r', encoding='utf-8') as currentfile:
                    for lineNum, line in enumerate(currentfile, 1):
                        line = line.strip()
                        match = re.search(manuallySearch, line, re.IGNORECASE) if IGNOREWORDCASE else re.search(
                            manuallySearch, line)
                        if match:
                            word = f" ----> {file},  {lineNum} in {line}"
                            wordlist.append(word)
            except IOError as ex:
                words = f"."
            except UnicodeDecodeError as ex:
                words = f"."
            except:
                words = f"."
    print_to_textbox(wordlist)


# unZip

def dezarhivare():
    try:
        dezarhivare3()
    except:
        listbox.insert(tk.END, "            !!!!!! ERROR, please unzip manually !!!!!!")

def dezarhivare3():
    shutil.unpack_archive(select_zip, main_folder)
    listbox.insert(tk.END, "                !!!!!! finished unzipped.... !!!!!!")
    search_files2()



def appreciate():
    if messagebox.askyesno("Donate", "If you want to support this project press 'Yes'"):
        webbrowser.open('https://www.paypal.com/paypalme/FlorinelBejinaru?country.x=RO&locale.x=en_US')



def search_files2():
    after_time = Timer(0.1, search_all_license)
    after_time.start() 


# Persistent Curations

def add_text_exception():
    if text_dialog.tag_ranges("sel"):
        exception_files = open(os.path.join(dirname, "exceptions/" + lic_click + ".txt"), "a")
        exception_files.write("|||")
        exception_files.write(text_dialog.selection_get())
        curations.destroy()
    else:
        if messagebox.askokcancel('Error', 'You have deselected the text. Please try again.'):
            curations.destroy()


def add_text_exception_lines():
    if text_dialog.tag_ranges("sel"):
        exception_files = open(os.path.join(dirname, "exceptions/" + lic_click + "_line.txt"), "a")
        exception_files.write("|||")
        exception_files.write(text_dialog.selection_get())
        curations.destroy()
    else:
        if messagebox.askokcancel('Error', 'You have deselected the text. Please try again.'):
            curations.destroy()


def persistent_curations():
    if len(lic_click) == 0:
        messagebox.askokcancel("Error", "You have to be in a license tab")
    else:
        if text_dialog.tag_ranges("sel"):
            if len(text_dialog.selection_get()) <= 3:
                messagebox.askokcancel("Error", "You have to select min. 4 characters")
            else:
                global curations
                curations = Toplevel(window)
                curations.title("Persistent Curations")
                curations.geometry("580x100")

                def confirm_btn_word():
                    confirm_pc_button = tk.Button(curations, text=" SURE? ", bg='#807020', fg='white',
                                                  command=add_text_exception)
                    confirm_pc_button.pack()
                    confirm_pc_button.place(x=190, y=60)
                    ok_word_button.destroy()
                    try:
                        ok_line_button.destroy()
                    except:
                        pass

                def confirm_btn_line():
                    confirm_pc_button = tk.Button(curations, text=" SURE? ", bg='#807020', fg='white',
                                                  command=add_text_exception_lines)
                    confirm_pc_button.pack()
                    confirm_pc_button.place(x=190, y=60)
                    ok_word_button.destroy()
                    ok_line_button.destroy()

                text_label = Label(curations,
                                   text="If this phrase (or word) appears in a line where the license is found will be ignored in the future")
                text_label.pack()
                text_label.place(x=30, y=3)
                ok_word_button = tk.Button(curations, text=" Word ", bg='#807020', fg='white', command=confirm_btn_word)
                ok_word_button.pack()
                ok_word_button.place(x=160, y=60)
                if lic_click == 'Unknown':
                    ok_line_button = tk.Button(curations, text=" Line ", bg='#807020', fg='white',
                                               command=confirm_btn_line)
                    ok_line_button.pack()
                    ok_line_button.place(x=260, y=60)
                else:
                    pass
                cancel_pc_button = tk.Button(curations, text="Cancel", bg='#800020', fg='white',
                                             command=curations.destroy)
                cancel_pc_button.pack()
                cancel_pc_button.place(x=370, y=60)
                text_selected = text_dialog.selection_get()
                text_curations = Label(curations, text=text_selected, bg="#D3D3D3", width=40)
                text_curations.pack()
                text_curations.place(x=220, y=25)
                license_curations = Label(curations, text='', bg='white')
                license_curations.pack()
                license_curations.place(x=80, y=25)
                license_curations['text'] = lic_click
        else:
            messagebox.askokcancel('Error', 'You have to select the text first')

#exit

def exit_button():
    if messagebox.askokcancel("Quit", "Are you sure?"):
        window.destroy()

        
# Open other apps
def check_license_curations():
    if len(lic_click) == 0:
        messagebox.askokcancel("Error", "You have to be in a license tab")
    else:
        file_check = dirname + "/exceptions/" + lic_click + ".txt"
        print(file_check)

        subprocess.run(["notepad", file_check])

def open_url():
    webbrowser.open(text_dialog.selection_get())

def open_notepad():
    subprocess.run(["notepad", file_current])

def open_readme():
    global file_current
    text_dialog.delete("1.0", tk.END)
    language_label['text'] = ''
    license_label['text'] = ''
    file_label['text'] = 'README.md'
    text_file = open( dirname + "\README.md", encoding='utf-8')
    stuff = text_file.read()
    text_dialog.insert(END, stuff)
    file_current = dirname + "\README.md"
    try:
        destroy_focus_buttons()
        destroy_other()
        destroy_other_focus()
    except:
        pass

def google_search():
    if text_dialog.tag_ranges('sel'):
        text_get = text_dialog.selection_get()
        text_split = text_get.replace(' ', '+')
        webbrowser.open("https://www.google.com/search?q=" + text_split + "&start0=")
    else:
        messagebox.askokcancel("Error", 'You have to select the text first')


# Translate 
option_language = ['en', 'ro', 'sv', 'ja', 'fr']
def translate_text():
    if text_dialog.tag_ranges("sel"):
        selection_start = text_dialog.index('sel.first')
        selection_end = text_dialog.index('sel.last')
        to_translate = text_dialog.selection_get()
        translated = GoogleTranslator(source='auto', target=var_language.get()).translate(to_translate)
        text_dialog.delete(selection_start, selection_end)
        text_dialog.insert(selection_start, translated)
        text_dialog.tag_add('green', selection_start, f"{selection_start}+{len(translated)}c")
        text_dialog.tag_config("green", foreground="green")
    else:
        messagebox.showinfo("Translate", "you have to select the text first")


# tKinter script

window = tk.Tk()
window.geometry("1760x650")
window.title('-> ' + version_number + ' <--> LicenseDAC <-------------------------->')

# Button to select directory.
select_directory = tk.Button(window, text="Select Directory", bg='#800020', fg='white', border=0, command=browse_button)
select_directory.pack()
myTip = Hovertip(select_directory, 'Choose your package. Must be unarchived')

# Button to select archive file.
select_zip = tk.Button(window, text="Select zip  ", bg='#800020', fg='white', border=0, command=browse_zip)
select_zip.pack()
myTip = Hovertip(select_zip, 'Choose your zip file')

# Button to check the Copyright.
copyright_bt = tk.Button(window, text="Copyright", bg='#800020', fg='white', border=0, command=copyright_check)
copyright_bt.pack()
myTip = Hovertip(copyright_bt, 'Check for Copyright')

# Label to store chosen directory.
folder_path = tk.StringVar()
directory_label = tk.Label(window, textvariable=folder_path, bg="#D3D3D3", width=100)
directory_label.pack()

# Button to run main script.
go_button = tk.Button(window, text="License   search", bg='#800020', fg='white', border=0, command=search_files2)
go_button.pack()
myTip = Hovertip(go_button, 'Search on the selected folder')

# Entry to type search string.
manually_entry = tk.Entry(window, width=20)
manually_entry.pack()

# Button to open the donation link.
thanks_button = tk.Button(window, text = "Thanks!!", bg='#800020', fg='white', border=0, command=appreciate)
thanks_button.pack()
myTip = Hovertip(thanks_button, 'Support this project')

# Check button to turn ignore case on/off.
var1 = tk.IntVar()
stringCase_select = tk.Checkbutton(window, text='Ignore Case', variable=var1, onvalue=1, offvalue=0)
stringCase_select.pack()

# Label for Copyright
copyright_my = tk.Message(window, text="@copyright 2022 by Florinel Bejinaru!", relief=RAISED, width=220)
copyright_my.pack()

# Button to check the files
open_a_file = tk.Button(window, text="Open file  ", bg='#800020', fg='white', border=0, command=open_file)
open_a_file.pack()
myTip = Hovertip(open_a_file, 'Open a specific file')

# Button to manually check
manually_button = tk.Button(window, text = "Check for:", bg='#800020', fg='white', border=0, command=manually_check)
manually_button.pack()
myTip = Hovertip(manually_button, 'Check for a specific string')

# Text Dialog
text_dialog = ScrolledText(window, width=105, borderwidth=2, relief="sunken", padx=20)
text_dialog.pack(side="left")
text_dialog.place(x=825, y=80)

# Label Programming Language
release_label = tk.Label(window, text="")
release_label.pack()

# Label Programming Language
language_label = tk.Label(window, text="")
language_label.pack()

# Label license
license_label = tk.Label(window, text="")
license_label.pack()

# Label file
file_label = tk.Label(window, text="")
file_label.pack()

# Help button
img = tk.PhotoImage( file= dirname + "\img\help-icon.png")
help_button = tk.Button(window, image=img, width=25, height=25, border=0, command=open_readme)
myTip = Hovertip(help_button, 'Open README file')
help_button.pack()

# language
var_language = tk.StringVar(window)
var_language.set(option_language[0])
set_language = tk.OptionMenu(window, var_language, *option_language)
set_language.config(width=3, font=('Helvetica', 8), border=1.5)
myTip = Hovertip(set_language, 'Translate language')
set_language.pack()

scrollbar = tk.Scrollbar(window)
listbox = tk.Listbox(window, width=117, yscrollcommand=scrollbar.set)
listbox.bind("<Double-Button-1>", on_item_doubleclick)
scrollbar.config(command=listbox.yview)
listbox.config(yscrollcommand=scrollbar.set)
scrollbar.pack()
listbox.pack(side=tk.LEFT)

listbox.place(x=20, y=120)
scrollbar.place(x=725, y=120)
directory_label.place(x=20, y=95)
select_directory.place(x=110, y=30)
thanks_button.place(x=780, y=590)
go_button.place(x=110, y=60)
stringCase_select.place(x=490, y=29)
copyright_my.place(x=700, y=620)
manually_entry.place(x=370, y=33)
manually_button.place(x=300, y=30)
select_zip.place(x=20, y=30)
open_a_file.place(x=20, y=60)
language_label.place(x=843, y=30)
release_label.place(x=1050, y=30)
license_label.place(x=1253, y=30)
file_label.place(x=843, y=50)
set_language.place(x=370, y=56)
copyright_bt.place(x=300, y=60)
help_button.place(x=1690, y=10)


# Right Click Menu
def my_popup(ef):
    my_menu.tk_popup(ef.x_root, ef.y_root)

my_menu = Menu(window, tearoff=False, fg='#800020')
text_dialog.bind('<Button-3>', my_popup)
curationmenu = Menu(my_menu, tearoff=False)
curationmenu.add_command(label="Add", command=persistent_curations)
curationmenu.add_command(label="Check", command=check_license_curations)

my_menu.add_command(label=' Open URL', command=open_url)
my_menu.add_command(label='Translate', command=translate_text)
my_menu.add_cascade(label='Correction', menu=curationmenu)
my_menu.add_command(label='   Find  ', command=(lambda: search_inside(window, text_dialog)))
my_menu.add_command(label='  Search ', command=google_search)
my_menu.add_command(label='Open file', command=open_notepad)
my_menu.add_command(label='  Clear  ', command=(lambda:text_dialog.delete("1.0", tk.END)))
window.bind_class('Text', '<Control-f>', lambda event: search_inside(window, text_dialog))
manually_entry.bind('<Return>', lambda x: manually_check())
window.protocol('WM_DELETE_WINDOW', exit_button)

###################################

for widget in window.winfo_children():
    if isinstance(widget, tk.Toplevel):
        widget.destroy()


### CLA https://cla-assistant.io/Luckian0/LicenseDAC


window.mainloop()
