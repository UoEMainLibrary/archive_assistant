import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk

from PIL import ImageTk, Image
import os
import shutil
import getpass
import platform
import json
import datetime

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.grid_columnconfigure(0, weight=1)
        self.input_dir = ''
        self.output_dir = ''
        self.metadata = []
        self.non_empties = []
        self.create_widgets()

    def create_widgets(self):
        row_count = 0
        main_label_width = 18
        main_label_font = ('Arial', 18)
        main_input_font = ('Arial', 16)
        y_pad = 8

        tk.Label(text='Package title:', width=main_label_width, font=main_label_font).grid(row=row_count, column=0, padx=(10, 0), pady=y_pad)
        package_title = tk.Entry(borderwidth=1, relief=tk.RIDGE, width=40, font=('Arial', 18), validate="focusout", validatecommand=lambda : self._check_empty(package_title))
        package_title.grid(row=row_count, column=1, padx=(0, 10), pady=y_pad, columnspan=2)
        self.metadata.append(('dc.title', package_title))
        #self.non_empties.append(package_title)

        row_count += 1

        tk.Label(text='Date:', width=main_label_width, font=main_label_font).grid(row=row_count, column=0, padx=(10, 0), pady=y_pad, sticky=tk.E)
        package_date = tk.Entry(borderwidth=1, relief=tk.RIDGE, width=10, font=main_input_font, validate="focusout", validatecommand=lambda : self._check_empty(package_date))
        package_date.grid(row=row_count, column=1, padx=(5, 5), pady=y_pad, sticky=tk.W)
        tk.Label(text='(DD/MM/YYYY)', width=22, font=('Arial', 12)).grid(row=row_count, column=2, padx=(0, 10), pady=y_pad, sticky=tk.W)
        self.metadata.append(('dc.date.issued', package_date))

        row_count += 1

        tk.Label(text='Author:', width=main_label_width, font=main_label_font).grid(row=row_count, column=0, padx=(10, 0),
                                                                                   pady=y_pad, sticky=tk.E)
        package_author = tk.Entry(borderwidth=1, relief=tk.RIDGE, width=30, font=main_input_font)
        package_author.grid(row=row_count, column=1, padx=(5, 5), pady=y_pad, sticky=tk.W)
        #tk.Label(text='?', width=12, font=('Arial', 12)).grid(row=row_count, column=2, padx=(0, 10), pady=y_pad, sticky=tk.W)
        self.metadata.append(('dc.creator', package_author))

        row_count += 1

        tk.Label(text='Publisher:', width=main_label_width, font=main_label_font).grid(row=row_count, column=0, padx=(10, 0),
                                                                                     pady=y_pad, sticky=tk.E)
        package_publisher = tk.Entry(borderwidth=1, relief=tk.RIDGE, width=30, font=main_input_font)
        package_publisher.grid(row=row_count, column=1, padx=(5, 5), pady=y_pad, sticky=tk.W)
        #tk.Label(text='?', width=12, font=('Arial', 12)).grid(row=row_count, column=2, padx=(0, 10), pady=y_pad, sticky=tk.W)
        self.metadata.append(('dc.publisher', package_publisher))

        row_count += 1

        sep = ttk.Separator(orient=tk.HORIZONTAL)
        sep.grid(row=row_count, column=0, columnspan=3, pady=y_pad, sticky=tk.EW)

        row_count += 1

        tk.Label(text='DSpace AIP collection:', width=main_label_width, font=main_label_font).grid(row=row_count, column=0, padx=(10, 0),
                                                                                  pady=y_pad, sticky=tk.E)
        package_dspace_aip = tk.Entry(borderwidth=1, relief=tk.RIDGE, width=40, font=main_input_font, validate="focusout",
                                validatecommand=lambda: self._check_empty(package_date))
        package_dspace_aip.grid(row=row_count, column=1, padx=(5, 5), pady=y_pad, sticky=tk.W)
        package_dspace_aip.insert(0, '436a3c02-255e-4d84-ac8f-8ae91d7ecd02')
        tk.Label(text='?', width=22, font=('Arial', 12)).grid(row=row_count, column=2, padx=(0, 10), pady=y_pad,
                                                                         sticky=tk.W)
        self.metadata.append(('dspace_aip_collection', package_dspace_aip))

        row_count += 1

        tk.Label(text='DSpace DIP collection:', width=main_label_width, font=main_label_font).grid(row=row_count, column=0, padx=(10, 0),
                                                                                  pady=y_pad, sticky=tk.E)
        package_dspace_dip = tk.Entry(borderwidth=1, relief=tk.RIDGE, width=40, font=main_input_font, validate="focusout",
                                validatecommand=lambda: self._check_empty(package_date))
        package_dspace_dip.grid(row=row_count, column=1, padx=(5, 5), pady=y_pad, sticky=tk.W)
        package_dspace_dip.insert(0, '09c098c1-99b1-4130-8337-7733409d39b8')
        tk.Label(text='?', width=22, font=('Arial', 12)).grid(row=row_count, column=2, padx=(0, 10), pady=y_pad,
                                                                         sticky=tk.W)
        self.metadata.append(('dspace_dip_collection', package_dspace_dip))

        row_count += 1

        tk.Label(text='ArchivesSpace DIP link:', width=main_label_width, font=main_label_font).grid(row=row_count,
                                                                                                   column=0,
                                                                                                   padx=(10, 0),
                                                                                                   pady=y_pad,
                                                                                                   sticky=tk.E)
        package_archivesspace = tk.Entry(borderwidth=1, relief=tk.RIDGE, width=40, font=main_input_font,
                                      validate="focusout",
                                      validatecommand=lambda: self._check_empty(package_date))
        package_archivesspace.grid(row=row_count, column=1, padx=(5, 5), pady=y_pad, sticky=tk.W)
        package_archivesspace.insert(0, '135569')
        tk.Label(text='?', width=22, font=('Arial', 12)).grid(row=row_count, column=2, padx=(0, 10), pady=y_pad,
                                                              sticky=tk.W)
        self.metadata.append(('archivesspace_dip_collection', package_archivesspace))

        row_count += 1

        sep = ttk.Separator(orient=tk.HORIZONTAL)
        sep.grid(row=row_count, column=0, columnspan=3, pady=y_pad, sticky=tk.EW)

        row_count += 1

        tk.Button(text='Select input directory', command=lambda: self._get_directory(self.input_dir, self.input_dir.label)).grid(row=row_count, column=0, padx=(10, 5), pady=y_pad, sticky=tk.E)
        self.input_dir = tk.Entry(width=40, font=main_input_font, validate="focusout", validatecommand=self._validate_input_dir)
        self.input_dir.grid(row=row_count, column=1, padx=(5, 10), pady=y_pad, sticky=tk.W)
        self.input_dir.label = tk.Label(text='?', width=22, font=('Arial', 12))
        self.input_dir.label.grid(row=row_count, column=2, padx=(0, 10), pady=y_pad, sticky=tk.W)
        #self.non_empties.append(self.input_dir)

        row_count += 1

        tk.Button(text='Select output directory', command=lambda: self._get_directory(self.output_dir)).grid(row=row_count, column=0, padx=(10, 5), pady=y_pad, sticky=tk.E)
        self.output_dir = tk.Entry(width=40, font=main_input_font)
        self.output_dir.grid(row=row_count, column=1, columnspan=2, padx=(5, 10), pady=y_pad, sticky=tk.W)
        self.non_empties.append(self.output_dir)

        row_count += 1

        tk.Button(text="Start transfer", font=('Arial', 18), command=self._start_transfer).grid(row=row_count, column=0, padx=(10, 5), pady=y_pad,
                                                                                        sticky=tk.E)
        tk.Button(text="Reset", font=('Arial', 18), fg="red", command=self._reset).grid(row=row_count, column=1, padx=(5, 5),
                                                                                        pady=y_pad)
        tk.Button(text="Quit", font=('Arial', 18), fg="red", command=root.destroy).grid(row=row_count, column=2, padx=(5, 10), pady=y_pad)
        #self.quit.pack(side="bottom")

    def _get_directory_size(self, dir):
        total_files = 0
        total_size = 0
        for subdir, dirs, files in os.walk(dir):
            for file in files:
                full_filename = os.path.join(subdir, file)
                total_files += 1
                total_size += os.path.getsize(full_filename)

        return (total_files, total_size)

    def _validate_input_dir(self):
        #print(self._check_empty(self.input_dir))
        if self._check_empty(self.input_dir):
            for subdir, dirs, files in os.walk(self.input_dir.get()):
                for file in files:
                    full_filename = os.path.join(subdir, file)
                    print(full_filename)

            #self.input_dir.label.config(text=total_size)


    def _generate_json(self):
        test = { 'parts': 'objects/',
                 'dc.description.provenance': 'Submitted to Archivematica by ' + getpass.getuser() + " on computer "
                 + platform.node() + ' at ' + str(datetime.datetime.now())}

        for p in self.metadata:
            print(p, p[0], p[1])
            test[p[0]] = p[1].get()

        return [test]

    def _check_empty(self, tk_obj):
        if len(tk_obj.get()) == 0:
            tk_obj.config(highlightbackground='red')
            return False
        else:
            tk_obj.config(highlightbackground='white')
            return True


    def _check_errors(self, tk_obj):
        for t in tk_obj:
            v = t.get()
            if len(v) == 0:
                t.config(highlightbackground='red')
                return False

        return True

    def _reset(self):
        for p in self.metadata:
            p[1].delete(0, tk.END)

        self.input_dir.delete(0, tk.END)
        self.input_dir.label.config(text='')
        self.output_dir.delete(0, tk.END)
        #self.metadata = []


    def _start_transfer(self):
        if self._check_errors(self.non_empties) and messagebox.askokcancel("Confirm transfer?", "Do you want to start this transfer?"):
            self._copy_directory()
            self._reset()


    def _copy_directory(self):
        try:
            input_dir = self.input_dir.get()
            output_dir = self.output_dir.get() + '/' + input_dir.split('/')[-1]
            shutil.copytree(input_dir, output_dir + '/objects/')

            os.mkdir(output_dir + '/metadata')

            with open(output_dir + '/metadata/metadata.json', 'w') as outfile:
                json.dump(self._generate_json(), outfile)
        except FileExistsError as e:
            print('Error: ' + e)
        except IOError as e:
            print('Error: ' + e)

        messagebox.showinfo('Transfer status', "Successfully copied from:\n\n" + input_dir + "\n\nto:\n\n" + output_dir)



    def _get_directory(self, text_obj, text_label=None):
        dir = tk.filedialog.askdirectory()
        text_obj.insert(tk.END, dir)

        if text_label is not None:
            files, size = self._get_directory_size(dir)
            size = str(size/(1024*1024.0))
            size = size[:size.find('.')+2]
            text_label.config(text="Files: " + str(files) + " Size: " + size + " mb")



root = tk.Tk()
root.title('Archive assistant')
app = Application(master=root)
app.mainloop()