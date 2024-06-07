class Paginator:
    def __init__(self, items, page, per_page, total_count):
        self._items = items
        self.page = page
        self.per_page = per_page
        self.total_count = total_count
        self.pages = (self.total_count - 1) // self.per_page + 1

    @property
    def has_prev(self):
        return self.page > 1

    @property
    def has_next(self):
        return self.page < self.pages

    @property
    def prev_num(self):
        return self.page - 1

    @property
    def next_num(self):
        return self.page + 1

    @property
    def page_range(self):
        # Вычисляем диапазон страниц для вывода
        if self.pages <= 10:
            # Если всего страниц меньше или равно 10, то выводим все
            return range(1, self.pages + 1)
        else:
            # Если всего страниц больше 10, то выводим текущую страницу и еще несколько до и после нее
            half_range = 5
            start = self.page - half_range
            end = self.page + half_range
            if start < 1:
                # Если диапазон выходит за пределы начала, то сдвигаем его вправо
                start = 1
                end = 2 * half_range + 1
            if end > self.pages:
                # Если диапазон выходит за пределы конца, то сдвигаем его влево
                end = self.pages
                start = self.pages - 2 * half_range
            return range(start, end + 1)

    def __iter__(self):
        return (self[i] for i in range(len(self)))

    def __getitem__(self, index):
        if index < 0 or index >= len(self):
            raise IndexError
        if self.per_page * self.page > len(self._items):
            end = len(self._items)
        else:
            end = self.per_page * self.page
        return self._items[self.per_page * (self.page - 1) + index:end]
