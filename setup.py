import cx_Freeze
import tkinter
import sys
import sqlite3
import idna
import os
from os.path import join, basename



def collect_dist_info(packages):
    """
    Recursively collects the path to the packages' dist-info.
    """
    if not isinstance(packages, list):
        packages = [packages]
    dirs = []
    for pkg in packages:
        distrib = pkg_resources.get_distribution(pkg)
        for req in distrib.requires():
            dirs.extend(collect_dist_info(req.key))
        dirs.append((distrib.egg_info, join('Lib', basename(distrib.egg_info))))
    return dirs

includes = ["models.py",
            r"C:\Users\sarforo\Downloads\CSMS_EXE\forms\addinvoice.py","forms\home.py",
            "modules\\tktoolbar.py",
            "forms\products.py","forms\calc.exe",
            "forms\invoices.py",
            "modules\peewee.py",
            "modules\\tkcalendar.py",
            "modules\\tklistview.py",
            "Passwords",
            "db.sqlite3",
            "Receipt.txt",
            r"C:\Users\JOE\AppData\Local\Programs\Python\Python36\DLLs\\tcl86t.dll",
            r"C:\Users\JOE\AppData\Local\Programs\Python\Python36\DLLs\\tk86t.dll"
            ]

os.environ['TCL_LIBRARY'] = r"C:\Users\JOE\AppData\Local\Programs\Python\Python36\\tcl\\tcl8.6"
os.environ['TK_LIBRARY'] = r"C:\Users\JOE\AppData\Local\Programs\Python\Python36\\tcl\\tk8.6"

base = None

if sys.platform == 'win32':
    base = "WIN32GUI"
    
executables = [cx_Freeze.Executable("login_register.py", base=base, icon="icon.ico")]

cx_Freeze.setup(
    name = "ComStore Pro",
    options = {"build_exe":{"packages":["tkinter","tkinter.ttk","nexmo","sqlite3","idna.idnadata",],"include_files":includes}},
    version = "1.0",
    description = "Computer Shop Monitoring System",
    executables = executables
    )


