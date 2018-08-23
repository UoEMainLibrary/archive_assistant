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

from urllib.parse import urlparse
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# TODO
# Fix hidden values in treeview

# Perhaps first choose directory so that it is possible to create metadata for
# every file/object as well before transfer starts

# Do metadata verification?

# File structure in treeview?

# Save/load templates

# Import embedded metadata functionality

# Create package but not start transfer?

# Form item styling
MAIN_LABEL_FONT = ('Helvetica', 13)
MAIN_LABEL_FONT_BOLD = ('Helvetica', 13, 'bold')
MAIN_INPUT_FONT = ('Helvetica', 12)
MAIN_LABEL_WIDTH = 16
Y_PAD = 8
X_PAD = 5

DC_TERMS = ['dc.contributor.advisor', 'dc.contributor.author', 'dc.contributor.editor',
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


class MetadataWindow(tk.Toplevel):
    def __init__(self, root=None, part=None):
        super().__init__()
        self.root = root

        if part:
            self.json_object = part
        else:
            self.json_object = {**self.root._generate_json(), **self.root.package_metadata_extra}

        self.controls_frame = self.dcterm = self.dcterm_value = None

        # self.metadata_delete = []

        # Background color manually set because themed style doesn't for some reason
        self.configure(background='#F0F0F0')

        if self.json_object['parts'] == 'objects/':
            self.title('Edit package metadata')
        else:
            self.title(self.json_object['parts'])

        n_f = ttk.Frame(self)
        self.m_f = ttk.Frame(n_f)
        self.list_metadata(self.m_f)
        self.m_f.pack()
        self.position_metadata_controls(n_f)
        n_f.pack()

    def save(self):
        # for json_property in self.metadata_delete:
        #    del self.root.package_metadata_extra[json_property]

        for json_property in self.json_object:
            if isinstance(self.json_object[json_property], tk.StringVar):
                self.json_object[json_property] = self.json_object[json_property].get()

        if self.title() != 'Edit package metadata':
            self.root.item_metadata.append(self.json_object)
        else:
            del self.json_object['parts']
            del self.json_object['dc.title']
            del self.json_object['dc.creator']
            del self.json_object['dc.description.provenance']
            del self.json_object['dc.date.issued']
            self.root.package_metadata_extra = self.json_object

        # print(self.root.item_metadata)
        # print(self.root.package_metadata)
        # print(self.root.package_metadata_extra)
        self.destroy()

    def add_metadata(self):
        if self.dcterm.get() == '':
            pass
        elif self.dcterm.get() not in self.json_object:
            tv = tk.StringVar()
            fr = ttk.Frame(self.m_f)
            ttk.Label(fr, text=self.dcterm.get() + ': ', width=20, font=MAIN_LABEL_FONT, anchor=tk.E)\
                .pack(side=tk.LEFT, pady=Y_PAD)

            if 'description' in self.dcterm.get():
                tk.Text(fr, width=40, height=4, font=MAIN_INPUT_FONT).pack(side=tk.LEFT, pady=Y_PAD)
            else:
                ttk.Entry(fr, width=40, font=MAIN_INPUT_FONT, textvariable=tv).pack(side=tk.LEFT, pady=Y_PAD)

            ttk.Button(fr, text='Delete', command=fr.destroy).pack(side=tk.RIGHT, pady=Y_PAD, padx=X_PAD)
            tv.set(self.dcterm_value.get())
            self.json_object[self.dcterm.get()] = tv
            fr.pack(pady=Y_PAD)  # grid(row=self.metadata_entries)
        else:
            messagebox.showerror('Error', 'Property {} already exists'.format(self.dcterm.get()))

        # print(self.json_object)

    def list_metadata(self, contents_frame):
        for json_property in self.json_object:
            if not (json_property == 'parts' or
                    (self.json_object['parts'] == 'objects/' and json_property == 'dc.description.provenance')):

                tv = tk.StringVar()
                fr = ttk.Frame(contents_frame)
                ttk.Label(fr, text=json_property + ': ', width=20, font=MAIN_LABEL_FONT, anchor=tk.E)\
                    .pack(side=tk.LEFT, pady=Y_PAD)

                if 'description' in json_property:
                    tk.Text(fr, width=40, height=4, font=MAIN_INPUT_FONT)
                else:
                    if self.json_object['parts'] == 'objects/':
                        if json_property == 'dc.title':
                            ttk.Entry(fr, width=40, font=MAIN_INPUT_FONT, textvariable=self.root.package_title)\
                                .pack(side=tk.LEFT, pady=Y_PAD)
                        elif json_property == 'dc.date.issued':
                            ttk.Entry(fr, width=40, font=MAIN_INPUT_FONT,
                                      textvariable=self.root.package_date).pack(side=tk.LEFT, pady=Y_PAD)
                        elif json_property == 'dc.creator':
                            ttk.Entry(fr, width=40, font=MAIN_INPUT_FONT,
                                      textvariable=self.root.package_author).pack(side=tk.LEFT, pady=Y_PAD)
                        else:
                            ttk.Entry(fr, width=40, font=MAIN_INPUT_FONT, textvariable=tv)\
                                .pack(side=tk.LEFT, pady=Y_PAD)

                    else:
                        ttk.Entry(fr, width=40, font=MAIN_INPUT_FONT, textvariable=tv).pack(side=tk.LEFT, pady=Y_PAD)

                if json_property != 'dc.title' and json_property != 'dc.date.issued' and json_property != 'dc.creator':
                    ttk.Button(fr, text='Delete', command=fr.destroy).pack(side=tk.RIGHT, pady=Y_PAD, padx=X_PAD)

                tv.set(self.json_object[json_property])
                self.json_object[json_property] = tv
                fr.pack(pady=Y_PAD)

        # sep = ttk.Separator(contents_frame, orient=tk.HORIZONTAL).pack()
        # sep.pack() # grid(row=self.row_count, column=0, columnspan=3, pady=Y_PAD, sticky=tk.EW)

    def position_metadata_controls(self, controls_frame):
        fr = ttk.Frame(controls_frame)

        ttk.Label(fr, text='DC Terms:', width=10, font=MAIN_LABEL_FONT)\
            .grid(row=0, column=0, padx=(10, 0), pady=Y_PAD, sticky=tk.E)

        self.dcterm = tk.StringVar()
        ttk.Combobox(fr, width=50, font=MAIN_INPUT_FONT, values=DC_TERMS, textvariable=self.dcterm)\
            .grid(row=0, column=1, padx=(5, 5), pady=Y_PAD, sticky=tk.W)
        ttk.Button(fr, text='Add', command=self.add_metadata)\
            .grid(row=0, column=2, rowspan=2, padx=(5, 10), pady=Y_PAD, sticky=tk.W)

        self.dcterm_value = tk.StringVar()
        ttk.Entry(fr, width=50, font=MAIN_INPUT_FONT, textvariable=self.dcterm_value)\
            .grid(row=1, column=0, columnspan=2, padx=(5, 5), pady=Y_PAD, sticky=tk.E)

        fr.pack()

        fr = ttk.Frame(controls_frame)
        ttk.Button(fr, text='Save', command=self.save).pack(side=tk.LEFT, pady=Y_PAD)
        ttk.Button(fr, text='Cancel', command=self.destroy).pack(side=tk.LEFT, pady=Y_PAD)
        fr.pack()


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        # self.grid_columnconfigure(0, weight=1)
        self.package_title = tk.StringVar()
        self.package_date = tk.StringVar()
        self.package_author = tk.StringVar()
        self.ds_host = tk.StringVar()
        self.as_host = tk.StringVar()
        self.as_user = tk.StringVar()
        self.as_password = tk.StringVar()
        self.as_repo = tk.StringVar()

        self.input_dir = tk.StringVar()
        self.output_dir = tk.StringVar()

        self.inputs = [self.package_title, self.package_date, self.package_author, self.ds_host, self.as_host,
                       self.as_user, self.as_password, self.as_repo, self.input_dir, self.output_dir]

        self._reset()  # Set values to reset value

        # List of tuples of form items and their corresponding variables
        self.package_metadata = []
        self.package_metadata_extra = {}
        # List of json objects
        self.item_metadata = []

        self.non_empties = []

        self.metadata_tree = self.contents_tree = self.md_window = None
        
        self.create_menu(master)
        self.create_widgets(master)

    # Helper methods

    @staticmethod
    def create_frame(n, text):
        f = ttk.Frame(n, relief=tk.GROOVE)
        n.add(f, text=text)
        return f

    def open_metadata_window(self, part=None):
        if self.md_window is None or self.md_window.winfo_exists() == 0:
            if part is None:
                self.md_window = MetadataWindow(self)
            else:
                self.md_window = MetadataWindow(self, part)

    @staticmethod
    def do_nothing():
        pass

    @staticmethod
    def create_label_entry(parent_obj, text, column=0, row=0, tv=None, entry_width=50):
        ttk.Label(parent_obj, text=text,
                  width=MAIN_LABEL_WIDTH+10,
                  font=MAIN_LABEL_FONT,
                  anchor=tk.E)\
            .grid(row=row,
                  column=column,
                  padx=(10, 0),
                  sticky=tk.W,
                  pady=Y_PAD)

        entry_object = ttk.Entry(parent_obj, width=entry_width, textvariable=tv, font=MAIN_LABEL_FONT)
        entry_object.grid(row=row, column=column+1, padx=(0, 10), pady=Y_PAD, sticky=tk.W)

        return entry_object

    @staticmethod
    def _get_base_url(parsed_url):
        return '{url.scheme}://{url.netloc}{url.path}'.format(url=parsed_url)

    # Treeview manipulation

    @staticmethod
    def on_click(event):
        tree = event.widget
        # print(tree)
        item_name = tree.identify_row(event.y)
        # print(item_name)
        if item_name:
            # print(tree.item(item_name))
            tags = tree.item(item_name, 'tags')
            if tags and ('collection' in tags or 'archival_object' in tags):
                tree.selection_set(item_name)

    @staticmethod
    def add_metadata(tree, dc_terms, dc_terms_value):
        if isinstance(dc_terms, ttk.Combobox):
            tree.insert('', index='end', values=(dc_terms.get(), dc_terms_value.get()))
        else:
            return tree.insert('', index='end', values=(dc_terms, dc_terms_value))

    def edit_metadata(self, tree):
        if tree.selection():
            part = list(tree.item(tree.selection()).items())[2][1][1]
            found = False

            for item in self.item_metadata:
                if item['parts'] == part:
                    self.item_metadata.remove(item)
                    # print(item)
                    self.open_metadata_window(item)
                    found = True
                    break

            if not found:
                # print({'parts': part})
                self.open_metadata_window({'parts': part})

    # Connect to ArchivesSpace

    @staticmethod
    def login_to_as(host, user, password):
        try:
            response = requests.post(host + '/users/' + user + '/login',
                                     data={'password': password, 'expiring': False})
        except requests.ConnectionError as e:
            raise Exception("Unable to connect to ArchivesSpace server.\n\nIs the server URL correct?")
        except Exception as e:
            raise Exception("Unable to connect to ArchivesSpace server.\n\nIs the server URL correct?")

        try:
            output = response.json()
        except Exception:
            print(response.content)
            raise Exception("ArchivesSpace server responded with status {}, but returned a non-JSON document"
                            .format(response.status_code))

        if 'error' in output:
            raise Exception("Unable to log into ArchivesSpace.\n\n{}\n\nAre the user name and password correct?"
                            .format(output['error']))
        else:
            token = output['session']

        session = requests.Session()
        session.headers.update({'X-ArchivesSpace-Session': token})
        return session

    @staticmethod
    def request_from_as(host, method, url, params, expected_response, data=None):
        if not url.startswith('/'):
            url = '/' + url

        response = method(host + url, params=params, data=data)
        if response.status_code != expected_response:
            print('Response code: %s', response.status_code)
            print('Response body: %s', response.text)
            # raise Exception(response.status_code, response)

        try:
            output = response.json()
        except Exception:
            raise Exception("ArchivesSpace server responded with status {}, but returned a non-JSON document"
                            .format(response.status_code))

        if 'error' in output:
            raise Exception(output['error'])

        return response

    def _populate_as_tree(self, tree):
        base_url = None
        session = None

        try:
            base_url = urlparse(self.as_host.get())

            if not base_url.port:
                base_url = base_url._replace(netloc='{}:{}'.format(base_url.netloc, 8089))

        except Exception:
            messagebox.showerror('Error', 'Could not parse URL.')

        if base_url:
            try:
                session = self.login_to_as(self._get_base_url(base_url), self.as_user.get(), self.as_password.get())
            except Exception as e:
                messagebox.showerror('Error', e)

        if session:
            url = '/repositories/' + self.as_repo.get() + '/resources'

            try:
                resources = self.request_from_as(self._get_base_url(base_url), session.get, url,
                                                 {'all_ids': True}, 200).json()

                for r in resources:
                    as_tree = self.request_from_as(self._get_base_url(base_url), session.get,
                                                   url + '/' + str(r) + '/tree', {}, 200).json()
                    self.traverse_tree(tree, [as_tree])
            except Exception as e:
                errortext = ''
                if 'The Repository must exist' in str(e):
                    errortext = '\n\nCould not find repository: {}'.format(self.as_repo.get())

                messagebox.showerror('Error', 'Could not access ArchivesSpace.{}'.format(errortext))

    def traverse_tree(self, tree, as_tree, parent_obj=''):
        obj = None
        for node in as_tree:
            if 'title' in node:
                obj = tree.insert(parent_obj, index='end', text=node['title'],
                                  tags='archival_object', values=node['id'])

            if 'children' in node:
                self.traverse_tree(tree, node['children'], obj)

    # Connnect to DSpace

    def _walk_community(self, communities, tree, parent_obj=''):
        for c in communities:
            obj = tree.insert(parent_obj, index='end', text=c.get('name'))

            for co in c.get('collection'):
                tree.insert(obj, index='end', text=co.get('name'), tags='collection', values=co['id'])

            if len(c.get('community')) > 0:
                self._walk_community(c.get('community'), tree, obj)

    def _populate_dspace_tree(self, trees):
        try:
            response = requests.get(self.ds_host.get() + '/rest/hierarchy', verify=False)
            c = response.json().get('community')

            # Make sure trees are empty before populating
            for t in trees:
                t.delete(*t.get_children())
                self._walk_community(c, t)
                t.tag_configure('collection', font=MAIN_LABEL_FONT_BOLD)
        except requests.exceptions.ConnectionError:
            messagebox.showerror('Error', 'Could not access DSpace.\n\nIs the DSpace server URL correct?')

    # Controller methods

    def _get_directory_size(self, directory):
        # TODO
        # Will time out if very low level selected
        total_files = 0
        total_size = 0

        # If dir is low level don't attempt to count
        if len(os.path.normpath(directory).split(os.path.sep)) > 3:
            try:
                for root, dirs, files in os.walk(directory):
                    for name in files:
                        total_size += os.path.getsize(os.path.join(root, name))
                        # 1 added because else space in file name gets cut off
                        self.contents_tree.insert('', index='end',
                                                  values=('1', str('...' + root[len(directory):] + '/' + name)))
                    total_files += len(files)
            except Exception as e:
                messagebox.showerror('Error', "Could not estimate total number and size of files in " + directory)
                print(e)

        return total_files, total_size

    def _validate_input_dir(self):
        if self._check_empty(self.input_dir):
            for subdir, dirs, files in os.walk(self.input_dir.get()):
                for file in files:
                    full_filename = os.path.join(subdir, file)

    def _generate_json(self):
        json_obj = { 'parts': 'objects/',
                     'dc.description.provenance': 'Submitted to Archivematica by ' + getpass.getuser() + " on computer "
                                                  + platform.node() + ' at ' + str(datetime.datetime.now())}

        for json_property in self.package_metadata:
            if len(json_property) == 2 and isinstance(json_property[1], tk.StringVar):
                # print(property, property[0], property[1])
                json_obj[json_property[0]] = json_property[1].get()
            elif len(json_property) == 2 and isinstance(json_property[1], ttk.Treeview):
                t_item = json_property[1].item(json_property[1].focus())
                # print(p[1].item(p[1].focus()))
                try:
                    json_obj[json_property[0]] = str(t_item['values'][0])  # Converting all values to string
                except IndexError as e:
                    pass
                    # print('Index out of range ' + str(e))
            else:
                print(json_property)

        return json_obj

    @staticmethod
    def _check_empty(tk_obj):
        if len(tk_obj.get()) == 0:
            messagebox.showerror('Error', 'Error 1')
            # tk_obj.config(background='red')
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
        '''print("Package metadata extra:" + str(self.package_metadata_extra))
        print("Package metadata: " + str(self.package_metadata))
        print("Item:" + str(self.item_metadata))
        '''
        for p in self.inputs:
            p.set('')

        self.package_date.set(datetime.datetime.today().strftime('%d/%m/%Y'))
        self.ds_host.set('http://test.digitalpreservation.is.ed.ac.uk')
        self.as_host.set('http://lac-archives-test.is.ed.ac.uk')
        self.as_user.set('archivematica')
        self.as_repo.set('14')
        # self.metadata = []

    def _start_transfer(self):
        if self._check_errors(self.non_empties) and \
                messagebox.askokcancel("Confirm transfer?",
                                       "Do you want to start this transfer?\n" + self.input_dir.label.cget("text")):
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
                json.dump([self._generate_json()], outfile)
        except FileExistsError as e:
            print('Error: ' + str(e))
        except IOError as e:
            print('Error: ' + str(e))

        messagebox.showinfo('Transfer status', "Successfully copied from:\n\n" + input_dir + "\n\nto:\n\n" + output_dir)

    def _get_directory(self, text_obj):
        directory = tk.filedialog.askdirectory()

        if directory:
            text_obj.set(directory)

        if hasattr(text_obj, 'label'):
            # If tree is already populated then delete
            # for child in self.contents_tree.get_children():
            self.contents_tree.delete(*self.contents_tree.get_children())

            files, size = self._get_directory_size(text_obj.get())
            size = str(size/(1024*1024.0))
            size = size[:size.find('.')+2]
            text_obj.label.config(text="Files: " + str(files) + " Size: " + size + " mb")

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
        self.create_package_form(package_frame)
        package_frame.pack()

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
        self.create_select_frame(submit_frame)

        # Controls frame
        controls_frame = ttk.Frame(master)
        ttk.Button(controls_frame, text="Start transfer", command=self._start_transfer).pack(side=tk.LEFT, padx=15)
        ttk.Button(controls_frame, text="Reset", command=self._reset).pack(side=tk.LEFT)
        ttk.Button(controls_frame, text="Quit", command=master.destroy).pack(side=tk.LEFT, padx=15, pady=20)
        controls_frame.pack()

    def create_package_form(self, package_frame):
        # Package title entry
        ttk.Label(package_frame, text='Package title:', width=MAIN_LABEL_WIDTH, font=MAIN_LABEL_FONT,
                  anchor=tk.E).grid(row=0, column=0, padx=(10, 0), pady=Y_PAD, sticky=tk.E)

        ttk.Entry(package_frame, width=40, font=('Helvetica', 16), validate="focusout",
                  textvariable=self.package_title, validatecommand=self.do_nothing)\
            .grid(row=0, column=1, padx=(0, 10),
                  pady=Y_PAD, columnspan=2,
                  sticky=tk.W)

        self.package_metadata.append(('dc.title', self.package_title))
        # self.non_empties.append(package_title)

        # Date entry
        ttk.Label(package_frame, text='Date:', width=MAIN_LABEL_WIDTH, font=MAIN_LABEL_FONT,
                  anchor=tk.E).grid(row=1, column=0, padx=(10, 0), pady=Y_PAD, sticky=tk.E)

        ttk.Entry(package_frame, width=10, font=MAIN_INPUT_FONT, validate="focusout",
                  textvariable=self.package_date,
                  validatecommand=lambda: self._check_empty(self.package_date))\
            .grid(row=1, column=1, padx=(5, 5), pady=Y_PAD, sticky=tk.W)

        ttk.Label(package_frame, text='(DD/MM/YYYY)', width=22, font=MAIN_LABEL_FONT,
                  anchor=tk.W).grid(row=1, column=2, padx=(0, 10), pady=Y_PAD, sticky=tk.W)

        self.package_metadata.append(('dc.date.issued', self.package_date))

        # Author entry
        ttk.Label(package_frame, text='Author:', width=MAIN_LABEL_WIDTH, font=MAIN_LABEL_FONT,
                  anchor=tk.E).grid(row=2, column=0, padx=(10, 0), pady=Y_PAD, sticky=tk.E)

        ttk.Entry(package_frame, width=30, textvariable=self.package_author, font=MAIN_INPUT_FONT)\
            .grid(row=2, column=1, padx=(5, 5), pady=Y_PAD, sticky=tk.W, columnspan=2)
        self.package_metadata.append(('dc.creator', self.package_author))

        # Edit package metadata button
        ttk.Button(package_frame, text='Edit package metadata',
                   command=self.open_metadata_window)\
            .grid(row=3, column=0, columnspan=3, padx=(5, 10), pady=Y_PAD, sticky=tk.E)

    def create_as_frame(self, as_dip_frame):
        sbar_frame = ttk.Frame(as_dip_frame)

        # Content for DSpace DIP tree panel
        as_dip_tree = ttk.Treeview(sbar_frame, selectmode='none', show='tree',
                                   columns=('ID #', 'Name'), displaycolumns='Name')
        as_dip_tree.column("#0", minwidth=0, width=400)
        as_dip_tree.bind("<Button-1>", self.on_click)
        as_dip_tree.pack(side=tk.LEFT)

        self.package_metadata.append(('archivesspace_dip_collection', as_dip_tree))

        vsb = ttk.Scrollbar(sbar_frame, orient="vertical", command=as_dip_tree.yview)
        vsb.pack(side=tk.RIGHT, fill=tk.Y)
        sbar_frame.grid(row=0, column=0, columnspan=3)

        as_dip_tree.configure(yscrollcommand=vsb.set)

        # as_labelframe = ttk.Labelframe(as_dip_frame, text='ArchivesSpace config')

        self.create_label_entry(as_dip_frame, 'Server URL:', row=1, column=0, tv=self.as_host)
        self.create_label_entry(as_dip_frame, 'Repository:', row=2, column=0, tv=self.as_repo)
        self.create_label_entry(as_dip_frame, 'Username:', row=3, column=0, tv=self.as_user)
        self.create_label_entry(as_dip_frame, 'Password:', row=4, column=0, tv=self.as_password)

        ttk.Button(as_dip_frame, text="Load ArchivesSpace hierarchy",
                   command=lambda: self._populate_as_tree(as_dip_tree))\
            .grid(row=5, column=0, columnspan=2, padx=(10, 5), pady=Y_PAD, sticky=tk.E)

    def create_dspace_widgets(self, ds_aip_frame, ds_dip_frame):
        # Create frame for scrollbar + treeview
        sbar_frame = ttk.Frame(ds_aip_frame)

        # Content for DSpace AIP tree panel
        ds_aip_tree = ttk.Treeview(sbar_frame, selectmode='none', show='tree',
                                   columns=('ID #', 'Name'), displaycolumns='Name')
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
        ds_aip_tree.pack(side=tk.LEFT)

        vsb = ttk.Scrollbar(sbar_frame, orient="vertical", command=ds_aip_tree.yview)
        vsb.pack(side=tk.RIGHT, fill=tk.Y)
        sbar_frame.grid(row=0, column=0, columnspan=3)

        ds_aip_tree.configure(yscrollcommand=vsb.set)

        self.package_metadata.append(('ds_aip_collection', ds_aip_tree))

        # Content for DSpace config panel
        self.create_label_entry(ds_aip_frame, 'DSpace server:', row=1, column=0, tv=self.ds_host)

        ttk.Button(ds_aip_frame, text="Load DSpace hierarchy",
                   command=lambda: self._populate_dspace_tree([ds_aip_tree, ds_dip_tree])).\
            grid(row=2, column=0, columnspan=2, padx=(10, 5), pady=Y_PAD, sticky=tk.E)

        # Do DIP frame

        # Create frame for scrollbar + treeview
        sbar_frame = ttk.Frame(ds_dip_frame)

        self.create_label_entry(ds_dip_frame, 'DSpace server:', row=1, column=0, tv=self.ds_host)

        ttk.Button(ds_dip_frame,
                   text="Load DSpace hierarchy",
                   command=lambda: self._populate_dspace_tree([ds_aip_tree, ds_dip_frame]))\
            .grid(row=2, column=0, columnspan=2, padx=(10, 5), pady=Y_PAD, sticky=tk.E)

        # Content for DSpace DIP tree panel
        ds_dip_tree = ttk.Treeview(sbar_frame, selectmode='none', show='tree', columns=('ID #', 'Name'),
                                    displaycolumns='Name')
        ds_dip_tree.column("#0", minwidth=0, width=400)
        # ds_dip_frame.column("Name", minwidth=0, width=300)
        ds_dip_tree.bind("<Button-1>", self.on_click)
        ds_dip_tree.pack(side=tk.LEFT)

        vsb = ttk.Scrollbar(sbar_frame, orient="vertical", command=ds_dip_tree.yview)
        vsb.pack(side=tk.RIGHT, fill=tk.Y)
        sbar_frame.grid(row=0, column=0, columnspan=3)

        ds_dip_tree.configure(yscrollcommand=vsb.set)
        self.package_metadata.append(('ds_dip_collection', ds_dip_tree))

    def create_select_frame(self, submit_frame):
        # Create frame for scrollbar + treeview
        sbar_frame = ttk.Frame(submit_frame)

        # List of files
        self.contents_tree = ttk.Treeview(sbar_frame, selectmode='browse',
                                          columns=('#1', '#2'), displaycolumns=('#1', '#2'))

        self.contents_tree.column("#0", minwidth=0, width=0, stretch=tk.NO)
        # self.contents_tree.heading("#1", text="name")
        self.contents_tree.column("#1", minwidth=0, width=0, stretch=tk.NO)
        self.contents_tree.column("#2", minwidth=0, width=600, stretch=tk.NO)
        self.contents_tree.grid(row=0, column=0, pady=Y_PAD)
        # https://stackoverflow.com/questions/5286093/display-listbox-with-columns-using-tkinter
        # https://stackoverflow.com/questions/5286093/display-listbox-with-columns-using-tkinter

        vsb = ttk.Scrollbar(sbar_frame, orient=tk.VERTICAL, command=self.contents_tree.yview)
        vsb.grid(row=0, column=1, sticky=tk.N+tk.S+tk.E+tk.W)
        # sbar_frame.grid(row=0, column=0, columnspan=3)

        self.contents_tree.configure(yscrollcommand=vsb.set)
        sbar_frame.grid(row=0, column=0, columnspan=3)

        ttk.Button(submit_frame, text='Edit item metadata',
                   command=lambda: self.edit_metadata(self.contents_tree))\
            .grid(row=1, column=0,  columnspan=3, padx=(5, 10), pady=Y_PAD, sticky=tk.E)

        ttk.Button(submit_frame,
                   text='Select input directory',
                   command=lambda: self._get_directory(self.input_dir)) \
            .grid(row=2, column=0, padx=(10, 5), pady=Y_PAD, sticky=tk.E)

        ttk.Entry(submit_frame, width=40, font=MAIN_INPUT_FONT, textvariable=self.input_dir,
                  validate="focusout",
                  validatecommand=self._validate_input_dir)\
            .grid(row=2, column=1, padx=(5, 10), pady=Y_PAD, sticky=tk.W)
        self.input_dir.label = ttk.Label(submit_frame, text='?', width=22, font=MAIN_LABEL_FONT)
        self.input_dir.label.grid(row=2, column=2, padx=(0, 10), pady=Y_PAD, sticky=tk.W)
        # self.non_empties.append(self.input_dir)

        ttk.Button(submit_frame,
                   text='Select output directory',
                   command=lambda: self._get_directory(self.output_dir)) \
            .grid(row=3, column=0, padx=(10, 5), pady=Y_PAD, sticky=tk.E)

        ttk.Entry(submit_frame, width=40, textvariable=self.output_dir, font=MAIN_INPUT_FONT)\
            .grid(row=3, column=1, columnspan=2, padx=(5, 10), pady=Y_PAD, sticky=tk.W)
        self.non_empties.append(self.output_dir)


def main():
    root = tk.Tk()
    root.title('Archive assistant 0.3')

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

