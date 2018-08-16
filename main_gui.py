#!/usr/bin/python3

import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk
from tkinter import Menu
from ttkthemes.themed_style import ThemedStyle

import os
import shutil
import getpass
import platform
import json
import datetime
import requests

# TODO
# Fix hidden values in treeview

# Perhaps first choose directory so that it is possible to create metadata for
# every file/object as well before transfer starts

# Do metadata verification?

# File structure in treeview?

# Save/load templates

# Import embedded metadata functionality

# Create package but not start transfer?


class MetadataWindow(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)

    '''def create_contents_frame(self, contents_frame):
           self.contents_tree = ttk.Treeview(contents_frame,
                                             selectmode='browse',
                                             columns=('#1'),
                                             displaycolumns=('#1'),
                                             show=["headings"])
           # tree.bind("<<TreeviewSelect>>", self.treeview)
           self.contents_tree.grid(row=0, column=0, pady=self.y_pad)
           # tree.heading("#0", text="dcterm")
           # tree.column("#0", minwidth=0, width=100)
           self.contents_tree.heading("#1", text="name")
           self.contents_tree.column("#1", minwidth=0,
                                     width=400)
           # https://stackoverflow.com/questions/5286093/display-listbox-with-columns-using-tkinter
           # self.contents_tree.heading("#2", text="value")
           # self.contents_tree.column("#2", minwidth=0, width=200)
           # https://stackoverflow.com/questions/5286093/display-listbox-with-columns-using-tkinter
           # self.metadata_tree.bind("<Button-1>", (lambda x: self.on_click2(x, dcterms_combo, dcterms_value)))

           # self.add_metadata(tree, 'dc.title', 'A transfer title')

           ttk.Button(contents_frame,
                      text='Edit item metadata',
                      command=lambda: self.edit_metadata(self.contents_tree)) \
               .grid(row=0,
                     column=2,
                     padx=(5, 10),
                     pady=self.y_pad,
                     sticky=tk.W)

           ttk.Button(contents_frame,
                      text='Delete item',
                      command=lambda: self.delete_metadata(self.contents_tree)) \
               .grid(row=4,
                     column=2,
                     padx=(5, 10),
                     pady=self.y_pad,
                     sticky=tk.W)

           self.row_count += 1

           # sep = ttk.Separator(orient=tk.HORIZONTAL)
           # sep.grid(row=self.row_count, column=0, columnspan=3, pady=self.y_pad, sticky=tk.EW)

           ttk.Label(contents_frame, text='DC Terms:', width=10, font=self.main_label_font)\
               .grid(row=0,
                     column=0,
                     padx=(10, 0),
                     pady=self.y_pad,
                     sticky=tk.E)

           dcterms_combo = ttk.Combobox(contents_frame, width=50, font=self.main_input_font, values=self.dcterms)
           dcterms_combo.grid(row=0, column=1, padx=(5, 5), pady=self.y_pad, sticky=tk.W)

           self.row_count += 1

           dcterms_value = ttk.Entry(contents_frame, width=40, font=self.main_input_font)
           dcterms_value.grid(row=2, column=1, padx=(5, 5), pady=self.y_pad, sticky=tk.W)
           ttk.Button(contents_frame,
                      text='Add',
                      command=lambda : self.add_metadata(self.contents_tree, dcterms_combo, dcterms_value))\
               .grid(row=2,
                     column=2,
                     padx=(5, 10),
                     pady=self.y_pad,
                     sticky=tk.W)'''


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        # self.grid_columnconfigure(0, weight=1)
        self.package_title = tk.StringVar()
        self.package_date = tk.StringVar()
        self.package_date.set(datetime.datetime.today().strftime('%d/%m/%Y'))
        self.package_author = tk.StringVar()

        self.ds_host = tk.StringVar()
        self.ds_host.set('http://test.digitalpreservation.is.ed.ac.uk')

        self.as_host = tk.StringVar()
        self.as_host.set('http://test.archivematica.is.ed.ac.uk')
        self.as_user = tk.StringVar()
        self.as_user.set('archivematica')
        self.as_password = tk.StringVar()
        self.as_repo = tk.StringVar()
        self.as_repo.set('14')

        self.input_dir = ''
        self.output_dir = ''
        # List of tuples of form items and their corresponding variables
        self.metadata = []

        self.non_empties = []

        self.dcterms = ['dc.contributor.advisor', 'dc.contributor.author', 'dc.contributor.editor',
                        'dc.contributor.illustrator', 'dc.contributor.other', 'dc.contributor', 'dc.coverage.spatial',
                        'dc.coverage.temporal', 'dc.creator', 'dc.date.accessioned', 'dc.date.available',
                        'dc.date.copyright', 'dc.date.created', 'dc.date.issued', 'dc.date.submitted',
                        'dc.date.updated', 'dc.date', 'dc.description.abstract', 'dc.description.provenance',
                        'dc.description.sponsorship', 'dc.description.statementofresponsibility',
                        'dc.description.tableofcontents', 'dc.description.uri', 'dc.description.version',
                        'dc.description', 'dc.format.extent', 'dc.format.medium', 'dc.format.mimetype', 'dc.format',
                        'dc.identifier.citation', 'dc.identifier.govdoc', 'dc.identifier.isbn', 'dc.identifier.ismn',
                        'dc.identifier.issn', 'dc.identifier.other', 'dc.identifier.sici', 'dc.identifier.slug',
                        'dc.identifier.uri', 'dc.identifier', 'dc.language.iso', 'dc.language.rfc3066', 'dc.language',
                        'dc.provenance', 'dc.publisher', 'dc.relation.haspart', 'dc.relation.hasversion',
                        'dc.relation.isbasedon', 'dc.relation.isformatof', 'dc.relation.ispartof',
                        'dc.relation.ispartofseries', 'dc.relation.isreferencedby', 'dc.relation.isreplacedby',
                        'dc.relation.isversionof', 'dc.relation.replaces', 'dc.relation.requires', 'dc.relation.uri',
                        'dc.relation', 'dc.rights.holder', 'dc.rights.license', 'dc.rights.uri', 'dc.rights',
                        'dc.source.uri', 'dc.source', 'dc.subject.classification', 'dc.subject.ddc', 'dc.subject.lcc',
                        'dc.subject.lcsh', 'dc.subject.mesh', 'dc.subject.other', 'dc.subject', 'dc.title.alternative',
                        'dc.title', 'dc.type']
        
        self.row_count = 0

        # Form item styling
        self.main_label_width = 16
        self.main_label_font = ('Helvetica', 12)
        self.main_label_font_bold = ('Helvetica', 12, 'bold')
        self.main_input_font = ('Helvetica', 10)
        self.y_pad = 8

        self.metadata_tree = self.contents_tree = None
        
        self.create_menu(master)
        self.create_widgets(master)

    # Helper methods

    @staticmethod
    def create_frame(n, text):
        f = ttk.Frame(n, relief=tk.GROOVE)
        n.add(f, text=text)
        return f

    def do_nothing(self):
        pass

    def create_label_entry(self, parent_obj, text, column=0, row=0, tv=None, entry_width=50):
        ttk.Label(parent_obj, text=text,
                  width=self.main_label_width+10,
                  font=self.main_label_font,
                  anchor=tk.E)\
            .grid(row=row,
                  column=column,
                  padx=(10, 0),
                  sticky=tk.W,
                  pady=self.y_pad)

        entry_object = ttk.Entry(parent_obj, width=entry_width, textvariable=tv, font=self.main_label_font)
        #entry_object.insert('0', tv)
        entry_object.grid(row=row, column=column+1, padx=(0, 10), pady=self.y_pad, sticky=tk.W)

        return entry_object

    # Treeview manipulation

    @staticmethod
    def on_click(event):
        tree = event.widget
        # print(tree)
        item_name = tree.identify_row(event.y)
        # print(item_name)
        if item_name:
            print(tree.item(item_name))
            tags = tree.item(item_name, 'tags')
            if tags and ('collection' in tags or 'archival_object' in tags):
                tree.selection_set(item_name)

    @staticmethod
    def add_metadata(tree, dc_terms, dc_terms_value):
        if isinstance(dc_terms, ttk.Combobox):
            tree.insert('', index='end', values=(dc_terms.get(), dc_terms_value.get()))
        else:
            return tree.insert('', index='end', values=(dc_terms, dc_terms_value))

    @staticmethod
    def edit_metadata(tree, dc_terms_combobox, dc_terms_value):
        for item_name in tree.selection():
            tree.item(item_name, values=(dc_terms_combobox.get(), dc_terms_value.get()))

    @staticmethod
    def delete_metadata(tree):
        for item_name in tree.selection():
            tree.delete(item_name)

    # Connect to ArchivesSpace

    @staticmethod
    def login_to_as(host, user, password):
        try:
            response = requests.post(host + '/users/' + user + '/login',
                                     data={'password': password, 'expiring': False})
        except requests.ConnectionError as e:
            raise Exception("Unable to connect to ArchivesSpace server: " + str(e))

        try:
            output = response.json()
        except Exception:
            print(response.content)
            raise Exception(
                "ArchivesSpace server responded with status {}, but returned a non-JSON document".format(
                    response.status_code))

        if 'error' in output:
            raise Exception(
                "Unable to log into ArchivesSpace installation; message from server: {}".format(output['error']))
        else:
            token = output['session']

        session = requests.Session()
        session.headers.update({'X-ArchivesSpace-Session': token})
        return session

    @staticmethod
    def request_from_as(host, method, url, params, expected_response, data=None):
        if not url.startswith('/'):
            url = '/' + url
        # print(host + url)
        response = method(host + url, params=params, data=data)
        if response.status_code != expected_response:
            print('Response code: %s', response.status_code)
            print('Response body: %s', response.text)
            # raise Exception(response.status_code, response)

        try:
            output = response.json()
        except Exception:
            raise Exception("ArchivesSpace server responded with status {}, but returned a non-JSON document".format(
                response.status_code))

        if 'error' in output:
            raise Exception(output['error'])

        # print(json.dumps(response.json(), indent=4, sort_keys=True))

        return response

    def _populate_as_tree(self, tree):
        session = self.login_to_as(self.as_host.get(), self.as_user.get(), self.as_password.get())
        url = '/repositories/' + self.as_repo.get() + '/resources'
        resources = self.request_from_as(self.as_host.get(), session.get, url, {'all_ids': True}, 200).json()

        for r in resources:
            as_tree = self.request_from_as(self.as_host.get(), session.get, url + '/' + str(r) + '/tree', {}, 200).json()
            self.traverse_tree(tree, [as_tree])

    def traverse_tree(self, tree, as_tree, parent_obj=''):
        # print(as_tree)
        obj = None
        for node in as_tree:
            print(node)
            if 'title' in node:
                obj = tree.insert(parent_obj,
                                  index='end',
                                  text=node['title'],
                                  tags='archival_object',
                                  values=node['id'])

            if 'children' in node:
                self.traverse_tree(tree, node['children'], obj)

    # Connnect to DSpace

    def _walk_community(self, communities, tree, parent_obj=''):
        for c in communities:
            print("C: " + str(c))
            obj = tree.insert(parent_obj, index='end', text=c.get('name'))

            for co in c.get('collection'):
                tree.insert(obj, index='end', text=co.get('name'), tags='collection', values=co['id'])
                print("Co: " + str(co))

            if len(c.get('community')) > 0:
                print("Recursive")
                self._walk_community(c.get('community'), tree, obj)

    def _populate_dspace_tree(self, trees):
        response = requests.get(self.ds_host.get() + '/rest/hierarchy', verify=False)
        c = response.json().get('community')

        # Make sure trees are empty before populating
        for t in trees:
            t.delete(*t.get_children())
            self._walk_community(c, t)
            t.tag_configure('collection', font=self.main_label_font_bold)

    # Controller methods

    def _get_directory_size(self, directory):
        # TODO
        # Will time out if very low level selected
        total_files = 0
        total_size = 0

        if len(os.path.normpath(directory).split(os.path.sep)) > 3: # If dir is low level don't attempt to count
            try:
                for root, dirs, files in os.walk(directory):
                    for name in files:
                        total_size += os.path.getsize(os.path.join(root, name))
                        # 1 added because else space in file name gets cut off
                        self.contents_tree.insert('', index='end', values=('1', str('.../' + name)))
                    total_files += len(files)
            except Exception as e:
                messagebox.showerror('Error', "Could not estimate total number and size of files in " + directory)

        return total_files, total_size

    def _validate_input_dir(self):
        # print(self._check_empty(self.input_dir))
        if self._check_empty(self.input_dir):
            for subdir, dirs, files in os.walk(self.input_dir.get()):
                for file in files:
                    full_filename = os.path.join(subdir, file)
                    print(full_filename)

            # self.input_dir.label.config(text=total_size)

    def _generate_json(self):
        json_obj = { 'parts': 'objects/',
                     'dc.description.provenance': 'Submitted to Archivematica by ' + getpass.getuser() + " on computer "
                                                  + platform.node() + ' at ' + str(datetime.datetime.now())}

        for json_property in self.metadata:
            if len(json_property) == 2 and isinstance(json_property[1], ttk.Entry):
                # print(property, property[0], property[1])
                json_obj[json_property[0]] = json_property[1].get()
            elif len(json_property) == 2 and isinstance(json_property[1], ttk.Treeview):
                t_item = json_property[1].item(json_property[1].focus())
                # print(p[1].item(p[1].focus()))
                try:
                    json_obj[json_property[0]] = str(t_item['values'][0]) # Converting all values to string
                except IndexError as e:
                    print('Index out of range ' + str(e))
            else:
                print(json_property)

        return [json_obj]

    @staticmethod
    def _check_empty(tk_obj):
        if len(tk_obj.get()) == 0:
            messagebox.showerror('Error', 'Error 1')
            tk_obj.config(background='red')
            return False
        else:
            # messagebox.showerror('Error', 'Error 2')
            # tk_obj.config(highlightbackground='white')
            return True

    @staticmethod
    def _check_errors(tk_obj):
        for t in tk_obj:
            v = t.get()
            if len(v) == 0:
                messagebox.showerror('Error', 'Error 2')
                t.config(background='red')
                return False

        return True

    def _reset(self):
        for p in self.metadata:
            p[1].delete(0, tk.END)

        self.input_dir.delete(0, tk.END)
        self.input_dir.label.config(text='')
        self.output_dir.delete(0, tk.END)
        # self.metadata = []

    def _start_transfer(self):
        if self._check_errors(self.non_empties) and \
                messagebox.askokcancel("Confirm transfer?",
                                       "Do you want to start this transfer?\n" + self.input_dir.label.cget("text")):
            self._generate_json()
            self._copy_directory()
            # self._reset()

    def _copy_directory(self):
        input_dir = output_dir = None
        try:
            input_dir = self.input_dir.get()
            output_dir = self.output_dir.get() + '/' + input_dir.split('/')[-1]
            shutil.copytree(input_dir, output_dir + '/objects/')

            os.mkdir(output_dir + '/metadata')

            with open(output_dir + '/metadata/metadata.json', 'w') as outfile:
                json.dump(self._generate_json(), outfile)
        except FileExistsError as e:
            print('Error: ' + str(e))
        except IOError as e:
            print('Error: ' + str(e))

        messagebox.showinfo('Transfer status', "Successfully copied from:\n\n" + input_dir + "\n\nto:\n\n" + output_dir)

    def _get_directory(self, text_obj, text_label=None):
        directory = tk.filedialog.askdirectory()
        text_obj.insert(tk.END, directory)

        if text_label is not None:
            # If tree is already populated then delete
            for child in self.contents_tree.get_children():
                self.contents_tree.delete(child)

            files, size = self._get_directory_size(directory)
            size = str(size/(1024*1024.0))
            size = size[:size.find('.')+2]
            text_label.config(text="Files: " + str(files) + " Size: " + size + " mb")

    # Content

    def create_menu(self, master):
        """Create entries for the menu bar.
        Currently not working"""
        menu_bar = Menu(master)
        file_menu = Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="New", command=self.do_nothing)
        file_menu.add_command(label="Open", command=self.do_nothing)
        file_menu.add_command(label="Save", command=self.do_nothing)
        file_menu.add_command(label="Save as...", command=self.do_nothing)
        file_menu.add_command(label="Close", command=self.do_nothing)
        file_menu.add_separator()

        file_menu.add_command(label="Exit", command=master.quit)
        menu_bar.add_cascade(label="File", menu=file_menu)

        help_menu = Menu(menu_bar, tearoff=0)
        help_menu.add_command(label="Help Index", command=self.do_nothing)
        help_menu.add_command(label="About...", command=self.do_nothing)
        menu_bar.add_cascade(label="Help", menu=help_menu)

        master.config(menu=menu_bar)

    def create_widgets(self, master):
        """Create the window content"""
        # Transfer package metadata
        package_frame = ttk.Frame(master)
        package_frame.pack()
        self.create_package_form(package_frame)

        # Creating notebook and the three frames
        n = ttk.Notebook(padding=(10, 20))
        submit_frame = self.create_frame(n, text='Select directory and destination')
        # content_frame = self.create_frame(n, text='Contents')
        # metadata_frame = self.create_frame(n, text='Metadata')
        ds_aip_frame = self.create_frame(n, text='DSpace AIP Collection')
        ds_dip_frame = self.create_frame(n, text='DSpace DIP Collection')
        as_dip_frame = self.create_frame(n, text='ArchivesSpace DIP link')
        n.pack()

        # self.create_contents_frame(content_frame)
        # self.create_metadata_frame(metadata_frame)

        self.create_dspace_widgets(ds_aip_frame, ds_dip_frame)
        self.create_as_frame(as_dip_frame)
        self.create_submit_frame(master, submit_frame)

        # Controls frame
        controls_frame = ttk.Frame(master)
        ttk.Button(controls_frame, text="Start transfer", command=self._start_transfer).pack(side=tk.LEFT, padx=15)
        ttk.Button(controls_frame, text="Reset", command=self._reset).pack(side=tk.LEFT)
        ttk.Button(controls_frame, text="Quit", command=master.destroy).pack(side=tk.LEFT, padx=15, pady=20)
        controls_frame.pack()

    def create_package_form(self, package_frame):
        # Package title entry
        ttk.Label(package_frame, text='Package title:', width=self.main_label_width, font=self.main_label_font,
                  anchor=tk.E).grid(row=0, column=0, padx=(10, 0), pady=self.y_pad, sticky=tk.E)

        ttk.Entry(package_frame, width=40, font=('Helvetica', 16), validate="focusout",
                  textvariable=self.package_title,
                  validatecommand=lambda: print(self.package_title.get())).grid(row=0, column=1, padx=(0, 10),
                                                                                pady=self.y_pad, columnspan=2,
                                                                                sticky=tk.W)

        self.metadata.append(('dc.title', self.package_title))
        # self.non_empties.append(package_title)

        # Date entry
        ttk.Label(package_frame, text='Date:', width=self.main_label_width, font=self.main_label_font,
                  anchor=tk.E).grid(row=1, column=0, padx=(10, 0), pady=self.y_pad, sticky=tk.E)

        ttk.Entry(package_frame, width=10, font=self.main_input_font, validate="focusout",
                  textvariable=self.package_date,
                  validatecommand=lambda: self._check_empty(self.package_date)).grid(row=1, column=1, padx=(5, 5), pady=self.y_pad, sticky=tk.W)

        ttk.Label(package_frame, text='(DD/MM/YYYY)', width=22, font=self.main_label_font,
                  anchor=tk.W).grid(row=1, column=2, padx=(0, 10), pady=self.y_pad, sticky=tk.W)

        self.metadata.append(('dc.date.issued', self.package_date))

        # Author entry
        ttk.Label(package_frame, text='Author:', width=self.main_label_width, font=self.main_label_font,
                  anchor=tk.E).grid(row=2, column=0, padx=(10, 0), pady=self.y_pad, sticky=tk.E)

        ttk.Entry(package_frame, width=30, font=self.main_input_font).grid(row=2, column=1, padx=(5, 5), pady=self.y_pad, sticky=tk.W, columnspan=2)
        self.metadata.append(('dc.creator', self.package_author))

        # Edit package metadata button
        ttk.Button(package_frame, text='Edit package metadata',
                   command=self.do_nothing).grid(row=3, column=0, columnspan=3, padx=(5, 10),
                                                 pady=self.y_pad, sticky=tk.E)

    def create_as_frame(self, as_dip_frame):
        # Content for DSpace DIP tree panel
        as_dip_tree = ttk.Treeview(as_dip_frame, selectmode='none', show='tree', columns=('ID #', 'Name'),
                                   displaycolumns='Name')
        as_dip_tree.column("#0", minwidth=0, width=400)
        as_dip_tree.bind("<Button-1>", self.on_click)
        as_dip_tree.grid(row=0, column=0, columnspan=2, padx=(5, 5), pady=self.y_pad, sticky=tk.W)

        self.metadata.append(('archivesspace_dip_collection', as_dip_tree))

        self.create_label_entry(as_dip_frame, 'ArchivesSpace server:', row=1, column=0, tv=self.as_host)
        self.create_label_entry(as_dip_frame, 'ArchivesSpace repository:', row=2, column=0, tv=self.as_repo)
        self.create_label_entry(as_dip_frame, 'ArchivesSpace username:', row=3, column=0, tv=self.as_user)
        self.create_label_entry(as_dip_frame, 'ArchivesSpace password:', row=4, column=0, tv=self.as_password)

        ttk.Button(as_dip_frame, text="Load ArchivesSpace hierarchy",
                   command=lambda: self._populate_as_tree(as_dip_tree)).grid(row=5,
                                                                             column=0,
                                                                             columnspan=2,
                                                                             padx=(10, 5),
                                                                             pady=self.y_pad,
                                                                             sticky=tk.E)

    def create_dspace_widgets(self, ds_aip_frame, ds_dip_frame):
        # Content for DSpace AIP tree panel
        ds_aip_tree = ttk.Treeview(ds_aip_frame,
                                   selectmode='none',
                                   show='tree',
                                   columns=('ID #', 'Name'),
                                   displaycolumns='Name')
        # tree.bind("<<TreeviewSelect>>", self.treeview)
        # tree.pack(expand=tk.YES, fill=tk.BOTH)
        # tree.heading("#0", text="C/C++ compiler")
        # ds_aip_tree.heading('#0', text='ID #')
        # ds_aip_tree.heading('#1', text='Name')
        # ds_aip_tree.heading('#2', text='UUID')
        ds_aip_tree.column('#0', minwidth=0, width=400, stretch=tk.NO)
        # ds_aip_tree.column('#1', minwidth=0, width=300)
        # ds_aip_tree.column('#2', minwidth=0, width=0)
        ds_aip_tree.bind("<Button-1>", self.on_click)
        # tree.pack()
        ds_aip_tree.grid(row=0, column=0, columnspan=2, padx=(5, 5), pady=self.y_pad, sticky=tk.W)

        self.metadata.append(('ds_aip_collection', ds_aip_tree))

        # Content for DSpace config panel
        self.create_label_entry(ds_aip_frame, 'DSpace server:', row=1,
                                column=0, tv=self.ds_host)

        ttk.Button(ds_aip_frame, text="Load DSpace hierarchy",
                   command=lambda: self._populate_dspace_tree([ds_aip_tree, ds_dip_frame])). \
            grid(row=2,
                 column=0,
                 columnspan=2,
                 padx=(10, 5),
                 pady=self.y_pad,
                 sticky=tk.E)

        # Do DIP frame

        self.create_label_entry(ds_dip_frame, 'DSpace server:', row=1, column=0, tv=self.ds_host)

        # dspace_password = self.create_label_entry(f1, 'DSpace password:', row=row_count)
        # row_count += 1
        ttk.Button(ds_dip_frame,
                   text="Load DSpace hierarchy",
                   command=lambda: self._populate_dspace_tree([ds_aip_tree, ds_dip_frame]))\
            .grid(row=2,
                  column=0,
                  columnspan=2,
                  padx=(10, 5),
                  pady=self.y_pad,
                  sticky=tk.E)

        # Content for DSpace DIP tree panel
        ds_dip_frame = ttk.Treeview(ds_dip_frame, selectmode='none', show='tree', columns=('ID #', 'Name'),
                                    displaycolumns='Name')
        ds_dip_frame.column("#0", minwidth=0, width=400)
        # ds_dip_frame.column("Name", minwidth=0, width=300)
        ds_dip_frame.bind("<Button-1>", self.on_click)
        ds_dip_frame.grid(row=0, column=0, columnspan=2, padx=(5, 5), pady=self.y_pad, sticky=tk.W)

        self.metadata.append(('ds_dip_collection', ds_dip_frame))

    def create_metadata_frame(self, metadata_frame):
        self.metadata_tree = ttk.Treeview(metadata_frame, selectmode='browse', columns=('#1', '#2'), show=["headings"])
        # tree.bind("<<TreeviewSelect>>", self.treeview)
        self.metadata_tree.grid(row=3, column=0, columnspan=2, rowspan=2, pady=self.y_pad)
        # tree.heading("#0", text="dcterm")
        # tree.column("#0", minwidth=0, width=100)
        self.metadata_tree.heading("#1", text="dcterms")
        self.metadata_tree.column("#1", minwidth=0,
                                  width=200)
        # https://stackoverflow.com/questions/5286093/display-listbox-with-columns-using-tkinter
        self.metadata_tree.heading("#2", text="value")
        self.metadata_tree.column("#2", minwidth=0,
                                  width=200)
        # https://stackoverflow.com/questions/5286093/display-listbox-with-columns-using-tkinter
        # self.metadata_tree.bind("<Button-1>", (lambda x: self.on_click2(x, dcterms_combo, dcterms_value)))

        # self.add_metadata(tree, 'dc.title', 'A transfer title')

        ttk.Button(metadata_frame,
                   text='Edit',
                   command=lambda: self.edit_metadata(self.metadata_tree, dcterms_combo, dcterms_value)) \
            .grid(row=3,
                  column=2,
                  padx=(5, 10),
                  pady=self.y_pad,
                  sticky=tk.W)

        ttk.Button(metadata_frame,
                   text='Delete',
                   command=lambda: self.delete_metadata(self.metadata_tree)) \
            .grid(row=4,
                  column=2,
                  padx=(5, 10),
                  pady=self.y_pad,
                  sticky=tk.W)

        self.row_count += 1

        # sep = ttk.Separator(orient=tk.HORIZONTAL)
        # sep.grid(row=self.row_count, column=0, columnspan=3, pady=self.y_pad, sticky=tk.EW)

        ttk.Label(metadata_frame, text='DC Terms:', width=10, font=self.main_label_font)\
            .grid(row=0,
                  column=0,
                  padx=(10, 0),
                  pady=self.y_pad,
                  sticky=tk.E)

        dcterms_combo = ttk.Combobox(metadata_frame, width=50, font=self.main_input_font, values=self.dcterms)
        dcterms_combo.grid(row=0, column=1, padx=(5, 5), pady=self.y_pad, sticky=tk.W)

        self.row_count += 1

        dcterms_value = ttk.Entry(metadata_frame, width=40, font=self.main_input_font)
        dcterms_value.grid(row=2, column=1, padx=(5, 5), pady=self.y_pad, sticky=tk.W)
        ttk.Button(metadata_frame,
                   text='Add',
                   command=lambda: self.add_metadata(self.metadata_tree, dcterms_combo, dcterms_value))\
            .grid(row=2,
                  column=2,
                  padx=(5, 10),
                  pady=self.y_pad,
                  sticky=tk.W)

    def create_submit_frame(self, master, submit_frame):
        self.row_count = 0

        self.contents_tree = ttk.Treeview(submit_frame,
                                          selectmode='browse',
                                          columns=('#1', '#2'),
                                          displaycolumns=('#1', '#2'))
        #                                   show=["headings"])
        # tree.bind("<<TreeviewSelect>>", self.treeview)

        # tree.heading("#0", text="dcterm")
        self.contents_tree.column("#0", minwidth=0, width=0)
        # self.contents_tree.heading("#1", text="name")
        self.contents_tree.column("#1", minwidth=0, width=0)
        self.contents_tree.column("#2", minwidth=0, width=600)
        self.contents_tree.grid(row=self.row_count, column=0, columnspan=3, pady=self.y_pad)
        # https://stackoverflow.com/questions/5286093/display-listbox-with-columns-using-tkinter
        # self.contents_tree.heading("#0", text="value")
        # self.contents_tree.column("#0", minwidth=0, width=200)
        # https://stackoverflow.com/questions/5286093/display-listbox-with-columns-using-tkinter
        # self.metadata_tree.bind("<Button-1>", (lambda x: self.on_click2(x, dcterms_combo, dcterms_value)))

        # self.add_metadata(tree, 'dc.title', 'A transfer title')

        self.row_count += 1

        ttk.Button(submit_frame,
                   text='Edit item metadata',
                   command=lambda: self.edit_metadata(self.contents_tree)) \
            .grid(row=self.row_count,
                  column=0,
                  columnspan=3,
                  padx=(5, 10),
                  pady=self.y_pad,
                  sticky=tk.E)

        self.row_count += 1

        ttk.Button(submit_frame,
                   text='Select input directory',
                   command=lambda: self._get_directory(self.input_dir, self.input_dir.label)) \
            .grid(row=self.row_count, column=0, padx=(10, 5), pady=self.y_pad, sticky=tk.E)

        self.input_dir = ttk.Entry(submit_frame,
                                   width=40,
                                   font=self.main_input_font,
                                   validate="focusout",
                                   validatecommand=self._validate_input_dir)
        self.input_dir.grid(row=self.row_count, column=1, padx=(5, 10), pady=self.y_pad, sticky=tk.W)
        self.input_dir.label = ttk.Label(submit_frame, text='?', width=22, font=self.main_label_font)
        self.input_dir.label.grid(row=self.row_count, column=2, padx=(0, 10), pady=self.y_pad, sticky=tk.W)
        # self.non_empties.append(self.input_dir)

        self.row_count += 1

        ttk.Button(submit_frame,
                   text='Select output directory',
                   command=lambda: self._get_directory(self.output_dir)) \
            .grid(row=self.row_count, column=0, padx=(10, 5), pady=self.y_pad, sticky=tk.E)

        self.output_dir = ttk.Entry(submit_frame, width=40, font=self.main_input_font)
        self.output_dir.grid(row=self.row_count, column=1, columnspan=2, padx=(5, 10), pady=self.y_pad, sticky=tk.W)
        self.non_empties.append(self.output_dir)


def main():
    root = tk.Tk()
    root.title('Archive assistant 0.2')

    # Background color manually set because themed style doesn't for some reason
    root.configure(background='#F0F0F0')

    # Make window unresizable
    root.resizable(width=0, height=0)

    app = Application(master=root)

    style = ThemedStyle(root)

    # About possible themes:
    # The themes plastik, clearlooks and elegance are recommended to make your UI look nicer
    # on all platforms when using Tkinter and the ttk extensions in Python.
    # When you are targeting Ubuntu, consider using the great radiance theme.
    style.theme_use("plastik")

    app.mainloop()


if __name__ == "__main__": main()

