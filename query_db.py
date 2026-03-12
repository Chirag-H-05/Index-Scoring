#!/usr/bin/env python3
"""
Query the lifestyle_index.db database and display all contents
"""
import sqlite3
import json
from datetime import datetime

db_path = 'backend/lifestyle_index.db'
conn = sqlite3.connect(db_path)
conn.row_factory = sqlite3.Row
cur = conn.cursor()

print('='*80)
print('DATABASE CONTENTS: lifestyle_index.db')
print('='*80)

# Get all table names
cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = [row[0] for row in cur.fetchall()]
print(f'\nTables found: {tables}\n')

# Query each table
for table in tables:
    print(f'\n{"="*80}')
    print(f'TABLE: {table.upper()}')
    print(f'{"="*80}')
    
    # Get column info
    cur.execute(f'PRAGMA table_info({table})')
    columns = cur.fetchall()
    col_names = [col[1] for col in columns]
    print(f'Columns: {col_names}')
    
    # Get row count
    cur.execute(f'SELECT COUNT(*) FROM {table}')
    count = cur.fetchone()[0]
    print(f'Rows: {count}\n')
    
    if count > 0:
        # Display rows
        cur.execute(f'SELECT * FROM {table} ORDER BY id DESC LIMIT 100')
        rows = cur.fetchall()
        
        # Print formatted with readable timestamps
        for i, row in enumerate(rows, 1):
            row_dict = dict(row)
            # Convert unix timestamps to readable format
            if 'ts' in row_dict and row_dict['ts']:
                try:
                    row_dict['ts_readable'] = datetime.fromtimestamp(row_dict['ts']).strftime('%Y-%m-%d %H:%M:%S')
                except:
                    pass
            print(f"\n  Row {i}:")
            for key, value in row_dict.items():
                print(f"    {key}: {value}")
    else:
        print('(empty table)')

print('\n' + '='*80)
print('END OF QUERY')
print('='*80)

conn.close()
