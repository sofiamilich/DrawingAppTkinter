import tkinter as tk  # Импортируем библиотеку tkinter для создания графического интерфейса
from tkinter import colorchooser, filedialog, \
    simpledialog  # Импортируем модули для выбора цвета и диалогового окна сохранения файла
from PIL import Image, ImageDraw  # Импортируем классы для работы с изображениями


class DrawingApp:
    def __init__(self, root):
        # Инициализация основного окна приложения
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

        # Привязываем события мыши к методам
        self.canvas.bind('<B1-Motion>', self.paint)  # ЛевКнопкиМыши для рисования
        self.canvas.bind('<ButtonRelease-1>', self.reset)  # Сброс координат при отпускании ЛКМ
        self.canvas.bind('<Button-3>', self.start_color_picker)  # ПКМ для выбора цвета
        self.canvas.bind('<ButtonRelease-3>', self.release_color_picker)  # Завершение выбора цвета

        # Добавляем горячие клавиши
        self.root.bind('<Control-s>', self.save_image)  # Ctrl + S для сохранения изображения
        self.root.bind('<Control-c>', self.choose_color)  # Ctrl + C для выбора цвета

        self.setup_ui()  # Настройка пользовательского интерфейса

    def setup_ui(self):
        # Настройка пользовательского интерфейса
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
                                                  "Ctrl + C - выбрать цвет,  Ctrl + S - сохранить")
        info_label.pack(side=tk.LEFT)  # Размещаем метку слева

        # Кнопка для очистки холста
        clear_button = tk.Button(control_frame, text="Очистить", command=self.clear_canvas)
        clear_button.pack(side=tk.LEFT)  # Размещаем кнопку слева

        # Кнопка для сохранения изображения
        save_button = tk.Button(control_frame, text="Сохранить", command=self.save_image)
        save_button.pack(side=tk.LEFT)  # Размещаем кнопку слева

    def change_canvas_size(self):
        # Изменение размера холста
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

    def update_brush_size(self, size):
        # Обновление размера кисти
        self.brush_size = int(size)  # Устанавливаем размер кисти в соответствии с выбором

    def clear_canvas(self):
        # Очистка холста и изображения
        self.canvas.delete("all")  # Удаление всех объектов с холста
        self.image = Image.new("RGB", (800, 400), "white")  # Создание нового изображения
        self.draw = ImageDraw.Draw(self.image)  # Обновление объекта рисования

    def choose_color(self, event=None):
        # Выбор цвета кисти
        if self.is_eraser_active:
            self.toggle_eraser()  # Если активен ластик, переключаем его обратно
        self.previous_color = self.pen_color  # Сохраняем предыдущий цвет
        self.pen_color = colorchooser.askcolor(color=self.pen_color)[1]  # Открытие диалогового окна выбора цвета
        self.color_preview.config(bg=self.pen_color)  # Обновляем цвет фона метки

    def toggle_eraser(self):
        # Переключение состояния ластика
        self.is_eraser_active = not self.is_eraser_active  # Меняем состояние
        self.pen_color = 'white' if self.is_eraser_active else self.previous_color  # Установка цвета в зависимости от состояния
        self.color_preview.config(bg=self.pen_color)  # Обновляем цвет фона метки

    def paint(self, event):
        # Рисование на холсте
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

    def reset(self, event):
        # Сброс последних координат
        self.last_x, self.last_y = None, None  # Обнуляем координаты

    def save_image(self, event=None):
        # Сохранение изображения
        file_path = filedialog.asksaveasfilename(defaultextension=".png",
                                                 filetypes=[("PNG files", "*.png"),
                                                            ("All files", "*.*")])
        if file_path:  # Если путь указан
            self.image.save(file_path)  # Сохраняем изображение

    def start_color_picker(self, event):
        # Начало выбора цвета с помощью правой кнопки мыши
        self.canvas.config(cursor="cross")  # Изменяем курсор на крестик
        self.color_picker_x = event.x  # Сохраняем координаты для выбора цвета
        self.color_picker_y = event.y

    def release_color_picker(self, event):
        # Завершение выбора цвета
        pixel_color = self.image.getpixel((self.color_picker_x, self.color_picker_y))  # Получаем цвет пикселя
        self.pen_color = "#{:02x}{:02x}{:02x}".format(pixel_color[0], pixel_color[1],
                                                      pixel_color[2])  # Устанавливаем цвет кисти
        self.color_preview.config(bg=self.pen_color)  # Обновляем цвет фона метки
        self.is_eraser_active = False  # Деактивируем ластик
        self.canvas.config(cursor="")  # Возвращаем курсор к нормальному виду

    def paint_eraser(self, event):
        # Рисование с помощью ластика
        if self.last_x and self.last_y:  # Проверяем, что есть предыдущие координаты
            # Рисуем линию на холсте с цветом 'white' (ластик)
            self.canvas.create_line(self.last_x, self.last_y, event.x, event.y,
                                    width=self.brush_size, fill='white',
                                    capstyle=tk.ROUND, smooth=tk.TRUE)
            # Рисуем линию на изображении
            self.draw.line([self.last_x, self.last_y, event.x, event.y], fill='white',
                           width=self.brush_size)


def main():
    root = tk.Tk()  # Создание основного окна
    app = DrawingApp(root)  # Инициализация приложения
    root.mainloop()  # Запуск главного цикла приложения


if __name__ == "__main__":
    main()  # Запуск программы

