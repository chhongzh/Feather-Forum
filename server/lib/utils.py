# ---------------------------------------------------------------------------
def isSpecil(string: str, specil: str = "!@#$%^&*()+_|\\[]{}:;\"\'?/>.<,") -> bool:
    for char in specil:
        if (char in string):
            return True
    else:
        return False
# ---------------------------------------------------------------------------
