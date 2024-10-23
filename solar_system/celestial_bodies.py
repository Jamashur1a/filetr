import math

class Planet:
    def __init__(self, name: str, radius: float, mass: float, x: float, y: float) -> None:
        """
        Initialize a Planet object.
        
        Parameters:
        - name (str): The name of the planet.
        - radius (float): The radius of the planet.
        - mass (float): The mass of the planet.
        - x (float): The initial x-coordinate of the planet's position.
        - y (float): The initial y-coordinate of the planet's position.
        """
        self.name = name
        self.radius = radius
        self.mass = mass
        self.x = x
        self.y = y

        # Set the initial velocity to 0
        self.x_velocity = 0
        self.y_velocity = 0

        # Graphics color representation
        self.color = (255, 255, 255)
    
    def add_force(self, direction: tuple, force: float) -> None:
        """
        Add a force to the planet, affecting its velocity.
        
        Parameters:
        - direction (tuple): A tuple representing the direction of the force (dx, dy).
        - force (float): The magnitude of the force to apply.
        """
        # Calculate the force applied to the velocity
        x_force = force * direction[0] / self.mass
        y_force = force * direction[1] / self.mass
        
        # Update the planet's velocity based on the applied force
        self.x_velocity += x_force
        self.y_velocity += y_force
    
    def move_toward_direction(self, direction: tuple, units: float) -> None:
        """
        Move the planet in a specific direction by a certain number of units.
        
        Parameters:
        - direction (tuple): A tuple representing the direction to move (dx, dy).
        - units (float): The distance to move in the specified direction.
        """
        angle = math.atan2(direction[1], direction[0])
        self.x += units * math.cos(angle)
        self.y += units * math.sin(angle)
    
    def set_color(self, color: tuple) -> None:
        """
        Set the color of the planet.
        
        Parameters:
        - color (tuple): A tuple representing the RGB color of the planet.
        """
        self.color = color

    def update_position(self) -> None:
        """
        Update the planet's position based on its current velocity.
        """
        self.x += self.x_velocity
        self.y += self.y_velocity

    def __str__(self) -> str:
        """
        Return a string representation of the planet.
        
        Returns:
        - str: A string describing the planet's name, radius, mass, and position.
        """
        return f"{self.name} ({self.radius}km, {self.mass}kg) at (x = {self.x}, y = {self.y})"
