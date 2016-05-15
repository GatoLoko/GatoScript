# -*- coding: utf-8 *-*

Script hierarchy:

/
 |gatoscript.py
 |gatiscript2/
    |doc/
       |readme.md
       |hierarchy.md
       |notes.txt
    |gmodules/
       |__init__.py
       |helper.py
       |highlight.py


/ - Root folder: contains everything, that's all HexChat/X-Chat files.

gatoscript.py: main script, this is what HexChat/X-Chat loads. Loads and
initializes everything else.

gatiscript2: everything else must be inside this folder. This is to keep all
the script files concentrated in a single place as much as to keep the
HexChat/X-Chat folder clean.

doc: documentation folder, any and all documentation must be stored here.

  README.md: useful information for anybody wanting to mess with the code

  hierarchy.md: this file, contains a description of every single file in the
  script

  notes.txt: temporal notes not yet given a proper place in the documentation

gmodules: a python package. All modules are stored here. Must contain only
python code and should be as well documented as possible.

  \_\_init\_\_.py: python package initialization. This is loaded by the main
  script.

  antispam.py: python module. Contains all antispam related functions. Message
  filtering and filters management.

  example.py: python module. Contains a basic skelleton of a gatoscript module.
  Tends to be unkempt, but should be a good template for new modules.

  helper.py: python module. Contains common functions, if anything is useful
  for more than one module, this is the appropriate place for it. This module
  CONTAINS VERY IMPORTANT CODE. Keep it CLEAN and DOCUMENTED.

  highlight.py: python module. Contains highlighting functions. URLs are
  colored and messages containing highlighted words are copied to the script
  query to keep them from scrolling out of the visible buffer.

  p2p.py: python module. Contains functions to interact with p2p software like
  amule or torrent clients, and show related info in public channels.

  protections.py: python module. Contains anything that protects us from
  anoying users, like: anti-ctcp, anti-notice, anti-caps, anti-colors,
  anti-drone.

  sysinfo.py: python module. Contains functions to help us share information
  about our system's hardware and software.

  whois.py: python module. Contains functions to intercept, reformat and show
  whois reponses. Anything whois related goes here.
