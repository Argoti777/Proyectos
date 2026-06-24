def validar_cedula(cedula: str) -> bool:
    if len(cedula) != 10 or not cedula.isdigit():
        return False

    provincia = int(cedula[:2])
    if provincia < 1 or provincia > 24:
        return False

    coeficientes = [2, 1] * 5
    total = 0

    for i in range(9):
        val = int(cedula[i]) * coeficientes[i]
        if val >= 10:
            val -= 9
        total += val

    digito_verificador = (10 - (total % 10)) % 10

    return digito_verificador == int(cedula[-1])