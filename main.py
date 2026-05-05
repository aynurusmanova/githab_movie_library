import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

class MovieLibrary:
    def __init__(self, root):
        self.root = root
        self.root.title("Movie Library - Библиотека фильмов")
        self.root.geometry("900x600")
       
        self.movies_file = "movies.json"
        self.movies = self.load_movies()
       
        self.create_widgets()
        self.display_movies()
   
    def create_widgets(self):
        # Рамка для ввода данных
        input_frame = ttk.LabelFrame(self.root, text="Добавление фильма", padding="10")
        input_frame.pack(fill=tk.X, padx=10, pady=5)
       
        # Поля ввода
        ttk.Label(input_frame, text="Название фильма:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.title_entry = ttk.Entry(input_frame, width=30)
        self.title_entry.grid(row=0, column=1, padx=5, pady=5)
       
        ttk.Label(input_frame, text="Жанр:").grid(row=0, column=2, sticky=tk.W, padx=5, pady=5)
        self.genre_entry = ttk.Entry(input_frame, width=20)
        self.genre_entry.grid(row=0, column=3, padx=5, pady=5)
       
        ttk.Label(input_frame, text="Год выпуска:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.year_entry = ttk.Entry(input_frame, width=30)
        self.year_entry.grid(row=1, column=1, padx=5, pady=5)
       
        ttk.Label(input_frame, text="Рейтинг (0-10):").grid(row=1, column=2, sticky=tk.W, padx=5, pady=5)
        self.rating_entry = ttk.Entry(input_frame, width=20)
        self.rating_entry.grid(row=1, column=3, padx=5, pady=5)
       
        # Кнопка добавления
        self.add_button = ttk.Button(input_frame, text="Добавить фильм", command=self.add_movie)
        self.add_button.grid(row=2, column=0, columnspan=4, pady=10)
       
        # Рамка для фильтрации
        filter_frame = ttk.LabelFrame(self.root, text="Фильтрация", padding="10")
        filter_frame.pack(fill=tk.X, padx=10, pady=5)
       
        ttk.Label(filter_frame, text="Фильтр по жанру:").pack(side=tk.LEFT, padx=5)
        self.filter_genre_entry = ttk.Entry(filter_frame, width=20)
        self.filter_genre_entry.pack(side=tk.LEFT, padx=5)
       
        self.filter_genre_button = ttk.Button(filter_frame, text="Применить фильтр", command=self.filter_by_genre)
        self.filter_genre_button.pack(side=tk.LEFT, padx=5)
       
        ttk.Button(filter_frame, text="Сбросить фильтр", command=self.display_movies).pack(side=tk.LEFT, padx=20)
       
        ttk.Label(filter_frame, text="Год выпуска (равен):").pack(side=tk.LEFT, padx=5)
        self.filter_year_entry = ttk.Entry(filter_frame, width=10)
        self.filter_year_entry.pack(side=tk.LEFT, padx=5)
       
        self.filter_year_button = ttk.Button(filter_frame, text="Применить", command=self.filter_by_year)
        self.filter_year_button.pack(side=tk.LEFT, padx=5)
       
        ttk.Button(filter_frame, text="Сбросить всё", command=self.reset_filters).pack(side=tk.LEFT, padx=20)
       
        # Таблица с фильмами
        table_frame = ttk.Frame(self.root)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
       
        columns = ("title", "genre", "year", "rating")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings")
       
        self.tree.heading("title", text="Название")
        self.tree.heading("genre", text="Жанр")
        self.tree.heading("year", text="Год")
        self.tree.heading("rating", text="Рейтинг")
       
        self.tree.column("title", width=300)
        self.tree.column("genre", width=150)
        self.tree.column("year", width=100)
        self.tree.column("rating", width=100)
       
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
       
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
       
        # Кнопка удаления
        delete_frame = ttk.Frame(self.root)
        delete_frame.pack(fill=tk.X, padx=10, pady=5)
       
        self.delete_button = ttk.Button(delete_frame, text="Удалить выбранный фильм", command=self.delete_movie)
        self.delete_button.pack(side=tk.LEFT, padx=5)
       
        self.clear_all_button = ttk.Button(delete_frame, text="Очистить всё", command=self.clear_all)
        self.clear_all_button.pack(side=tk.LEFT, padx=5)
       
        # Счётчик фильмов
        self.count_label = ttk.Label(self.root, text="Всего фильмов: 0")
        self.count_label.pack(side=tk.BOTTOM, pady=5)
       
        self.update_count()
   
    def add_movie(self):
        title = self.title_entry.get().strip()
        genre = self.genre_entry.get().strip()
        year = self.year_entry.get().strip()
        rating = self.rating_entry.get().strip()
       
        if not title or not genre or not year or not rating:
            messagebox.showwarning("Предупреждение", "Все поля должны быть заполнены!")
            return
       
        try:
            year = int(year)
            if year < 1888 or year > 2026:
                raise ValueError
        except ValueError:
            messagebox.showwarning("Предупреждение", "Год должен быть числом от 1888 до 2026!")
            return
       
        try:
            rating = float(rating)
            if rating < 0 or rating > 10:
                raise ValueError
        except ValueError:
            messagebox.showwarning("Предупреждение", "Рейтинг должен быть числом от 0 до 10!")
            return
       
        movie = {
            "title": title,
            "genre": genre,
            "year": year,
            "rating": rating
        }
        self.movies.append(movie)
        self.save_movies()
        self.display_movies()
       
        self.title_entry.delete(0, tk.END)
        self.genre_entry.delete(0, tk.END)
        self.year_entry.delete(0, tk.END)
        self.rating_entry.delete(0, tk.END)
       
        messagebox.showinfo("Успех", f"Фильм '{title}' добавлен!")
   
    def display_movies(self, movies_to_show=None):
        for item in self.tree.get_children():
            self.tree.delete(item)
       
        if movies_to_show is None:
            movies_to_show = self.movies
       
        for movie in movies_to_show:
            self.tree.insert("", tk.END, values=(
                movie["title"],
                movie["genre"],
                movie["year"],
                movie["rating"]
            ))
       
        self.update_count()
   
    def filter_by_genre(self):
        genre = self.filter_genre_entry.get().strip().lower()
        if not genre:
            messagebox.showwarning("Предупреждение", "Введите жанр для фильтрации!")
            return
       
        filtered = [movie for movie in self.movies if genre in movie["genre"].lower()]
        self.display_movies(filtered)
        messagebox.showinfo("Результат", f"Найдено фильмов: {len(filtered)}")
   
    def filter_by_year(self):
        year_str = self.filter_year_entry.get().strip()
        if not year_str:
            messagebox.showwarning("Предупреждение", "Введите год!")
            return
       
        try:
            year = int(year_str)
        except ValueError:
            messagebox.showwarning("Предупреждение", "Введите число!")
            return
       
        filtered = [movie for movie in self.movies if movie["year"] == year]
        self.display_movies(filtered)
        messagebox.showinfo("Результат", f"Найдено фильмов: {len(filtered)}")
   
    def reset_filters(self):
        self.filter_genre_entry.delete(0, tk.END)
        self.filter_year_entry.delete(0, tk.END)
        self.display_movies()
   
    def delete_movie(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Предупреждение", "Выберите фильм для удаления!")
            return
       
        item = self.tree.item(selected[0])
        values = item["values"]
        title = values[0]
       
        if messagebox.askyesno("Подтверждение", f"Удалить фильм '{title}'?"):
            for i, movie in enumerate(self.movies):
                if movie["title"] == title and movie["genre"] == values[1]:
                    del self.movies[i]
                    break
            self.save_movies()
            self.display_movies()
   
    def clear_all(self):
        if messagebox.askyesno("Подтверждение", "Удалить все фильмы?"):
            self.movies = []
            self.save_movies()
            self.display_movies()
   
    def update_count(self):
        self.count_label.config(text=f"Всего фильмов: {len(self.movies)}")
   
    def load_movies(self):
        if os.path.exists(self.movies_file):
            try:
                with open(self.movies_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                return []
        return []
   
    def save_movies(self):
        with open(self.movies_file, "w", encoding="utf-8") as f:
            json.dump(self.movies, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    root = tk.Tk()
    app = MovieLibrary(root)
    root.mainloop()