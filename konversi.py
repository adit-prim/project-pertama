def binary_to_gray(binary_str):
    binary = int(binary_str, 2)
    gray = binary ^ (binary >> 1)
    return format(gray, f'0{len(binary_str)}b')

def gray_to_binary(gray_str):
    gray = int(gray_str, 2)
    mask = gray
    while mask != 0:
        mask >>= 1
        gray ^= mask
    return format(gray, f'0{len(gray_str)}b')

def decimal_to_excess3(n):
    return ''.join([format(int(d)+3, '04b') for d in str(n)])

def excess3_to_decimal(excess_str):
    if len(excess_str) % 4 != 0:
        raise ValueError("Excess-3 harus terdiri dari kelipatan 4 bit.")
    result = ''
    for i in range(0, len(excess_str), 4):
        nibble = excess_str[i:i+4]
        val = int(nibble, 2) - 3
        if val < 0 or val > 9:
            raise ValueError("Digit Excess-3 tidak valid.")
        result += str(val)
    return int(result)

def to_decimal(value, base_from):
    try:
        if '.' in value:
            int_part, frac_part = value.split('.')
        else:
            int_part, frac_part = value, ''

        base_dict = {
            'Biner': 2,
            'Desimal': 10,
            'Heksadesimal': 16,
            'Octal': 8
        }

        if base_from in base_dict:
            base = base_dict[base_from]
            decimal_int = int(int_part, base) if int_part else 0

            # Konversi pecahan
            decimal_frac = 0
            for i, digit in enumerate(frac_part):
                if base <= 10:
                    val = int(digit)
                else:
                    val = int(digit, 16)
                decimal_frac += val / (base ** (i + 1))

            return decimal_int + decimal_frac

        elif base_from == 'Desimal':
            return float(value)

        elif base_from in ['BCD', 'Excess-3', 'Gray Code']:
            if '.' in value:
                raise ValueError(f"{base_from} tidak mendukung pecahan.")

            if base_from == 'BCD':
                if len(value) % 4 != 0:
                    raise ValueError("BCD harus kelipatan 4 bit")
                decimal = ''
                for i in range(0, len(value), 4):
                    nibble = value[i:i+4]
                    digit = int(nibble, 2)
                    if digit > 9:
                        raise ValueError("Digit BCD tidak valid")
                    decimal += str(digit)
                return int(decimal)
            elif base_from == 'Excess-3':
                return excess3_to_decimal(value)
            elif base_from == 'Gray Code':
                binary = gray_to_binary(value)
                return int(binary, 2)
    except:
        raise ValueError(f"Input tidak valid untuk basis {base_from}")

def from_decimal(decimal, base_to):
    if base_to in ['Biner', 'Heksadesimal', 'Octal']:
        if isinstance(decimal, float):
            int_part = int(decimal)
            frac_part = decimal - int_part

            # Konversi integer part
            if base_to == 'Biner':
                result = bin(int_part)[2:]
            elif base_to == 'Heksadesimal':
                result = hex(int_part)[2:].upper()
            elif base_to == 'Octal':
                result = oct(int_part)[2:]

            # Konversi fractional part
            result += '.'
            count = 0
            while frac_part > 0 and count < 10:  # Maks 10 digit
                frac_part *= {'Biner': 2, 'Heksadesimal': 16, 'Octal': 8}[base_to]
                digit = int(frac_part)
                if base_to == 'Biner':
                    result += str(digit)
                elif base_to == 'Heksadesimal':
                    result += hex(digit)[2:].upper()
                elif base_to == 'Octal':
                    result += str(digit)
                frac_part -= digit
                count += 1
            return result.rstrip('.')

        else:
            # Asli untuk bilangan bulat
            if base_to == 'Biner':
                return bin(decimal)[2:]
            elif base_to == 'Heksadesimal':
                return hex(decimal)[2:].upper()
            elif base_to == 'Octal':
                return oct(decimal)[2:]

    elif base_to == 'Desimal':
        return str(decimal)

    elif base_to == 'BCD':
        if not float(decimal).is_integer():
            raise ValueError("BCD tidak mendukung pecahan.")
        bcd = ''
        for digit in str(int(decimal)):
            bcd += format(int(digit), '04b')
        return bcd

    elif base_to == 'Excess-3':
        if not float(decimal).is_integer():
            raise ValueError("Excess-3 tidak mendukung pecahan.")
        return decimal_to_excess3(int(decimal))

    elif base_to == 'Gray Code':
        if not float(decimal).is_integer():
            raise ValueError("Gray Code tidak mendukung pecahan.")
        binary = format(int(decimal), 'b')
        return binary_to_gray(binary)