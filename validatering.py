from collections import defaultdict
from typing import List, Dict, Set, Tuple, Any, Type
import json
from sqlalchemy import create_engine
from sqlalchemy.engine.reflection import Inspector
from sqlalchemy.sql.schema import sqlalchemy
import argparse

class CustomField:
    def __init__(self, name: str, typ: Type[int | str | float | dict | list] | tuple, validator, errorString) -> None:
        self.name = name
        self.typ = typ
        self.validator = validator
        self.errorString = errorString

    def __str__(self) -> str:
        return f"Name: {self.name}, Type: {self.typ}, Validator: {self.validator}, errorString: {self.errorString}"

class ParseDict:
    def __init__(self, fields: List[CustomField]):
        self.fields: List[CustomField] = fields
 
    def validate(self, json: Dict):
        for field in self.fields:
            try:
                validate_field(field, json)
            except:
                raise Exception(f"Error in field: {field}")

class ParseList:
    def __init__(self, listType: CustomField , specificValue: Any = None, specificNumber: None | int = None) -> None:
        self.listType = listType 
        self.specificValue = specificValue
        self.specificNumber = specificNumber

    def validate(self, json: Dict):
        if(self.specificNumber != None and self.specificNumber != len(json)):
            raise Exception(f"RingValidator: List doesn't have required number of elements, has: {len(json)}, needs: {self.specificNumber}")
        for element in json:
            validate_type(element, self.listType, self.specificValue)

def validate_type(content: Dict, typ: CustomField, specificValue: Any = None):
    if not isinstance(content, typ.typ):
        if(typ.name != None):
            raise Exception(f"RingValidator: '{typ.name}' must be {typ.errorString}")
        else:
            raise Exception(f"RingValidator: List must contain type {typ.errorString}")

    if(specificValue != None):
        if(content not in specificValue):
            raise Exception(f"RingValidator: List value must be {' '.join(str(i) for i in specificValue)}")

    if(typ.validator != None):
        typ.validator.validate(content)

def validate_field(field: CustomField, curjson: Dict):
    global DatabaseValidator
    if(field.name != '' and field.name not in curjson):
        raise Exception(f"RingValidator: '{field.name}' field is missing")
    if(field.name == ""):
        validate_type(curjson[next(iter(curjson))], field)
    else:
        validate_type(curjson[field.name], field)
    DatabaseValidator.validate_field(field, curjson)
    

def CreateNumeric(name):
    return CustomField(name, (int, float), None, "numeric")
def CreateStr(name):
    return CustomField(name, str, None, "string")
def CreateDict(name, validator):
    return CustomField(name, dict, validator, "dict")
def CreateList(name, validator):
    return CustomField(name, list, validator, "list")

class ValidateDB:
    def __init__(self, source_type: str):
        self.source_type = source_type
        self.joins = set()
        self.entities = set()
        self.relation_entities = defaultdict(list)
    def validate_field(self, field: CustomField, curjson: Dict):
        self.validate_data_source(field, curjson)
        self.validate_entity(field, curjson)

    def validate_data_source(self, field: CustomField, curjson: Dict):
        if(field.name == "dataSource"):
            dataSource = curjson[field.name]

            self.validate_connection_string(dataSource['connectionString'])
            for table in dataSource["tables"]:
                self.validate_table(table["name"])
            for join in dataSource["joins"]:
                self.validate_join(join)

    def validate_ring_attribute(self, field: CustomField, curjson: Dict, table_name: str):
        if(field.name == "attributes"):
            for keys, values in curjson[field.name].items():
                source = values["source"]
                self.validate_table(source["table"])
                for column_name in source["columns"]:
                    self.validate_column_name(source["table"], column_name)

                if(source["table"] != table_name):
                    for join in source["joins"]:
                        if(join not in self.joins):
                            raise Exception(f"Join {join} in attributes {keys} is not found")

    def validate_join(self, join: Dict):
        self.joins.add(join["name"])
        self.validate_table(join["from"])
        self.validate_table(join["to"])
        path = join["path"]

        from_column = path[0][0].split('.', 1)[1]
        to_column = path[0][1].split('.', 1)[1]
        self.validate_column_name(join["from"], from_column)
        self.validate_column_name(join["to"], to_column)

        hasConstraint = False
        constraints = self.inspector.get_foreign_keys(join["from"])
        if(len(constraints) > 0):
            for cur in constraints:
                try:
                    i1 = cur['constrained_columns'].index(from_column)
                    i2 = cur['referred_columns'].index(to_column)
                    if(i1 == i2):
                        hasConstraint = True
                except:
                    pass

        if(not hasConstraint):
            columns1_dict = {col['name']: col['type'] for col in self.inspector.get_columns(join["from"])}
            columns2_dict = {col['name']: col['type'] for col in self.inspector.get_columns(join["to"])}
            if(type(columns1_dict[from_column]) != type(columns2_dict[to_column])):
                raise Exception(f"Join {join['name']} is invalid because columns do not have matching datatypes, {from_column} has type {columns1_dict[from_column]} but {to_column} has type {columns2_dict[to_column]}")
            # from_values = self.connection.execute(f"SELECT {from_column} FROM {join['from']}")
            # to_values = self.connection.execute(f"SELECT {to_column} FROM {join['to']}")

            # to_set = set()
            # to_len = 0
            # for row in to_values:
            #     to_set.add(row[0])
            #     to_len += 1
            #
            # if(len(to_set) != to_len):
            #     raise Exception(f"Column {to_column} must have unique values due to a foreign key constraint")
            # for row in from_values:
            #     if(row[0] not in to_set):
            #         raise Exception(f"Values in {from_column} don't correspond to {to_column}, specifically value {row[0]}")

    def validate_column_name(self, table_name: str, column_name: str):
        columns = self.inspector.get_columns(table_name)

        column_names = [col["name"] for col in columns]

        if column_name not in column_names:
            raise Exception(f"{column_name} not found within {table_name}")
    def validate_connection_string(self, connection_string):
        self.connection_string = connection_string
        self.engine = create_engine(self.connection_string)
        self.inspector = sqlalchemy.inspect(self.engine)
        self.table_names = set(self.inspector.get_table_names())
        self.table_names.update(self.inspector.get_view_names())
        try:
            self.connection = self.engine.connect()
            print("Successful Database Connection!")
        except:
            raise Exception("Invalid Database Connection String")

    def validate_table(self, table_name):
        if(table_name not in self.table_names):
            raise Exception(f"Table {table_name} not found")

    def validate_entity(self, field: CustomField, curjson: Dict):
        if(field.name == "entities"):
            for entity in curjson[field.name]:
                self.entities.add(entity["name"])
                self.validate_table(entity["table"])
                self.validate_column_name(entity["table"], entity["id"]) 
                self.validate_ring_attribute(field, curjson, entity["table"])
            for relationship_name, entity_names in self.relation_entities:
                for entity_name in entity_names:
                    if(entity_name not in self.entities):
                        raise Exception(f"Entity {entity_name} not found in relationship {relationship_name}")

     
    def validate_relationship(self, field: CustomField, curjson: Dict):
        if(field.name == "relationships"):
            for relationship in curjson[field.name]:
                self.relation_entities[relationship["name"]].append(relationship["from"])
                self.relation_entities[relationship["name"]].append(relationship["to"])
                for join in relationship["join"]:
                    if(join not in self.joins):
                        raise Exception("Join {join} not found in relationship {relationship['name']}")

    

class ValidateRing:
    def __init__(self):
        self.primaryKey = [CreateStr("")]
        self.table = [CreateStr("name"), CreateDict("primaryKey", ParseDict(self.primaryKey))]
        self.pathStructure = ParseList(CreateStr(None), None, 3) 
        self.pathList = CreateList("path", self.pathStructure) 
        self.join = [
            CreateStr("name"),
            CreateStr("from"),
            CreateStr("to"),
            CreateList("path", ParseList(self.pathList))
        ]
        self.joinStructure = CreateDict(None,ParseDict(self.join))
        self.dataSource = [
            CreateStr("type"),
            CreateStr("connectionString"),
            CreateList("tables", ParseList(CreateDict(None, ParseDict(self.table)))),
            CreateList("joins", ParseList(self.joinStructure))
        ]
        self.relationshipStructure = [
            CreateStr("name"),
            CreateStr("from"),
            CreateStr("to"),
            CreateList("join", ParseList(CreateStr(None))),
            CreateStr("relation")
        ]
        self.source = [
                CreateStr("table"),
                CreateList("columns", ParseList(CreateStr(None)))
            ]
        self.attributeStructure = [
            CreateList("nicename", ParseList(CreateStr(None), None, 2)),
            CustomField("isa", (int, str, float), None, "string, float, int, or date"),
            CreateList("type", ParseList(CreateStr(None))),
            CreateDict("source", ParseDict(self.source))
        ]
        self.attribute = [CreateDict("", ParseDict(self.attributeStructure))]
        self.metric = [
            CreateList("", ParseList(CreateStr(None), ["-inf", "+inf"], 2))
                ]
        self.entity = [
                CreateStr("name"),
                CreateList("nicename", ParseList(CreateStr(None), None, 2)),
                CreateStr("table"),
                CreateStr("id"),
                CreateStr("idType"),
                # CreateDict("metrics", ParseDict(metric)),
                CreateDict("attributes", ParseDict(self.attribute))
                ]

        self.ontology = [
            CreateList("relationships", ParseList(CreateDict(None, ParseDict(self.relationshipStructure)))),
            CreateList("entities", ParseList(CreateDict(None, ParseDict(self.entity))))
        ]
        self.ring = [
                CreateNumeric("id"),
                CreateNumeric("userId"),
                CreateStr("rid"),
                CreateStr("name"),
                CreateStr("description"),
                CreateNumeric("version"),
                CreateNumeric("schemaVersion"),
                CreateDict("dataSource", ParseDict(self.dataSource)),
                CreateDict("ontology", ParseDict(self.ontology)) 
        ]
        self.parser = ParseDict(self.ring)
    def validate(self, json: Dict):
        self.parser.validate(json)
        print("Validation Successful!")

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description = "Process a ring")

    parser.add_argument('--ring', type=str, default='ring.json', help='Ring to parse')
    args = parser.parse_args()
    f = open(args.ring) 
    data = json.load(f)
    RingValidator = ValidateRing()
    DatabaseValidator = ValidateDB("postgres")

    try:
        RingValidator.validate(data)
    finally:
        DatabaseValidator.connection.close()
        f.close()
