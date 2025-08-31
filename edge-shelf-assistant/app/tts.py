import pyttsx3
_engine = None

def _get_engine():
    global _engine
    if _engine is None:
        _engine = pyttsx3.init()
    return _engine

def speak_to_file(text: str, out_path: str):
    eng = _get_engine()
    eng.save_to_file(text, out_path)
    eng.runAndWait()
    return out_path
