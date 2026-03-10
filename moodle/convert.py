import os
import win32com.client

root = r"C:\222\4 курс\єдкі"

word_ext = (".doc",".docx",".rtf",".odt")
ppt_ext = (".ppt",".pptx")
excel_ext = (".xls",".xlsx")

word = win32com.client.Dispatch("Word.Application")
word.Visible = False

ppt = win32com.client.Dispatch("PowerPoint.Application")
excel = win32com.client.Dispatch("Excel.Application")

for path, dirs, files in os.walk(root):

    # пропускаємо HTML ресурсні папки
    dirs[:] = [d for d in dirs if not d.endswith("_files")]

    for file in files:

        name, ext = os.path.splitext(file)
        ext = ext.lower()

        full = os.path.join(path,file)
        pdf = os.path.join(path,name+".pdf")

        # не чіпаємо якщо PDF вже існує
        if os.path.exists(pdf):
            continue

        try:

            if ext in word_ext:

                doc = word.Documents.Open(full)
                doc.SaveAs(pdf,FileFormat=17)
                doc.Close()

                print("WORD → PDF:",file)


            elif ext in ppt_ext:

                pres = ppt.Presentations.Open(full)
                pres.SaveAs(pdf,32)
                pres.Close()

                print("PPT → PDF:",file)


            elif ext in excel_ext:

                wb = excel.Workbooks.Open(full)
                wb.ExportAsFixedFormat(0,pdf)
                wb.Close()

                print("EXCEL → PDF:",file)


        except Exception as e:
            print("Помилка:",file,e)


word.Quit()
ppt.Quit()
excel.Quit()

print("Готово.")