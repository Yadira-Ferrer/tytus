from storage.team07.storageBeans.TableHash import Hash

# funciones de bases de datos
t = Hash()  # hash para almacenar base de datos , estructura incial


# dabatase  functions , only name database
def createDatabase(database):  # recibo el string con el nombre de  la base de datos
    try:
        if (t.search(database) is False):
            t.insert(database)
            return 0  # la operación es exito
        else:
            return 2  # no realize nada porque la base de datos ya existe
    except:
        return 1  # error en la operación


def showDatabases():  # retornare una lista
    return t.getData()  # metodo que me retorna una lista con los nombres de las bases de datos


def alterDatabase(databaseOld, databaseNew):  # cambio de nombres en las bases de datos , (nodo en la table hash)
    try:
        if t.search(databaseOld):  # chech if the old database exist
            if t.search(databaseNew):  # check if the new database doesn´t exist
                return 3  # new database exist , so is like an error
            else:  # if all is correct , change the name of database
                if t.updateName(databaseNew, databaseOld):
                    return 0  # succesfull
                else:
                    return 1  # error
        else:
            return 2  # database doesn´t exist
    except:
        return 2  # error


def dropDatabase(database):
    try:
        if t.search(database):  # means that the database exist
            t.delete(database)
            return 0  # succesfull operation delete
        else:  # database doesn´t exist
            return 2
    except:
        return 1  # error


# tables functions only the name table
def showTables(database):
    if t.search(database):
        data = t.getDataBase(database)  # get the database
        return data.BHash.getDataTables()  # return name of tables
    else:
        return None


def alterTable(database, tableOld, tableNew):
    try:
        if t.search(database):
            data = t.getDataBase(database)  # get the database
            if data.BHash.searchTable(tableOld):  # table exist
                if data.BHash.searchTable(tableNew):  # new table exist
                    return 4
                else:
                    data.BHash.updateNameTable(tableNew, tableOld)  # all data is correct  -> change the name of table
                    return 0
            else:  # table doesn´t exist
                return 3
        else:
            return 2
    except:
        return 1

def dropTable(database, table):
    try:
        if t.search(database):
            data = t.getDataBase(database)
            if data.BHash.searchTable(table):
                data.BHash.deleteTable(table)
                return 0
            else:
                return 3 # table doesn´t exist
        else:
            return 2    # database doesn´t exist
    except:
        return 1
