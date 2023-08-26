from animeflv import AnimeFLV

api = AnimeFLV()

#print(api.list(49))
anime_list = api.get_latest_animes()
print(anime_list[0])
print(anime_list[0].id)
#print(api.get_anime_info('nanatsu-no-taizai'))
#print(api.get_anime_info('akibas-trip-the-animation'))
#print(api.get_anime_info('pokemon-sun-moon'))
#id Anime 2
#title Anime 2
#poster Anime 2
#banner Anime 2
#synopsis Anime 2
#rating Anime 2
#genres Generos 1
#debut Anime 2
#type Anime 2
#episodes #EpisodeInfo(id, anime, image_preview,) [(),(),()] Episodios 3

#print(api.get_links('nanatsu-no-taizai', '1')) [(),(),()]

#server DownloadServer 4
#url DownloadServer 4

#print(api.get_video_servers('nanatsu-no-taizai', '1')) [[{}]]

#for server in servers:
    #print(server)
    #print("////////")
#server 4
#title 4
#ads 4
#url Episodios 4
#allow_mobile 4
#code 4


