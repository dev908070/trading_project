import os
import pandas as pd
from django.db import transaction
from trade.models import NiftyData

BATCH_SIZE = 10000  # Adjust batch size depending on your system's capacity

def upload_tick_excel_to_sql(directory_path):
    # Iterate over all Excel files in the directory
    file_count = 0
    
    for filename in os.listdir(directory_path):
        if filename.endswith(".csv"):
            file_path = os.path.join(directory_path, filename)
            
            try:
                # Read Excel file into a DataFrame
                df = pd.read_csv(file_path)
                
                # Convert columns to appropriate data types
                df['date'] = pd.to_datetime(df['date']).dt.date
                df['time'] = pd.to_datetime(df['time']).dt.time
                
                # Collect model instances to bulk create
                model_instances = [
                    NiftyData(
                        date=row['date'],
                        time=row['time'],
                        tick_price=row['tick_price'],
                        volume=row['volume'],
                        open_interest=row['open_interest']
                    )
                    for _, row in df.iterrows()
                ]
                
                # Insert data into database in batches to avoid memory overload
                for i in range(0, len(model_instances), BATCH_SIZE):
                    with transaction.atomic():
                        NiftyData.objects.bulk_create(model_instances[i:i+BATCH_SIZE])
                
                file_count += 1
                print(f"{filename} uploaded successfully.")
                print(file_count)
            
            except Exception as e:
                print(f"Error processing file {filename}: {str(e)}")

    print(f"Total files processed: {file_count}")
