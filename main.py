import tkinter as tk
from tkinter import colorchooser, filedialog, messagebox
from PIL import Image, ImageDraw

''' Пользователь может рисовать на холсте, выбирать цвет и размер кисти, очищать холст и сохранять в формате PNG.
Данная программа представляет собой пример использования библиотеки TKinter
для создания графического интерфейса. Конструктор класса принимает один параметр:
- root: Это корневой виджет Tkinter, который служит контейнером для всего интерфейса приложения.'''


class DrawingApp:
    def __init__(self, root):
        self.root = root
        # Устанавливается заголовок окна приложения.
        self.root.title("Рисовалка с сохранением в PNG")

        # Создается объект изображения (self.image) с использованием библиотеки Pillow.
        # Это изображение служит виртуальным холстом, на котором происходит рисование.
        # Изначально оно заполнено белым цветом.

        self.image = Image.new("RGB", (600, 400), "white")
        # Инициализируется объект ImageDraw.Draw(self.image), который позволяет рисовать на объекте изображения
        self.draw = ImageDraw.Draw(self.image)

        # Создается виджет Canvas Tkinter, который отображает графический интерфейс для рисования.
        # Размеры холста установлены в 600x400 пикселей
        self.canvas = tk.Canvas(root, width=600, height=400, bg='white')
        self.canvas.pack()

        # Определяем все атрибуты экземпляра внутри __init__
        self.brush_size_var = tk.StringVar(value="1")  # Переменная для хранения текущего размера кисти
        self.brush_size_menu = None  # Изначально None, будет создано позже

        # Вызывается метод self.setup_ui(), который настраивает элементы управления интерфейса
        self.setup_ui()

        self.last_x, self.last_y = None, None
        self.pen_color = 'black'
        self.brush_size = 1  # Изначальный размер кисти

        self.canvas.bind('<B1-Motion>', self.paint)
        self.canvas.bind('<ButtonRelease-1>', self.reset)

    ''' Этот метод отвечает за создание и расположение виджетов управления'''

    # Кнопки "Очистить", "Выбрать цвет" и "Сохранить" позволяют пользователю очищать холст,
    # выбирать цвет кисти и сохранять текущее изображение

    def setup_ui(self):
        control_frame = tk.Frame(self.root)
        control_frame.pack(fill=tk.X)

        clear_button = tk.Button(control_frame, text="Очистить", command=self.clear_canvas)
        clear_button.pack(side=tk.LEFT)

        color_button = tk.Button(control_frame, text="Выбрать цвет", command=self.choose_color)
        color_button.pack(side=tk.LEFT)

        save_button = tk.Button(control_frame, text="Сохранить", command=self.save_image)
        save_button.pack(side=tk.LEFT)

        # Список предопределенных размеров кисти
        sizes = [1, 2, 5, 10]

        # Создание выпадающего списка для выбора размера кисти
        self.brush_size_menu = tk.OptionMenu(control_frame, self.brush_size_var, *sizes, command=self.update_brush_size)
        self.brush_size_menu.pack(side=tk.LEFT)

        # Слайдер для изменения размера кисти дает возможность выбирать толщину линии от 1 до 10 пикселей
        # self.brush_size_scale = tk.Scale(control_frame, from_=1, to=10, orient=tk.HORIZONTAL)
        # self.brush_size_scale.pack(side=tk.LEFT)

    def update_brush_size(self, size):
        self.brush_size = int(size)  # Обновление текущего размера кисти

    ''' paint - Функция вызывается при движении мыши с нажатой левой кнопкой по холсту. Она рисует
        линии на холсте Tkinter и параллельно на объекте Image из Pillow:
       - event: Событие содержит координаты мыши, которые используются для рисования.
        Линии рисуются между текущей и последней зафиксированной позициями курсора, что создает
        непрерывное изображение.'''

    # Функция при изменении кисти ползунком, который заменили
    # def paint(self, event):
    #     if self.last_x and self.last_y:
    #         self.canvas.create_line(self.last_x, self.last_y, event.x, event.y,
    #                                 width=self.brush_size_scale.get(), fill=self.pen_color,
    #                                 capstyle=tk.ROUND, smooth=tk.TRUE)
    #         self.draw.line([self.last_x, self.last_y, event.x, event.y], fill=self.pen_color,
    #                        width=self.brush_size_scale.get())

    def paint(self, event):
        if self.last_x and self.last_y:
            self.canvas.create_line(self.last_x, self.last_y, event.x, event.y,
                                    width=self.brush_size, fill=self.pen_color,
                                    capstyle=tk.ROUND, smooth=tk.TRUE)
            self.draw.line([self.last_x, self.last_y, event.x, event.y], fill=self.pen_color,
                           width=self.brush_size)

        self.last_x = event.x
        self.last_y = event.y

    ''' reset -  Сбрасывает последние координаты кисти. Это необходимо для корректного начала новой линии
    после того, как пользователь отпустил кнопку мыши и снова начал рисовать.'''

    def reset(self, event):
        self.last_x, self.last_y = None, None

    ''' clear_canvas - Очищает холст, удаляя все нарисованное, и пересоздает объекты Image и
    ImageDrawдля нового изображения.'''

    def clear_canvas(self):
        self.canvas.delete("all")
        self.image = Image.new("RGB", (600, 400), "white")
        self.draw = ImageDraw.Draw(self.image)

    ''' choose_color - Открывает стандартное диалоговое окно выбора цвета и устанавливает
    выбранный цвет как текущий для кисти.'''

    def choose_color(self):
        self.pen_color = colorchooser.askcolor(color=self.pen_color)[1]

    ''' save_image - Позволяет пользователю сохранить изображение, используя стандартное
    диалоговое окно для сохранения файла. Поддерживает только формат PNG. В случае успешного
    сохранения выводится сообщение об успешном сохранении.'''

    def save_image(self):
        file_path = filedialog.asksaveasfilename(filetypes=[('PNG files', '*.png')])
        if file_path:
            if not file_path.endswith('.png'):
                file_path += '.png'
            self.image.save(file_path)
            messagebox.showinfo("Информация", "Изображение успешно сохранено!")


def main():
    root = tk.Tk()
    app = DrawingApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
