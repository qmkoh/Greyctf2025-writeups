# Layer Cake

Layer Cake is a very simple forensics challenge. We are first given an mp3 file. Clearly, this should be raising red flags because mp3s are often used in steganography, metadata leaks or audio-based encoding in a ctf context. TLDR: this cant simply be an mp3 file!  
Executing a simple `file` command, we get:
```
file layer\ cake.mp3         
layer cake.mp3: Zip archive data, made by v2.0 UNIX, extract using at least v2.0, last modified May 30 2025 18:15:02, uncompressed size 0, method=store
```
As shown from the output, the mp3 file is actually a ZIP archive. From there, we need to convert it into a zip file and extract the contents from it.
We use a simple `mv` command for this:
```
mv layer\ cake.mp3 layer_cake.zip
unzip layer_cake.zip
```
After which, this gives us a singular folder named 'layers'. The contents of the folder can be found in [/layers](./layers).  
The contents of the folder are as follows:
- [Content_Types].xml
- A docProps folder
- A _rels folder
- A word folder

This is the internal structure of a Microsoft Word `.docx` file that has been unzipped. The following is a breakdown of the folder contents:
- [Content_Types].xml – Describes content types for each part of the document.
- docProps/ – Contains core.xml and app.xml, which store document metadata like author, creation date, etc. These can sometimes contain leaked usernames or hints.
- _rels/ – Relationships folder; links parts of the document together.
- word/ – The actual Word document contents are here, as well as the formatting of the document. In this case, this folder contains the following content:
  - document.xml
  - fontTable.xml
  - _rels
  - settings.xml
  - styles.xml
  - theme
  - webSettings.xml

Approaching this, I figured the quickest and easiest way would be to check if the file is hidden as readable plaintext in the files. However, it is tedious to iterate through all .xml files manually. As such, I used the following command: 
```
cd layers
grep -i grey **/*.xml
```

Although this command did, fortunately, gave me an output, there was too much junk around the actual text. Therefore, we would need to filter out the flag more precisely.
```
grep -rio 'grey{[^}]*}' .
```
To break down the code,
- -r: recursively search through subdirectories
- -i: case-sensitive, includes matches like GREY, grey etc. (may be removable as all flags in this competition are in lowercase 'grey{}'
- -o: only output the line that matches the pattern. 

That's how we get the flag!
