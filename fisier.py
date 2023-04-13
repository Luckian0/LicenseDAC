
from tkinter import *

def search_inside(asas, text_box):
    global search_toplevel
    search_toplevel = Toplevel(asas)
    search_toplevel.title('Find Text')
    search_toplevel.transient(asas)
    search_toplevel.resizable(False, False)
    Label(search_toplevel, text="Find All:").grid(row=0, column=0, sticky='e')
    search_entry_widget = Entry(search_toplevel, width=25)
    search_entry_widget.grid(row=0, column=1, padx=2, pady=2, sticky='we')
    search_entry_widget.focus_set()
    ignore_case_value = IntVar()
    Checkbutton(search_toplevel, text='Ignore Case', variable=ignore_case_value).grid(row=1, column=1, sticky='e', padx=2, pady=2)
    Button(search_toplevel, text="Find All", underline=0,
        command=lambda: search_output1(
            search_entry_widget.get(), ignore_case_value.get(),
            text_box, search_toplevel, search_entry_widget)
        ).grid(row=0, column=2, sticky='e' + 'w', padx=2, pady=2)
    def close_search_window():
        text_box.tag_remove('match', '1.0', END)
        search_toplevel.destroy()
    search_toplevel.protocol('WM_DELETE_WINDOW', close_search_window)
    search_toplevel.bind('<Escape>', lambda event:( search_toplevel.destroy(), text_box.tag_remove('match', '1.0', END)))
    search_entry_widget.bind('<Return>', lambda x: search_output1(search_entry_widget.get(), ignore_case_value.get(), text_box, search_toplevel, search_entry_widget))
    return "break"
def search_output1(needle,if_ignore_case, text_box, search_toplevel, search_box):
    text_box.tag_remove('match','1.0', END)
    matches_found=0
    if needle:
        start_pos = '1.0'
        while True:
            start_pos = text_box.search(needle,start_pos, nocase=if_ignore_case, stopindex=END)
            if not start_pos:
                break
            end_pos = '{} + {}c'. format(start_pos, len(needle))
            text_box.tag_add('match', start_pos, end_pos)
            matches_found +=1
            start_pos = end_pos
        text_box.tag_config('match', background='yellow', foreground='blue')
    search_box.focus_set()
    search_toplevel.title('{} matches found'.format(matches_found))
    
def find_box_delete():
    search_toplevel.destroy()