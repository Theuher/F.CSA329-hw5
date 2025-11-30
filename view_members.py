"""
Simple script to view all members in the database
"""

from database_design import DatabaseManager, display_members

if __name__ == "__main__":
    print("="*60)
    print("VIEWING ALL MEMBERS")
    print("="*60)
    
    with DatabaseManager("library.db") as db:
        display_members(db)

