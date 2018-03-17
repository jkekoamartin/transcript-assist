# transcript-assist
Tool for assisting management of transcription efforts.

The script is run from the command line as follows: 
`py ext_comparator.py <ext1> <ext2> <search path> <output path>`

This will find matching file names between the two specified extensions.
For example, ".pdf" and ".doc*" as extension parameter would consider these as a match:

`file1.pdf file1.docx`

This is useful for managing large scale transciption efforts such as transcribers manually writing the contents of pdfs to word documents.
The script allows for the detection of duplicate transcriptions, completed transcriptions, and incomplete transcriptions.

It can be used for other use cases, such as messy directory where there might be duplication in subdirectories, or you want to track tedious file conversions accross multiple subdirectories. 
Should work on any platform with python 3.6 installed.
