import cloudscraper
import json, re
import html

from typing import Dict, List, Optional, Tuple, Type, Union
from types import TracebackType
from bs4 import BeautifulSoup, Tag, ResultSet
from urllib.parse import unquote, urlencode
from enum import Flag, auto
from .exception import AnimeFLVParseError
from dataclasses import dataclass


def removeprefix(str: str, prefix: str) -> str:
    """
    Remove the prefix of a given string if it contains that
    prefix for compatability with Python >3.9

    :param _str: string to remove prefix from.
    :param episode: prefix to remove from the string.
    :rtype: str
    """

    if type(str) is type(prefix):
        if str.startswith(prefix):
            return str[len(prefix) :]
        else:
            return str[:]


def parse_table(table: Tag):
    columns = list([x.string for x in table.thead.tr.find_all("th")])
    rows = []

    for row in table.tbody.find_all("tr"):
        values = row.find_all("td")

        if len(values) == 1 and "No hay links de descarga" in values[0].get_text():
            # Manejar la fila unificada de "No hay links de descarga"
            rows.append({"No hay links de descarga": "No hay links de descarga"})
        elif len(values) != len(columns):
            raise AnimeFLVParseError("Don't match values size with columns size")
        else:
            rows.append({h: x for h, x in zip(columns, values)})

    return rows



BASE_URL = "https://animeflv.net"
BROWSE_URL = "https://animeflv.net/browse"
ANIME_VIDEO_URL = "https://animeflv.net/ver/"
ANIME_URL = "https://animeflv.net/anime/"
BASE_EPISODE_IMG_URL = "https://cdn.animeflv.net/screenshots/"


@dataclass
class EpisodeInfo:
    id: Union[str, int]
    anime: str
    image_preview: Optional[str] = None


@dataclass
class AnimeInfo:
    id: Union[str, int]
    title: str
    poster: Optional[str] = None
    banner: Optional[str] = None
    synopsis: Optional[str] = None
    rating: Optional[str] = None
    genres: Optional[List[str]] = None
    debut: Optional[str] = None
    type: Optional[str] = None
    episodes: Optional[List[EpisodeInfo]] = None
    
    def __post_init__(self):
        # Verificar si la propiedad 'synopsis' no es None y, si es así, aplicar strip()
        if self.synopsis is not None:
            self.synopsis = self.synopsis.strip()


@dataclass
class DownloadLinkInfo:
    server: str
    url: str


class EpisodeFormat(Flag):
    Subtitled = auto()
    Dubbed = auto()


class AnimeFLV(object):
    def __init__(self, *args, **kwargs):
        session = kwargs.get("session", None)
        self._scraper = cloudscraper.create_scraper(session)

    def close(self) -> None:
        self._scraper.close()

    def __enter__(self) -> "AnimeFLV":
        return self

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> None:
        self.close()

    def get_links(
        self,
        id: str,
        episode: Union[str, int],
        format: EpisodeFormat = EpisodeFormat.Subtitled,
        **kwargs,
    ) -> List[DownloadLinkInfo]:
        """
        Get download links of specific episode.
        Return a list of dictionaries like:
        [
            {
                "server": "...",
                "url": "..."
            },
            ...
        ]

        :param id: Anime id, like as 'nanatsu-no-taizai'.
        :param episode: Episode id, like as '1'.
        :param **kwargs: Optional arguments for filter output (see doc).
        :rtype: list
        """
        response = self._scraper.get(f"{ANIME_VIDEO_URL}{id}-{episode}")
        soup = BeautifulSoup(response.text, "lxml")
        table = soup.find("table", attrs={"class": "RTbl"})

        try:
            ret = []

            if table:
                rows = parse_table(table)
                
                for row in rows:
                    if (
                        row.get("FORMATO") == "SUB" and EpisodeFormat.Subtitled in format
                    ) or (
                        row.get("FORMATO") == "LAT" and EpisodeFormat.Dubbed in format
                    ):
                        ret.append(
                            DownloadLinkInfo(
                                server=row.get("SERVIDOR", ""),
                                url=re.sub(
                                    r"^http[s]?://ouo.io/[A-Za-z0-9]+/[A-Za-z0-9]+\?[A-Za-z0-9]+=",
                                    "",
                                    unquote(row["DESCARGAR"].a["href"]),
                                ),
                            )
                        )

            return ret
        except Exception as exc:
            raise AnimeFLVParseError(exc)


    def list(self, page: int = None) -> List[Dict[str, str]]:
        """
        Shortcut for search(query=None)
        """

        return self.search(page=page)

    def search(self, query: str = None, page: int = None) -> List[AnimeInfo]:
        """
        Search in animeflv.net by query.
        :param query: Query information like: 'Nanatsu no Taizai'.
        :param page: Page of the information return.
        :rtype: list[AnimeInfo]
        """

        if page is not None and not isinstance(page, int):
            raise TypeError

        params = dict()
        if query is not None:
            params["q"] = query
        if page is not None:
            params["page"] = page
        params = urlencode(params)

        url = f"{BROWSE_URL}"
        if params != "":
            url += f"?{params}"

        response = self._scraper.get(url)
        soup = BeautifulSoup(response.text, "lxml")

        elements = soup.select("div.Container ul.ListAnimes li article")

        if elements is None:
            raise AnimeFLVParseError("Unable to get list of animes")

        return self._process_anime_list_info(elements)

    def get_video_servers(
        self,
        id: str,
        episode: int,
        format: EpisodeFormat = EpisodeFormat.Subtitled,
        **kwargs,
    ) -> List[Dict[str, str]]:
        """
        Get in video servers, this work only using the iframe element.
        Return a list of dictionaries.

        :param id: Anime id, like as 'nanatsu-no-taizai'.
        :param episode: Episode id, like as '1'.
        :rtype: list
        """

        response = self._scraper.get(f"{ANIME_VIDEO_URL}{id}-{episode}")
        soup = BeautifulSoup(response.text, "lxml")
        scripts = soup.find_all("script")

        servers = []

        for script in scripts:
            content = str(script)
            if "var videos = {" in content:
                videos = content.split("var videos = ")[1].split(";")[0]
                data = json.loads(videos)

                if "SUB" in data and EpisodeFormat.Subtitled in format:
                    servers.append(data["SUB"])
                if "LAT" in data and EpisodeFormat.Dubbed in format:
                    servers.append(data["LAT"])
        
        if servers:  # Verifica si la lista no está vacía
            return servers[0]  # Devuelve el primer elemento de la lista
        else:
            return []  # Si la lista está vacía, devuelve una lista vacía

    def get_latest_episodes(self) -> List[EpisodeInfo]:
        """
        Get a list of new episodes released (possibly this last week).
        Return a list

        :rtype: list
        """

        response = self._scraper.get(BASE_URL)
        soup = BeautifulSoup(response.text, "lxml")

        elements = soup.select("ul.ListEpisodios li a")
        ret = []

        for element in elements:
            try:
                anime, _, id = element["href"].rpartition("-")

                ret.append(
                    EpisodeInfo(
                        id=id,
                        anime=removeprefix(anime, "/ver/"),
                        image_preview=f"{BASE_URL}{element.select_one('span.Image img').get('src')}",
                    )
                )
            except Exception as exc:
                raise AnimeFLVParseError(exc)

        return ret

    def get_latest_animes(self) -> List[AnimeInfo]:
        """
        Get a list of new animes released.
        Return a list

        :rtype: list
        """

        response = self._scraper.get(BASE_URL)
        soup = BeautifulSoup(response.text, "lxml")

        elements = soup.select("ul.ListAnimes li article")

        if elements is None:
            raise AnimeFLVParseError("Unable to get list of animes")

        return self._process_anime_list_info(elements)

    def get_anime_info(self, id: str) -> AnimeInfo:
        """
        Get information about specific anime.
        Return an AnimeInfo object.

        :param id: Anime id, like as 'nanatsu-no-taizai'.
        :rtype: AnimeInfo
        """
        response = self._scraper.get(f"{ANIME_URL}/{id}")
        soup = BeautifulSoup(response.text, "lxml")
        information = {
            "title": "",
            "poster": "",
            "synopsis": "",
            "rating": "",
            "debut": "",
            "type": "",
            "banner": "",
        }

        # Obtener título
        title_element = soup.select_one(
            "body div.Wrapper div.Body div div.Ficha.fchlt div.Container h1.Title"
        )
        if title_element:
            title = title_element.get_text()
            information["title"] = title.replace("'", "\\'")

        # Obtener sinopsis
        synopsis_element = soup.select_one(
            "body div div div div div main section div.Description p"
        )
        if synopsis_element:
            synopsis = synopsis_element.get_text()
            information["synopsis"] = synopsis.replace("'", "\\'")

        # Obtener otros detalles
        information["rating"] = soup.select_one(
            "body div div div.Ficha.fchlt div.Container div.vtshr div.Votes span#votes_prmd"
        ).string
        information["debut"] = soup.select_one(
            "body div.Wrapper div.Body div div.Container div.BX.Row.BFluid.Sp20 aside.SidebarA.BFixed p.AnmStts"
        ).string
        information["type"] = soup.select_one(
            "body div.Wrapper div.Body div div.Ficha.fchlt div.Container span.Type"
        ).string

        # Obtener póster
        poster_element = soup.select_one(
            "body div div div div div aside div.AnimeCover div.Image figure img"
        )
        if poster_element:
            information["poster"] = BASE_URL + "/" + poster_element.get("src", "")

        # Obtener banner
        information["banner"] = (
            information["poster"].replace("covers", "banners").strip()
        )

        # Obtener géneros
        genres = []
        for element in soup.select("main.Main section.WdgtCn nav.Nvgnrs a"):
            if "=" in element["href"]:
                genres.append(element["href"].split("=")[1])

        # Obtener episodios
        episodes_data = []
        episodes = []
        try:
            for script in soup.find_all("script"):
                contents = str(script)
                if "var anime_info = [" in contents:
                    anime_info = contents.split("var anime_info = ")[1].split(";")[0]
                    info_ids = json.loads(anime_info)
                    AnimeThumbnailsId = info_ids[0][0]
                    animeId = info_ids[0][2]

                if "var episodes = [" in contents:
                    data = contents.split("var episodes = ")[1].split(";")[0]
                    episodes_data.extend(json.loads(data))

            for episode, _ in episodes_data:
                episodes.append(
                    EpisodeInfo(
                        id=episode,
                        anime=id,
                        image_preview=f"{BASE_EPISODE_IMG_URL}{AnimeThumbnailsId}/{episode}/th_3.jpg",
                    )
                )
        except (ValueError, IndexError, KeyError, json.JSONDecodeError) as exc:
            print(f"Error while parsing anime info {animeId}: {exc}")

        return AnimeInfo(
            id=id,
            episodes=episodes,
            genres=genres,
            **information,
        )


    def _process_anime_list_info(self, elements: ResultSet) -> List[AnimeInfo]:
        ret = []

        for element in elements:
            try:
                ret.append(
                    AnimeInfo(
                        id=removeprefix(
                            element.select_one("div.Description a.Button")["href"][1:],
                            "anime/",
                        ),
                        title=element.select_one("a h3").string,
                        poster=(
                            element.select_one("a div.Image figure img").get(
                                "src", None
                            )
                            or element.select_one("a div.Image figure img")["data-cfsrc"]
                        ),
                        banner=(
                            element.select_one("a div.Image figure img").get(
                                "src", None
                            )
                            or element.select_one("a div.Image figure img")["data-cfsrc"]
                        )
                        .replace("covers", "banners")
                        .strip(),
                        type=element.select_one("div.Description p span.Type").string,
                        synopsis=(
                            element.select("div.Description p")[1].string.strip()
                            if element.select("div.Description p")[1].string
                            else None
                        ),
                        rating=element.select_one("div.Description p span.Vts").string,
                        debut=(
                            element.select_one("a span.Estreno").string.lower()
                            if element.select_one("a span.Estreno")
                            else None
                        ),
                    )
                )
            except Exception as exc:
                raise AnimeFLVParseError(exc)

        return ret
