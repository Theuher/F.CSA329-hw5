# Chapter 6 Exercise: Database Design and Management
## Software Engineering for Absolute Beginners

Энэхүү дадлага нь "Software Engineering for Absolute Beginners" номын 6-р бүлгийн дасгалуудыг агуулна.

## Агуулга

Энэ дадлагад дараах сэдвүүдийг судална:

1. **Өгөгдлийн сангийн дизайн** - Хүснэгтүүд болон тэдгээрийн хоорондын харилцаа
2. **Өгөгдлийн сан үүсгэх** - SQLite ашиглан өгөгдлийн сан үүсгэх
3. **CRUD үйлдлүүд** - Create, Read, Update, Delete үйлдлүүд
4. **SQL хүсэлтүүд** - Төрөл бүрийн хүсэлтүүд (JOIN, GROUP BY, WHERE, гэх мэт)

## Файлууд

- `database_design.py` - Үндсэн өгөгдлийн сангийн класс болон CRUD үйлдлүүд
- `database_queries.py` - Төрөл бүрийн SQL хүсэлтүүдийн жишээ
- `view_members.py` - Гишүүдийн жагсаалтыг харах энгийн скрипт
- `library.db` - SQLite өгөгдлийн сан (програм ажиллуулахад автоматаар үүснэ)

## Ашиглах заавар

### 1. Үндсэн програм ажиллуулах

```bash
python database_design.py
```

Энэ програм:
- Өгөгдлийн сан үүсгэнэ
- Хүснэгтүүдийг үүсгэнэ
- Жишээ өгөгдөл оруулна
- CRUD үйлдлүүдийг демонстрацилна

### 2. Хүсэлтүүдийн жишээг ажиллуулах

```bash
python database_queries.py
```

Энэ програм:
- Төрөл бүрийн SQL хүсэлтүүдийг харуулна
- JOIN, GROUP BY, WHERE зэрэг үйлдлүүдийг демонстрацилна

### 3. Гишүүдийн жагсаалтыг харах

```bash
python view_members.py
```

Энэ програм:
- Бүх гишүүдийн мэдээллийг харуулна
- ID, нэр, имэйл, утас, элссэн огноо зэргийг харуулна

## Өгөгдлийн сангийн бүтэц

### Authors (Зохиолчид)
- `author_id` - Үндсэн түлхүүр
- `first_name` - Нэр
- `last_name` - Овог
- `email` - Имэйл (уникаль)
- `created_at` - Үүсгэсэн огноо

### Books (Номнууд)
- `book_id` - Үндсэн түлхүүр
- `title` - Гарчиг
- `isbn` - ISBN код (уникаль)
- `author_id` - Зохиолчийн ID (гадаад түлхүүр)
- `publication_year` - Хэвлэгдсэн он
- `price` - Үнэ
- `created_at` - Үүсгэсэн огноо

### Members (Гишүүд)
- `member_id` - Үндсэн түлхүүр
- `first_name` - Нэр
- `last_name` - Овог
- `email` - Имэйл (уникаль)
- `phone` - Утас
- `join_date` - Элссэн огноо

### Borrowings (Зээлдүүлэлт)
- `borrowing_id` - Үндсэн түлхүүр
- `member_id` - Гишүүний ID (гадаад түлхүүр)
- `book_id` - Номны ID (гадаад түлхүүр)
- `borrow_date` - Зээлдүүлсэн огноо
- `return_date` - Буцаасан огноо

## Харилцаа (Relationships)

- **Authors ↔ Books**: Нэг зохиолч олон номтой (One-to-Many)
- **Members ↔ Borrowings**: Нэг гишүүн олон зээлдүүлэлттэй (One-to-Many)
- **Books ↔ Borrowings**: Нэг ном олон зээлдүүлэлттэй (One-to-Many)
- **Members ↔ Books**: Олон гишүүн олон номтой (Many-to-Many, Borrowings хүснэгтээр дамжин)

## CRUD үйлдлүүд

### Create (Үүсгэх)
- `add_author()` - Зохиолч нэмэх
- `add_book()` - Ном нэмэх
- `add_member()` - Гишүүн нэмэх
- `borrow_book()` - Зээлдүүлэлт бүртгэх

### Read (Унших)
- `get_all_authors()` - Бүх зохиолчдыг авах
- `get_all_books()` - Бүх номыг авах
- `get_all_members()` - Бүх гишүүдийг авах
- `get_books_by_author()` - Зохиолчийн номыг авах
- `get_member_borrowings()` - Гишүүний зээлдүүлэлтийг авах

### Update (Шинэчлэх)
- `update_book_price()` - Номны үнийг шинэчлэх
- `return_book()` - Ном буцаах

### Delete (Устгах)
- `delete_book()` - Ном устгах

## SQL хүсэлтүүдийн жишээнүүд

`database_queries.py` файлд дараах хүсэлтүүдийн жишээнүүд байна:

1. **JOIN хүсэлт** - Хоёр хүснэгтийг нэгтгэх
2. **GROUP BY** - Өгөгдлийг бүлэглэх
3. **WHERE** - Нөхцөлт хүсэлт
4. **LIKE** - Текст хайлт
5. **BETWEEN** - Завсрын утга хайлт
6. **Aggregate functions** - COUNT, AVG зэрэг

## Шаардлага

- Python 3.6+ 
- SQLite3 (Python-тай хамт ирдэг)

## Өгөгдөл харах функцүүд

Програмд дараах display функцүүд байна:

- `display_authors(db)` - Бүх зохиолчдыг форматлагдсан байдлаар харуулна
- `display_books(db)` - Бүх номыг форматлагдсан байдлаар харуулна
- `display_members(db)` - Бүх гишүүдийг форматлагдсан байдлаар харуулна

Жишээ:
```python
from database_design import DatabaseManager, display_members

with DatabaseManager("library.db") as db:
    display_members(db)
```

## Нэмэлт мэдээлэл

SQLite өгөгдлийн сан файлыг (`library.db`) SQLite browser эсвэл бусад хэрэгслээр нээж үзэх боломжтой.

## Дасгалууд

1. Шинэ зохиолч, ном, гишүүн нэмэх
2. Номны үнийг шинэчлэх
3. Зээлдүүлэлт бүртгэх
4. Төрөл бүрийн хүсэлтүүд ажиллуулах
5. Өгөгдлийн сангийн бүтцийг өөрчлөх (хүснэгт нэмэх/устгах)

## Гүйцэтгэсэн

- ✓ Өгөгдлийн сангийн дизайн
- ✓ Хүснэгтүүд болон харилцаа
- ✓ CRUD үйлдлүүд
- ✓ SQL хүсэлтүүдийн жишээнүүд
- ✓ Практик жишээ програм

