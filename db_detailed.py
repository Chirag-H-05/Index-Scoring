#!/usr/bin/env python3
"""
Detailed database report with full data
"""
import sqlite3
from datetime import datetime

db = sqlite3.connect('backend/lifestyle_index.db')
db.row_factory = sqlite3.Row
cur = db.cursor()

# Get all tables
cur.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
tables = [row[0] for row in cur.fetchall()]

print('\n' + '='*100)
print('DETAILED DATABASE REPORT: lifestyle_index.db')
print('='*100)

for table in tables:
    if table == 'sqlite_sequence':
        continue
        
    cur.execute(f'SELECT COUNT(*) FROM {table}')
    count = cur.fetchone()[0]
    
    # Get column names
    cur.execute(f'PRAGMA table_info({table})')
    columns = [(row[1], row[2]) for row in cur.fetchall()]
    col_names = [col[0] for col in columns]
    
    print(f'\n\n{"="*100}')
    print(f'TABLE: {table.upper()} ({count} rows)')
    print(f'{"="*100}')
    print(f'Columns: {col_names}\n')
    
    if count > 0:
        # Show all rows or first 50 if too many
        limit = 50 if count > 50 else count
        cur.execute(f'SELECT * FROM {table} LIMIT {limit}')
        rows = cur.fetchall()
        
        for i, row in enumerate(rows, 1):
            print(f'\n  Row {i}:')
            for col_name in col_names:
                value = row[col_name]
                
                # Format timestamps
                if 'timestamp' in col_name.lower() or col_name in ['ts', 'created_at', 'updated_at', 'last_login', 'last_active']:
                    if isinstance(value, (int, float)):
                        try:
                            readable = datetime.fromtimestamp(value).strftime('%Y-%m-%d %H:%M:%S')
                            print(f'    {col_name}: {value} ({readable})')
                        except:
                            print(f'    {col_name}: {value}')
                    else:
                        print(f'    {col_name}: {value}')
                else:
                    # Truncate long strings
                    if isinstance(value, str) and len(value) > 80:
                        print(f'    {col_name}: {value[:80]}...')
                    else:
                        print(f'    {col_name}: {value}')
        
        if count > 50:
            print(f'\n  ... and {count - 50} more rows')
    else:
        print('  (empty table)')

print(f'\n\n{"="*100}')
print('END OF REPORT')
print(f'{"="*100}\n')

db.close()
