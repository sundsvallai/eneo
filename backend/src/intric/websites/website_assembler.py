from intric.websites.website_models import (
    Website,
    WebsitePublic,
    WebsiteMetadata,
)


class WebsiteAssembler:

    @staticmethod
    def from_website_to_model(website: Website):
        return WebsitePublic(
            **website.model_dump(), metadata=WebsiteMetadata(size=website.size)
        )
