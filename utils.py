# Assuming finishedExercises is the given dictionary containing Exercise objects
def to_dict(obj):
    if isinstance(obj, list):
        return [to_dict(item) for item in obj]
    elif hasattr(obj, '__dict__'):
        return {key: to_dict(value) for key, value in obj.__dict__.items()}
    else:
        return obj
