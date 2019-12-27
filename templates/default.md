---
{% block frontmatter_guts -%}
layout: default
title: Playlist Bárjaké reďkovky
{%- endblock frontmatter_guts %}
---
# Bárjaké reďkovky
Toto je aktuálna forma playlistu Bárjaké reďkovky z dňa {{ time }}:  

*Nultý (000) sondžik je ako vždy Bon Jovi - You Give Love a Bad Name*  

{% block playlist %}
{% for song in songs -%}
{{ loop.index }}. **{{ song.artist.strip() }}** - {{ song.title }}  
{% endfor %}
{% endblock playlist %}

Použitý seed: ```{{ seed }}```