"""
Chapter 6 Exercise: Advanced Database Queries
Demonstrates various SQL query patterns and database relationships
"""

import sqlite3
from database_design import DatabaseManager


def demonstrate_queries():
    """Demonstrate various database query patterns."""
    
    db = DatabaseManager("library.db")
    
    print("\n" + "="*60)
    print("ADVANCED DATABASE QUERIES")
    print("="*60)
    
    # Query 1: Find books by a specific author
    print("\n--- Query 1: Books by George Orwell ---")
    cursor = db.conn.cursor()
    cursor.execute("""
        SELECT b.title, b.publication_year, b.price
        FROM books b
        JOIN authors a ON b.author_id = a.author_id
        WHERE a.last_name = 'Orwell'
        ORDER BY b.publication_year
    """)
    results = cursor.fetchall()
    for row in results:
        print(f"  - {row['title']} ({row['publication_year']}) - ${row['price']:.2f}")
    
    # Query 2: Count books per author
    print("\n--- Query 2: Number of books per author ---")
    cursor.execute("""
        SELECT a.first_name || ' ' || a.last_name AS author_name,
               COUNT(b.book_id) AS book_count
        FROM authors a
        LEFT JOIN books b ON a.author_id = b.author_id
        GROUP BY a.author_id
        ORDER BY book_count DESC
    """)
    results = cursor.fetchall()
    for row in results:
        print(f"  - {row['author_name']}: {row['book_count']} book(s)")
    
    # Query 3: Find currently borrowed books
    print("\n--- Query 3: Currently borrowed books (not returned) ---")
    cursor.execute("""
        SELECT m.first_name || ' ' || m.last_name AS member_name,
               b.title,
               br.borrow_date
        FROM borrowings br
        JOIN members m ON br.member_id = m.member_id
        JOIN books b ON br.book_id = b.book_id
        WHERE br.return_date IS NULL
        ORDER BY br.borrow_date
    """)
    results = cursor.fetchall()
    if results:
        for row in results:
            print(f"  - {row['member_name']} borrowed '{row['title']}' on {row['borrow_date']}")
    else:
        print("  No books currently borrowed.")
    
    # Query 4: Average book price by author
    print("\n--- Query 4: Average book price by author ---")
    cursor.execute("""
        SELECT a.first_name || ' ' || a.last_name AS author_name,
               AVG(b.price) AS avg_price,
               COUNT(b.book_id) AS book_count
        FROM authors a
        JOIN books b ON a.author_id = b.author_id
        WHERE b.price IS NOT NULL
        GROUP BY a.author_id
        HAVING COUNT(b.book_id) > 0
        ORDER BY avg_price DESC
    """)
    results = cursor.fetchall()
    for row in results:
        print(f"  - {row['author_name']}: ${row['avg_price']:.2f} (avg of {row['book_count']} books)")
    
    # Query 5: Search books by title (LIKE query)
    print("\n--- Query 5: Search books containing 'Harry' ---")
    cursor.execute("""
        SELECT b.title, a.first_name || ' ' || a.last_name AS author_name
        FROM books b
        LEFT JOIN authors a ON b.author_id = a.author_id
        WHERE b.title LIKE '%Harry%'
    """)
    results = cursor.fetchall()
    for row in results:
        print(f"  - {row['title']} by {row['author_name']}")
    
    # Query 6: Books published in a specific year range
    print("\n--- Query 6: Books published between 1940 and 1950 ---")
    cursor.execute("""
        SELECT b.title, b.publication_year, a.first_name || ' ' || a.last_name AS author_name
        FROM books b
        JOIN authors a ON b.author_id = a.author_id
        WHERE b.publication_year BETWEEN 1940 AND 1950
        ORDER BY b.publication_year
    """)
    results = cursor.fetchall()
    for row in results:
        print(f"  - {row['title']} ({row['publication_year']}) by {row['author_name']}")
    
    db.close()


if __name__ == "__main__":
    demonstrate_queries()

