from jsonMode import createDatabase, createTable, dropDatabase
from parse.ast_node import ASTNode
from parse.symbol_table import SymbolTable, DatabaseSymbol, TableSymbol, FieldSymbol, TypeSymbol
from parse.errors import Error, ErrorType


class CreateEnum(ASTNode):
    def __init__(self, name, value_list, line, column):
        ASTNode.__init__(self, line, column)
        self.name = name  # type name
        self.value_list = value_list  # list of possible values

    def execute(self, table: SymbolTable, tree):
        super().execute(table, tree)
        result_values = self.value_list.execute(table, tree)
        symbol = TypeSymbol(self.name, result_values)
        return table.add(symbol)


class CreateDatabase(ASTNode):
    def __init__(self, name, owner, mode, replace, line, column):
        ASTNode.__init__(self, line, column)
        self.name = name  # database name
        self.owner = owner  # optional owner
        self.mode = mode  # mode integer
        self.replace = replace  # boolean type

    def execute(self, table: SymbolTable, tree):
        super().execute(table, tree)
        # result_name = self.name.execute(table, tree)
        result_name = self.name
        result_owner = self.owner.execute(table, tree) if self.owner else None  # Owner seems to be stored only to ST
        result_mode = self.mode(table, tree) if self.mode is not None else 6  # Change to 1 when default mode available
        if self.replace:
            dropDatabase(result_name)
        result = 0
        if result_mode == 6:  # add more ifs when modes from EDD available
            result = createDatabase(result_name)

        if result == 1:
            # log error on operation
            raise Error(0, 0, ErrorType.RUNTIME, '5800: system_error')
            return False
        elif result == 2:
            # log error because db already exists
            raise Error(0, 0, ErrorType.RUNTIME, '42P04: duplicate_database')
            return False
        else:
            return table.add(DatabaseSymbol(result_name, result_owner, result_mode))


class CreateTable(ASTNode):  # TODO: Check grammar, complex instructions are not added yet
    def __init__(self, name, inherits_from, fields, line, column):
        ASTNode.__init__(self, line, column)
        self.name = name  # table name
        self.inherits_from = inherits_from  # optional inheritance
        self.fields = fields  # list of fields

    def execute(self, table: SymbolTable, tree):
        super().execute(table, tree)
        result_name = self.name.execute(table, tree)
        result_inherits_from = self.inherits_from.execute(table, tree) if self.inherits_from else None
        result_fields = []
        if result_inherits_from:
            # get inheritance table, if doesn't exists throws semantic error, else append result
            result_fields.append(table.get_fields_from_table(result_inherits_from))

        result = createTable('db_from_st', result_name, len(result_fields))
        if result == 1:
            raise Error(0, 0, ErrorType.RUNTIME, '5800: system_error')
            return False
        elif result == 2:
            raise Error(0, 0, ErrorType.RUNTIME, '42P04: database_does_not_exists')
            return False
        elif result == 3:
            raise Error(0, 0, ErrorType.RUNTIME, '42P07: duplicate_table')
            return False
        else:
            table.add(TableSymbol(table.get_current_db().name, result_name))

        result_fields = self.fields.execute(table, tree)  # A list of TableField assumed
        for field in result_fields:
            field.table_name = result_name
            table.add(field)
        return


class TableField(ASTNode):  # returns an item, grammar has to add it to a list and synthesize value to table
    def __init__(self, name, field_type, length, allows_null, is_pk, line, column):
        ASTNode.__init__(self, line, column)
        self.name = name  # field name
        self.field_type = field_type  # type of field
        self.length = length
        self.allows_null = allows_null  # if true then NULL or default, if false the means is NOT NULL
        self.is_pk = is_pk  # field is primary key

    def execute(self, table, tree):
        super().execute(table, tree)
        result_name = self.name.execute(table, tree)
        result_field_type = self.field_type.execute(table, tree)
        result_length = self.length.execute(table, tree)
        return FieldSymbol(
            table.get_current_db().name,
            None,
            result_name,
            result_field_type,
            result_length,
            self.allows_null,
            self.is_pk
        )


# table = SymbolTable([])
# cdb_obj = CreateDatabase('db_test2', None, None, False, 1, 2)
# print(cdb_obj.execute(table, None))
