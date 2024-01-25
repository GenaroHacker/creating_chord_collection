class Director:
    def __init__(self, builder):
        self._builder = builder

    def _build_diagram(self, root, starting_fret, finger_ascending=None, scale=None):
        self._builder.draw_boundaries()
        self._builder.root = root
        self._builder.starting_fret = starting_fret
        self._builder.finger_ascending = finger_ascending
        self._builder.scale = scale
        self._builder.write_starting_fret()
        self._builder.draw_frets()
        self._builder.draw_strings()

        self._builder.draw_notes()

    def build_chord(self, chord):
        self._build_diagram(chord.root, chord.starting_fret, finger_ascending=chord.finger_ascending)

    def build_scale(self, root, scale):
        self._build_diagram(root, starting_fret=1, scale=scale)
