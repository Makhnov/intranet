import io

from wagtail.images.image_operations import FilterOperation
from willow.svg import SvgImage, SvgWrapper

def sanitize_svg(svg_image: SvgImage) -> SvgImage:
    buf = io.BytesIO()

    # Write the underlying SvgWrapper's ElementTree to the buffer
    svg_image.image.write(buf)
    buf.seek(0)

    # Sans nettoyage, utiliser le SVG tel quel
    out = io.BytesIO(buf.read())
    return SvgImage(SvgWrapper.from_file(out))

class FilterSvgOperation(FilterOperation):
    def construct(self):
        pass

    def run(self, willow, image, env):
        if not isinstance(willow, SvgImage):
            return willow
        return sanitize_svg(willow)
