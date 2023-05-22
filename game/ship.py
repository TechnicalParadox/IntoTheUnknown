# Ship class, represents a ship in the game. The ship has a location, condition, capabilities, resources, mount points, crew members, subsystems with individual health, etc.
# Ships will have a model that fits subsystems inside the shell. During combat, etc, certain areas are more likely to be hit depending on enemy relative location.
class Ship:
    def __init__(self, name, location, condition, capabilities, resources, mount_points, crew_members, subsystems):
        self.location = location
        self.condition = condition
        self.capabilities = capabilities

    def repair(self):
        # Implement ship repair logic here
        pass

    def upgrade(self):
        # Implement ship upgrade logic here
        pass

    # Add more ship-related methods as needed

# CrewMember class, represents a crew member on the ship. All crew members are capable of any task but it is affected by their skill levels.
class CrewMember:
    def __init__(self, name, skills=None):
        self.name = name
        if skills is None:
            self.skills = {
                'piloting': 0.0,
                'engineering': 0.0,
                'combat': 0.0,
                'science': 0.0,
                'medical': 0.0
            }
        else:
            self.skills = skills

# Captain class, represents the captain of the ship. This will be the player, TODO: eventually the player can be any crew member. The captain is the only one with full control of the ship's AI.
