from creating_chord_collection.collection.resources.scales import scales

class Director:
    def __init__(self, builder):
        self._builder = builder

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

    def save_image(self, file_path):
        """
        Save the image to a file.
        :param file_path: The path where the image will be saved.
        """
        image = self._builder.get_result()
        image.save(file_path)

    def display_image(self):
        """
        Display the image using the IPython display function.
        """
        image = self._builder.get_result()
        display(image)

        
