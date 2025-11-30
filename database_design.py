"""
Chapter 6 Exercise: Database Design and Implementation
Software Engineering for Absolute Beginners

This module demonstrates:
1. Database schema design
2. Creating and connecting to a database
3. Basic CRUD operations
"""

import sqlite3
import os
from typing import List, Tuple, Optional
from datetime import datetime


class DatabaseManager:
    """Manages database operations for a simple library system."""
    
    def __init__(self, db_name: str = "library.db"):
        """Initialize database connection."""
        self.db_name = db_name
        self.conn = None
        self.connect()
        self.create_tables()
    
    def connect(self):
        """Establish connection to the database."""
        try:
            self.conn = sqlite3.connect(self.db_name)
            self.conn.row_factory = sqlite3.Row  # Access columns by name
            print(f"[OK] Connected to database: {self.db_name}")
        except sqlite3.Error as e:
            print(f"[ERROR] Error connecting to database: {e}")
            raise
    
    def create_tables(self):
        """Create database tables with proper relationships."""
        cursor = self.conn.cursor()
        
        # Create Authors table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS authors (
                author_id INTEGER PRIMARY KEY AUTOINCREMENT,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                email TEXT UNIQUE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Create Books table (with foreign key to authors)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS books (
                book_id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                isbn TEXT UNIQUE,
                author_id INTEGER,
                publication_year INTEGER,
                price REAL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (author_id) REFERENCES authors(author_id)
            )
        """)
        
        # Create Members table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS members (
                member_id INTEGER PRIMARY KEY AUTOINCREMENT,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                phone TEXT,
                join_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Create Borrowings table (many-to-many relationship)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS borrowings (
                borrowing_id INTEGER PRIMARY KEY AUTOINCREMENT,
                member_id INTEGER NOT NULL,
                book_id INTEGER NOT NULL,
                borrow_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                return_date TIMESTAMP,
                FOREIGN KEY (member_id) REFERENCES members(member_id),
                FOREIGN KEY (book_id) REFERENCES books(book_id)
            )
        """)
        
        self.conn.commit()
        print("[OK] Database tables created successfully")
    
    # CREATE operations
    def add_author(self, first_name: str, last_name: str, email: Optional[str] = None) -> int:
        """Add a new author to the database."""
        cursor = self.conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO authors (first_name, last_name, email)
                VALUES (?, ?, ?)
            """, (first_name, last_name, email))
            self.conn.commit()
            author_id = cursor.lastrowid
            print(f"[OK] Author added: {first_name} {last_name} (ID: {author_id})")
            return author_id
        except sqlite3.IntegrityError as e:
            print(f"[ERROR] Error adding author: {e}")
            return None
    
    def add_book(self, title: str, author_id: int, isbn: Optional[str] = None,
                 publication_year: Optional[int] = None, price: Optional[float] = None) -> int:
        """Add a new book to the database."""
        cursor = self.conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO books (title, isbn, author_id, publication_year, price)
                VALUES (?, ?, ?, ?, ?)
            """, (title, isbn, author_id, publication_year, price))
            self.conn.commit()
            book_id = cursor.lastrowid
            print(f"[OK] Book added: {title} (ID: {book_id})")
            return book_id
        except sqlite3.Error as e:
            print(f"[ERROR] Error adding book: {e}")
            return None
    
    def add_member(self, first_name: str, last_name: str, email: str, phone: Optional[str] = None) -> int:
        """Add a new member to the database."""
        cursor = self.conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO members (first_name, last_name, email, phone)
                VALUES (?, ?, ?, ?)
            """, (first_name, last_name, email, phone))
            self.conn.commit()
            member_id = cursor.lastrowid
            print(f"[OK] Member added: {first_name} {last_name} (ID: {member_id})")
            return member_id
        except sqlite3.IntegrityError as e:
            print(f"[ERROR] Error adding member: {e}")
            return None
    
    def borrow_book(self, member_id: int, book_id: int) -> int:
        """Record a book borrowing."""
        cursor = self.conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO borrowings (member_id, book_id)
                VALUES (?, ?)
            """, (member_id, book_id))
            self.conn.commit()
            borrowing_id = cursor.lastrowid
            print(f"[OK] Book borrowed (Borrowing ID: {borrowing_id})")
            return borrowing_id
        except sqlite3.Error as e:
            print(f"[ERROR] Error recording borrowing: {e}")
            return None
    
    # READ operations
    def get_all_authors(self) -> List[Tuple]:
        """Retrieve all authors from the database."""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM authors ORDER BY last_name, first_name")
        return cursor.fetchall()
    
    def get_all_books(self) -> List[Tuple]:
        """Retrieve all books with author information."""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT b.book_id, b.title, b.isbn, b.publication_year, b.price,
                   a.first_name || ' ' || a.last_name AS author_name
            FROM books b
            LEFT JOIN authors a ON b.author_id = a.author_id
            ORDER BY b.title
        """)
        return cursor.fetchall()
    
    def get_books_by_author(self, author_id: int) -> List[Tuple]:
        """Retrieve all books by a specific author."""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT * FROM books
            WHERE author_id = ?
            ORDER BY publication_year DESC
        """, (author_id,))
        return cursor.fetchall()
    
    def get_member_borrowings(self, member_id: int) -> List[Tuple]:
        """Get all books borrowed by a member."""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT b.title, br.borrow_date, br.return_date
            FROM borrowings br
            JOIN books b ON br.book_id = b.book_id
            WHERE br.member_id = ?
            ORDER BY br.borrow_date DESC
        """, (member_id,))
        return cursor.fetchall()
    
    # UPDATE operations
    def update_book_price(self, book_id: int, new_price: float) -> bool:
        """Update the price of a book."""
        cursor = self.conn.cursor()
        try:
            cursor.execute("""
                UPDATE books
                SET price = ?
                WHERE book_id = ?
            """, (new_price, book_id))
            self.conn.commit()
            if cursor.rowcount > 0:
                print(f"[OK] Book price updated (Book ID: {book_id})")
                return True
            else:
                print(f"[ERROR] No book found with ID: {book_id}")
                return False
        except sqlite3.Error as e:
            print(f"[ERROR] Error updating book: {e}")
            return False
    
    def return_book(self, borrowing_id: int) -> bool:
        """Record the return of a borrowed book."""
        cursor = self.conn.cursor()
        try:
            cursor.execute("""
                UPDATE borrowings
                SET return_date = CURRENT_TIMESTAMP
                WHERE borrowing_id = ? AND return_date IS NULL
            """, (borrowing_id,))
            self.conn.commit()
            if cursor.rowcount > 0:
                print(f"[OK] Book returned (Borrowing ID: {borrowing_id})")
                return True
            else:
                print(f"[ERROR] No active borrowing found with ID: {borrowing_id}")
                return False
        except sqlite3.Error as e:
            print(f"[ERROR] Error returning book: {e}")
            return False
    
    # DELETE operations
    def delete_book(self, book_id: int) -> bool:
        """Delete a book from the database."""
        cursor = self.conn.cursor()
        try:
            cursor.execute("DELETE FROM books WHERE book_id = ?", (book_id,))
            self.conn.commit()
            if cursor.rowcount > 0:
                print(f"[OK] Book deleted (Book ID: {book_id})")
                return True
            else:
                print(f"[ERROR] No book found with ID: {book_id}")
                return False
        except sqlite3.Error as e:
            print(f"[ERROR] Error deleting book: {e}")
            return False
    
    def close(self):
        """Close the database connection."""
        if self.conn:
            self.conn.close()
            print("[OK] Database connection closed")
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()


def display_authors(db: DatabaseManager):
    """Display all authors in a formatted way."""
    print("\n" + "="*60)
    print("AUTHORS")
    print("="*60)
    authors = db.get_all_authors()
    if authors:
        for author in authors:
            print(f"ID: {author['author_id']:3d} | "
                  f"{author['first_name']} {author['last_name']:20s} | "
                  f"Email: {author['email'] or 'N/A'}")
    else:
        print("No authors found.")
    print()


def display_books(db: DatabaseManager):
    """Display all books in a formatted way."""
    print("\n" + "="*80)
    print("BOOKS")
    print("="*80)
    books = db.get_all_books()
    if books:
        for book in books:
            year_str = str(book['publication_year']) if book['publication_year'] else 'N/A'
            print(f"ID: {book['book_id']:3d} | "
                  f"Title: {book['title']:30s} | "
                  f"Author: {book['author_name'] or 'Unknown':20s} | "
                  f"Year: {year_str:4s} | "
                  f"Price: ${book['price'] or 0:.2f}")
    else:
        print("No books found.")
    print()


if __name__ == "__main__":
    # Example usage of the database
    print("="*60)
    print("Chapter 6 Exercise: Database Management System")
    print("="*60)
    
    # Remove existing database for clean start
    db_file = "library.db"
    if os.path.exists(db_file):
        os.remove(db_file)
        print(f"[INFO] Removed existing database: {db_file}")
    
    # Create database manager
    with DatabaseManager(db_file) as db:
        # Add sample authors
        print("\n--- Adding Authors ---")
        author1_id = db.add_author("J.K.", "Rowling", "jkrowling@example.com")
        author2_id = db.add_author("George", "Orwell", "gorwell@example.com")
        author3_id = db.add_author("Jane", "Austen", "jausten@example.com")
        
        # Add sample books
        print("\n--- Adding Books ---")
        db.add_book("Harry Potter and the Philosopher's Stone", author1_id, 
                   "978-0747532699", 1997, 12.99)
        db.add_book("1984", author2_id, "978-0451524935", 1949, 9.99)
        db.add_book("Pride and Prejudice", author3_id, "978-0141439518", 1813, 8.99)
        db.add_book("Animal Farm", author2_id, "978-0451526342", 1945, 7.99)
        
        # Add sample members
        print("\n--- Adding Members ---")
        member1_id = db.add_member("John", "Doe", "john.doe@example.com", "555-0101")
        member2_id = db.add_member("Jane", "Smith", "jane.smith@example.com", "555-0102")
        
        # Display data
        display_authors(db)
        display_books(db)
        
        # Demonstrate borrowing (only if members were added successfully)
        print("\n--- Borrowing Books ---")
        if member1_id and member2_id:
            db.borrow_book(member1_id, 1)  # John borrows Harry Potter
            db.borrow_book(member2_id, 2)  # Jane borrows 1984
            
            # Display member borrowings
            print("\n--- Member Borrowings ---")
            borrowings = db.get_member_borrowings(member1_id)
            print(f"Books borrowed by Member ID {member1_id}:")
            if borrowings:
                for borrowing in borrowings:
                    print(f"  - {borrowing['title']} (Borrowed: {borrowing['borrow_date']})")
            else:
                print("  No borrowings found.")
        else:
            print("[INFO] Skipping borrowings - members not added successfully")
        
        # Demonstrate update
        print("\n--- Updating Book Price ---")
        db.update_book_price(1, 14.99)
        
        # Display updated books
        display_books(db)
        
        print("\n" + "="*60)
        print("Exercise completed successfully!")
        print("="*60)

