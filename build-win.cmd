pyi-makespec --add-data="mangareader\styles.css;mangareader" ^
  --add-data="mangareader\menu.svg;mangareader" ^
  --add-data="mangareader\menu-light.svg;mangareader" ^
  --add-data="mangareader\scroll.svg;mangareader" ^
  --add-data="mangareader\scroll-light.svg;mangareader" ^
  --add-data="mangareader\boot.template.html;mangareader" ^
  --add-data="mangareader\doc.template.html;mangareader" ^
  --add-data="mangareader\img.template.html;mangareader" ^
  --add-data="mangareader\scripts.js;mangareader" ^
  --add-data="mangareader\roboto-regular.woff2;mangareader" ^
  --add-data="mangareader\roboto-bold.woff2;mangareader" ^
  --add-data="mangareader\zenscroll.js;mangareader" ^
  --add-data="version;." ^
  --add-data="unrar.exe;." ^
  --icon="icon\air1.ico" ^
  --name="mangareader" ^
  --noconsole ^
reader.py && ^
pyinstaller --noconfirm mangareader.spec
