"""
Meme Generator Pro - Расширенная версия
Лабораторная работа №8 (уровень Medium)
Добавлены: выбор шрифта, прозрачность, поворот текста, фильтры, история действий
"""

import tkinter as tk
from tkinter import ttk, filedialog, colorchooser, messagebox
from PIL import Image, ImageDraw, ImageFont, ImageTk, ImageEnhance
import os
from collections import deque

class MemeGeneratorPro:
    def __init__(self, root):
        self.root = root
        self.root.title("Meme Generator Pro - Расширенная версия")
        self.root.geometry("1100x750")
        
        # Переменные
        self.image_path = None
        self.original_image = None
        self.current_image = None
        self.display_image = None
        self.image_tk = None
        self.font_path = "arial.ttf"
        
        # История действий
        self.history = deque(maxlen=20)
        self.history_index = -1
        
        # Настройки текста
        self.top_text = tk.StringVar(value="ВЕРХНИЙ ТЕКСТ")
        self.bottom_text = tk.StringVar(value="НИЖНИЙ ТЕКСТ")
        self.font_size = tk.IntVar(value=40)
        self.text_color = "#FFFFFF"
        self.outline_color = "#000000"
        self.shadow_enabled = tk.BooleanVar(value=False)
        self.text_opacity = tk.IntVar(value=100)
        self.text_rotation = tk.IntVar(value=0)
        self.text_position = tk.StringVar(value="center")
        self.custom_x = tk.IntVar(value=0)
        self.custom_y = tk.IntVar(value=0)
        
        # Настройка интерфейса
        self.setup_ui()
        self.setup_menu()
        self.setup_shortcuts()
        
    def setup_menu(self):
        """Создание главного меню"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # Файл
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Файл", menu=file_menu)
        file_menu.add_command(label="Загрузить изображение", command=self.load_image, accelerator="Ctrl+O")
        file_menu.add_command(label="Сохранить как PNG", command=lambda: self.save_meme("png"), accelerator="Ctrl+S")
        file_menu.add_command(label="Сохранить как JPG", command=lambda: self.save_meme("jpg"))
        file_menu.add_separator()
        file_menu.add_command(label="Выход", command=self.root.quit, accelerator="Ctrl+Q")
        
        # Правка
        edit_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Правка", menu=edit_menu)
        edit_menu.add_command(label="Отменить", command=self.undo, accelerator="Ctrl+Z")
        edit_menu.add_command(label="Повторить", command=self.redo, accelerator="Ctrl+Y")
        
        # Изображение
        image_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Изображение", menu=image_menu)
        image_menu.add_command(label="Ч/Б фильтр", command=lambda: self.apply_filter("black_white"))
        image_menu.add_command(label="Сепия", command=lambda: self.apply_filter("sepia"))
        image_menu.add_command(label="Повысить контраст", command=lambda: self.apply_filter("contrast"))
        image_menu.add_command(label="Сбросить фильтры", command=self.reset_image)
        
    def setup_shortcuts(self):
        """Настройка горячих клавиш"""
        self.root.bind("<Control-o>", lambda e: self.load_image())
        self.root.bind("<Control-s>", lambda e: self.save_meme("png"))
        self.root.bind("<Control-z>", lambda e: self.undo())
        self.root.bind("<Control-y>", lambda e: self.redo())
        self.root.bind("<Control-q>", lambda e: self.root.quit())
        
    def setup_ui(self):
        """Создание расширенного интерфейса"""
        # Основной контейнер с вкладками
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Вкладка "Основные"
        self.create_main_tab()
        
        # Вкладка "Расширенные настройки"
        self.create_advanced_tab()
        
        # Вкладка "Фильтры"
        self.create_filters_tab()
        
        # Статус бар
        self.status_var = tk.StringVar(value="Готов к работе")
        status_bar = ttk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
    def create_main_tab(self):
        """Основная вкладка с управлением"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Основные")
        
        # Левая панель управления
        control_frame = ttk.LabelFrame(tab, text="Управление", padding="10")
        control_frame.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)
        
        # Загрузка
        ttk.Button(control_frame, text="Загрузить изображение", 
                  command=self.load_image, width=25).pack(pady=5)
        
        ttk.Separator(control_frame, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=10)
        
        # Текст
        ttk.Label(control_frame, text="Верхний текст:").pack(anchor=tk.W, pady=2)
        ttk.Entry(control_frame, textvariable=self.top_text, width=30).pack(pady=2)
        
        ttk.Label(control_frame, text="Нижний текст:").pack(anchor=tk.W, pady=2)
        ttk.Entry(control_frame, textvariable=self.bottom_text, width=30).pack(pady=2)
        
        ttk.Label(control_frame, text="Размер шрифта:").pack(anchor=tk.W, pady=2)
        ttk.Scale(control_frame, from_=10, to=120, variable=self.font_size, 
                 orient=tk.HORIZONTAL, command=lambda x: self.preview_meme()).pack(fill=tk.X, pady=2)
        
        # Цвета
        color_frame = ttk.Frame(control_frame)
        color_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(color_frame, text="Цвет текста", command=self.choose_text_color).pack(side=tk.LEFT, padx=2)
        self.text_color_label = tk.Label(color_frame, text="    ", bg=self.text_color, relief=tk.RIDGE)
        self.text_color_label.pack(side=tk.LEFT, padx=2)
        
        ttk.Button(color_frame, text="Цвет обводки", command=self.choose_outline_color).pack(side=tk.LEFT, padx=2)
        self.outline_color_label = tk.Label(color_frame, text="    ", bg=self.outline_color, relief=tk.RIDGE)
        self.outline_color_label.pack(side=tk.LEFT, padx=2)
        
        # Кнопки действий
        ttk.Separator(control_frame, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=10)
        
        btn_frame = ttk.Frame(control_frame)
        btn_frame.pack(fill=tk.X)
        
        ttk.Button(btn_frame, text="Предпросмотр", command=self.preview_meme).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_frame, text="Сохранить", command=lambda: self.save_meme("png")).pack(side=tk.LEFT, padx=2)
        
        # Правая область - предпросмотр
        preview_frame = ttk.LabelFrame(tab, text="Предпросмотр", padding="10")
        preview_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.canvas = tk.Canvas(preview_frame, width=550, height=450, bg="#2b2b2b")
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
    def create_advanced_tab(self):
        """Вкладка расширенных настроек"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Расширенные")
        
        # Шрифты
        font_frame = ttk.LabelFrame(tab, text="Шрифты", padding="10")
        font_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(font_frame, text="Выберите шрифт:").pack(side=tk.LEFT, padx=5)
        ttk.Button(font_frame, text="Загрузить шрифт (.ttf)", command=self.load_font).pack(side=tk.LEFT, padx=5)
        
        # Эффекты текста
        effect_frame = ttk.LabelFrame(tab, text="Эффекты текста", padding="10")
        effect_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Checkbutton(effect_frame, text="Включить тень", variable=self.shadow_enabled, 
                       command=lambda: self.preview_meme()).pack(anchor=tk.W)
        
        ttk.Label(effect_frame, text="Прозрачность текста (%):").pack(anchor=tk.W)
        ttk.Scale(effect_frame, from_=0, to=100, variable=self.text_opacity,
                 orient=tk.HORIZONTAL, command=lambda x: self.preview_meme()).pack(fill=tk.X)
        
        ttk.Label(effect_frame, text="Поворот текста (градусы):").pack(anchor=tk.W)
        ttk.Scale(effect_frame, from_=-180, to=180, variable=self.text_rotation,
                 orient=tk.HORIZONTAL, command=lambda x: self.preview_meme()).pack(fill=tk.X)
        
        # Позиционирование
        pos_frame = ttk.LabelFrame(tab, text="Позиционирование текста", padding="10")
        pos_frame.pack(fill=tk.X, padx=10, pady=5)
        
        positions = [("Центр", "center"), ("Лево", "left"), ("Право", "right"), ("Произвольно", "custom")]
        for text, value in positions:
            ttk.Radiobutton(pos_frame, text=text, variable=self.text_position, 
                           value=value, command=lambda: self.preview_meme()).pack(anchor=tk.W)
        
        custom_frame = ttk.Frame(pos_frame)
        custom_frame.pack(fill=tk.X, pady=5)
        ttk.Label(custom_frame, text="X:").pack(side=tk.LEFT)
        ttk.Spinbox(custom_frame, from_=0, to=1000, textvariable=self.custom_x, 
                   width=5, command=lambda: self.preview_meme()).pack(side=tk.LEFT, padx=5)
        ttk.Label(custom_frame, text="Y:").pack(side=tk.LEFT)
        ttk.Spinbox(custom_frame, from_=0, to=1000, textvariable=self.custom_y,
                   width=5, command=lambda: self.preview_meme()).pack(side=tk.LEFT, padx=5)
        
    def create_filters_tab(self):
        """Вкладка фильтров"""
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Фильтры")
        
        filter_frame = ttk.Frame(tab)
        filter_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        filters = [
            ("Оригинал", self.reset_image),
            ("Чёрно-белый", lambda: self.apply_filter("black_white")),
            ("Сепия", lambda: self.apply_filter("sepia")),
            ("Повысить контраст", lambda: self.apply_filter("contrast")),
            ("Понизить контраст", lambda: self.apply_filter("low_contrast")),
            ("Повысить яркость", lambda: self.apply_filter("brightness")),
            ("Затемнить", lambda: self.apply_filter("darken")),
        ]
        
        row, col = 0, 0
        for name, command in filters:
            btn = ttk.Button(filter_frame, text=name, command=command, width=25)
            btn.grid(row=row, column=col, padx=5, pady=5)
            col += 1
            if col > 2:
                col = 0
                row += 1
                
    def save_to_history(self):
        """Сохранение текущего состояния в историю"""
        if self.current_image:
            self.history.append(self.current_image.copy())
            self.history_index = len(self.history) - 1
            
    def undo(self):
        """Отмена последнего действия"""
        if self.history_index > 0:
            self.history_index -= 1
            self.current_image = self.history[self.history_index].copy()
            self.preview_meme()
            self.status_var.set("Отменено последнее действие")
            
    def redo(self):
        """Повтор отменённого действия"""
        if self.history_index < len(self.history) - 1:
            self.history_index += 1
            self.current_image = self.history[self.history_index].copy()
            self.preview_meme()
            self.status_var.set("Повторено действие")
            
    def load_image(self):
        file_path = filedialog.askopenfilename(
            title="Выберите изображение",
            filetypes=[("Image files", "*.png *.jpg *.jpeg *.bmp *.gif")]
        )
        if file_path:
            self.image_path = file_path
            self.original_image = Image.open(file_path)
            self.current_image = self.original_image.copy()
            self.save_to_history()
            self.status_var.set(f"Загружено: {os.path.basename(file_path)}")
            self.preview_meme()
            
    def load_font(self):
        file_path = filedialog.askopenfilename(
            title="Выберите шрифт (.ttf)",
            filetypes=[("TTF files", "*.ttf")]
        )
        if file_path:
            self.font_path = file_path
            self.status_var.set(f"Загружен шрифт: {os.path.basename(file_path)}")
            self.preview_meme()
            
    def choose_text_color(self):
        color = colorchooser.askcolor(title="Выберите цвет текста", initialcolor=self.text_color)
        if color[1]:
            self.text_color = color[1]
            self.text_color_label.configure(bg=self.text_color)
            self.preview_meme()
            
    def choose_outline_color(self):
        color = colorchooser.askcolor(title="Выберите цвет обводки", initialcolor=self.outline_color)
        if color[1]:
            self.outline_color = color[1]
            self.outline_color_label.configure(bg=self.outline_color)
            self.preview_meme()
            
    def apply_filter(self, filter_type):
        if not self.current_image:
            return
            
        self.save_to_history()
        img = self.current_image.convert("RGBA")
        
        if filter_type == "black_white":
            self.current_image = img.convert("L").convert("RGBA")
            
        elif filter_type == "sepia":
            pixels = img.load()
            for i in range(img.size[0]):
                for j in range(img.size[1]):
                    r, g, b, a = pixels[i, j]
                    tr = int(0.393 * r + 0.769 * g + 0.189 * b)
                    tg = int(0.349 * r + 0.686 * g + 0.168 * b)
                    tb = int(0.272 * r + 0.534 * g + 0.131 * b)
                    pixels[i, j] = (min(tr, 255), min(tg, 255), min(tb, 255), a)
            self.current_image = img
            
        elif filter_type == "contrast":
            enhancer = ImageEnhance.Contrast(img)
            self.current_image = enhancer.enhance(1.5)
            
        elif filter_type == "low_contrast":
            enhancer = ImageEnhance.Contrast(img)
            self.current_image = enhancer.enhance(0.5)
            
        elif filter_type == "brightness":
            enhancer = ImageEnhance.Brightness(img)
            self.current_image = enhancer.enhance(1.3)
            
        elif filter_type == "darken":
            enhancer = ImageEnhance.Brightness(img)
            self.current_image = enhancer.enhance(0.5)
            
        self.preview_meme()
        self.status_var.set(f"Применён фильтр: {filter_type}")
        
    def reset_image(self):
        if not self.original_image:
            return
        self.save_to_history()
        self.current_image = self.original_image.copy()
        self.preview_meme()
        self.status_var.set("Фильтры сброшены")
        
    def draw_text_with_effects(self, draw, text, position, font, image_width, image_height):
        """Рисование текста с эффектами"""
        x, y = position
        
        # Создаём отдельное изображение для текста
        text_img = Image.new("RGBA", (image_width, image_height), (0, 0, 0, 0))
        text_draw = ImageDraw.Draw(text_img)
        
        # Рисуем тень если включена
        if self.shadow_enabled.get():
            for dx, dy in [(2, 2), (1, 2), (2, 1)]:
                text_draw.text((x + dx, y + dy), text, font=font, fill="#000000")
        
        # Рисуем обводку
        outline_width = 2
        for dx in range(-outline_width, outline_width + 1):
            for dy in range(-outline_width, outline_width + 1):
                if dx != 0 or dy != 0:
                    text_draw.text((x + dx, y + dy), text, font=font, fill=self.outline_color)
        
        # Основной текст
        text_draw.text((x, y), text, font=font, fill=self.text_color)
        
        # Применяем поворот
        if self.text_rotation.get() != 0:
            text_img = text_img.rotate(self.text_rotation.get(), expand=True, center=(x, y))
        
        # Применяем прозрачность
        if self.text_opacity.get() < 100:
            alpha = int(255 * self.text_opacity.get() / 100)
            r, g, b, a = text_img.split()
            a = a.point(lambda p: min(p, alpha))
            text_img = Image.merge("RGBA", (r, g, b, a))
        
        # Накладываем текст
        draw._image.paste(text_img, (0, 0), text_img)
        
    def preview_meme(self):
        if not self.current_image:
            messagebox.showwarning("Предупреждение", "Сначала загрузите изображение!")
            return
            
        # Создаём копию для предпросмотра
        preview_img = self.current_image.copy()
        
        # Масштабируем для отображения
        max_width = 550
        max_height = 450
        ratio = min(max_width / preview_img.width, max_height / preview_img.height)
        new_size = (int(preview_img.width * ratio), int(preview_img.height * ratio))
        preview_img = preview_img.resize(new_size, Image.Resampling.LANCZOS)
        
        draw = ImageDraw.Draw(preview_img)
        
        # Загружаем шрифт
        try:
            font = ImageFont.truetype(self.font_path, self.font_size.get())
        except:
            font = ImageFont.load_default()
        
        def get_text_position(text, font, img_width, img_height, is_top):
            bbox = draw.textbbox((0, 0), text, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            
            pos_type = self.text_position.get()
            
            if pos_type == "center":
                x = (img_width - text_width) // 2
            elif pos_type == "left":
                x = 10
            elif pos_type == "right":
                x = img_width - text_width - 10
            elif pos_type == "custom":
                x = self.custom_x.get()
            else:
                x = (img_width - text_width) // 2
            
            if is_top:
                y = 10
            else:
                y = img_height - text_height - 10
            
            return (x, y)
        
        # Верхний текст
        top_text = self.top_text.get().upper()
        if top_text:
            pos = get_text_position(top_text, font, preview_img.width, preview_img.height, True)
            self.draw_text_with_effects(draw, top_text, pos, font, preview_img.width, preview_img.height)
        
        # Нижний текст
        bottom_text = self.bottom_text.get().upper()
        if bottom_text:
            pos = get_text_position(bottom_text, font, preview_img.width, preview_img.height, False)
            self.draw_text_with_effects(draw, bottom_text, pos, font, preview_img.width, preview_img.height)
        
        # Отображаем на канвасе
        self.image_tk = ImageTk.PhotoImage(preview_img)
        self.canvas.delete("all")
        self.canvas.config(width=preview_img.width, height=preview_img.height)
        self.canvas.create_image(preview_img.width//2, preview_img.height//2, image=self.image_tk, anchor="center")
        
    def save_meme(self, format_type="png"):
        if not self.current_image:
            messagebox.showwarning("Предупреждение", "Сначала загрузите изображение!")
            return
            
        file_path = filedialog.asksaveasfilename(
            defaultextension=f".{format_type}",
            filetypes=[(f"{format_type.upper()} files", f"*.{format_type}")]
        )
        
        if file_path:
            # Создаём финальное изображение
            meme_img = self.current_image.copy()
            draw = ImageDraw.Draw(meme_img)
            
            try:
                font = ImageFont.truetype(self.font_path, self.font_size.get())
            except:
                font = ImageFont.load_default()
            
            def get_final_position(text, font, img_width, img_height, is_top):
                bbox = draw.textbbox((0, 0), text, font=font)
                text_width = bbox[2] - bbox[0]
                text_height = bbox[3] - bbox[1]
                
                pos_type = self.text_position.get()
                
                if pos_type == "center":
                    x = (img_width - text_width) // 2
                elif pos_type == "left":
                    x = 10
                elif pos_type == "right":
                    x = img_width - text_width - 10
                elif pos_type == "custom":
                    x = self.custom_x.get()
                else:
                    x = (img_width - text_width) // 2
                
                if is_top:
                    y = 10
                else:
                    y = img_height - text_height - 10
                
                return (x, y)
            
            top_text = self.top_text.get().upper()
            if top_text:
                pos = get_final_position(top_text, font, meme_img.width, meme_img.height, True)
                self.draw_text_with_effects(draw, top_text, pos, font, meme_img.width, meme_img.height)
            
            bottom_text = self.bottom_text.get().upper()
            if bottom_text:
                pos = get_final_position(bottom_text, font, meme_img.width, meme_img.height, False)
                self.draw_text_with_effects(draw, bottom_text, pos, font, meme_img.width, meme_img.height)
            
            # Сохраняем
            meme_img.save(file_path)
            self.status_var.set(f"Сохранено: {os.path.basename(file_path)}")
            messagebox.showinfo("Успех", f"Мем сохранён в:\n{file_path}")


if __name__ == "__main__":
    root = tk.Tk()
    app = MemeGeneratorPro(root)
    root.mainloop()