# Facebook messages downloader


- To download data from messenger.com, I use this Google Chrome extension: https://chatsaver.org/files.html
    - Sometimes, it collides with other extensions, if you have lots of them. 
    It should work out of the box, but if not, create new chrome profile, with only this extension.
    - I use the paid version, which allows export to csv, but you can write parser from txt for free version.
    
- Little note: since I work only with text here, this does not support images in conversations. 
Images could be supported without problem, you'll just need to modify the csv to pdf procedure

- Then I export the CSV into the HTM by the `csv_to_html.py` script. You need to set the input and output filenames to make it work.

- Second little note: used font is set in the html file. Some fonts don't support emojis. 
    If you want to change the font, simply download it and specify it in the css in the beginning of the html file.
    `two-column-template.html` file is used as the template for html generation, so if you want to do some changes 
    for more fb conversations, you can change it there.
      
- Lastly, HTML will be converted into the PDF using the software Prince. 
    - Download Prince here: https://www.princexml.com/download/
    - Simply open Prince program, select the HTML file and convert it.
    - PDF file with the same name will be created, and now you are done.

