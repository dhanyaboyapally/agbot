"""
Database migration script to add new fields to User model
Run this script once to add the new columns
"""
from app import app, db
from sqlalchemy import text

def migrate_database():
    with app.app_context():
        try:
            # Add new columns to users table
            with db.engine.connect() as conn:
                # Check if columns exist first to avoid errors
                result = conn.execute(text("PRAGMA table_info(users)"))
                existing_columns = [row[1] for row in result]

                if 'theme' not in existing_columns:
                    conn.execute(text("ALTER TABLE users ADD COLUMN theme VARCHAR(20) DEFAULT 'emerald'"))
                    conn.commit()
                    print("✓ Added 'theme' column")

                if 'farm_name' not in existing_columns:
                    conn.execute(text("ALTER TABLE users ADD COLUMN farm_name VARCHAR(100)"))
                    conn.commit()
                    print("✓ Added 'farm_name' column")

                if 'farm_size' not in existing_columns:
                    conn.execute(text("ALTER TABLE users ADD COLUMN farm_size VARCHAR(50)"))
                    conn.commit()
                    print("✓ Added 'farm_size' column")

                if 'crops' not in existing_columns:
                    conn.execute(text("ALTER TABLE users ADD COLUMN crops TEXT"))
                    conn.commit()
                    print("✓ Added 'crops' column")

                if 'notification_email' not in existing_columns:
                    conn.execute(text("ALTER TABLE users ADD COLUMN notification_email BOOLEAN DEFAULT 1"))
                    conn.commit()
                    print("✓ Added 'notification_email' column")

                if 'notification_push' not in existing_columns:
                    conn.execute(text("ALTER TABLE users ADD COLUMN notification_push BOOLEAN DEFAULT 1"))
                    conn.commit()
                    print("✓ Added 'notification_push' column")

            print("\n✅ Database migration completed successfully!")

        except Exception as e:
            print(f"\n❌ Migration failed: {str(e)}")
            raise

if __name__ == '__main__':
    migrate_database()
