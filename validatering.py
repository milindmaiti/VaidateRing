from typing import List, Dict, Set, Tuple, Any, Type
import json

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
            print(content)
            print(specificValue)
            raise Exception(f"RingValidator: List value must be {' '.join(str(i) for i in specificValue)}")

    if(typ.validator != None):
        typ.validator.validate(content)

def validate_field(field: CustomField, curjson: Dict): 
    if(field.name != '' and field.name not in curjson):
        raise Exception(f"RingValidator: '{field.name}' field is missing")
    if(field.name == ""):
        validate_type(curjson[next(iter(curjson))], field)
    else:
        validate_type(curjson[field.name], field)
    

def CreateNumeric(name):
    return CustomField(name, (int, float), None, "numeric")
def CreateStr(name):
    return CustomField(name, str, None, "string")
def CreateDict(name, validator):
    return CustomField(name, dict, validator, "dict")
def CreateList(name, validator):
    return CustomField(name, list, validator, "list")

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

if __name__ == "__main__":
    f = open('ring.json') 
    data = json.load(f)
    RingValidator = ValidateRing()
    RingValidator.validate(data)   
