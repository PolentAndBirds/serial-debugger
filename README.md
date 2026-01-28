# serial-debugger

per creare l'eseguibile:

python -m PyInstaller --noconsole --onefile --add-data "C:\Users\nicola.roso\AppData\Local\Programs\Python\Python314\Lib\site-packages\customtkinter;customtkinter/" --icon "icon.ico" --name "JDT Python Debugger" jte_gui.py