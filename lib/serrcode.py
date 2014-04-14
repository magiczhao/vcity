
UNKNOWN_OPERATION = -255
error_map = {
    UNKNOWN_OPERATION : "unknown operation"
}
def Strerror(code):
    if code in error_map:
        return error_map[code]
    return "unknown error!"

class VCityException(Exception):
    pass

if __name__ == "__main__":
    pass
