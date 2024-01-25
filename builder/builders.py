from PIL import Image, ImageDraw, ImageFont

class AbstractBuilder:
    all_notes = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
    open_string_notes = ["E", "B", "G", "D", "A", "E"]

    def __init__(self):
        self.image_size = None
        self.fret_edges = []
        self.frets_starting_points = []
        self.string_edges = []
        self.strings_starting_points = []
        self.notes_coordenates = None
        self.name_coordenate = None
        self.font = "/content/creating_chord_collection/builder/times.ttf"
        self.font_size = 50
        self.line_thickness = 3
        self.is_horizontal = None
        self.root = None
        self.starting_fret = None
        self.chord_type = None
        self.finger_ascending = None
        self.scale_name = None
        self.scale = None
        self.note_colors = {'C': (13, 116, 255), 'D': (255, 0, 6), 'E': (255, 242, 0), 'F': (152, 39, 201), 'G': (253, 148, 4), 'A': (32, 255, 49), 'B': (255, 77, 215)}


    def draw_boundaries(self):
        self.image = Image.new('RGB', self.image_size, 'white')
        self.draw = ImageDraw.Draw(self.image)

    def draw_frets(self):
        for fret_start in self.frets_starting_points:
            start_point = (fret_start, self.fret_edges[0]) if self.is_horizontal else (self.fret_edges[0], fret_start)
            end_point = (fret_start, self.fret_edges[1]) if self.is_horizontal else (self.fret_edges[1], fret_start)
            self.draw.line(start_point + end_point, fill='black', width=self.line_thickness)

    def write_name(self, name):
        try:
            font = ImageFont.truetype(self.font, self.font_size)
        except IOError:
            font = ImageFont.load_default()
        self.draw.text(self.name_coordenate, name, fill='black', font=font)

    def draw_notes(self, notes_style):
        raise NotImplementedError

    def get_result(self):
        return self.image



    def get_note_colors(self, note):
        if note in ['C', 'D', 'E', 'F', 'G', 'A', 'B']:
            return (self.note_colors[note], None)

        if '#' in note:
            note_index = self.all_notes.index(note)
            previous_note = self.all_notes[note_index - 1]
            next_note = self.all_notes[(note_index + 1) % len(self.all_notes)]
            return (self.note_colors[previous_note], self.note_colors[next_note])

        raise ValueError(f"Unrecognized note: {note}")


    def draw_note_at_coordenate(self, coordenate, color_a, color_b, rotation_angle=45, label=''):
        draw = ImageDraw.Draw(self.image)
        radius = 15
        upper_left = (coordenate[0] - radius, coordenate[1] - radius)
        lower_right = (coordenate[0] + radius, coordenate[1] + radius)

        # Draw the circle or pie chart
        if color_b is None:
            draw.ellipse([upper_left, lower_right], fill=color_a)
        else:
            start_angle = rotation_angle
            end_angle = start_angle + 180
            draw.pieslice([upper_left, lower_right], start=start_angle, end=end_angle, fill=color_a)
            draw.pieslice([upper_left, lower_right], start=end_angle, end=start_angle + 360, fill=color_b)

        # Draw the label
        if label:
            try:
                font = ImageFont.truetype(self.font, int(radius * 1.2))
            except IOError:
                font = ImageFont.load_default()

            text_bbox = draw.textbbox((0, 0), label, font=font)
            text_width = text_bbox[2] - text_bbox[0]
            text_height = text_bbox[3] - text_bbox[1]
            text_coordenate = (coordenate[0] - text_width / 2, coordenate[1] - text_height / 2 - 3)  # Shift 7 pixels up
            draw.text(text_coordenate, label, fill='black', font=font)

    def coordenate_to_note(self, coordenate):
        def calculate_note(string, fret):
            note_index = self.all_notes.index(self.open_string_notes[string])
            return self.all_notes[(note_index + fret) % len(self.all_notes)]

        def find_string_index(coord, coord_list):
            if coord in coord_list:
                return coord_list.index(coord)
            else:
                raise ValueError("Coordenate not found in diagram")

        if self.is_horizontal == False:
            string_coord, fret_coord = coordenate
            string_index = find_string_index(string_coord, self.notes_coordenates["strings"])
            fret_index = find_string_index(fret_coord, self.notes_coordenates["frets"])
        else:
            fret_coord, string_coord = coordenate
            fret_index = find_string_index(fret_coord, self.notes_coordenates["frets"])
            string_index = find_string_index(string_coord, self.notes_coordenates["strings"])
            fret_index += self.starting_fret - 1

        return calculate_note(string_index, fret_index)

    def get_chord_figure_coordenates(self):
        # Initialize an empty list to store coordenates
        chord_coordenates = []

        # Adjust fret numbers if the diagram is horizontal
        adjusted_finger_ascending = [
            fret + self.starting_fret - 1 if fret is not None else None
            for fret in self.finger_ascending
        ] if self.is_horizontal else self.finger_ascending

        # Iterate over the finger positions
        for string_index, fret in enumerate(adjusted_finger_ascending):
            if fret is not None:
                # Calculate the x and y coordenates
                if self.is_horizontal:
                    x_coord = self.notes_coordenates['frets'][fret]
                    y_coord = self.notes_coordenates['strings'][string_index]
                else:
                    y_coord = self.notes_coordenates['frets'][fret]
                    x_coord = self.notes_coordenates['strings'][string_index]

                # Append the coordenate to the list
                chord_coordenates.append((x_coord, y_coord))

        return chord_coordenates


    def calculate_scale_notes(self):
        # Calculate notes in the scale
        root_index = self.all_notes.index(self.root)
        scale_notes = [self.all_notes[(root_index + interval) % len(self.all_notes)] for interval in self.scale]
        return scale_notes

    def get_scale_figure_coordenates(self):
        scale_notes = self.calculate_scale_notes()
        scale_coordenates = []

        for string_index, open_note in enumerate(self.open_string_notes):
            for fret_index, fret in enumerate(self.notes_coordenates['frets']):
                # Calculate the note at this string and fret
                note_index = (self.all_notes.index(open_note) + fret_index) % len(self.all_notes)
                note = self.all_notes[note_index]

                # Check if the note is in the scale
                if note in scale_notes:
                    # Calculate the coordenate
                    if self.is_horizontal:
                        x_coord = fret
                        y_coord = self.notes_coordenates['strings'][string_index]
                    else:
                        y_coord = fret
                        x_coord = self.notes_coordenates['strings'][string_index]

                        # Adjust for starting fret if not horizontal
                        if self.starting_fret > 1 and fret_index == 0:
                            continue

                    # Append the coordenate to the list
                    scale_coordenates.append((x_coord, y_coord))

        return scale_coordenates


    def draw_notes(self):
        if self.finger_ascending is not None:
            chord_coords = self.get_chord_figure_coordenates()
            for coord in chord_coords:
                note = self.coordenate_to_note(coord)
                note_colors = self.get_note_colors(note)
                self.draw_note_at_coordenate(coord, *note_colors, label=note)

        if self.scale is not None:
            scale_coords = self.get_scale_figure_coordenates()
            for coord in scale_coords:
                note = self.coordenate_to_note(coord)
                note_colors = self.get_note_colors(note)
                self.draw_note_at_coordenate(coord, *note_colors, label=note)


class ShortBuilder(AbstractBuilder):
    def __init__(self):
        super().__init__()
        self.image_size = (351, 351)
        self.is_horizontal = False
        self.fret_edges = [78, 273]
        self.frets_starting_points = [107, 157, 207, 257, 307]
        self.string_edges = [107, 307]
        self.strings_starting_points = [273, 234, 195, 156, 117, 78]
        self.notes_coordenates = {"strings": [273, 234, 195, 156, 117, 78], "frets": [82, 132, 182, 232, 282]}
        self.name_coordenate = (145, 10)

    def draw_strings(self):
        custom_grey = (210, 210, 210)

        for index, string_start in enumerate(self.strings_starting_points):
            color = custom_grey if self.finger_ascending and self.finger_ascending[index] is None else 'black'
            start_point = (string_start, self.string_edges[0])
            end_point = (string_start, self.string_edges[1])
            self.draw.line(start_point + end_point, fill=color, width=self.line_thickness - 1)

    def write_starting_fret(self):
        try:
            font = ImageFont.truetype(self.font, 35)
        except IOError:
            font = ImageFont.load_default()

        starting_fret_text = str(self.starting_fret)
        self.draw.text((30, 110), starting_fret_text, fill='black', font=font)


class LongBuilder(AbstractBuilder):
    def __init__(self):
        super().__init__()
        self.image_size = (717, 362)
        self.is_horizontal = True
        self.fret_edges = [82, 277]
        self.frets_starting_points = [67, 117, 167, 217, 267, 317, 367, 417, 467, 517, 567, 617, 667]
        self.string_edges = [67, 667]
        self.strings_starting_points = [82, 121, 160, 199, 238, 277]
        self.notes_coordenates = {"strings": [82, 121, 160, 199, 238, 277], "frets": [42, 92, 142, 192, 242, 292, 342, 392, 442, 492, 542, 592, 642]}
        self.name_coordenate = (330, 7)

    def draw_strings(self):
        for index, string_start in enumerate(self.strings_starting_points):
            start_point = (self.string_edges[0], string_start)
            end_point = (self.string_edges[1], string_start)
            self.draw.line(start_point + end_point, fill='black', width=self.line_thickness - 1)

    def write_starting_fret(self):
        try:
            font = ImageFont.truetype(self.font, 20)
        except IOError:
            font = ImageFont.load_default()

        for i, fret_start in enumerate(self.frets_starting_points, start=1):
            if i > 12:  # Only write numbers for frets 1 to 12
                break
            fret_number_text = str(i)
            x_coordenate = fret_start + 15
            y_coordenate = 300
            self.draw.text((x_coordenate, y_coordenate), fret_number_text, fill='black', font=font)


