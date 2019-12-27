{% extends "default.md" %}
{% block frontmatter_guts -%}
layout: default
title: Playlist Bárjaké reďkovky
datatable: true
{%- endblock frontmatter_guts %}
{% block playlist %}
{: #table_id .display}
|#  |Interpret|Názov skladby|
|---|---------|-------------|
{% for song in songs -%}
|{{ loop.index }}|**{{ song.artist.strip() }}**|{{ song.title }}  
{% endfor %}
{% endblock playlist %}