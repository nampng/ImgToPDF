import PyPDF4
import tkinter
from tkinter import filedialog
import fitz
from PIL import Image, ImageTk
import os
import io

image_list = []
page_num = None

root = tkinter.Tk()
root.geometry('1000x500')

menu_frame = tkinter.Frame(root, height=50)
content_frame = tkinter.Frame(root)

menu_frame.grid(row=0, column=0, padx=5, pady=5, sticky='nw')
content_frame.grid(row=1, column=0, padx=5, pady=5, sticky='nesw')

image_label = tkinter.Label(content_frame)
image_label.grid(row=0, column=0, sticky='nesw')

page_count_label = tkinter.Label(menu_frame, text='0 / 0')
page_count_label.pack(side='left')

app_alert_label = tkinter.Label(menu_frame)
app_alert_label.pack(side='right')

def rotateCallback():
    if page_num == None:
        print("No images")
        app_alert_label.configure(text="No images")
        return
    try:
        image = image_list[page_num].rotate(90)
        image_list[page_num] = image

        tkimage = ImageTk.PhotoImage(returnThumbnail())
        image_label.configure(image=tkimage)
        image_label.image = tkimage
    except Exception as e:
        print(e)

def saveCallback():
    output = 'output.pdf'
    with open(output, 'wb') as pdf_output_file:
        writer = PyPDF4.PdfFileWriter()
        for x in range(len(image_list)):
            writer.addBlankPage(width=816, height=1056)
        writer.write(pdf_output_file)
    
    print("PDF foundation created. Placing images...")
    app_alert_label.configure(text="PDF foundation created. Placing images...")
    rect = fitz.Rect(0, 0, 800, 1000)
    pdf = fitz.open(output)

    for index in range(len(image_list)):
        page = pdf[index]
        image_byte_arr = io.BytesIO()
        image = image_list[index]
        image.save(image_byte_arr, format='PNG')
        page.insertImage(rect, stream=image_byte_arr, overlay=True)
        print(f"Page {index + 1} created.")
        app_alert_label.configure(text=f"Page {index + 1} created.")

    pdf.saveIncr()

    return

def returnThumbnail():
    copy_of_image = image_list[page_num].copy()
    basewidth = 800
    wpercent = (basewidth/float(copy_of_image.size[0]))
    hsize = int((float(copy_of_image.size[1])*float(wpercent)))
    copy_of_image = copy_of_image.resize((basewidth,hsize), Image.ANTIALIAS)
    return copy_of_image

def showImg():
    if page_num == None:
        print("No images")
        app_alert_label.configure(text="No images")
        return
    tkimage = ImageTk.PhotoImage(returnThumbnail())
    image_label.configure(image=tkimage)
    image_label.image = tkimage

def updatePageCount():
    page_count_label.configure(text=f'{page_num + 1} / {len(image_list)}')

def nextCallback():
    global page_num
    if page_num == None:
        print("No images")
        app_alert_label.configure(text="No images")
        return

    if page_num < len(image_list) - 1:
        page_num += 1
    else:
        print("End of list.")
        app_alert_label.configure(text="End of list.")
        return
    showImg()
    updatePageCount()

def prevCallback():
    global page_num
    if page_num == None:
        print("No images")
        app_alert_label.configure(text="No images")
        return

    if page_num > 0:
        page_num -= 1
    else:
        print("End of list.")
        app_alert_label.configure(text="End of list.")
        return
    showImg()
    updatePageCount()

def addfileCallback():
    global page_num
    file_path = filedialog.askopenfilenames(filetypes=[('Image Files','.png .jpeg .jpg')])
    for file_name in file_path:
        if file_name != None:
            try:
                image_list.append(Image.open(file_name))
                if page_num == None:
                    page_num = 0
                showImg()
                updatePageCount()
            except Exception as e:
                print(e)

if __name__ == '__main__':
    button_rotate = tkinter.Button(menu_frame, text = "rotate", command = rotateCallback)
    button_save = tkinter.Button(menu_frame, text = "Save To PDF", command = saveCallback)
    button_next = tkinter.Button(menu_frame, text = "next", command = nextCallback)
    button_prev = tkinter.Button(menu_frame, text = "prev", command = prevCallback)
    button_addfile = tkinter.Button(menu_frame, text = "Add Image", command = addfileCallback)

    button_rotate.pack(side='left')
    button_prev.pack(side='left')
    button_next.pack(side='left')
    button_addfile.pack(side='left')
    button_save.pack(side='left')
    root.mainloop()
