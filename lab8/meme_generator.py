import tkinter as tk
from tkinter import filedialog, messagebox, ttk, colorchooser
from PIL import Image, ImageDraw, ImageFont, ImageTk
import os
import random
from datetime import datetime

class MemeGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Meme Generator - Создай свой мем!")
        self.root.geometry("1200x700")
        self.root.configure(bg='#2b2b2b')
        
        # Переменные
        self.image_path = None
        self.original_image = None
        self.edited_image = None
        self.top_text = tk.StringVar(value="ВЕРХНИЙ ТЕКСТ")
        self.bottom_text = tk.StringVar(value="НИЖНИЙ ТЕКСТ")
        self.font_size = tk.IntVar(value=40)
        self.text_color = "#FFFFFF"
        self.outline_color = "#000000"
        
        # Цветовая схема
        self.bg_color = "#2b2b2b"
        self.fg_color = "#ffffff"
        self.accent_color = "#ff6b35"
        
        self.setup_ui()
        
    def setup_ui(self):
        # Главный фрейм
        main_frame = tk.Frame(self.root, bg=self.bg_color)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Левый фрейм - панель управления
        control_frame = tk.Frame(main_frame, bg=self.bg_color, width=300)
        control_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        control_frame.pack_propagate(False)
        
        # Правый фрейм - область预览
        preview_frame = tk.Frame(main_frame, bg=self.bg_color)
        preview_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Заголовок
        title_label = tk.Label(control_frame, text="🎭 ГЕНЕРАТОР МЕМОВ", 
                               font=("Arial", 20, "bold"), 
                               bg=self.bg_color, fg=self.accent_color)
        title_label.pack(pady=10)
        
        # Кнопка загрузки изображения
        load_btn = tk.Button(control_frame, text="📁 Загрузить изображение", 
                            font=("Arial", 12), bg=self.accent_color, fg="white",
                            command=self.load_image, cursor="hand2", height=2)
        load_btn.pack(fill=tk.X, pady=5)
        
        # Кнопка выбора шаблона
        template_btn = tk.Button(control_frame, text="🎨 Выбрать шаблон", 
                                font=("Arial", 12), bg="#4a4a4a", fg="white",
                                command=self.show_templates, cursor="hand2", height=2)
        template_btn.pack(fill=tk.X, pady=5)
        
        # Разделитель
        separator = ttk.Separator(control_frame, orient='horizontal')
        separator.pack(fill=tk.X, pady=10)
        
        # Верхний текст
        tk.Label(control_frame, text="ВЕРХНИЙ ТЕКСТ:", font=("Arial", 11, "bold"),
                bg=self.bg_color, fg=self.fg_color).pack(anchor=tk.W, pady=(10,0))
        self.top_entry = tk.Entry(control_frame, textvariable=self.top_text, 
                                  font=("Arial", 10), bg="#3a3a3a", fg="white",
                                  insertbackground="white")
        self.top_entry.pack(fill=tk.X, pady=5)
        
        # Нижний текст
        tk.Label(control_frame, text="НИЖНИЙ ТЕКСТ:", font=("Arial", 11, "bold"),
                bg=self.bg_color, fg=self.fg_color).pack(anchor=tk.W, pady=(10,0))
        self.bottom_entry = tk.Entry(control_frame, textvariable=self.bottom_text,
                                     font=("Arial", 10), bg="#3a3a3a", fg="white",
                                     insertbackground="white")
        self.bottom_entry.pack(fill=tk.X, pady=5)
        
        # Размер шрифта
        tk.Label(control_frame, text="РАЗМЕР ШРИФТА:", font=("Arial", 11, "bold"),
                bg=self.bg_color, fg=self.fg_color).pack(anchor=tk.W, pady=(10,0))
        self.font_scale = tk.Scale(control_frame, from_=20, to=100, 
                                   orient=tk.HORIZONTAL, variable=self.font_size,
                                   bg=self.bg_color, fg=self.fg_color,
                                   highlightbackground=self.bg_color)
        self.font_scale.pack(fill=tk.X, pady=5)
        
        # Цвет текста
        tk.Label(control_frame, text="ЦВЕТ ТЕКСТА:", font=("Arial", 11, "bold"),
                bg=self.bg_color, fg=self.fg_color).pack(anchor=tk.W, pady=(10,0))
        color_frame = tk.Frame(control_frame, bg=self.bg_color)
        color_frame.pack(fill=tk.X, pady=5)
        
        self.color_btn = tk.Button(color_frame, text="Выбрать цвет", 
                                   bg=self.text_color, command=self.choose_color)
        self.color_btn.pack(side=tk.LEFT, padx=5)
        
        self.color_label = tk.Label(color_frame, text="#FFFFFF", 
                                    bg=self.bg_color, fg=self.fg_color)
        self.color_label.pack(side=tk.LEFT, padx=5)
        
        # Контур текста
        outline_check = tk.Checkbutton(control_frame, text="Добавить контур",
                                       variable=tk.BooleanVar(value=True),
                                       command=self.toggle_outline,
                                       bg=self.bg_color, fg=self.fg_color,
                                       selectcolor=self.bg_color)
        outline_check.pack(anchor=tk.W, pady=5)
        
        # Кнопки действий
        action_frame = tk.Frame(control_frame, bg=self.bg_color)
        action_frame.pack(fill=tk.X, pady=20)
        
        generate_btn = tk.Button(action_frame, text="✨ СГЕНЕРИРОВАТЬ МЕМ", 
                                font=("Arial", 12, "bold"), bg=self.accent_color, 
                                fg="white", command=self.generate_meme, height=2)
        generate_btn.pack(fill=tk.X, pady=5)
        
        save_btn = tk.Button(action_frame, text="💾 СОХРАНИТЬ МЕМ", 
                            font=("Arial", 12), bg="#4CAF50", fg="white",
                            command=self.save_meme, height=2)
        save_btn.pack(fill=tk.X, pady=5)
        
        # Кнопка экспорта в GIF
        gif_btn = tk.Button(action_frame, text="🎬 СОЗДАТЬ GIF (анимация)", 
                           font=("Arial", 10), bg="#9C27B0", fg="white",
                           command=self.create_gif, height=1)
        gif_btn.pack(fill=tk.X, pady=5)
        
        reset_btn = tk.Button(action_frame, text="🔄 СБРОСИТЬ", 
                             font=("Arial", 10), bg="#f44336", fg="white",
                             command=self.reset_image, height=1)
        reset_btn.pack(fill=tk.X, pady=5)
        
        # Область预览 изображения
        self.preview_label = tk.Label(preview_frame, bg=self.bg_color, 
                                      text="Загрузите изображение\nили выберите шаблон",
                                      font=("Arial", 14), fg="#888888")
        self.preview_label.pack(expand=True, fill=tk.BOTH)
        
        # Создаём папки
        os.makedirs("memes", exist_ok=True)
        os.makedirs("templates", exist_ok=True)
        
    def load_image(self):
        file_path = filedialog.askopenfilename(
            title="Выберите изображение",
            filetypes=[("Image files", "*.png *.jpg *.jpeg *.gif *.bmp")]
        )
        if file_path:
            self.image_path = file_path
            self.original_image = Image.open(file_path)
            self.show_preview(self.original_image)
            
    def show_templates(self):
        # Создаём демо-шаблоны если их нет
        self.create_demo_templates()
        
        # Окно выбора шаблона
        template_window = tk.Toplevel(self.root)
        template_window.title("Выберите шаблон")
        template_window.geometry("600x400")
        template_window.configure(bg=self.bg_color)
        
        templates = [f for f in os.listdir("templates") if f.endswith(('.png', '.jpg', '.jpeg'))]
        
        if not templates:
            tk.Label(template_window, text="Нет доступных шаблонов", 
                    bg=self.bg_color, fg=self.fg_color, font=("Arial", 12)).pack(expand=True)
            return
            
        # Canvas с прокруткой
        canvas = tk.Canvas(template_window, bg=self.bg_color, highlightthickness=0)
        scrollbar = tk.Scrollbar(template_window, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.bg_color)
        
        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        for i, template in enumerate(templates):
            frame = tk.Frame(scrollable_frame, bg=self.bg_color)
            frame.pack(pady=10)
            
            # Загружаем миниатюру
            img = Image.open(f"templates/{template}")
            img.thumbnail((200, 150))
            photo = ImageTk.PhotoImage(img)
            
            label = tk.Label(frame, image=photo, bg=self.bg_color, cursor="hand2")
            label.image = photo
            label.pack(side=tk.LEFT, padx=10)
            
            info_frame = tk.Frame(frame, bg=self.bg_color)
            info_frame.pack(side=tk.LEFT, padx=10)
            
            tk.Label(info_frame, text=template.replace('_', ' ').replace('.jpg', ''), 
                    bg=self.bg_color, fg=self.fg_color, font=("Arial", 12)).pack(anchor=tk.W)
            
            tk.Button(info_frame, text="Выбрать", 
                     command=lambda t=template: self.load_template(t, template_window),
                     bg=self.accent_color, fg="white").pack(pady=5)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
    def load_template(self, template_name, window):
        self.image_path = f"templates/{template_name}"
        self.original_image = Image.open(self.image_path)
        self.show_preview(self.original_image)
        window.destroy()
        
    def create_demo_templates(self):
        templates_dir = "templates"
        demo_templates = [
            ("дрейк.jpg", "https://i.imgur.com/9zQ4Mq9.jpg", "Drake Hotline Bling"),
            ("трейлер.jpg", "https://i.imgur.com/5BbjYqS.jpg", "This Is Fine"),
            ("старик.jpg", "https://i.imgur.com/8YjDvZw.jpg", "Old Man Yells at Cloud"),
        ]
        
        for name, url, desc in demo_templates:
            if not os.path.exists(f"{templates_dir}/{name}"):
                # Создаём заглушки для демонстрации
                img = Image.new('RGB', (500, 400), color=(random.randint(0,255), 
                                                           random.randint(0,255), 
                                                           random.randint(0,255)))
                draw = ImageDraw.Draw(img)
                draw.text((250, 200), desc, fill='white', anchor="mm")
                img.save(f"{templates_dir}/{name}")
        
    def choose_color(self):
        color = colorchooser.askcolor(color=self.text_color)[1]
        if color:
            self.text_color = color
            self.color_btn.configure(bg=color)
            self.color_label.configure(text=color)
            
    def toggle_outline(self):
        # Переключатель контура
        pass
        
    def generate_meme(self):
        if not self.original_image:
            messagebox.showwarning("Предупреждение", "Сначала загрузите изображение или выберите шаблон!")
            return
            
        # Создаём копию изображения
        self.edited_image = self.original_image.copy()
        draw = ImageDraw.Draw(self.edited_image)
        
        # Загружаем шрифт
        try:
            font = ImageFont.truetype("arial.ttf", self.font_size.get())
        except:
            font = ImageFont.load_default()
        
        # Получаем размеры изображения
        width, height = self.edited_image.size
        
        # Верхний текст
        top_text_content = self.top_text.get().upper()
        if top_text_content:
            # Вычисляем позицию
            bbox = draw.textbbox((0, 0), top_text_content, font=font)
            text_width = bbox[2] - bbox[0]
            x = (width - text_width) // 2
            y = 20
            
            # Рисуем контур
            outline_color = "#000000"
            draw.text((x-2, y-2), top_text_content, fill=outline_color, font=font)
            draw.text((x+2, y-2), top_text_content, fill=outline_color, font=font)
            draw.text((x-2, y+2), top_text_content, fill=outline_color, font=font)
            draw.text((x+2, y+2), top_text_content, fill=outline_color, font=font)
            
            # Основной текст
            draw.text((x, y), top_text_content, fill=self.text_color, font=font)
        
        # Нижний текст
        bottom_text_content = self.bottom_text.get().upper()
        if bottom_text_content:
            bbox = draw.textbbox((0, 0), bottom_text_content, font=font)
            text_width = bbox[2] - bbox[0]
            x = (width - text_width) // 2
            y = height - 80
            
            draw.text((x-2, y-2), bottom_text_content, fill=outline_color, font=font)
            draw.text((x+2, y-2), bottom_text_content, fill=outline_color, font=font)
            draw.text((x-2, y+2), bottom_text_content, fill=outline_color, font=font)
            draw.text((x+2, y+2), bottom_text_content, fill=outline_color, font=font)
            
            draw.text((x, y), bottom_text_content, fill=self.text_color, font=font)
        
        self.show_preview(self.edited_image)
        
    def show_preview(self, image):
        # Масштабируем для preview
        preview_width = 600
        preview_height = 400
        image_copy = image.copy()
        image_copy.thumbnail((preview_width, preview_height), Image.Resampling.LANCZOS)
        
        photo = ImageTk.PhotoImage(image_copy)
        self.preview_label.configure(image=photo, text="")
        self.preview_label.image = photo
        
    def save_meme(self):
        if not self.edited_image and not self.original_image:
            messagebox.showwarning("Предупреждение", "Нет изображения для сохранения!")
            return
            
        if not self.edited_image:
            self.generate_meme()
            
        filename = f"memes/meme_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        self.edited_image.save(filename)
        messagebox.showinfo("Успех", f"Мем сохранён как:\n{filename}")
        
    def create_gif(self):
        if not self.original_image:
            messagebox.showwarning("Предупреждение", "Сначала загрузите изображение!")
            return
            
        # Создаём GIF с анимацией текста
        frames = []
        texts = ["Вот так мем!", "Супер!", "Классно!", "🔥", "👍", self.top_text.get()]
        
        for i, text in enumerate(texts):
            img = self.original_image.copy()
            draw = ImageDraw.Draw(img)
            try:
                font = ImageFont.truetype("arial.ttf", 30 + i * 5)
            except:
                font = ImageFont.load_default()
                
            width, height = img.size
            bbox = draw.textbbox((0, 0), text, font=font)
            text_width = bbox[2] - bbox[0]
            x = (width - text_width) // 2
            y = height // 2 - 20 + i * 10
            
            draw.text((x, y), text, fill=self.text_color, font=font)
            frames.append(img)
            
        gif_path = f"memes/animated_meme_{datetime.now().strftime('%Y%m%d_%H%M%S')}.gif"
        frames[0].save(gif_path, save_all=True, append_images=frames[1:], 
                      duration=500, loop=0)
        messagebox.showinfo("Успех", f"GIF сохранён:\n{gif_path}")
        
    def reset_image(self):
        if self.original_image:
            self.show_preview(self.original_image)
            self.edited_image = None
            self.top_text.set("ВЕРХНИЙ ТЕКСТ")
            self.bottom_text.set("НИЖНИЙ ТЕКСТ")
            self.font_size.set(40)
            self.text_color = "#FFFFFF"
            self.color_btn.configure(bg="#FFFFFF")
            self.color_label.configure(text="#FFFFFF")

if __name__ == "__main__":
    root = tk.Tk()
    app = MemeGenerator(root)
    root.mainloop()