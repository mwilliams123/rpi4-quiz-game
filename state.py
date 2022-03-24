class State():
    """
    Parent class for individual game states to inherit from.
    """
    def __init__(self):
        self.store = {}
        
    def startup(self, store):
        """
        Called when a state resumes being active.
        Allows information to be passed between states.
        
        store: a dict passed from state to state
        """
        self.store = store
        
    def handle_event(self, event):
        """
        Handle a single event passed by the Game object.
        """
        pass
        
    
    def update(self, player_manager, elapsed_time):
        """
        Update the state. Called by the Game object once
        per frame. 
        
        dt: time since last frame
        """
        pass
        
    def draw(self, screen):
        """
        Draw everything to the screen.
        """
        pass