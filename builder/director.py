from creating_chord_collection.collection.resources.scales import scales
from PIL import Image

class Director:
    def __init__(self, builder):
        self._builder = builder
        self._composite_image = None
        self._current_row_images = []
        self._all_rows = []

    def _build_diagram(self, root, starting_fret, finger_ascending=None, scale=None, name=None):
        self._builder.draw_boundaries()
        self._builder.root = root
        self._builder.starting_fret = starting_fret
        self._builder.finger_ascending = finger_ascending
        self._builder.scale = scale
        self._builder.write_starting_fret()
        self._builder.draw_frets()
        self._builder.draw_strings()
        self._builder.draw_notes()
        self._builder.write_name(name)

    def build_chord(self, chord):
        # Generate the name for the chord
        chord_name = f"{chord.root}{chord.chord_type}"
        self._build_diagram(chord.root, chord.starting_fret, finger_ascending=chord.finger_ascending, name=chord_name)
        self._save_image()
        
    def build_scale(self, root, scale):
        self._builder.name_coordenate = (self._builder.name_coordenate[0] - 45, self._builder.name_coordenate[1])

        scale_name = None
        for key, value in scales.items():
            if value == scale:
                scale_name = f'{root} {key}'
                break
        if not scale_name:
            scale_name = root

        self._build_diagram(root, starting_fret=1, scale=scale, name=scale_name)
        self._save_image()
    
    def _save_image(self):
        """
        Save the current image internally.
        """
        image = self._builder.get_result()
        self._current_row_images.append(image)
        
    def _concatenate_images(self, images, direction='horizontal'):
        """
        Concatenate a list of images in the specified direction.
        """
        widths, heights = zip(*(i.size for i in images))
        if direction == 'horizontal':
            total_width = sum(widths)
            max_height = max(heights)
            combined_image = Image.new('RGB', (total_width, max_height))
            x_offset = 0
            for im in images:
                combined_image.paste(im, (x_offset, 0))
                x_offset += im.width
        else:  # vertical concatenation
            total_height = sum(heights)
            max_width = max(widths)
            combined_image = Image.new('RGB', (max_width, total_height))
            y_offset = 0
            for im in images:
                combined_image.paste(im, (0, y_offset))
                y_offset += im.height
        return combined_image


    def build_multiple_chords(self, chords, columns=4):
        for chord in chords:
            self.build_chord(chord)
            if len(self._current_row_images) == columns:
                self._all_rows.append(self._concatenate_images(self._current_row_images))
                self._current_row_images = []

        if self._current_row_images:  # Append any remaining images
            self._all_rows.append(self._concatenate_images(self._current_row_images))

        self._composite_image = self._concatenate_images(self._all_rows, direction='vertical')

    def save_image(self, file_path):
        """
        Save the final composite image to a file.
        """
        if self._composite_image:
            self._composite_image.save(file_path)
        else:
            print("No image to save.")

    def display_image(self):
        """
        Display the final composite image.
        """
        if self._composite_image:
            display(self._composite_image)
        else:
            print("No image to display.")

