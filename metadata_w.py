import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk
from ttkthemes.themed_style import ThemedStyle

import os
import shutil
import getpass
import platform
import json
import datetime
import requests


class metadataWidget():
    def __init__(self):
        #super().__init__(master)
        #self.grid_columnconfigure(0, weight=1)
        self.input_dir = ''
        self.output_dir = ''
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
        self.main_label_width = 18
        self.main_label_font = ('Arial', 18)
        self.main_input_font = ('Arial', 16)
        self.y_pad = 8


    def create_metadata_widget(self):
        ttk.Label(text='Package title:', width=self.main_label_width, font=self.main_label_font).grid(row=self.row_count, column=0, padx=(10, 0), pady=self.y_pad)
        package_title = ttk.Entry(width=40, font=('Arial', 18), validate="focusout", validatecommand=lambda: self._check_empty(package_title))
        package_title.grid(row=self.row_count, column=1, padx=(0, 10), pady=self.y_pad, columnspan=2)
        self.metadata.append(('dc.title', package_title))
        #self.non_empties.append(package_title)

        self.row_count += 1

        ttk.Label(text='Date:', width=self.main_label_width, font=self.main_label_font).grid(row=self.row_count, column=0, padx=(10, 0), pady=self.y_pad, sticky=tk.E)
        package_date = ttk.Entry(width=10, font=self.main_input_font, validate="focusout", validatecommand=lambda : self._check_empty(package_date))
        package_date.grid(row=self.row_count, column=1, padx=(5, 5), pady=self.y_pad, sticky=tk.W)
        ttk.Label(text='(DD/MM/YYYY)', width=22, font=('Arial', 12)).grid(row=self.row_count, column=2, padx=(0, 10), pady=self.y_pad, sticky=tk.W)
        self.metadata.append(('dc.date.issued', package_date))

        self.row_count += 1

        ttk.Label(text='Author:', width=self.main_label_width, font=self.main_label_font).grid(row=self.row_count, column=0, padx=(10, 0),
                                                                                   pady=self.y_pad, sticky=tk.E)
        package_author = ttk.Entry(width=30, font=self.main_input_font)
        package_author.grid(row=self.row_count, column=1, padx=(5, 5), pady=self.y_pad, sticky=tk.W)
        #ttk.Label(text='?', width=12, font=('Arial', 12)).grid(row=self.row_count, column=2, padx=(0, 10), pady=self.y_pad, sticky=tk.W)
        self.metadata.append(('dc.creator', package_author))

        '''self.row_count += 1

        ttk.Label(text='Publisher:', width=self.main_label_width, font=self.main_label_font).grid(row=self.row_count, column=0, padx=(10, 0),
                                                                                     pady=self.y_pad, sticky=tk.E)
        package_publisher = ttk.Entry(width=30, font=self.main_input_font)
        package_publisher.grid(row=self.row_count, column=1, padx=(5, 5), pady=self.y_pad, sticky=tk.W)
        #ttk.Label(text='?', width=12, font=('Arial', 12)).grid(row=self.row_count, column=2, padx=(0, 10), pady=self.y_pad, sticky=tk.W)
        self.metadata.append(('dc.publisher', package_publisher))'''

        self.row_count += 1

        ttk.Label(text='DC Terms:', width=self.main_label_width, font=self.main_label_font).grid(row=self.row_count,
                                                                                                  column=0,
                                                                                                  padx=(10, 0),
                                                                                                  pady=self.y_pad,
                                                                                                  sticky=tk.E)

        package_publisher = ttk.Combobox(width=30, font=self.main_input_font, values=self.dcterms)
        package_publisher.grid(row=self.row_count, column=1, padx=(5, 5), pady=self.y_pad, sticky=tk.W)

        self.row_count += 1

        package_publisher = ttk.Entry(width=30, font=self.main_input_font)
        package_publisher.grid(row=self.row_count, column=1, padx=(5, 5), pady=self.y_pad, sticky=tk.W)
        ttk.Button(text='Add').grid(row=self.row_count,
                                    column=2,
                                    padx=(5, 10),
                                    pady=self.y_pad,
                                    sticky=tk.W)
        # ttk.Label(text='?', width=12, font=('Arial', 12)).grid(row=self.row_count, column=2, padx=(0, 10), pady=self.y_pad, sticky=tk.W)
        #self.metadata.append(('dc.publisher', package_publisher))

        self.row_count += 1

        tree = ttk.Treeview(selectmode='browse', columns=('#0', '#1'))
        # tree.bind("<<TreeviewSelect>>", self.treeview)
        tree.grid(row=self.row_count, column=0, columnspan=3)
        tree.heading("#0", text="dcterm")
        tree.column("#0", minwidth=0, width=100)
        tree.heading("#1", text="value")
        tree.column("#1", minwidth=0, width=100)

        tree.insert('', index='end', values=('dcterms.author', 'test'))
        #tree.item()

        self.row_count += 1

        sep = ttk.Separator(orient=tk.HORIZONTAL)
        sep.grid(row=self.row_count, column=0, columnspan=3, pady=self.y_pad, sticky=tk.EW)