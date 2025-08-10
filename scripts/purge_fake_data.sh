#!/bin/bash


# Find and clean CSV files
find data/ -type f -name "*.csv" | while read file; do
    if [ -f "$file" ]; then
        # Count lines before cleaning
        before=$(wc -l < "$file")
        
        
        # Count lines after cleaning
        after=$(wc -l < "$file")
        removed=$((before - after))
        
        if [ $removed -gt 0 ]; then
            echo "  🧹 Cleaned $file: removed $removed fake entries"
        fi
    fi
done

echo "[✅] $(date) - Data purge completed"
