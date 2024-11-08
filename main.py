import tkinter as tk  # Импортируем библиотеку tkinter для создания графического интерфейса
from tkinter import colorchooser, filedialog  # Импортируем модули для выбора цвета и диалогового окна сохранения файлов
from PIL import Image, ImageDraw  # Импортируем библиотеки PIL для работы с изображениями


class DrawingApp:
    def __init__(self, root):
        # Инициализация основного окна приложения
        self.root = root
        self.root.title("Рисовалка с сохранением в PNG")  # Устанавливаем заголовок окна
        self.image = Image.new("RGB", (800, 400), "white")  # Создаем новое изображение с белым фоном
        self.draw = ImageDraw.Draw(self.image)  # Создаем объект для рисования на изображении
        self.canvas = tk.Canvas(root, width=800, height=400, bg='white')  # Создаем холст для рисования
        self.canvas.pack()  # Размещаем холст в окне
        self.setup_ui()  # Настраиваем пользовательский интерфейс
        self.last_x, self.last_y = None, None  # Переменные для хранения последних координат мыши
        self.pen_color = 'black'  # Устанавливаем цвет кисти по умолчанию
        self.previous_color = self.pen_color  # Переменная для хранения предыдущего цвета кисти
        self.brush_size = 1  # Устанавливаем размер кисти по умолчанию
        self.is_eraser_active = False  # Переменная для отслеживания состояния ластика
        # Привязываем события мыши к соответствующим методам
        self.canvas.bind('<B1-Motion>', self.paint)  # Рисование при перемещении мыши с нажатой левой кнопкой
        self.canvas.bind('<ButtonRelease-1>', self.reset)  # Сброс координат при отпускании кнопки мыши
        self.canvas.bind('<Button-3>', self.start_color_picker)  # Начало выбора цвета при нажатии правой кнопки мыши
        self.canvas.bind('<ButtonRelease-3>',
                         self.release_color_picker)  # Завершение выбора цвета при отпускании правой кнопки

    def setup_ui(self):
        # Настройка пользовательского интерфейса
        control_frame = tk.Frame(self.root)  # Создаем фрейм для кнопок управления
        control_frame.pack(fill=tk.X)  # Размещаем фрейм по ширине окна
        color_button = tk.Button(control_frame, text="Выбрать цвет кисти",
                                 command=self.choose_color)  # Кнопка выбора цвета
        color_button.pack(side=tk.LEFT)  # Размещаем кнопку слева
        size_label = tk.Label(control_frame, text="Выбрать толщину кисти/ластика:")  # Метка для выбора размера
        size_label.pack(side=tk.LEFT)  # Размещаем метку слева
        self.brush_size_var = tk.StringVar(value="1")  # Переменная для хранения размера кисти
        sizes = [1, 2, 5, 10]  # Доступные размеры кисти
        # Создаем выпадающее меню для выбора размера кисти
        self.brush_size_menu = tk.OptionMenu(control_frame, self.brush_size_var, *sizes, command=self.update_brush_size)
        self.brush_size_menu.pack(side=tk.LEFT)  # Размещаем меню слева
        eraser_button = tk.Button(control_frame, text="Выбрать ластик",
                                  command=self.toggle_eraser)  # Кнопка для выбора ластика
        eraser_button.pack(side=tk.LEFT)  # Размещаем кнопку слева
        # Добавляем метку с информацией о выборе пипетки
        info_label = tk.Label(control_frame, text="Чтобы выбрать пипетку - нажмите правую кнопку мыши")
        info_label.pack(side=tk.LEFT)

        clear_button = tk.Button(control_frame, text="Очистить", command=self.clear_canvas)  # Кнопка для очистки холста
        clear_button.pack(side=tk.LEFT)  # Размещаем кнопку слева
        save_button = tk.Button(control_frame, text="Сохранить",
                                command=self.save_image)  # Кнопка для сохранения изображения
        save_button.pack(side=tk.LEFT)  # Размещаем кнопку слева

    def update_brush_size(self, size):
        # Обновление размера кисти
        self.brush_size = int(size)  # Присваиваем новый размер кисти

    def clear_canvas(self):
        # Очистка холста и изображения
        self.canvas.delete("all")  # Удаляем все элементы с холста
        self.image = Image.new("RGB", (800, 400), "white")  # Создаем новое изображение с белым фоном
        self.draw = ImageDraw.Draw(self.image)  # Создаем новый объект для рисования

    def choose_color(self):
        # Выбор цвета кисти
        if self.is_eraser_active:  # Если ластик активен
            self.toggle_eraser()  # Деактивируем ластик
        self.previous_color = self.pen_color  # Сохраняем текущий цвет кисти
        self.pen_color = colorchooser.askcolor(color=self.pen_color)[1]  # Открываем диалог выбора цвета

    def toggle_eraser(self):
        # Переключение состояния ластика
        self.is_eraser_active = not self.is_eraser_active  # Инвертируем состояние ластика
        self.pen_color = 'white' if self.is_eraser_active else self.previous_color  # Устанавливаем цвет кисти в белый, если ластик активен

    def paint(self, event):
        # Рисование на холсте
        if self.is_eraser_active:  # Если ластик активен
            self.paint_eraser(event)  # Вызываем метод рисования ластиком
        else:
            if self.last_x and self.last_y:  # Если есть предыдущие координаты
                # Рисуем линию на холсте
                self.canvas.create_line(self.last_x, self.last_y, event.x, event.y,
                                        width=self.brush_size, fill=self.pen_color,
                                        capstyle=tk.ROUND, smooth=tk.TRUE)
                # Рисуем линию на изображении
                self.draw.line([self.last_x, self.last_y, event.x, event.y], fill=self.pen_color,
                               width=self.brush_size)
        self.last_x = event.x  # Обновляем последние координаты
        self.last_y = event.y  # Обновляем последние координаты

    def reset(self, event):
        # Сброс последних координат
        self.last_x, self.last_y = None, None  # Устанавливаем координаты в None

    def save_image(self):
        # Сохранение изображения
        file_path = filedialog.asksaveasfilename(defaultextension=".png",
                                                 filetypes=[("PNG files", "*.png"),
                                                            ("All files", "*.*")])  # Открываем диалог сохранения файла
        if file_path:  # Если путь не пустой
            self.image.save(file_path)  # Сохраняем изображение по указанному пути

    def start_color_picker(self, event):
        # Начало выбора цвета с помощью правой кнопки мыши
        self.canvas.config(cursor="cross")  # Изменяем курсор на "крестик"
        self.color_picker_x = event.x  # Запоминаем координаты при нажатии правой кнопки мыши
        self.color_picker_y = event.y

    def release_color_picker(self, event):
        # Завершение выбора цвета
        pixel_color = self.image.getpixel((self.color_picker_x, self.color_picker_y))  # Получаем цвет пикселя
        self.pen_color = "#{:02x}{:02x}{:02x}".format(pixel_color[0], pixel_color[1],
                                                      pixel_color[2])  # Устанавливаем цвет кисти
        print(f"Выбранный цвет: {self.pen_color}")  # Выводим выбранный цвет в консоль
        self.is_eraser_active = False  # Деактивируем ластик после выбора цвета
        self.canvas.config(cursor="")  # Возвращаем курсор в исходное состояние

    def paint_eraser(self, event):
        # Рисование с помощью ластика
        if self.last_x and self.last_y:  # Если есть предыдущие координаты
            # Рисуем линию на холсте с белым цветом
            self.canvas.create_line(self.last_x, self.last_y, event.x, event.y,
                                    width=self.brush_size, fill='white',
                                    capstyle=tk.ROUND, smooth=tk.TRUE)
            # Рисуем линию на изображении с белым цветом
            self.draw.line([self.last_x, self.last_y, event.x, event.y], fill='white',
                           width=self.brush_size)


def main():
    root = tk.Tk()  # Создаем основное окно приложения
    app = DrawingApp(root)  # Создаем экземпляр класса DrawingApp
    root.mainloop()  # Запускаем главный цикл приложения


if __name__ == "__main__":
    main()  # Запускаем приложение
