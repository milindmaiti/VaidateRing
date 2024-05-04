
class ValidateRing:
    def __init__(self, json):
        self.json = json

    def validate_structure(self):

        # id
        if 'id' not in self.json:
            raise Exception("RingValidator: 'id' field is missing")
        elif not isinstance(self.json['id'],(int, float)):
            raise Exception("RingValidator: 'id' must be numeric")

        # userId
        if 'userId' not in self.json:
            raise Exception("RingValidator: 'userId' field is missing")
        elif not isinstance(self.json['userId'],(int,float)):
            raise Exception("RingValidator: 'userId' must be numeric")

        # rid
        if 'rid' not in self.json:
            raise Exception("RingValidator: 'rid' field is missing")
        elif not isinstance(self.json['rid'],str):
            raise Exception("RingValidator: 'rid' must be string")

        # name
        if 'name' not in self.json:
            raise Exception("RingValidator: 'name' field is missing")
        elif not isinstance(self.json['name'],str):
            raise Exception("RingValidator: 'name' must be string")

        # description
        if 'description' not in self.json:
            raise Exception("RingValidator: 'description' field is missing")
        elif not isinstance(self.json['description'],str):
            raise Exception("RingValidator: 'description' must be string")

        # version
        if 'version' not in self.json:
            raise Exception("RingValidator: 'version' field is missing")
        elif not isinstance(self.json['version'],(int, float)):
            raise Exception("RingValidator: 'version' must be numeric")

        # schemaVersion
        if 'schemaVersion' not in self.json:
            raise Exception("RingValidator: 'schemaVersion' field is missing")
        elif not isinstance(self.json['schemaVersion'],(int,float)):
            raise Exception("RingValidator: 'schemaVersion' must be numeric")

        # dataSource
        if 'dataSource' not in self.json:
            raise Exception("RingValidator: 'dataSource' field is missing")
        elif not isinstance(self.json['dataSource'],dict):
            raise Exception("RingValidator: 'dataSource' must be dict")

        data_source = self.json['dataSource']

        # dataSource -> type
        if 'type' not in data_source:
            raise Exception("RingValidator: 'type' field is missing in 'dataSource'")
        elif not isinstance(data_source['type'],str):
            raise Exception("RingValidator: 'type' must be string in 'dataSource'")

        # dataSource -> connectionString
        if 'connectionString' not in data_source:
            raise Exception("RingValidator: 'connectionString' field is missing")
        elif not isinstance(data_source['connectionString'],str):
            raise Exception("RingValidator: 'connectionString' must be string in 'dataSource'")

        # dataSource -> tables
        if 'tables' not in data_source:
            raise Exception("RingValidator: 'tables' field is missing in 'dataSource'")
        elif not isinstance(data_source['tables'],list):
            raise Exception("RingValidator: 'tables' must be list in 'dataSource'")

        tables = data_source['tables']

        for table in tables:
            if not isinstance(table, dict):
                raise Exception("RingValidator: 'tables' must be a list of dicts in 'dataSource'")

            # dataSource -> tables -> name
            if 'name' not in table:
                raise Exception("RingValidator: 'name' field is missing in 'tables'")
            elif not isinstance(table['name'],str):
                raise Exception("RingValidator: 'name' must be string in 'tables'")

            # dataSource -> tables -> primaryKey
            if 'primaryKey' not in table:
                raise Exception("RingValidator: 'primaryKey' field is missing in 'tables'")
            elif not isinstance(table['primaryKey'],dict):
                raise Exception("RingValidator: 'primaryKey' must be dict in 'tables'")
            elif len(table['primaryKey']) != 1:
                raise Exception("RingValidator: 'primaryKey' must have exactly one primary key")
            for key in table['primaryKey']:
                if not isinstance(key,str):
                    raise Exception("RingValidator: 'primaryKey' must have string key in 'tables'")
                if not isinstance(table['primaryKey'][key], str):
                    raise Exception("RingValidator: 'primaryKey' must have string value in 'tables'")

        # dataSource -> joins
        if 'joins' not in data_source:
            raise Exception("RingValidator: 'joins' field is missing in 'dataSource'")
        elif not isinstance(data_source['joins'],list):
            raise Exception("RingValidator: 'joins' must be list in 'dataSource'")

        joins = data_source['joins']

        for join in joins:
            if not isinstance(join,dict):
                raise Exception("RingValidator: 'joins' must be a list of dicts in 'dataSource'")

            # dataSource -> joins -> name
            if 'name' not in join:
                raise Exception("RingValidator: 'name' field is missing in 'joins'")
            elif not isinstance(join['name'],str):
                raise Exception("RingValidator: 'name' must be string in 'joins'")

            # dataSource -> joins -> from
            if 'from' not in join:
                raise Exception("RingValidator: 'from' field is missing in 'joins'")
            elif not isinstance(join['from'],str):
                raise Exception("RingValidator: 'from' must be string in 'joins'")

            # dataSource -> joins -> to
            if 'to' not in join:
                raise Exception("RingValidator: 'to' field is missing in 'joins'")
            elif not isinstance(join['to'],str):
                raise Exception("RingValidator: 'to' must be string in 'joins'")

            # dataSource -> joins -> path
            if 'path' not in join:
                raise Exception("RingValidator: 'path' field is missing in 'joins'")
            elif not isinstance(join['path'],list):
                raise Exception("RingValidator: 'path' must be a list in 'joins'")

            path = join['path']

            for p in path:
                if not isinstance(p,list):
                    raise Exception("RingValidator: 'path' must be a list of lists in 'joins'")
                if len(p) != 3:
                    raise Exception("RingValidator: 'path' must be a list of lists of length three in 'joins'")
                for entry in p:
                    if not isinstance(entry,str):
                        raise Exception("RingValidator: 'path' must be a list of lists of strings in 'joins'")

        # ontology
        if 'ontology' not in self.json:
            raise Exception("RingValidator: 'ontology' field is missing")
        elif not isinstance(self.json['ontology'],dict):
            raise Exception("RingValidator: 'ontology' must be a dict")

        ontology = self.json['ontology']

        # ontology -> relationships
        if 'relationships' not in ontology:
            raise Exception("RingValidator: 'relationships' field is missing in 'ontology'")
        elif not isinstance(ontology['relationships'],list):
            raise Exception("RingValidator: 'relationships' must be a list in 'ontology'")

        relationships = ontology['relationships']

        for relationship in relationships:
            if not isinstance(relationship,dict):
                raise Exception("RingValidator: 'relationships' must be a list of dicts in 'ontology'")

            # ontology -> relationships -> name
            if 'name' not in relationship:
                raise Exception("RingValidator: 'name' field is missing in 'relationships'")
            elif not isinstance(relationship['name'],str):
                raise Exception("RingValidator: 'name' must be string in 'relationships'")

            # ontology -> relationships -> from
            if 'from' not in relationship:
                raise Exception("RingValidator: 'from' field is missing in 'relationships'")
            elif not isinstance(relationship['from'],str):
                raise Exception("RingValidator: 'from' must be string in 'relationships'")

            # ontology -> relationships -> to
            if 'to' not in relationship:
                raise Exception("RingValidator: 'to' field is missing in 'relationships'")
            elif not isinstance(relationship['to'],str):
                raise Exception("RingValidator: 'to' must be string in 'relationships'")

            # ontology -> relationships -> join
            if 'join' not in relationship:
                raise Exception("RingValidator: 'join' field is missing in 'relationships'")
            elif not isinstance(relationship['join'],list):
                raise Exception("RingValidator: 'join' must be a list in 'relationships'")

            for entry in relationship['join']:
                if not isinstance(entry,str):
                    raise Exception("RingValidator: 'join' must be a list of strings in 'relationships'")

            # ontology -> relationships -> relation
            if 'relation' not in relationship:
                raise Exception("RingValidator: 'relation' field is missing in 'relationships'")
            elif not isinstance(relationship['relation'],str):
                raise Exception("RingValidator: 'relation' must be string in 'relationships'")

        # ontology -> entities

        if 'entities' not in ontology:
            raise Exception("RingValidator: 'entities' field is missing in 'ontology'")
        elif not isinstance(ontology['entities'],list):
            raise Exception("RingValidator: 'entities' must be a list in 'ontology'")

        entities = ontology['entities']

        for entity in entities:
            if not isinstance(entity,dict):
                raise Exception("RingValidator: 'entities' must be a list of dicts in 'ontology'")

            # ontology -> entities -> name
            if 'name' not in entity:
                raise Exception("RingValidator: 'name' field is missing in 'entities'")
            elif not isinstance(entity['name'],str):
                raise Exception("RingValidator: 'name' must be string in 'entities'")

            # ontology -> entities -> nicename
            if 'nicename' not in entity:
                raise Exception("RingValidator: 'nicename' field is missing in 'entities'")
            elif not isinstance(entity['nicename'],list):
                raise Exception("RingValidator: 'nicename' must be a list in 'entities'")
            elif len(entity['nicename']) != 2:
                raise Exception("RingValidator: 'nicename' must be a list of length two in 'entities'")
            for entry in entity['nicename']:
                if not isinstance(entry,str):
                    raise Exception("RingValidator: 'nicename' must be a list of two strings in 'entities'")

            # ontology -> entities -> table
            if 'table' not in entity:
                raise Exception("RingValidator: 'table' field is missing in 'entities'")
            elif not isinstance(entity['table'],str):
                raise Exception("RingValidator: 'table' must be string in 'entities'")

            # ontology -> entities -> id
            if 'id' not in entity:
                raise Exception("RingValidator: 'id' field is missing in 'entities'")
            elif not isinstance(entity['id'],str):
                raise Exception("RingValidator: 'id' must be string in 'entities'")

            # ontology -> entities ->idType
            if 'idType' not in entity:
                raise Exception("RingValidator: 'idType' field is missing in 'entities'")
            elif not isinstance(entity['idType'],str):
                raise Exception("RingValidator: 'idType' must be string in 'entities'")

            # ontology -> entities -> metrics
            if 'metrics' not in entity:
                raise Exception("RingValidator: 'metrics' field is missing in 'entities'")
            elif not isinstance(entity['metrics'],dict):
                raise Exception("RingValidator: 'metrics' must be a dict")
            for key in entity['metrics']:
                if not isinstance(key, str):
                    raise Exception("RingValidator: 'metrics' must be a dict with string keys in 'entities'")
                value = entity['metrics'][key]
                if not isinstance(value,list):
                    raise Exception("RingValidator: 'metrics' must be a dict with list values in 'entities'")
                if len(value) != 2:
                    raise Exception("RingValidator: 'metrics' must be a dict with length 2 list values in 'entities'")
                if value[0] != "-inf" and value[0] != "+inf":
                    raise Exception("RingValidator: 'metrics' has invalid values in 'entities'")
                if value[1] != "-inf" and value[1] != "+inf":
                    raise Exception("RingValidator: 'metrics' has invalid values in 'entities'")

            # ontology -> entities -> attributes
            if 'attributes' not in entity:
                raise Exception("RingValidator: 'attributes' field is missing in 'entities'")
            elif not isinstance(entity['attributes'],dict):
                raise Exception("RingValidator: 'attributes' must be a dict")



    
    def validate(self):
        pass