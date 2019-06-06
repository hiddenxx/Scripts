def getFixedString(s):
    return s.replace("/[^\x00-\x7F]/g", "");
