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

        # Write the name on the diagram
        if name:
            self._builder.write_name(name)

    def build_chord(self, chord):
        # Generate the name for the chord
        chord_name = f"{chord.root} {chord.chord_type}"
        self._build_diagram(chord.root, chord.starting_fret, finger_ascending=chord.finger_ascending, name=chord_name)

    def build_scale(self, root, scale):
        # Find the scale name or use the string representation of the scale
        scale_name = None
        for key, value in scales.items():
            if value == scale:
                scale_name = key
                break
        if not scale_name:
            scale_name = str(scale)

        self._build_diagram(root, starting_fret=1, scale=scale, name=scale_name)
