from enum import Enum
from parse.errors import ErrorType, Error

index = 0


def generate_id():  # Probably it would be better to use a random generator but this is more legible if debug needed
    global index
    index += 1
    return index


class SymbolType(Enum):
    DATABASE = 1
    TABLE = 2
    FIELD = 3
    TYPE = 4


class Symbol:
    # Symbol to use inside Symbol table

    def __init__(self, symbol_type, name, position='Not Specified'):
        self.id = generate_id()
        self.type = symbol_type
        self.name = name
        self.position = position


class DatabaseSymbol(Symbol):
    def __init__(self, name, owner, mode):
        Symbol.__init__(self, SymbolType.DATABASE, name)
        self.name = name
        self.owner = owner
        self.mode = mode
        self.selected = False


class TableSymbol(Symbol):
    def __init__(self, db_name, table_name):
        Symbol.__init__(self, SymbolType.TABLE, table_name)
        self.db_name = db_name
        self.table_name = table_name


class FieldSymbol(Symbol):
    def __init__(self, db_name, table_name, field_name, field_type, length, is_not_null, is_pk, fk_table, fk_field):
        Symbol.__init__(self, SymbolType.FIELD, field_name)
        self.db_name = db_name
        self.table_name = table_name
        self.field_name = field_name
        self.field_type = field_type
        self.length = length
        self.is_not_null = is_not_null
        self.is_pk = is_pk
        self.fk_table = fk_table
        self.fk_field = fk_field


class TypeSymbol(Symbol):
    def __init__(self, enum_name, value_list):
        Symbol.__init__(self, SymbolType.TYPE, enum_name)
        self.value_list = value_list


class SymbolTable:
    # Symbol Table itself

    def __init__(self, symbols=[]):
        self.symbols = symbols

    def add(self, symbol):
        match = next((sym for sym in self.symbols if sym.name == symbol.name and sym.type == symbol.type), None)
        if match is None:
            self.symbols.append(symbol)
        else:
            raise Error(0, 0, ErrorType.RUNTIME, f'[TS]{symbol.name} ya ha sido declarado previamente')
        return True

    def get(self, symbol_id):
        result = next((sym for sym in self.symbols if sym.id == symbol_id), None)
        if result is None:
            raise Error(0, 0, ErrorType.RUNTIME, f'[TS]Simbolo id:{symbol_id} no pudo ser encontrado')
        return result

    def get(self, symbol_name, symbol_type):
        result = next((sym for sym in self.symbols if sym.type == symbol_type and sym.name == symbol_name), None)
        if result is None:
            raise Error(0, 0, ErrorType.RUNTIME, f'[TS]{symbol_name} no pudo ser encontrado')
        return result

    def get_fields_from_table(self, table_name):
        # check if table exists
        self.get(table_name, SymbolType.TABLE)
        result = list(filter(lambda sym: sym.type == SymbolType.FIELD and sym.table_name == table_name, self.symbols))
        return result

    def update(self, symbol):
        result = self.get(symbol.id)
        self.symbols[self.symbols.index(result)] = symbol
        return True

    def get_current_db(self):
        result = next((sym for sym in self.symbols if sym.type == SymbolType.DATABASE and sym.selected == True), None)
        if result is None:
            raise Error(0, 0, ErrorType.RUNTIME, 'No se ha seleccionado base de datos')
        return result

    def set_current_db(self, db_name):
        db_to_select = self.get(db_name, SymbolType.DATABASE)
        db_to_select.selected = True
        self.update(db_to_select)
        return True

    def get_all_db(self, table_name):
        result = list(filter(lambda sym: sym.type == SymbolType.DATABASE, self.symbols))
        return result

    def return_content(self):
        return self.symbols

    def print_content(self):
        for x in range(len(self.symbols)):
            print(f'{self.symbols[x].id} - {self.symbols[x].type} - {self.symbols[x].name}')


# BLOCK TO TEST SYMBOL TABLE
# db = DatabaseSymbol('test_db', None, 6)
# table = TableSymbol(db.name, 'test_table')
# field = FieldSymbol(db.name, table.name, 'test_field', 'int', None, False, True, None, None)
# ts = SymbolTable([])
# ts.add(db)
# ts.add(table)
# ts.add(field)
# field = FieldSymbol(db.name, table.name, 'test_field2', 'int', None, False, True, None, None)
# ts.add(field)
# ts.print_content()
# print(ts.get_fields_from_table('test_table'))
