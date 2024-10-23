import pygame
import json
import math

#costum imports
from celestial_bodies import Planet



class SolarSystem:
    def __init__(self):
        """Initialize the solar system simulation with planets and settings."""
        self.planets = []
        self.settings = self.import_settings()

        if not self.settings:
            print("File not found. Please check the file path.")
            quit()  # Exit if settings file is not found

        self.height = self.settings["simulation_settings"]["screen_height"]
        self.width = self.settings["simulation_settings"]["screen_width"]
        self.fps = self.settings["simulation_settings"]["fps"]
        self.gravitational_constant = self.settings["simulation_settings"]["gravitational_constant"]

        self.colors = self.get_colors()
        self.create_planets()

        pygame.init()
        pygame.display.set_caption("Solar System Simulation")
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()

    def run(self):
        """Main loop for running the simulation."""
        while True:
            self.input()
            self.update()
            self.draw()
            pygame.display.update()
            self.clock.tick(self.fps)

    def create_planets(self):
        """Create the planets for the simulation."""
        earth = Planet("Earth", 30, 30, self.width // 2, self.height // 2)
        earth.set_color((0, 0, 255))
        moon = Planet("Moon", 10, 1, earth.x, 200)
        moon.set_color((255, 255, 255))

        moon.add_force((1, 0.5), 0.9)  # Initial force applied to the moon

        self.planets.append(earth)
        self.planets.append(moon)

    def get_colors(self):
        """Retrieve color settings from the configuration."""
        colors = self.settings["material_settings"]["Colors"]  # type: ignore
        return {key: eval(value) for key, value in colors.items()}

    def import_settings(self):
        """Load simulation settings from a JSON file."""
        try:
            with open("settings.json") as settings_file:
                settings = json.load(settings_file)
                return settings
        except FileNotFoundError:
            print("File not found. Please check the file path.")
            return None

    def draw(self):
        """Clear the screen and draw all planets."""
        self.screen.fill((0, 0, 0))
        self.draw_planets()

    def draw_planets(self):
        """Draw all planets on the screen."""
        for planet in self.planets:
            px, py, pr = int(planet.x), int(planet.y), int(planet.radius)
            pygame.draw.circle(self.screen, planet.color, (px, py), pr)

    def update(self):
        """Update the simulation state by calculating forces and moving planets."""
        self.calculate_forces()
        self.update_planets()
        self.check_for_collisions()

    def calculate_forces(self):
        """Calculate gravitational forces between planets and apply them."""
        for first_planet in self.planets:
            for second_planet in self.planets:
                if first_planet == second_planet:
                    continue

                direction = (second_planet.x - first_planet.x, second_planet.y - first_planet.y)
                distance = math.hypot(direction[0], direction[1])

                # Normalize the direction vector if distance is non-zero
                if distance > 0:
                    normalized_direction = (direction[0] / distance, direction[1] / distance)

                    # Calculate gravitational force
                    force_magnitude = (self.gravitational_constant * first_planet.mass * second_planet.mass) / distance**2
                    first_planet.add_force(normalized_direction, force_magnitude)

    def update_planets(self):
        """Update the position of all planets based on their velocities."""
        for planet in self.planets:
            planet.update_position()

    def check_for_collisions(self):
        """Check for collisions between planets and resolve them."""
        for planet in self.planets:
            for other_planet in self.planets:
                if planet == other_planet:
                    continue

                combined_radius = planet.radius + other_planet.radius
                distance = math.hypot(planet.x - other_planet.x, planet.y - other_planet.y)

                if distance > combined_radius:
                    continue

                first_planet_direction = (planet.x - other_planet.x, planet.y - other_planet.y)
                second_planet_direction = (other_planet.x - planet.x, other_planet.y - planet.y)

                dominant_planet = planet if planet.mass > other_planet.mass else other_planet
                subtract_distance = combined_radius - distance

                if other_planet.mass == planet.mass:
                    planet.move_toward_direction(first_planet_direction, subtract_distance / 2)
                    other_planet.move_toward_direction(second_planet_direction, subtract_distance / 2)
                else:
                    percent_to_move = (max(planet.mass, other_planet.mass) * 100) / dominant_planet.mass
                    planet_move_dist = subtract_distance * (100 - percent_to_move) / 100
                    other_planet_move_dist = subtract_distance * percent_to_move / 100

                    planet.move_toward_direction(first_planet_direction, planet_move_dist)
                    other_planet.move_toward_direction(second_planet_direction, other_planet_move_dist)

    def input(self):
        """Handle user input events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()


if __name__ == "__main__":
    solar_system = SolarSystem()
    solar_system.run()
