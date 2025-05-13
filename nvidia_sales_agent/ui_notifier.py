from typing import Callable, Dict, Any

class UINotifier:
    """
    Provides real-time UI notifications for agent activities.
    """
    
    def __init__(self, callback: Callable[[Dict[str, Any]], None]):
        """
        Initialize the UINotifier with a callback function.
        
        Args:
            callback: Function that will be called with notification data
        """
        self.callback = callback
        
    def notify(self, notification: Dict[str, Any]):
        """
        Send a notification to the UI.
        
        Args:
            notification: Dictionary containing notification data
        """
        if self.callback:
            self.callback(notification) 