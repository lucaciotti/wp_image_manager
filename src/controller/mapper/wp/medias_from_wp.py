from ...dto.wp.media import WpMediaDTO
from src.provider.wooApi import wooApi


class MediasFromWp:

    media_list = []
    media_to_update = []
    media_to_create = []

    def _retriveAllMedias(self):
        _wooApi = wooApi()
        page = 1
        while True:
            medias = _wooApi.getWooInstance('media', {'per_page': 100, 'page': page})
            if len(medias) == 0:  # no more products
                break
            page = page + 1
            self.media_list = self.media_list + medias

    def _mapToDTO(self):
        for media in self.media_list:
            slug = media['slug']
            mediaDTO = WpMediaDTO(slug, **media)
            # TODO
            # if mediaDTO.exist():
            #     self.media_to_update.add(mediaDTO)
            mediaDTO.dto2DB()


    def sync(self):
        self._retriveAllMedias()
        self._mapToDTO()
