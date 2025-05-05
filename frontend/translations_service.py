TRANSLATIONS = {}

def update_translations(new_translations):
    global TRANSLATIONS
    TRANSLATIONS = new_translations

def get_translation(key):
    global TRANSLATIONS
    try:
        return TRANSLATIONS[key]
    except:
        return key