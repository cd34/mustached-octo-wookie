aws-glacier-scripts
===================

Set of Glacier tools

* glaciergetter.py - retrieve object from vault
* glacierls.py - display listing of local storage replica of vault
* glacierlist.py - request a listing of files in your vault
* glacierputter.py - upload a file or files from the command line.
* glacierresults.py - with no command line arguments, displays list of jobs. 
With a jobid, it will retrieve the job. 
* glacierrm.py - remove a file from the vault
* glaciersched.py - upload for x hours a list of files. Will skip duplicates.

The goal
========

glaciersched.py 6 /path/to/files

This will run for 6 hours and upload files. For larger files, it'll take the rolling average and stop if it doesn't think it can
upload within the window.

glacierputter.py

This runs and will put a file or list of files in glacier.

glacierls.py

A local content listing is maintained so you can find object IDs to retrieve.

glacierlist.py

Request a catalog of the objects. Once generated, you can recreate your local vault listing.

glacierrm.py

Remove an object from the archive.


