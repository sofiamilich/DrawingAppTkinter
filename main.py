import tkinter as tk  # Импортируем библиотеку tkinter для создания графического интерфейса
from tkinter import colorchooser, filedialog, \
    simpledialog  # Импортируем модули для выбора цвета и диалогового окна сохранения файла
from PIL import Image, ImageDraw  # Импортируем классы для работы с изображениями


class DrawingApp:
    """ Инициализация основного окна приложения"""

    def __init__(self, root):
        self.root = root
        self.root.title("Рисовалка с сохранением в PNG")  # Устанавливаем заголовок окна

        # Изначальные размеры холста
        self.canvas_width = 800
        self.canvas_height = 400

        # Создание нового изображения и объекта для рисования
        self.image = Image.new("RGB", (self.canvas_width, self.canvas_height), "white")
        # Создали новое белое изображение
        self.draw = ImageDraw.Draw(self.image)  # Создаем объект для рисования на изображении

        # Создание холста для рисования
        self.canvas = tk.Canvas(root, width=self.canvas_width, height=self.canvas_height, bg='white')
        # Создали холст с белым фоном
        self.canvas.pack()  # Добавляем холст в главное окно

        # Переменные для хранения последних координат мыши
        self.last_x, self.last_y = None, None

        # Переменные для цвета кисти и размера
        self.pen_color = 'black'  # Начальный цвет кисти
        self.previous_color = self.pen_color  # Переменная для хранения предыдущего цвета кисти
        self.brush_size = 1  # Начальный размер кисти
        self.is_eraser_active = False  # Флаг для определения, активен ли ластик
        self.text_added = False  # Флаг для отслеживания добавления текста (изменено)

        # Привязываем события мыши к методам
        self.canvas.bind('<B1-Motion>', self.paint)  # ЛевКнопкиМыши для рисования
        self.canvas.bind('<ButtonRelease-1>', self.reset)  # Сброс координат при отпускании ЛКМ
        self.canvas.bind('<Button-3>', self.start_color_picker)  # ПКМ для выбора цвета
        self.canvas.bind('<ButtonRelease-3>', self.release_color_picker)  # Завершение выбора цвета
        self.canvas.bind('<Button-1>', self.add_text)  # Добавляем обработчик для добавления текста

        # Добавляем горячие клавиши
        self.root.bind('<Control-s>', self.save_image)  # Ctrl + S для сохранения изображения
        self.root.bind('<Control-c>', self.choose_color)  # Ctrl + C для выбора цвета

        self.setup_ui()

    '''Настройка пользовательского интерфейса'''

    def setup_ui(self):
        control_frame = tk.Frame(self.root)  # Создание рамки для управления
        control_frame.pack(fill=tk.X)  # Заполнение по горизонтали

        # Кнопка для выбора цвета кисти
        color_button = tk.Button(control_frame, text="Выбрать цвет кисти", command=self.choose_color)
        color_button.pack(side=tk.LEFT)  # Размещаем кнопку слева

        # Метка для предварительного просмотра цвета
        self.color_preview = tk.Label(control_frame, bg=self.pen_color, width=3,
                                      height=1)  # Создаем метку для отображения цвета
        self.color_preview.pack(side=tk.LEFT, padx=5)  # Размещаем метку слева с отступом

        # Метка для выбора толщины кисти/ластика
        size_label = tk.Label(control_frame, text="Выбрать толщину кисти/ластика:")
        size_label.pack(side=tk.LEFT)  # Размещаем метку слева

        # Переменная для хранения размера кисти
        self.brush_size_var = tk.StringVar(value="1")  # Инициализация переменной для размера кисти
        sizes = [1, 2, 5, 10]  # Доступные размеры кисти
        # Меню для выбора размера кисти
        self.brush_size_menu = tk.OptionMenu(control_frame, self.brush_size_var, *sizes, command=self.update_brush_size)
        self.brush_size_menu.pack(side=tk.LEFT)  # Размещаем меню слева

        # Кнопка для выбора ластика
        eraser_button = tk.Button(control_frame, text="Выбрать ластик", command=self.toggle_eraser)
        eraser_button.pack(side=tk.LEFT)  # Размещаем кнопку слева

        # Кнопка для изменения размера холста
        resize_button = tk.Button(control_frame, text="Изменить размер холста", command=self.change_canvas_size)
        resize_button.pack(side=tk.LEFT)  # Размещаем кнопку слева

        # Информационная метка
        info_label = tk.Label(control_frame, text="Чтобы выбрать пипетку - нажмите правую кнопку мыши\n"
                                                  "Ctrl + C - выбрать цвет,  Ctrl + S - сохранить\n"
                                                  "Чтобы добавить текст, напишите его и кликните на поля для его установки в желаемое место")
        info_label.pack(side=tk.LEFT)  # Размещаем метку слева

        # кнопка для текста
        text_button = tk.Button(control_frame, text="Текст", command=self.add_text_dialog)
        text_button.pack(side=tk.LEFT)

        # Добавляем кнопку для изменения цвета фона
        background_button = tk.Button(control_frame, text="Изменить фон", command=self.change_background_color)
        background_button.pack(side=tk.LEFT)

        # Кнопка для очистки холста
        clear_button = tk.Button(control_frame, text="Очистить", command=self.clear_canvas)
        clear_button.pack(side=tk.LEFT)  # Размещаем кнопку слева

        # Кнопка для сохранения изображения
        save_button = tk.Button(control_frame, text="Сохранить", command=self.save_image)
        save_button.pack(side=tk.LEFT)  # Размещаем кнопку слева

    '''Изменение размера холста'''

    def change_canvas_size(self):
        new_width = simpledialog.askinteger("Ширина", "Введите новую ширину:", minvalue=100, maxvalue=2000)
        new_height = simpledialog.askinteger("Высота", "Введите новую высоту:", minvalue=100, maxvalue=2000)

        if new_width and new_height:  # Если размеры введены
            self.canvas_width = new_width  # Обновляем ширину
            self.canvas_height = new_height  # Обновляем высоту

            # Обновляем холст
            self.canvas.config(width=self.canvas_width, height=self.canvas_height)
            self.clear_canvas()  # Очищаем холст и создаем новое изображение

            # Создание нового изображения
            self.image = Image.new("RGB", (self.canvas_width, self.canvas_height), "white")
            self.draw = ImageDraw.Draw(self.image)  # Обновление объекта рисования

    ''' Обновление размера кисти'''

    def update_brush_size(self, size):
        self.brush_size = int(size)  # Устанавливаем размер кисти в соответствии с выбором

    '''Очистка холста и изображения'''

    def clear_canvas(self):
        self.canvas.delete("all")  # Удаление всех объектов с холста
        self.image = Image.new("RGB", (800, 400), "white")  # Создание нового изображения
        self.draw = ImageDraw.Draw(self.image)  # Обновление объекта рисования
        self.text_added = False  # Сбрасываем флаг добавленного текста (изменено)

    '''Выбор цвета кисти'''

    def choose_color(self, event=None):
        if self.is_eraser_active:
            self.toggle_eraser()  # Если активен ластик, переключаем его обратно
        self.previous_color = self.pen_color  # Сохраняем предыдущий цвет
        self.pen_color = colorchooser.askcolor(color=self.pen_color)[1]  # Открытие диалогового окна выбора цвета
        self.color_preview.config(bg=self.pen_color)  # Обновляем цвет фона метки

    '''Переключение состояния ластика'''

    def toggle_eraser(self):
        self.is_eraser_active = not self.is_eraser_active  # Меняем состояние
        self.pen_color = 'white' if self.is_eraser_active else self.previous_color  # Установка цвета в зависимости от состояния
        self.color_preview.config(bg=self.pen_color)  # Обновляем цвет фона метки

    '''Рисование на холсте'''

    def paint(self, event):
        if self.is_eraser_active:
            self.paint_eraser(event)  # Если активен ластик, вызываем метод рисования ластиком
        else:
            if self.last_x and self.last_y:  # Проверяем, что есть предыдущие координаты
                # Рисуем линию на холсте
                self.canvas.create_line(self.last_x, self.last_y, event.x, event.y,
                                        width=self.brush_size, fill=self.pen_color,
                                        capstyle=tk.ROUND, smooth=tk.TRUE)
                # Рисуем линию на изображении
                self.draw.line([self.last_x, self.last_y, event.x, event.y],
                               fill=self.pen_color, width=self.brush_size)
        self.last_x = event.x  # Обновляем последние координаты
        self.last_y = event.y

    '''Сброс последних координат'''

    def reset(self, event):

        self.last_x, self.last_y = None, None  # Обнуляем координаты

    '''Сохранение изображения'''

    def save_image(self, event=None):

        file_path = filedialog.asksaveasfilename(defaultextension=".png",
                                                 filetypes=[("PNG files", "*.png"),
                                                            ("All files", "*.*")])
        if file_path:  # Если путь указан
            self.image.save(file_path)  # Сохраняем изображение

    '''Начало выбора цвета с помощью правой кнопки мыши'''

    def start_color_picker(self, event):
        self.canvas.config(cursor="cross")  # Изменяем курсор на крестик
        self.color_picker_x = event.x  # Сохраняем координаты для выбора цвета
        self.color_picker_y = event.y

    '''Завершение выбора цвета'''

    def release_color_picker(self, event):
        pixel_color = self.image.getpixel((self.color_picker_x, self.color_picker_y))  # Получаем цвет пикселя
        self.pen_color = "#{:02x}{:02x}{:02x}".format(pixel_color[0], pixel_color[1],
                                                      pixel_color[2])  # Устанавливаем цвет кисти
        self.color_preview.config(bg=self.pen_color)  # Обновляем цвет фона метки
        self.is_eraser_active = False  # Деактивируем ластик
        self.canvas.config(cursor="")  # Возвращаем курсор к нормальному виду

    '''Рисование с помощью ластика'''

    def paint_eraser(self, event):
        if self.last_x and self.last_y:  # Проверяем, что есть предыдущие координаты
            # Рисуем линию на холсте с цветом 'white' (ластик)
            self.canvas.create_line(self.last_x, self.last_y, event.x, event.y,
                                    width=self.brush_size, fill='white',
                                    capstyle=tk.ROUND, smooth=tk.TRUE)
            # Рисуем линию на изображении
            self.draw.line([self.last_x, self.last_y, event.x, event.y], fill='white',
                           width=self.brush_size)

    '''Ввод текста'''

    def add_text_dialog(self):
        text = simpledialog.askstring("Введите текст", "Текст:")
        if text:
            self.current_text = text  # Сохраняем текст для дальнейшего использования
            self.text_added = False  # Сбрасываем флаг добавленного текста

    '''Проверяем, был ли введен текст'''

    def add_text(self, event):
        if hasattr(self, 'current_text') and not self.text_added:  # Проверка состояния флага
            # Добавляем текст на изображение
            self.draw.text((event.x, event.y), self.current_text, fill=self.pen_color)
            # Рисуем текст на холсте
            self.canvas.create_text(event.x, event.y, text=self.current_text, fill=self.pen_color)
            self.text_added = True  # Устанавливаем флаг, что текст добавлен

    '''Изменение цвета фона холста'''

    def change_background_color(self):
        new_color = colorchooser.askcolor()[1]  # Открываем диалог для выбора цвета
        if new_color:
            self.canvas.config(bg=new_color)  # Изменяем цвет фона холста
            self.image = Image.new("RGB", (self.canvas_width, self.canvas_height), new_color)  # Обновляем изображение


def main():
    root = tk.Tk()  # Создание основного окна
    app = DrawingApp(root)  # Инициализация приложения
    root.mainloop()  # Запуск главного цикла приложения


if __name__ == "__main__":
    main()  # Запуск программы
