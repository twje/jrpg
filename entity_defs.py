class EntityDefs:
    def __init__(self, definition):
        self.definition = definition

    def get_entity_def(self, entity_id):
        return self.definition["entities"].get(entity_id)

    def get_character_def(self, character_id):
        return self.definition["characters"].get(character_id)
