from spotipy.oauth2 import SpotifyOAuth
import spotipy
import mplcyberpunk
from django.utils import timezone
from django.contrib import messages
import matplotlib
import asyncio
import seaborn as sns
from music.settings import BASE_DIR
from django.conf import settings
import matplotlib.pyplot as plt
import os
import pandas as pd
from django.shortcuts import render, redirect
from .models import BillBoard
from .forms import MyForm, SingerForm, ArtistTopForm
matplotlib.use('Agg')
# from billboard import ChartData
# Create your views here.


def home(request):
    if request.method == 'POST':
        singer = SingerForm(request.POST)
        form = MyForm(request.POST)
        artist = ArtistTopForm(request.POST)

        if form.is_valid():
            my_models = []
            date = form.cleaned_data['date']

            if date > timezone.now().date():
                messages.warning(
                    request, "Time traveling to the future to view charts of future dates is currently in beta version!")
                return redirect('home')
            # chart = ChartData('hot-100',date =date)[:100]
            # for song in chart:
            #     list_details = [song.rank,song.title,song.artist,song.lastPos,song.peakPos,song.weeks]
            #     my_models.append({column:value for column,value in zip(columns,list_details)})
            else:
                my_models = BillBoard.objects.filter(
                    date__gte=date).order_by('date')[:100]
                if my_models:
                    df = pd.DataFrame.from_records(my_models.values())
                    df['song'] = df['song'].str.replace('/', '_')
                    df['artist'] = df['artist'].str.replace('/', '_')
                    table = df.to_dict(orient='records')
                    return render(request, 'songs/results.html', {'my_models': table})
                else:
                    my_models = BillBoard.objects.filter(
                        date=BillBoard.objects.last().date).order_by('date')[:100]
                    df = pd.DataFrame.from_records(my_models.values())
                    df['song'] = df['song'].str.replace('/', '_')
                    df['artist'] = df['artist'].str.replace('/', '_')
                    table = df.to_dict(orient='records')

                    return render(request, 'songs/results.html', {'my_models': table})

        elif singer.is_valid():
            singer = singer.cleaned_data['artist']
            singer = singer.title()
            match = BillBoard.objects.filter(artist__contains=singer)
            if match:
                all = BillBoard.objects.all()
                total = pd.DataFrame.from_records(all.values())
                total['date2'] = pd.to_datetime(total['date'])
                sns.set_style("darkgrid")
                sns.color_palette("dark")
                plt.style.use('dark_background')
                plt.figure(figsize=(18, 10))
                art1 = total[total['artist'].str.contains(
                    singer, case=False, regex=False)]['date2']
                # final[final['artist'].str.contains(singer, case=False, regex=False)]['date'].dt.year.value_counts().plot(kind = 'bar')
                value = art1.dt.year.value_counts()
                value.sort_index(inplace=True)
                sns.barplot(x=value.index, y=value.values)

                plt.xticks(fontsize=18, rotation=90)
                plt.yticks(fontsize=22)
                plt.xlabel('Years', fontsize=20)
                plt.ylabel('Number of Songs', fontsize=20)
                plt.title("Track record of the artist", fontdict={
                          'family': 'serif', 'color': 'white', 'size': 30})

                path = os.path.join(settings.MEDIA_ROOT, 'graph1.png')
                plt.savefig(path)
                return render(request, 'songs/graph.html', {'graph': '/media/graph1.png'})
            else:
                messages.warning(
                    request, "The artist name you entered might be mispelled, or you might have better music taste than I do!")
                return redirect('home')

        elif artist.is_valid():
            artist = artist.cleaned_data['artist_top']
            sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id="49040ed518c04ad48bed57f27c5a9c01", client_secret="4828821a70fe4711b770b30642279c44",
                                 redirect_uri="http://localhost:8888/callback", scope=['user-library-read', 'user-top-read']))
            artist_name = artist
            results = sp.search(q='artist:' + artist_name, type='artist')
            artist_id = results['artists']['items'][0]['id']
            



            top_tracks = sp.artist_top_tracks(artist_id)
            
            for track in top_tracks['tracks']:
                print(track['artists'][0]['name'])
            return render(request, 'songs/spoti.py', {'top_track':top_tracks['tracks']})
           















    else:
        form = MyForm()
        singer = SingerForm()
        artist = ArtistTopForm()
        context = {'form': form, 'singer': singer, 'artist': artist}
        return render(request, 'songs/home.html', context)


def result(request, artist, song):
    song1 = song.replace("_", "/")
    artist1 = artist.replace("_", "/")
    final = BillBoard.objects.filter(
        song__contains=song1).filter(artist__contains=artist1)

    df = pd.DataFrame.from_records(final.values())
    df['date1'] = pd.to_datetime(df['date'])

    sns.set_style("darkgrid")
    plt.style.use('dark_background')
    print(plt.style.available)
    pic = df[(df['song'] == song) & (df['artist'] == artist)]
    fig, ax = plt.subplots(figsize=(12, 8), dpi=150)
    # sns.lineplot(data = pic, x = 'date1', y= 'rank', ax= ax, marker = 'o', color='red')
    sns.set(rc={'figure.figsize': (100, 100)})
    plt.xticks(rotation=360)
    plt.gca().yaxis.set_major_locator(plt.MaxNLocator(integer=True))
    plt.plot(pic['date1'], pic['rank'], marker='o',
             linewidth=2, color='magenta')
    plt.gca().invert_yaxis()
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)
    plt.xlabel('Date', fontsize=16)
    plt.ylabel('Rank', fontsize=16)
    plt.title("The performance of the Song on the Chart", fontdict={
              'family': 'serif', 'color': 'red', 'size': 15})

    path = os.path.join(settings.MEDIA_ROOT, 'graph.png')
    plt.savefig(path)

    return render(request, 'songs/graph.html', {'graph': '/media/graph.png'})
