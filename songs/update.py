from songs.models import BillBoard
import pandas as pd
df = pd.read_csv('bill2.csv')





for index, row in df.iterrows():
    BillBoard.objects.create(date = row['date'],rank = int(row['rank']), song = row['song'], artist = row['artist'], last_week = int(row['last-week']), peak_rank = int(row['peak-rank']), weeks_on_board = int(row['weeks-on-board']))
    # date,rank,song,artist,last-week,peak-rank,weeks-on-board