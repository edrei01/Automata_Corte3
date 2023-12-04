import re
import tkinter as tk

class PDA:
    def __init__(self, grammar, terminals):
        self.grammar = grammar
        self.terminals = terminals
        self.stack = []
        self.pila_historial = []  # Lista para mantener el historial de la pila

    # Resto del código de la clase PDA...

    def parse(self, input_string):
        self.stack.append("S")  # Símbolo de inicio
        self.pila_historial.append(list(self.stack))  # Guardar el estado inicial de la pila
        index = 0
        while self.stack and index <= len(input_string):
            index = self.skip_whitespace(input_string, index)
            if index >= len(input_string):
                break

            top = self.peek()
            remaining_input = input_string[index:]

            if top in self.grammar:
                self.process_non_terminal(top, remaining_input)
            elif self.match_terminal(top, remaining_input):
                match_length = len(re.match(self.terminals[top], remaining_input).group())
                index += match_length
                self.pop()
            else:
                raise Exception(f"Error de sintaxis cerca de la posición {index}")

            # Guardar el estado actual de la pila en el historial
            self.pila_historial.append(list(self.stack))
        return len(self.stack) == 0
    def process_non_terminal(self, non_terminal, input_string):
        self.pop()

        if non_terminal == "EL":
            self.choose_production_for_EL(input_string)
        elif (
            non_terminal == "S"
        ):  # accesos para distintas opciones en las producciones
            self.choose_production_for_S(input_string)
        elif non_terminal == "S":
            self.choose_production_for_S(input_string)
        elif non_terminal == "D1":
            self.push_production(self.grammar["D1"][0])
        elif non_terminal == "V":
            self.push_production(self.grammar["V"][0])
        elif non_terminal == "S4":
            self.push_production(self.grammar["S4"][0])
        elif non_terminal == "CA":
            self.push_production(self.grammar["CA"][0])
        elif non_terminal == "CD":
            self.push_production(self.grammar["CD"][0])
        elif non_terminal == "F1":
            self.push_production(self.grammar["F1"][0])
        elif non_terminal == "F3":
            self.push_production(self.grammar["F3"][0])
        elif non_terminal == "F4":
            self.push_production(self.grammar["F4"][0])
        elif non_terminal == "F5":
            self.push_production(self.grammar["F5"][0])
        else:
            self.choose_production(non_terminal, input_string)

    def choose_production_for_EL(self, input_string):
        if re.match(self.terminals["E"], input_string):
            self.push_production(self.grammar["EL"][0])
        elif re.match(self.terminals["Z"], input_string):
            self.push_production(self.grammar["EL"][1])

    def choose_production_for_S(self, input_string):
        if re.match(self.terminals["FU"], input_string):
            self.push_production(self.grammar["S"][0])
        elif re.match(self.terminals["TD"], input_string):
            self.push_production(self.grammar["S"][1])
        elif re.match(self.terminals["F"], input_string):
            self.push_production(self.grammar["S"][2])
        elif re.match(self.terminals["SW"], input_string):
            self.push_production(self.grammar["S"][3])
        elif re.match(self.terminals["IF"], input_string):
            self.push_production(self.grammar["S"][4])
        else:
            raise Exception(
                f"No se pudo encontrar una producción adecuada para 'S' con entrada {input_string}"
            )

    def choose_production(self, non_terminal, input_string):
        for production in self.grammar[non_terminal]:
            if self.is_valid_production(production, input_string):
                self.push_production(production)
                return
        raise Exception(
            f"No se pudo encontrar una producción adecuada para {non_terminal} con entrada {input_string}"
        )

    def is_valid_production(self, production, input_string):
        symbols = production.split()
        if not symbols:
            return False
        first_symbol = symbols[0]
        if first_symbol in self.terminals:
            return re.match(self.terminals[first_symbol], input_string) is not None
        else:
            return False

    def push_production(self, production):
        for symbol in reversed(production.split()):
            self.push(symbol)

    def skip_whitespace(self, input_string, index):
        while index < len(input_string) and input_string[index].isspace():
            index += 1
        return index

    def match_terminal(self, terminal, input_string):
        pattern = self.terminals[terminal]
        return re.match(pattern, input_string)

    def push(self, symbol):
        if symbol != "ε":  # ε representa la cadena vacía
            self.stack.append(symbol)

    def pop(self):
        return self.stack.pop()

    def peek(self):
        return self.stack[-1] if self.stack else None
def evaluar_cadena():
    cadena = cadena_input.get()
    pda = PDA(grammar, terminals)
    es_valida = pda.parse(cadena)
    if es_valida:
        resultado.set("La cadena está bien escrita.")
    else:
        resultado.set("La cadena no está bien escrita.")
    actualizar_historial_pila(pda.pila_historial)
    
# Luego, en la función de actualización de la interfaz gráfica
def actualizar_historial_pila(pila_historial):
    historial_text.delete(1.0, tk.END)
    for paso, estado_pila in enumerate(pila_historial, start=1):
        historial_text.insert(tk.END, f"Paso {paso}:\n")
        for item in estado_pila[::-1]:
            historial_text.insert(tk.END, item + '\n')
        historial_text.insert(tk.END, "\n")

# Definir las reglas y gramática
terminals = {
    "FU": r"funt",
    "AP": r"\(",
    "CP": r"\)",
    "AL": r"\{",
    "CL": r"\}",
    "ID": r"[a-z0-9]+",
    "NUMBER": r"[0-9]+",
    "SEN": r"texto",
    "RT": r"return",
    "TD": r"(int|string)",
    "P": r"\:",
    "F": r"for",
    "PC": r"\;",
    "I": r"\=",
    "CM": r"(<|>|<=|>=|==)",
    "SW": r"switch",
    "O": r"opcion",
    "CS": r"case",
    "BK": r"break",
    "IF": r"if",
    "E": r"else",
    "OP": r"(\+|\-|\*|\/)",
    "Z": r"%",
}

grammar = {
  "S": ["FU FUN", "TD VA", "F FO", "SW SL", "IF CD"],
    "FUN": ["ID A1"],
    "A1": ["AP A2"],
    "A2": ["ID A3"],
    "A3": ["CP A4"],
    "A4": ["AL A5"],
    "A5": ["SEN A6"],
    "A6": ["RT A7"],
    "A7": ["AP A8"],
    "A8": ["ID A9"],
    "A9": ["CP CL"],
    "VA": ["ID V1"],
    "V1": ["P NUMBER", "Z"],
    "FO": ["AP F1"],
    "F1": ["DC F2"],
    "F2": ["PC F3"],
    "F3": ["CI F4"],
    "F4": ["PC F5"],
    "F5": ["IN F6"],
    "F6": ["CP F7"],
    "F7": ["AL F8"],
    "F8": ["ID CL"],
    "SL": ["AP S1"],
    "S1": ["O S2"],
    "S2": ["CP S3"],
    "S3": ["AL S4"],
    "S4": ["CA S5"],
    "S5": ["PC CL"],
    "CD": ["AP D1"],
    "D1": ["CI D2"],
    "D2": ["CP D3"],
    "D3": ["AL D4"],
    "D4": ["SEN D5"],
    "D5": ["CL EL"],
    "DC": ["TD DC1", "ID DC3"],
    "DC1": ["ID DC2"],
    "DC2": ["I NUMBER"],
    "DC3": ["I ID"],
    "CI": ["ID C1", "NUMBER C1"],
    "C1": ["CM NUMBER"],
    "IN": ["ID N1"],
    "N1": ["OP NUMBER"],
    "CA": ["CS L1"],
    "L1": ["NUMBER L2"],
    "L2": ["P L3"],
    "L3": ["SEN BK"],
    "EL": ["E E1", "Z"],
    "E1": ["AP E2"],
    "E2": ["CI E3"],
    "E3": ["CP E4"],
    "E4": ["AL E5"],
    "E5": ["SEN CL"],
}

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Evaluador de Cadenas - PDA")

tk.Label(ventana, text="Ingrese la cadena:").pack()
cadena_input = tk.Entry(ventana)
cadena_input.pack()

tk.Button(ventana, text="Evaluar", command=evaluar_cadena).pack()

resultado = tk.StringVar()
resultado.set("")
tk.Label(ventana, textvariable=resultado).pack()

tk.Label(ventana, text="Estado de la Pila:").pack()
historial_text = tk.Text(ventana, height=20, width=40)
historial_text.pack()

# Ejecutar la ventana
ventana.mainloop()
