{% extends "default.md" %}
{% block playlist %}
{% for song in songs -%}
{{ loop.index }}. **{{ song.artist.strip() }}** - {{ song.title }}  
{% endfor %}
{% endblock playlist %}