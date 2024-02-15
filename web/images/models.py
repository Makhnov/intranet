import re
from django.db import models
from wagtail.images.models import Image, AbstractImage, AbstractRendition

class CustomImage(AbstractImage):
    svg_html = models.TextField(blank=True, null=True, editable=False)
    admin_form_fields = Image.admin_form_fields

    def save(self, *args, **kwargs):
        # Vérifiez si le fichier est un SVG avant de le lire
        if self.is_svg():

            try:
                svg_bytes = self.file.read()
                svg_content = svg_bytes.decode('utf-8')
            except ValueError:
                svg_content = self.svg_html if self.svg_html else ''

            if not svg_content:
                pass
            else:
                svg_content = self.modify_svg_content(svg_content)

                self.svg_html = svg_content

        # Appel de la méthode save de la superclasse
        return super().save(*args, **kwargs)

    def modify_svg_content(self, content):        
        # Remplacement des couleurs
        content = self.replace_colors(content)        
        # Modification des stroke-width
        content = self.modify_stroke_width(content)   
             
        return content
    
    def replace_colors(self, content):
        black_patterns = [r"#000000\b", r"#000\b", r"black\b", r"rgb\(0,\s*0,\s*0\)", r"rgb\(0,0,0\)"]
        white_patterns = [r"#ffffff\b", r"#fff\b", r"white\b", r"rgb\(255,\s*255,\s*255\)", r"rgb\(255,255,255\)"]
        other_color_pattern = r"(#[0-9a-fA-F]{3,6}\b|rgb\(\d{1,3},\s*\d{1,3},\s*\d{1,3}\))"

        for pattern in black_patterns:
            content = re.sub(pattern, "var(--cgs-theme-dark)", content)

        for pattern in white_patterns:
            content = re.sub(pattern, "var(--cgs-theme-light)", content)

        # Remplacement des autres couleurs
        content = re.sub(other_color_pattern, "var(--cgs-theme-primary)", content)

        return content

    def modify_stroke_width(self, content):
        pattern = r'(stroke-width)\s*([:=])\s*"?\s*(\d+(?:\.\d+)?)\s*"?'
        replacement = lambda m: f"{m.group(1)}{m.group(2)} calc(var(--cgs-stroke-width) * {m.group(3)})" + ('"' if m.group(2) == '=' else '')

        return re.sub(pattern, replacement, content)    
    

class CustomRendition(AbstractRendition):
    image = models.ForeignKey(CustomImage, on_delete=models.CASCADE, related_name='renditions')

    class Meta:
        unique_together = (
            ('image', 'filter_spec', 'focal_point_key'),
        )
