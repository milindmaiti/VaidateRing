from typing import List, Dict, Set
import json

def validateType(content, typ, specificValue = None):
    if not isinstance(content, typ.typ):
        print(content)
        print(typ)
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

def validateField(field, curjson): 
    if(field.name != '' and field.name not in curjson):
        print(curjson)
        raise Exception(f"RingValidator: '{field.name}' field is missing")
        

    if(field.name == ""):
        validateType(curjson[next(iter(curjson))], field)
    else:
        validateType(curjson[field.name], field)
    
class customField:
    def __init__(self, name, typ, validator, errorString) -> None:
        self.name = name
        self.typ = typ
        self.validator = validator
        self.errorString = errorString

    def __str__(self) -> str:
        return f"Name: {self.name}, Type: {self.typ}, Validator: {self.validator}, errorString: {self.errorString}"

class parseDict:
    def __init__(self, fields):
        self.fields: List[customField] = fields
 
    def validate(self, json):
        for field in self.fields:
            try:
                validateField(field, json)
            except:
                raise Exception(f"Error in field: {field}")

class parseList:
    def __init__(self, listType, specificValue = None, specificNumber = None) -> None:
        self.listType: customField = listType 
        self.specificValue = specificValue
        self.specificNumber = specificNumber

    def validate(self, json):
        if(self.specificNumber != None and self.specificNumber != len(json)):
            raise Exception(f"RingValidator: List doesn't have required number of elements, has: {len(json)}, needs: {self.specificNumber}")
        for element in json:
            validateType(element, self.listType, self.specificValue)

def createNumeric(name):
    return customField(name, (int, float), None, "numeric")
def createStr(name):
    return customField(name, str, None, "string")
def createDict(name, validator):
    return customField(name, dict, validator, "dict")
def createList(name, validator):
    return customField(name, list, validator, "list")

primaryKey = [
        createStr("")
]
table = [
    createStr("name"),
    createDict("primaryKey", parseDict(primaryKey))
]

pathStructure = parseList(createStr(None), None, 3) 
pathList = createList("path", pathStructure) 
join = [
    createStr("name"),
    createStr("from"),
    createStr("to"),
    createList("path", parseList(pathList))
]
joinStructure = createDict(None,parseDict(join))
dataSource = [
    createStr("type"),
    createStr("connectionString"),
    createList("tables", parseList(createDict(None, parseDict(table)))),
    createList("joins", parseList(joinStructure))
]

relationshipStructure = [
    createStr("name"),
    createStr("from"),
    createStr("to"),
    createList("join", parseList(createStr(None))),
    createStr("relation")
]


source = [
        createStr("table"),
        createList("columns", parseList(createStr(None)))
        ]
attributeStructure = [
    createList("nicename", parseList(createStr(None), None, 2)),
    customField("isa", (int, str, float), None, "string, float, int, or date"),
    createList("type", parseList(createStr(None))),
    createDict("source", parseDict(source))
]
attribute = [
    createDict("", parseDict(attributeStructure))
        ]
metric = [
    createList("", parseList(createStr(None), ["-inf", "+inf"], 2))
        ]
entity = [
        createStr("name"),
        createList("nicename", parseList(createStr(None), None, 2)),
        createStr("table"),
        createStr("id"),
        createStr("idType"),
        createDict("metrics", parseDict(metric)),
        createDict("attributes", parseDict(attribute))
        ]

ontology = [
    createList("relationships", parseList(createDict(None, parseDict(relationshipStructure)))),
    createList("entities", parseList(createDict(None, parseDict(entity))))
]
ring = [
        createNumeric("id"),
        createNumeric("userId"),
        createStr("rid"),
        createStr("name"),
        createStr("description"),
        createNumeric("version"),
        createNumeric("schemaVersion"),
        createDict("dataSource", parseDict(dataSource)),
        createDict("ontology", parseDict(ontology)) 
]

f = open('ring.json') 
data = json.load(f)
RingValidator = parseDict(ring)
RingValidator.validate(data)   
