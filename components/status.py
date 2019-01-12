from game_messages import Message
from components.status_type import StatusType


import status_effects


class Status:
    def __init__(self, status_type, status_function=None, duration=None, **kwargs):
        self.status_function = status_function
        self.status_kwargs = kwargs
        self.status_type = status_type
        self.status_kwargs = kwargs
        self.duration = duration

    def to_json(self):
        json_data = {
            'use_function': self.status_function.__name__ if self.use_function is not None else None,
            'function_kwargs': self.function_kwargs,
            'status_type': self.status_type,
            'status_kwargs': self.status_kwargs,
            'duration': self.duration
        }

        return json_data

    @staticmethod
    def from_json(json_data):
        status_function_name = json_data.get('status_function')
        status_kwargs = json_data.get('status_kwargs', {})
        status_type = json_data.get('status_type')
        duration = json_data.get('duration')

        if status_function_name:
            status_function = getattr(status_effects, status_function_name)
        else:
            status_function = None

        status = Status(status_type, duration=duration, status_function=status_function, **status_kwargs)

        return status