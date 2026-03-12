#!/usr/bin/env python3
"""
Generate a concise summary of the database
"""
import sqlite3

db = sqlite3.connect('backend/lifestyle_index.db')
cur = db.cursor()

# Get all tables
cur.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
tables = [row[0] for row in cur.fetchall()]

print('\n' + '='*70)
print('DATABASE SUMMARY: lifestyle_index.db')
print('='*70 + '\n')

for table in tables:
    cur.execute(f'SELECT COUNT(*) FROM {table}')
    count = cur.fetchone()[0]
    
    # Get columns
    cur.execute(f'PRAGMA table_info({table})')
    cols = [row[1] for row in cur.fetchall()]
    
    print(f'📊 Table: {table}')
    print(f'   Rows: {count}')
    print(f'   Columns: {cols}')
    print()

# Show some sample data from non-empty tables
print('='*70)
print('SAMPLE DATA (First 5 rows from each non-empty table)')
print('='*70 + '\n')

for table in tables:
    cur.execute(f'SELECT COUNT(*) FROM {table}')
    count = cur.fetchone()[0]
    
    if count > 0:
        print(f'\n📋 {table} ({count} rows total):')
        cur.execute(f'SELECT * FROM {table} LIMIT 5')
        rows = cur.fetchall()
        
        # Get column names
        cur.execute(f'PRAGMA table_info({table})')
        cols = [row[1] for row in cur.fetchall()]
        
        # Print header
        header = ' | '.join(col[:15].ljust(15) for col in cols)
        print('   ' + header)
        print('   ' + '-'*len(header))
        
        # Print rows
        for row in rows:
            values = [str(val)[:15].ljust(15) if val is not None else 'None'.ljust(15) for val in row]
            print('   ' + ' | '.join(values))

print('\n' + '='*70)
db.close()
