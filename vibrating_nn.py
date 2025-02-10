from manim import *
import random
import numpy as np

class VibratingNeuralNetwork(Scene):
    def create_background_network(self):
        # Network parameters
        num_nodes = 60
        connection_probability = 0.15
        movement_range = 0.2  # Increased movement range for more spontaneity

        # Create nodes
        nodes = VGroup()
        positions = []
        for _ in range(num_nodes):
            pos = np.array([random.uniform(-10, 10), random.uniform(-6, 6), 0])
            node = Circle(radius=0.1, color=WHITE, fill_opacity=0.01, stroke_opacity=0.2)
            node.move_to(pos)
            nodes.add(node)
            positions.append(pos)

        # Create connections
        connections = VGroup()
        for i in range(num_nodes):
            for j in range(i + 1, num_nodes):
                if random.random() < connection_probability:
                    line = Line(positions[i], positions[j], color=WHITE, stroke_opacity=0.1)
                    connections.add(line)

        def update_network(mobject, dt):
            # Update node positions with more randomness
            for i, node in enumerate(nodes):
                movement = np.array([
                    random.uniform(-movement_range, movement_range),
                    random.uniform(-movement_range, movement_range),
                    0
                ])
                node.shift(movement)
                positions[i] = node.get_center()

                # Randomly change node color for a cool effect
                if random.random() < 0.1:  # 10% chance to change color
                    node.set_color(random.choice([BLUE, GREEN, ORANGE, PURPLE, YELLOW, PINK, TEAL]))

            # Update connections with dynamic opacity and color
            connection_index = 0
            for i in range(num_nodes):
                for j in range(i + 1, num_nodes):
                    if connection_index < len(connections):
                        connections[connection_index].put_start_and_end_on(
                            positions[i],
                            positions[j]
                        )
                        # Randomly change connection color and opacity
                        if random.random() < 0.1:  # 10% chance to change color and opacity
                            connections[connection_index].set_stroke(
                                color=random.choice([BLUE, GREEN, ORANGE, PURPLE, YELLOW, PINK, TEAL]),
                                opacity=random.uniform(0.01, 0.1)
                            )
                        connection_index += 1

        nodes.add_updater(update_network)
        return VGroup(connections, nodes)

    def construct(self):
        # Add background networks
        background_network = self.create_background_network()
        self.add(background_network)

        words = ["Deep", "Learning", "n", "stuff"]
        all_nodes = VGroup()
        positions = []
        radius = 0.3  # Circle size
        total_layers = len(words)
        layer_colors = [BLUE, GREEN, ORANGE]  # Layer-based colors
        colors = [WHITE, WHITE]  # Edge colors

        # Step 1: Create animated popping circles with letters
        node_objects = []
        initial_connections = VGroup()
        spawn_animations = []

        for layer_idx, word in enumerate(words):
            for char in word:
                position = np.array([random.uniform(-4, 4), random.uniform(-2, 2), 0])
                positions.append(position)

                # node_color = layer_colors[layer_idx]
                node_color = WHITE

                # Circle with only border (no fill)
                circle = Circle(radius=radius, color=node_color, stroke_width=3, fill_opacity=0)
                letter = Text(char, font_size=36, color=WHITE).move_to(position)
                circle.move_to(position)

                node = VGroup(circle, letter)
                node_objects.append(node)
                all_nodes.add(node)

                # Popping animation
                spawn_animations.append(AnimationGroup(
                    GrowFromCenter(circle),
                    FadeIn(letter, shift=UP * 0.2),
                    lag_ratio=0.01
                ))

        # Create connections while spawning nodes
        connection_animations = []
        for i in range(len(all_nodes)):
            for j in range(i + 1, len(all_nodes)):
                if random.random() < 0.4:
                    start, end = self.adjust_line_end(positions[i], positions[j], radius)  # Unpack the tuple
                    line_color = colors[(i + j) % 2]
                    line = Line(start, end, color=line_color, stroke_width=1.5)  # Pass the unpacked points
                    initial_connections.add(line)
                    connection_animations.append(Create(line))

        self.play(
            AnimationGroup(*spawn_animations + connection_animations, lag_ratio=0.01),
            run_time=.8
        )


        # Remove old connections
        self.play(FadeOut(initial_connections), run_time=0.05)

        # Step 4: Reorganize into structured layers with same color per layer
        sorted_positions = []
        layer_gap = 1.2
        center_y_offset = -layer_gap * (total_layers - 1) / 2

        structured_nodes = VGroup()
        index = 0
        for i, word in enumerate(words):
            y_position = center_y_offset + layer_gap * (total_layers - i - 1)
            for j, char in enumerate(word):
                new_pos = np.array([j - len(word)/2, y_position, 0])
                sorted_positions.append(new_pos)

                # node_color = layer_colors[i]
                node_color = WHITE
                all_nodes[index][0].set_color(node_color)

                structured_nodes.add(all_nodes[index])
                index += 1

        self.play(
            AnimationGroup(
                *[structured_nodes[i].animate.move_to(sorted_positions[i]) for i in range(len(structured_nodes))],
                lag_ratio=0.01
            ),
            run_time=.5
        )

        # Step 5: Reconnect structured nodes
        structured_connections = VGroup()
        connection_animations = []
        for i in range(len(words) - 1):
            upper_start = sum(len(w) for w in words[:i])
            lower_start = sum(len(w) for w in words[:i + 1])
            for u in range(upper_start, lower_start):
                for l in range(lower_start, lower_start + len(words[i + 1])):
                    start, end = self.adjust_line_end(sorted_positions[u], sorted_positions[l],
                                                      radius)  # Unpack the tuple
                    line_color = colors[(u + l) % 2]
                    line = Line(start, end, color=line_color, stroke_width=2)  # Pass the unpacked points
                    structured_connections.add(line)
                    connection_animations.append(Create(line))

        self.play(
            AnimationGroup(*connection_animations, lag_ratio=0.01),
            run_time=.5
        )

        # Step 6: Apply Vibration Effect with more randomness
        def vibrate(mobject, dt):
            # Vibrate the nodes with more randomness
            for node in structured_nodes:
                node.shift(np.array([
                    random.uniform(-0.05, 0.05),  # Increased vibration range
                    random.uniform(-0.05, 0.05),
                    0
                ]))

                # Randomly change node color for a cool effect
                if random.random() < 0.1:  # 10% chance to change color
                    node[0].set_color(random.choice([BLUE, GREEN, ORANGE, PURPLE, YELLOW, PINK, TEAL]))

            # Update line positions with dynamic opacity and color
            index = 0
            for i in range(len(words) - 1):
                upper_start = sum(len(w) for w in words[:i])
                lower_start = sum(len(w) for w in words[:i + 1])
                for u in range(upper_start, lower_start):
                    for l in range(lower_start, lower_start + len(words[i + 1])):
                        # Get the current positions of the nodes
                        start_pos = structured_nodes[u].get_center()
                        end_pos = structured_nodes[l].get_center()

                        # Adjust the line to start and end at the edges of the circles
                        adjusted_start, adjusted_end = self.adjust_line_end(start_pos, end_pos, radius)

                        # Update the line's start and end points
                        structured_connections[index].put_start_and_end_on(adjusted_start, adjusted_end)

                        # Randomly change connection color and opacity
                        if random.random() < 0.1:  # 10% chance to change color and opacity
                            structured_connections[index].set_stroke(
                                color=random.choice([BLUE, GREEN, ORANGE, PURPLE, YELLOW, PINK, TEAL]),
                                opacity=random.uniform(0.1, 0.5)
                            )
                        index += 1

        self.add(structured_nodes, structured_connections)
        structured_nodes.add_updater(vibrate)

        self.wait(2)  # Increased wait time to enjoy the effects

    def adjust_line_end(self, start, end, radius):
        """ Adjusts the line to start and end at the edges of the circles. """
        direction = end - start
        unit_direction = direction / np.linalg.norm(direction)
        adjusted_start = start + unit_direction * radius
        adjusted_end = end - unit_direction * radius
        return adjusted_start, adjusted_end  # Return a tuple of two points