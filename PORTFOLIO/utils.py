def convert_length(value, from_unit, to_unit):
    units = {
        'mm': 0.001,
        'cm': 0.01,
        'm': 1.0,
        'km': 1000.0,
        'in': 0.0254,
        'ft': 0.3048,
        'yd': 0.9144,
        'mi': 1609.34,
    }

    if from_unit not in units or to_unit not in units:
        raise ValueError("Invalid unit.")

    result = value * units[from_unit] / units[to_unit]
    return result

def convert_speed(value, from_unit, to_unit):
    units = {
        'm/s': 1.0,
        'km/h': 0.277778,
        'mi/h': 0.44704,
        'ft/s': 0.3048,
    }

    if from_unit not in units or to_unit not in units:
        raise ValueError("Invalid unit.")

    result = round(value * units[from_unit] / units[to_unit], 1)
    return result

def convert_temperature(value, from_unit, to_unit):
    if from_unit == to_unit:
        return value

    if from_unit == 'C':
        if to_unit == 'F':
            result = (value * 9/5) + 32
        elif to_unit == 'K':
            result = value + 273.15
        else:
            raise ValueError("Invalid unit.")
    elif from_unit == 'F':
        if to_unit == 'C':
            result = (value - 32) * 5/9
        elif to_unit == 'K':
            result = (value - 32) * 5/9 + 273.15
        else:
            raise ValueError("Invalid unit.")
    elif from_unit == 'K':
        if to_unit == 'C':
            result = value - 273.15
        elif to_unit == 'F':
            result = (value - 273.15) * 9/5 + 32
        else:
            raise ValueError("Invalid unit.")
    else:
        raise ValueError("Invalid unit.")

    return result

def convert_weight(value, from_unit, to_unit):
    units = {
        'g': 1.0,
        'kg': 1000.0,
        'mg': 0.001,
        'oz': 28.3495,
        'lb': 453.592,
        'ton': 1000000.0,
    }

    if from_unit not in units or to_unit not in units:
        raise ValueError("Invalid unit.")

    result = round(value * units[from_unit] / units[to_unit], 2)
    return result










