# Обработчик изображений

from tkinter import * # подключаем все элементы
from tkinter import filedialog # файловый диалог
from tkinter import ttk
from PIL import Image, ImageTk, ImageFilter, ImageEnhance


class App:
    def __init__(self):
        self.root = Tk() # корневой элемент
        self.root.title('Обработка изображений')
        self.root.geometry('800x600') # размеры окна в пикселях
        # self.root.resizable(True, False) - фиксация габаритов по желанию
        ttk.Style().theme_use("classic") # для применения классической темы стилей используем метод theme_use
        ttk.Style().configure(".",  font="helvetica 10", 
                              foreground="#000000", 
                              padding=8,
                              background='#C0C0C0')
        self.bg = PhotoImage(file="fon.png")
        self.page_bg = Label(self.root, image=self.bg) # в качестве фона страницы используем картинку png
        self.page_bg.place(x = 0, y = 0)
        self.root.iconphoto(False, PhotoImage(file='icon.png'))
        
        self.lable = ttk.Label(text='Фоторедактор', 
                           foreground='#000000',
                           font=('Arial', 15, 'bold'), relief="sunken")
        self.lable.pack() # Размещение надписи
        self.canvas = Canvas(bg='#C0C0C0', width=600, height=400)
        self.canvas.pack(anchor=CENTER, pady=20)

        # Кнопка "Загрузить"
        self.btn = ttk.Button(text='Загрузить', command=self.load)
        self.btn.pack(side=LEFT, anchor=N, padx=5, fill=X, expand=TRUE)
        # Кнопка "Размыть"
        self.blur = ttk.Button(text='Размыть', command=self.blur)
        self.blur.pack(side=LEFT, anchor=N, padx=5, fill=X, expand=TRUE)
        # Кнопка резкости
        self.shrp = ttk.Button(text='Резкость', command=self.sharp)
        self.shrp.pack(side=LEFT, anchor=N, padx=5, fill=X, expand=TRUE)
        # Кнопка отражения по горизонтали
        self.flp = ttk.Button(text='Отразить', command=self.flip)
        self.flp.pack(side=LEFT, anchor=N, padx=5, fill=X, expand=TRUE)
        # Кнопка к возврату оригинала
        self.orig = ttk.Button(text='Оригинал', command=self.back)
        self.orig.pack(side=LEFT, anchor=N, padx=5, fill=X, expand=TRUE)
        # Кнопка "Очистить"
        self.rect_btn = ttk.Button(text='Очистить', command=self.make_rect)
        self.rect_btn.pack(side=LEFT, anchor=N, padx=5, fill=X, expand=TRUE)
        # Кнопка "Сохранить"
        self.save_btn = ttk.Button(text='Сохранить', command=lambda: self.load_save('save'))
        self.save_btn.pack(side=LEFT, anchor=N, padx=5, fill=X, expand=TRUE)
        self.save_btn['state'] = DISABLED
        # self.btn.bind('<ButtonPress-1>', self.load)
        self.left, self.top = 0, 0 # точки привязки к холсту
        self.ext = '' # расширение файла картинки
        self.image = None
        self.empty = Image.new('RGB', (600, 400), (255, 255, 255)) # пустышка
        self.root.mainloop()

    def load(self):
        try:
            fullpath=filedialog.askopenfilename(initialdir='./',
                                                filetypes=(
                                                    ('PNG', '*.png'),
                                                    ('JPEG', '*.jpg')
                                                )) # диалог открытия картинки
            self.ext = fullpath.split('.')[-1] # получаем расширение из пути
            # print(self.ext)
            self.empty = Image.open(fullpath)
            mode = self.empty.mode # получаем цветовую схему
            if mode == 'P': # 256-color indexed image
                self.empty = self.empty.convert('RGB')
            w, h = self.empty.size
            self.left, self.top = 0, 0

            if w > 600:
                ratio = w / 600
                h = int(h / ratio)
                w = 600
                self.empty = self.empty.resize((600, int(h/ratio)))
                if h < 400:
                    self.left, self.top = 0, (400 - h) // 2
                else:
                    self.left, self.top = 0, 0
            else:
                self.left = (600 - w) // 2
                self.top = (400 - h) // 2

            self.image = ImageTk.PhotoImage(self.empty)
            self.canvas.create_image(self.left, self.top, anchor=NW, image=self.image)
        except AttributeError: # если не удалось подгрузить
            self.image = ImageTk.PhotoImage(self.empty)
            self.canvas.create_image(0, 0, anchor=NW, image=self.image)

    # Функционал кнопки "Размытие"
    def blur(self):
        blur_img = self.empty.filter(ImageFilter.GaussianBlur(5))
        self.image = ImageTk.PhotoImage(blur_img)
        self.canvas.create_image(self.left, self.top, anchor=NW, image=self.image)
        self.save_btn['state'] = NORMAL

    # Функционал кнопки "Резкость"
    def sharp(self):
        sharper = ImageEnhance.Sharpness(self.empty)
        sharp_img = sharper.enhance(2.0)
        self.image = ImageTk.PhotoImage(sharp_img)
        self.canvas.create_image(self.left, self.top, anchor=NW, image=self.image)
        self.save_btn['state'] = NORMAL

    # Функционал кнопки отразить
    def flip(self):
        flp_img = self.empty.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
        self.image = ImageTk.PhotoImage(flp_img)
        self.canvas.create_image(self.left, self.top, anchor=NW, image=self.image)
        self.save_btn['state'] = NORMAL

    # Функционал кнопки возврата к оригиналу
    def back(self):
        self.image = ImageTk.PhotoImage(self.empty)
        self.canvas.create_image(self.left, self.top, anchor=NW, image=self.image)
        self.save_btn['state'] = DISABLED

    # Функционал кнопки сохранить
    def load_save(self, *args):
        if len(args) == 1 and args[0] == 'save':
            # print(args[0])
            fullpath = filedialog.asksaveasfilename(initialfile=f'result.{self.ext}')
            if fullpath != '':
                if f'.{self.ext}' not in fullpath:
                    fullpath += self.ext
                res = ImageTk.getimage(self.image)
                if res.mode == 'RGBA' and 'jp' in self.ext:
                    res = res.convert('RGB')
                    res.save(fullpath)
                    self.save_btn['state'] = DISABLED

    # Функционал кнопки "Очистить"
    def make_rect(self):
        self.canvas.create_rectangle(0, 0, 600, 400, fill='#ffffff')

app = App()