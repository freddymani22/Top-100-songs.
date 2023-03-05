{% extends 'songs/base.html' %}

{% block music %}
    <ul>
     {% for track in top_track %}
         <li class = 'text-white'> <a  href = "https://youtube.com/results?search_query={{ track.name }}{{ track.artist.name }}">{{ track.name }} {{ track.artist.0.name }}</a></li>
         <p class = 'text_white'>{{ track.artist.name }}<p/>   
     {% endfor %}
    </ul>
{% endblock music %}