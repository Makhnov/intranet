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
        # Étape 1: Trouver 'stroke-width'
        print("Contenu original:", content)
        
        def replacement(match):
            # Étape 2: Vérifier le caractère suivant qui n'est pas un espace
            after_stroke_width = match.group(1)
            value = match.group(2)
            print(f"Caractère après 'stroke-width': '{after_stroke_width}'", f"Valeur détectée: {value}")

            # Étape 3 et 4: Construire la nouvelle chaîne de caractères
            new_value = f'calc(var(--cgs-stroke-width) * {value})'
            if after_stroke_width == ':':
                # 3a et 4a: Cas où on a trouvé ':', reconstruire la chaîne pour un style CSS
                return f'stroke-width: {new_value};'
            else:
                # 3b et 4b: Cas où on a trouvé '=', reconstruire la chaîne pour un attribut HTML
                return f'stroke-width="{new_value}"'

        # Cette expression régulière capture 'stroke-width' suivi par ':' ou '=' (avec gestion des espaces),
        # puis capture la valeur numérique jusqu'au prochain ';' ou espace ou guillemet.
        pattern = r'stroke-width\s*([:=])\s*["\']?\s*(\d+(?:\.\d+)?)(?=[;\s"\'\n])'
        modified_content = re.sub(pattern, replacement, content)
        
        print("Contenu modifié:", modified_content)
        return modified_content

class CustomRendition(AbstractRendition):
    image = models.ForeignKey(CustomImage, on_delete=models.CASCADE, related_name='renditions')

    class Meta:
        unique_together = (
            ('image', 'filter_spec', 'focal_point_key'),
        )
