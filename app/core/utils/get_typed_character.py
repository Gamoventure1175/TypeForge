from models import CharacterTyped


def is_space(event: CharacterTyped) -> bool:
    return ord(event.char) == 32
