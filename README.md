## Diaconu Marian Alexandru Curriculum Vitae

This repository just stores my personal CV. The CV can be downloaded as file `main.pdf`.

### Softeware Used:

```
Texmaker 5.0.3
(compiled with Qt 5.11.3)
Copyright (c) 2003-2018 by Pascal Brachet

Project home site : http://www.xm1math.net/texmaker/
```

### Additional dependencies

- Additional to Textmaker you need to install required standard libraries to enable Textmaker to successfully compile the document. 
- Specifically we need `texlive-full`.
- I used Devian 10, therefore, install it using the following command:

```
sudo apt-get install texlive-full
```

### Convert DVI to PDF

- Texmaker seems able to only henerate DVI files. 
- In order to covert DVI file to PDF use the following command:

```
dvipdfm your_dvi_file.dvi
```

- Substitute `your_dvi_file.dvi` with your file name.
- The above command will generate a PDF file with name `main.pdf`

### Convert JPG to EPS

- For this CV we needed to use EPS images instead of JPG. 
- Use the following command to convert JPG to EPS if you need it too.

```
convert path/to/ypur/img.jpg eps2:/path/to/new/image.eps
```