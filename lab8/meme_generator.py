import tkinter as tk
from tkinter import ttk, filedialog, colorchooser, messagebox
from PIL import Image, ImageDraw, ImageFont, ImageTk
import os

class MemeGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Meme Generator")
        self.root.geometry("900x700")
        self.root.resizable(True, True)
        
        # Переменные
        self.image_path = None
        self.original_image = None
        self.display_image = None
        self.image_tk = None
        self.font_path = "arial.ttf"
        
        # Настройки текста
        self.top_text = tk.StringVar(value="ВЕРХНИЙ ТЕКСТ")
        self.bottom_text = tk.StringVar(value="НИЖНИЙ ТЕКСТ")
        self.font_size = tk.IntVar(value=40)
        self.text_color = "#FFFFFF"
        self.outline_color = "#000000"
        
        self.setup_ui()
        
    def setup_ui(self):
        # Главный фрейм
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Панель управления (левая)
        control_frame = ttk.LabelFrame(main_frame, text="Управление", padding="10")
        control_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5)
        
        # Кнопка загрузки изображения
        ttk.Button(control_frame, text="📁 Загрузить изображение", 
                  command=self.load_image).grid(row=0, column=0, columnspan=2, pady=5, sticky=tk.W)
        
        # Верхний текст
        ttk.Label(control_frame, text="Верхний текст:").grid(row=1, column=0, sticky=tk.W, pady=2)
        ttk.Entry(control_frame, textvariable=self.top_text, width=25).grid(row=1, column=1, pady=2)
        
        # Нижний текст
        ttk.Label(control_frame, text="Нижний текст:").grid(row=2, column=0, sticky=tk.W, pady=2)
        ttk.Entry(control_frame, textvariable=self.bottom_text, width=25).grid(row=2, column=1, pady=2)
        
        # Размер шрифта
        ttk.Label(control_frame, text="Размер шрифта:").grid(row=3, column=0, sticky=tk.W, pady=2)
        size_spin = ttk.Spinbox(control_frame, from_=10, to=120, textvariable=self.font_size, width=23)
        size_spin.grid(row=3, column=1, pady=2)
        
        # Цвет текста
        ttk.Button(control_frame, text="🎨 Цвет текста", command=self.choose_text_color).grid(row=4, column=0, pady=2, sticky=tk.W)
        self.text_color_label = ttk.Label(control_frame, text="████", background="white", foreground="white")
        self.text_color_label.grid(row=4, column=1, pady=2, sticky=tk.W)
        
        # Цвет обводки
        ttk.Button(control_frame, text="✒️ Цвет обводки", command=self.choose_outline_color).grid(row=5, column=0, pady=2, sticky=tk.W)
        self.outline_color_label = ttk.Label(control_frame, text="████", background="black", foreground="black")
        self.outline_color_label.grid(row=5, column=1, pady=2, sticky=tk.W)
        
        # Кнопки действий
        ttk.Button(control_frame, text="👁️ Предпросмотр", command=self.preview_meme).grid(row=6, column=0, pady=5, sticky=tk.W)
        ttk.Button(control_frame, text="💾 Сохранить мем", command=self.save_meme).grid(row=6, column=1, pady=5, sticky=tk.W)
        
        # Область предпросмотра (правая)
        preview_frame = ttk.LabelFrame(main_frame, text="Предпросмотр", padding="10")
        preview_frame.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5)
        
        self.canvas = tk.Canvas(preview_frame, width=500, height=400, bg="#2b2b2b")
        self.canvas.pack()
        
        self.preview_label = ttk.Label(preview_frame, text="Загрузите изображение")
        self.preview_label.pack()
        
        # Статус бар
        self.status_var = tk.StringVar(value="Готов к работе")
        status_bar = ttk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.grid(row=1, column=0, sticky=(tk.W, tk.E))
        
        # Настройка весов
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(0, weight=1)
        
    def load_image(self):
        file_path = filedialog.askopenfilename(
            title="Выберите изображение",
            filetypes=[("Image files", "*.png *.jpg *.jpeg *.bmp *.gif")]
        )
        if file_path:
            self.image_path = file_path
            self.original_image = Image.open(file_path)
            self.display_image = self.original_image.copy()
            self.status_var.set(f"Загружено: {os.path.basename(file_path)}")
            self.preview_meme()
            
    def choose_text_color(self):
        color = colorchooser.askcolor(title="Выберите цвет текста", initialcolor=self.text_color)
        if color[1]:
            self.text_color = color[1]
            self.text_color_label.configure(background=self.text_color, foreground=self.text_color)
            if self.image_path:
                self.preview_meme()
                
    def choose_outline_color(self):
        color = colorchooser.askcolor(title="Выберите цвет обводки", initialcolor=self.outline_color)
        if color[1]:
            self.outline_color = color[1]
            self.outline_color_label.configure(background=self.outline_color, foreground=self.outline_color)
            if self.image_path:
                self.preview_meme()
    
    def draw_text_with_outline(self, draw, text, position, font, text_color, outline_color, outline_width=2):
        x, y = position
        # Рисуем обводку
        for dx in range(-outline_width, outline_width + 1):
            for dy in range(-outline_width, outline_width + 1):
                if dx != 0 or dy != 0:
                    draw.text((x + dx, y + dy), text, font=font, fill=outline_color)
        # Рисуем основной текст
        draw.text((x, y), text, font=font, fill=text_color)
        
    def preview_meme(self):
        if not self.original_image:
            messagebox.showwarning("Предупреждение", "Сначала загрузите изображение!")
            return
            
        # Создаем копию для предпросмотра (изменяем размер для отображения)
        preview_img = self.original_image.copy()
        
        # Масштабируем для предпросмотра
        max_width = 500
        max_height = 400
        ratio = min(max_width / preview_img.width, max_height / preview_img.height)
        new_size = (int(preview_img.width * ratio), int(preview_img.height * ratio))
        preview_img = preview_img.resize(new_size, Image.Resampling.LANCZOS)
        
        # Рисуем мем
        draw = ImageDraw.Draw(preview_img)
        
        # Загружаем шрифт
        try:
            font = ImageFont.truetype(self.font_path, self.font_size.get())
        except:
            font = ImageFont.load_default()
        
        # Верхний текст
        top_text = self.top_text.get().upper()
        if top_text:
            bbox = draw.textbbox((0, 0), top_text, font=font)
            text_width = bbox[2] - bbox[0]
            x = (preview_img.width - text_width) // 2
            y = 10
            self.draw_text_with_outline(draw, top_text, (x, y), font, self.text_color, self.outline_color)
        
        # Нижний текст
        bottom_text = self.bottom_text.get().upper()
        if bottom_text:
            bbox = draw.textbbox((0, 0), bottom_text, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            x = (preview_img.width - text_width) // 2
            y = preview_img.height - text_height - 10
            self.draw_text_with_outline(draw, bottom_text, (x, y), font, self.text_color, self.outline_color)
        
        # Отображаем на канвасе
        self.image_tk = ImageTk.PhotoImage(preview_img)
        self.canvas.delete("all")
        self.canvas.config(width=preview_img.width, height=preview_img.height)
        self.canvas.create_image(preview_img.width//2, preview_img.height//2, image=self.image_tk, anchor="center")
        
    def save_meme(self):
        if not self.original_image:
            messagebox.showwarning("Предупреждение", "Сначала загрузите изображение!")
            return
            
        file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg"), ("All files", "*.*")]
        )
        if file_path:
            # Создаем финальное изображение в оригинальном размере
            meme_img = self.original_image.copy()
            draw = ImageDraw.Draw(meme_img)
            
            try:
                font = ImageFont.truetype(self.font_path, self.font_size.get())
            except:
                font = ImageFont.load_default()
                
            # Верхний текст
            top_text = self.top_text.get().upper()
            if top_text:
                bbox = draw.textbbox((0, 0), top_text, font=font)
                text_width = bbox[2] - bbox[0]
                x = (meme_img.width - text_width) // 2
                y = 10
                self.draw_text_with_outline(draw, top_text, (x, y), font, self.text_color, self.outline_color)
            
            # Нижний текст
            bottom_text = self.bottom_text.get().upper()
            if bottom_text:
                bbox = draw.textbbox((0, 0), bottom_text, font=font)
                text_width = bbox[2] - bbox[0]
                text_height = bbox[3] - bbox[1]
                x = (meme_img.width - text_width) // 2
                y = meme_img.height - text_height - 10
                self.draw_text_with_outline(draw, bottom_text, (x, y), font, self.text_color, self.outline_color)
            
            # Сохраняем
            meme_img.save(file_path)
            self.status_var.set(f"Сохранено: {os.path.basename(file_path)}")
            messagebox.showinfo("Успех", f"Мем сохранён в:\n{file_path}")

if __name__ == "__main__":
    root = tk.Tk()
    app = MemeGenerator(root)
    root.mainloop()