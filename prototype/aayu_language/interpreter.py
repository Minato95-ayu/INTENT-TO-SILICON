from ast_nodes import *
from errors import AAYURuntimeError, AAYUDatabaseError, AAYUImportError, AAYUTestFailure
import difflib
import math
import random
from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import sqlite3
import datetime
import hashlib
import uuid
from http import cookies

class AayuJSONResponse:
    def __init__(self, data_str):
        self.data_str = data_str

class AayuHTMLResponse:
    def __init__(self, data_str):
        self.data_str = data_str

class AayuTextResponse:
    def __init__(self, data_str):
        self.data_str = data_str

class ReturnException(Exception):
    def __init__(self, value):
        self.value = value

class AayuRecord:
    def __init__(self, type_name, fields):
        self.type_name = type_name
        self.fields = fields

    def __repr__(self):
        return f"{self.type_name}({self.fields})"

class AayuModule:
    def __init__(self, exports):
        self.exports = exports

    def __repr__(self):
        return f"AayuModule(exports={list(self.exports.keys())})"

class Environment:
    def __init__(self, enclosing=None):
        self.enclosing = enclosing
        self.values = {}

    def define(self, name, value):
        self.values[name] = value

    def get(self, name: str, interpreter=None):
        if name in self.values:
            return self.values[name]
        if self.enclosing:
            return self.enclosing.get(name, interpreter)
            
        suggestion = None
        if interpreter:
            all_keys = self._get_all_keys()
            matches = difflib.get_close_matches(name, all_keys, n=1, cutoff=0.6)
            if matches:
                suggestion = f"Did you mean '{matches[0]}'?"
                
        if interpreter:
            interpreter.throw_error(f"Variable '{name}' was not found.", suggestion)
        else:
            raise Exception(f"Undefined variable '{name}'.")

    def _get_all_keys(self) -> list:
        keys = list(self.values.keys())
        if self.enclosing:
            keys.extend(self.enclosing._get_all_keys())
        return keys

    def assign(self, name, value):
        if name in self.values:
            self.values[name] = value
            return
        if self.enclosing is not None:
            self.enclosing.assign(name, value)
            return
        raise RuntimeError(f"Undefined variable '{name}'.")

class Interpreter:
    def __init__(self, test_mode: bool = False):
        self.environment = Environment()
        self.current_node = None
        self.exports = {}
        self.routes = {}
        self.test_mode = test_mode
        # Connect to SQLite for W-6 Database feature
        self.db_conn = sqlite3.connect("aayu_db.sqlite", check_same_thread=False)
        self.db_conn.row_factory = sqlite3.Row
        self.db_cursor = self.db_conn.cursor()
        
        # Bootstrap Auth Tables
        self.db_cursor.execute('''CREATE TABLE IF NOT EXISTS Account (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE,
            password_hash TEXT,
            created_at TEXT,
            updated_at TEXT
        )''')
        self.db_cursor.execute('''CREATE TABLE IF NOT EXISTS Session (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            account_id INTEGER,
            token TEXT UNIQUE,
            expires_at TEXT,
            created_at TEXT,
            updated_at TEXT
        )''')
        self.db_conn.commit()

        self.current_node = None
        self.exports = {}
        self.routes = {}
        
    def throw_error(self, message: str, suggestion: str = ""):
        line = getattr(self.current_node, 'line', 1) if self.current_node else 1
        raise AAYURuntimeError(message, line, suggestion)

    def interpret(self, ast: ProgramNode):
        try:
            self.visit_ProgramNode(ast)
        except ReturnException as r:
            return r.value

    def visit(self, node: Node):
        method_name = f"visit_{type(node).__name__}"
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def evaluate(self, node: Node):
        return self.visit(node)

    def generic_visit(self, node: Node):
        raise Exception(f"No visit_{type(node).__name__} method")

    def visit_ProgramNode(self, node: ProgramNode):
        for statement in node.statements:
            self.current_node = statement
            self.visit(statement)

    def visit_DeclarationNode(self, node: DeclarationNode):
        value = self.evaluate(node.value)
        self.environment.define(node.name, value)
        return value

    def visit_ExportNode(self, node: ExportNode):
        self.visit(node.declaration)
        # Assuming node.declaration has a 'name' (e.g. TaskNode)
        name = node.declaration.name
        self.exports[name] = self.environment.get(name, self)

    def visit_AssignmentNode(self, node: AssignmentNode):
        value = self.evaluate(node.value)
        
        if isinstance(node.target, VariableNode):
            self.environment.assign(node.target.name, value)
        elif isinstance(node.target, PropertyAccessNode):
            obj = self.evaluate(node.target.object_expr)
            if not isinstance(obj, AayuRecord):
                self.throw_error("Property assignment only allowed on records.")
            if node.target.property_name not in obj.fields:
                self.throw_error(f"Property '{node.target.property_name}' does not exist on {obj.type_name}.")
            obj.fields[node.target.property_name] = value
        else:
            self.throw_error("Invalid assignment target.")
            
        return value

    def visit_ShowNode(self, node: ShowNode):
        value = self.evaluate(node.expression)
        print(value)

    def visit_BinaryExpressionNode(self, node: BinaryExpressionNode):
        left = self.evaluate(node.left)
        right = self.evaluate(node.right)

        if node.operator == '+': return left + right
        if node.operator == '-': return left - right
        if node.operator == '*': return left * right
        if node.operator == '/':
            if right == 0:
                self.throw_error("Cannot divide by zero.")
            return left / right
        if node.operator == '>': return left > right
        if node.operator == '<': return left < right
        if node.operator == '==': return left == right

        self.throw_error(f"Unknown operator {node.operator}")

    def visit_VariableNode(self, node: VariableNode):
        return self.environment.get(node.name, self)

    def visit_TestNode(self, node: TestNode):
        if not self.test_mode:
            return None
        
        # We need a way to run the test and catch errors.
        # But wait, test runner should just call evaluate and catch exceptions there!
        # Actually, running the test in test_mode means we just evaluate the body.
        # But to isolate environments, let's create a new env.
        test_env = Environment(enclosing=self.environment)
        previous_env = self.environment
        self.environment = test_env
        try:
            for statement in node.body:
                self.evaluate(statement)
        finally:
            self.environment = previous_env
            
        return None

    def visit_ExpectNode(self, node: ExpectNode):
        actual_val = self.evaluate(node.actual)
        expected_val = self.evaluate(node.expected)
        
        if node.operator == "equals":
            if actual_val != expected_val:
                line = getattr(self.current_node, 'line', 1) if self.current_node else 1
                raise AAYUTestFailure(f"Expected:\n{expected_val}\n\nActual:\n{actual_val}", line)
        return None

    def visit_NumberNode(self, node: NumberNode):
        return node.value

    def visit_TextNode(self, node: TextNode):
        return node.value

    def visit_IfNode(self, node: IfNode):
        condition = self.evaluate(node.condition)
        if condition:
            self.execute_block(node.body, Environment(self.environment))
        elif node.else_body is not None:
            self.execute_block(node.else_body, Environment(self.environment))

    def visit_WhileNode(self, node: WhileNode):
        while self.evaluate(node.condition):
            self.execute_block(node.body, Environment(self.environment))

    def visit_TryCatchNode(self, node: TryCatchNode):
        try:
            self.execute_block(node.try_body, Environment(self.environment))
        except ReturnException:
            raise
        except Exception:
            self.execute_block(node.catch_body, Environment(self.environment))

    def visit_RepeatNode(self, node: RepeatNode):
        times = self.evaluate(node.count)
        for _ in range(int(times)):
            self.execute_block(node.body, Environment(self.environment))

    def visit_ForEachNode(self, node: ForEachNode):
        collection = self.evaluate(node.collection)
        
        if not isinstance(collection, list):
            var_name = node.collection.name if hasattr(node.collection, 'name') else 'expression'
            self.throw_error(f"Variable '{var_name}' is not iterable.")
            
        for item in collection:
            env = Environment(self.environment)
            env.define(node.iterator, item)
            self.execute_block(node.body, env)

    def execute_block(self, statements, environment):
        previous = self.environment
        try:
            self.environment = environment
            for statement in statements:
                self.current_node = statement
                self.visit(statement)
        finally:
            self.environment = previous

    def visit_TaskNode(self, node: TaskNode):
        self.environment.define(node.name, node)

    def visit_RunNode(self, node: RunNode):
        if node.module_name:
            try:
                module_obj = self.environment.get(node.module_name)
            except Exception:
                self.throw_error(f"Module '{node.module_name}' not found.")
                
            if not isinstance(module_obj, AayuModule):
                self.throw_error(f"'{node.module_name}' is not a module.")
                
            if node.name not in module_obj.exports:
                self.throw_error(f"Task '{node.name}' is not exported from module '{node.module_name}'.")
                
            task = module_obj.exports[node.name]
        else:
            try:
                task = self.environment.get(node.name)
            except Exception:
                self.throw_error(f"Task '{node.name}' was not found.")
            
        if not isinstance(task, TaskNode):
            self.throw_error(f"{node.name} is not a task.")

        env = Environment(self.environment)
        if len(task.parameters) != len(node.arguments):
            self.throw_error(f"Expected {len(task.parameters)} arguments but got {len(node.arguments)}.")

        for i, arg_name in enumerate(task.parameters):
            val = self.evaluate(node.arguments[i])
            env.define(arg_name, val)

        try:
            self.execute_block(task.body, env)
        except ReturnException as r:
            return r.value

    def visit_ReturnNode(self, node: ReturnNode):
        value = self.evaluate(node.value)
        raise ReturnException(value)

    def visit_ListDeclarationNode(self, node: ListDeclarationNode):
        val = []
        for el in node.elements:
            val.append(self.evaluate(el))
        self.environment.define(node.name, val)

    def visit_ListInitializationNode(self, node: ListInitializationNode):
        val = self.evaluate(node.value)
        if not isinstance(val, list):
            self.throw_error(f"Value must evaluate to a list. Found {type(val)}")
        print(f"DEBUG: ListInit {node.name} evaluated to: {val}")
        self.environment.define(node.name, val)

    def visit_AddToListNode(self, node: AddToListNode):
        try:
            target_list = self.environment.get(node.list_name, self)
        except Exception:
            self.throw_error(f"Variable '{node.list_name}' was not found.")
            
        if not isinstance(target_list, list):
            self.throw_error(f"Variable '{node.list_name}' is not a list.")
            
        item_val = self.evaluate(node.item)
        target_list.append(item_val)

    def visit_MapDeclarationNode(self, node: MapDeclarationNode):
        self.environment.define(node.name, {})

    def visit_SetInMapNode(self, node: SetInMapNode):
        try:
            target_map = self.environment.get(node.map_name, self)
        except Exception:
            self.throw_error(f"Variable '{node.map_name}' was not found.")
            
        if not isinstance(target_map, dict):
            self.throw_error(f"Variable '{node.map_name}' is not a map.")
            
        key_val = self.evaluate(node.key)
        val = self.evaluate(node.value)
        target_map[key_val] = val

    def visit_GetFromMapNode(self, node: GetFromMapNode):
        try:
            target_map = self.environment.get(node.map_name, self)
        except Exception:
            self.throw_error(f"Variable '{node.map_name}' was not found.")
            
        if isinstance(target_map, list):
            key_val = self.evaluate(node.key)
            try:
                idx = int(key_val)
                return target_map[idx]
            except (ValueError, TypeError):
                self.throw_error(f"List index must be an integer, got '{key_val}'.")
            except IndexError:
                self.throw_error(f"List index out of range: {key_val}.")
        elif isinstance(target_map, dict):
            key_val = self.evaluate(node.key)
            if key_val not in target_map:
                self.throw_error(f"Key '{key_val}' was not found in map '{node.map_name}'.")
            return target_map[key_val]
        else:
            self.throw_error(f"Variable '{node.map_name}' is not a collection.")

    def visit_BuiltinFunctionNode(self, node: BuiltinFunctionNode):
        args = [self.evaluate(arg) for arg in node.arguments]
        name = node.name

        # String module
        if name == "upper":
            if len(args) != 1 or not isinstance(args[0], str):
                self.throw_error("Function 'upper' expects 1 text argument.")
            return args[0].upper()
        elif name == "lower":
            if len(args) != 1 or not isinstance(args[0], str):
                self.throw_error("Function 'lower' expects 1 text argument.")
            return args[0].lower()
        elif name == "length":
            if len(args) != 1 or not isinstance(args[0], (str, list, dict)):
                self.throw_error("Function 'length' expects 1 text, list, or map argument.")
            return float(len(args[0]))
            
        # Math module
        elif name == "sqrt":
            if len(args) != 1 or not isinstance(args[0], (int, float)):
                self.throw_error("Function 'sqrt' expects 1 number argument.")
            return float(math.sqrt(args[0]))
        elif name == "abs":
            if len(args) != 1 or not isinstance(args[0], (int, float)):
                self.throw_error("Function 'abs' expects 1 number argument.")
            return float(abs(args[0]))
        elif name == "round":
            if len(args) != 1 or not isinstance(args[0], (int, float)):
                self.throw_error("Function 'round' expects 1 number argument.")
            return float(round(args[0]))
            
        # Random module
        elif name == "random_number":
            if len(args) != 2 or not isinstance(args[0], (int, float)) or not isinstance(args[1], (int, float)):
                self.throw_error("Function 'random_number' expects 2 number arguments.")
            return float(random.randint(int(args[0]), int(args[1])))
            
        # Unknown function
        else:
            self.throw_error(f"Unknown built-in function '{name}'.")

    def visit_RecordDeclarationNode(self, node: RecordDeclarationNode):
        self.environment.define(node.name, node)

    def visit_InstanceDeclarationNode(self, node: InstanceDeclarationNode):
        record_decl = self.environment.get(node.type_name)
        if not isinstance(record_decl, RecordDeclarationNode):
            self.throw_error(f"{node.type_name} is not a record.")

        fields = {}
        for k, v in node.properties.items():
            fields[k] = self.evaluate(v)

        instance = AayuRecord(node.type_name, fields)
        self.environment.define(node.name, instance)

    def visit_PropertyAccessNode(self, node: PropertyAccessNode):
        obj = self.evaluate(node.object_expr)
        
        # Standard Library: Lists
        if isinstance(obj, list):
            if node.property_name in ("length", "count"):
                return float(len(obj))
            self.throw_error(f"List has no property '{node.property_name}'.")

        # Standard Library: Text
        if isinstance(obj, str):
            if node.property_name == "upper":
                return obj.upper()
            if node.property_name == "lower":
                return obj.lower()
            if node.property_name in ("length", "count"):
                return float(len(obj))
            self.throw_error(f"Text has no property '{node.property_name}'.")

        if not isinstance(obj, AayuRecord):
            self.throw_error(f"Cannot access property '{node.property_name}' on a non-record.")
            
        if node.property_name not in obj.fields:
            self.throw_error(f"Property '{node.property_name}' does not exist on {obj.type_name}.")
            
        return obj.fields[node.property_name]

    def visit_UseNode(self, node: UseNode):
        import os
        module_name = node.module
        
        # Determine package path
        # Assume current working directory has .aayu/packages
        package_dir = os.path.join(".aayu", "packages", module_name)
        module_file = os.path.join(package_dir, f"{module_name}.aayu")
        
        if not os.path.exists(module_file):
            line = getattr(self.current_node, 'line', 1) if self.current_node else 1
            raise AAYUImportError(f"Module '{module_name}' not found.", line, f"Did you forget to run 'aayu install {module_name}'?")
            
        with open(module_file, "r", encoding="utf-8") as f:
            code = f.read()
            
        # Parse the module code
        from lexer import Lexer
        from parser import Parser
        
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        
        # Evaluate module AST in current context
        for stmt in ast.statements:
            self.evaluate(stmt)

    def visit_ReadExpressionNode(self, node: ReadExpressionNode):
        file_path = self.evaluate(node.file_path)
        if not isinstance(file_path, str):
            self.throw_error("File path must evaluate to text.")
        try:
            with open(file_path, "r") as f:
                return f.read()
        except FileNotFoundError:
            self.throw_error(f"File not found: {file_path}")

    def visit_WriteStatementNode(self, node: WriteStatementNode):
        data = self.evaluate(node.data)
        file_path = self.evaluate(node.destination)
        if not isinstance(file_path, str):
            self.throw_error("Destination file path must evaluate to text.")
        with open(file_path, "w") as f:
            f.write(str(data))

    def visit_RenderExpressionNode(self, node: RenderExpressionNode):
        file_path = self.evaluate(node.template_path)
        if not isinstance(file_path, str):
            self.throw_error("Template path must evaluate to text.")
            
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                template_str = f.read()
        except FileNotFoundError:
            self.throw_error(f"Template file not found: {file_path}")
            
        if node.context_map_name:
            context = self.environment.get(node.context_map_name)
            if not isinstance(context, dict):
                self.throw_error(f"Context '{node.context_map_name}' must be a map.")
                
            for key, value in context.items():
                if isinstance(value, (dict, list)):
                    val_str = json.dumps(value)
                else:
                    val_str = str(value)
                template_str = template_str.replace(f"{{{{ {key} }}}}", val_str)
                template_str = template_str.replace(f"{{{{{key}}}}}", val_str)
                
        # Handle missing variables by replacing any remaining {{ var }} with empty string
        import re
        template_str = re.sub(r'\{\{\s*[\w_]+\s*\}\}', '', template_str)
        
        return template_str

    def visit_FormGetNode(self, node: FormGetNode):
        key = self.evaluate(node.key)
        if not isinstance(key, str):
            self.throw_error("Form key must evaluate to text.")
            
        req_map = self.environment.get(node.req_name)
        if not isinstance(req_map, dict):
            self.throw_error(f"'{node.req_name}' must be a map.")
            
        form_data = req_map.get("_form_data", {})
        
        # form_data values are lists of strings in parse_qs
        val_list = form_data.get(key, [])
        if len(val_list) > 0:
            return val_list[0]
        return ""

    def visit_JsonSerializeNode(self, node: JsonSerializeNode):
        data = self.evaluate(node.data)
        print(f"DEBUG: JsonSerialize {node.data} evaluated to: {data}")
        try:
            json_str = json.dumps(data)
            return AayuJSONResponse(json_str)
        except TypeError:
            self.throw_error("Cannot serialize data to JSON.")

    def visit_EntityDeclarationNode(self, node: EntityDeclarationNode):
        table_name = node.name
        columns = ["id INTEGER PRIMARY KEY AUTOINCREMENT"]
        for field in node.fields:
            field_name = field["name"]
            field_type = field["type"]
            if field_type == "text":
                columns.append(f"{field_name} TEXT")
            elif field_type == "number":
                columns.append(f"{field_name} REAL")
            else:
                columns.append(f"{field_name} TEXT")
                
        # Auto-add timestamps
        columns.append("created_at TEXT")
        columns.append("updated_at TEXT")
        
        sql = f"CREATE TABLE IF NOT EXISTS {table_name} ({', '.join(columns)})"
        self.db_cursor.execute(sql)
        self.db_conn.commit()

    def visit_CreateEntityNode(self, node: CreateEntityNode):
        table_name = node.entity_name
        data_map = self.environment.get(node.data_map)
        if not isinstance(data_map, dict):
            self.throw_error(f"'{node.data_map}' must be a map.")
            
        now = datetime.datetime.now().isoformat()
        
        # Make a copy and insert timestamps
        insert_data = dict(data_map)
        insert_data["created_at"] = now
        insert_data["updated_at"] = now
        
        columns = list(insert_data.keys())
        placeholders = ["?"] * len(columns)
        values = list(insert_data.values())
        
        sql = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({', '.join(placeholders)})"
        try:
            self.db_cursor.execute(sql, values)
            self.db_conn.commit()
        except sqlite3.OperationalError as e:
            line = getattr(self.current_node, 'line', 1) if self.current_node else 1
            raise AAYUDatabaseError(f"Database error during create: {e}", line)

    def visit_UpdateEntityNode(self, node: UpdateEntityNode):
        table_name = node.entity_name
        cond_val = self.evaluate(node.condition_value)
        data_map = self.environment.get(node.data_map)
        if not isinstance(data_map, dict):
            self.throw_error(f"'{node.data_map}' must be a map.")
            
        now = datetime.datetime.now().isoformat()
        update_data = dict(data_map)
        update_data["updated_at"] = now
        
        set_clauses = [f"{k} = ?" for k in update_data.keys()]
        values = list(update_data.values())
        values.append(cond_val)
        
        sql = f"UPDATE {table_name} SET {', '.join(set_clauses)} WHERE {node.condition_field} = ?"
        try:
            self.db_cursor.execute(sql, values)
            self.db_conn.commit()
        except sqlite3.OperationalError as e:
            line = getattr(self.current_node, 'line', 1) if self.current_node else 1
            raise AAYUDatabaseError(f"Database error during update: {e}", line)

    def visit_DeleteEntityNode(self, node: DeleteEntityNode):
        table_name = node.entity_name
        cond_val = self.evaluate(node.condition_value)
        
        sql = f"DELETE FROM {table_name} WHERE {node.condition_field} = ?"
        try:
            self.db_cursor.execute(sql, [cond_val])
            self.db_conn.commit()
        except sqlite3.OperationalError as e:
            line = getattr(self.current_node, 'line', 1) if self.current_node else 1
            raise AAYUDatabaseError(f"Database error during delete: {e}", line)

    def visit_CreateAccountNode(self, node: CreateAccountNode):
        data = self.environment.get(node.data_map_name, self)
        if not isinstance(data, dict):
            self.throw_error(f"Create account data must be a map. Got {type(data)}: {data}")
        email = data.get("email")
        password = data.get("password")
        if not email or not password:
            self.throw_error(f"Account map must contain 'email' and 'password'. Got: {data}")
        
        salt = "aayu_salty"
        hashed = hashlib.sha256((password + salt).encode()).hexdigest()
        
        now = datetime.datetime.utcnow().isoformat()
        try:
            self.db_cursor.execute(
                "INSERT INTO Account (email, password_hash, created_at, updated_at) VALUES (?, ?, ?, ?)",
                (email, hashed, now, now)
            )
            self.db_conn.commit()
        except sqlite3.IntegrityError:
            self.throw_error(f"Account with email {email} already exists.")

    def visit_LoginNode(self, node: LoginNode):
        data = self.environment.get(node.user_map_name, self)
        email = data.get("email")
        password = data.get("password")
        
        salt = "aayu_salty"
        hashed = hashlib.sha256((password + salt).encode()).hexdigest()
        
        self.db_cursor.execute("SELECT id FROM Account WHERE email = ? AND password_hash = ?", (email, hashed))
        row = self.db_cursor.fetchone()
        
        if not row:
            raise ReturnException(AayuHTMLResponse("<h1>401 Unauthorized</h1><p>Invalid email or password.</p>"))
            
        account_id = row['id']
        token = str(uuid.uuid4())
        now = datetime.datetime.utcnow().isoformat()
        
        self.db_cursor.execute(
            "INSERT INTO Session (account_id, token, expires_at, created_at, updated_at) VALUES (?, ?, ?, ?, ?)",
            (account_id, token, now, now, now)
        )
        self.db_conn.commit()
        
        if hasattr(self, 'current_request') and self.current_request:
            if not hasattr(self, 'cookies_to_set'):
                self.cookies_to_set = []
            self.cookies_to_set.append(('Set-Cookie', f"AAYU_SESSION={token}; HttpOnly; Path=/"))

    def visit_LogoutNode(self, node: LogoutNode):
        if not hasattr(self, 'current_request') or not self.current_request:
            return
            
        cookie_header = self.current_request.headers.get('Cookie')
        if cookie_header:
            C = cookies.SimpleCookie(cookie_header)
            if 'AAYU_SESSION' in C:
                token = C['AAYU_SESSION'].value
                self.db_cursor.execute("DELETE FROM Session WHERE token = ?", (token,))
                self.db_conn.commit()
                
        if not hasattr(self, 'cookies_to_set'):
            self.cookies_to_set = []
        self.cookies_to_set.append(('Set-Cookie', "AAYU_SESSION=; HttpOnly; Path=/; Expires=Thu, 01 Jan 1970 00:00:00 GMT"))

    def visit_GuardSessionNode(self, node: GuardSessionNode):
        if not hasattr(self, 'current_request') or not self.current_request:
            raise ReturnException(AayuHTMLResponse("<h1>401 Unauthorized</h1><p>No active HTTP context.</p>"))
            
        cookie_header = self.current_request.headers.get('Cookie')
        if not cookie_header:
            raise ReturnException(AayuHTMLResponse("<h1>401 Unauthorized</h1><p>Session required.</p>"))
            
        C = cookies.SimpleCookie(cookie_header)
        if 'AAYU_SESSION' not in C:
            raise ReturnException(AayuHTMLResponse("<h1>401 Unauthorized</h1><p>Session required.</p>"))
            
        token = C['AAYU_SESSION'].value
        self.db_cursor.execute("SELECT * FROM Session WHERE token = ?", (token,))
        row = self.db_cursor.fetchone()
        
        if not row:
            raise ReturnException(AayuHTMLResponse("<h1>401 Unauthorized</h1><p>Invalid session.</p>"))

    def visit_FindEntityNode(self, node: FindEntityNode):
        table_name = node.entity_name
        if node.condition_field:
            cond_val = self.evaluate(node.condition_value)
            sql = f"SELECT * FROM {table_name} WHERE {node.condition_field} = ?"
            try:
                self.db_cursor.execute(sql, [cond_val])
            except sqlite3.OperationalError as e:
                line = getattr(self.current_node, 'line', 1) if self.current_node else 1
                raise AAYUDatabaseError(f"Database error during find: {e}", line)
        else:
            sql = f"SELECT * FROM {table_name}"
            try:
                self.db_cursor.execute(sql)
            except sqlite3.OperationalError as e:
                line = getattr(self.current_node, 'line', 1) if self.current_node else 1
                raise AAYUDatabaseError(f"Database error during find: {e}", line)
                
        rows = self.db_cursor.fetchall()
        result = []
        for row in rows:
            result.append(dict(row))
        return result

    def visit_RouteNode(self, node: RouteNode):
        path = self.evaluate(node.path)
        if not isinstance(path, str):
            self.throw_error("Route path must evaluate to text.")
        self.routes[path] = node.handler_name

    def visit_ServeNode(self, node: ServeNode):
        port_val = self.evaluate(node.port)
        if not isinstance(port_val, (int, float)):
            self.throw_error("Port must be a number.")
        port = int(port_val)

        if node.handler_name:
            task_decl = self.environment.get(node.handler_name)
            if not isinstance(task_decl, TaskNode):
                self.throw_error(f"'{node.handler_name}' is not a valid task for server handler.")
            if len(task_decl.parameters) != 1:
                self.throw_error(f"Server handler task '{node.handler_name}' must accept exactly 1 parameter (req).")
        else:
            # We are using dynamic routing
            pass

        # Capture interpreter instance for the HTTP request handler
        interp_instance = self

        class AayuHTTPRequestHandler(BaseHTTPRequestHandler):
            def handle_request(self):
                # Create a map for the request
                req_map = {
                    "path": self.path,
                    "method": self.command,
                    "_form_data": {}
                }
                
                # Parse form data for POST
                if self.command == "POST":
                    content_length = int(self.headers.get('Content-Length', 0))
                    if content_length > 0:
                        post_data = self.rfile.read(content_length).decode('utf-8')
                        import urllib.parse
                        req_map["_form_data"] = urllib.parse.parse_qs(post_data)

                # Determine which task to run
                task_name_to_run = node.handler_name
                print(f"DEBUG: do_GET received {self.path}")
                print(f"Request: {self.command} {self.path}")
                print(f"Routes available: {interp_instance.routes}")
                if task_name_to_run is None:
                    # Strip query params for routing match
                    route_path = self.path.split('?')[0]
                    if route_path in interp_instance.routes:
                        task_name_to_run = interp_instance.routes[route_path]
                
                print(f"Matched task: {task_name_to_run}")
                if task_name_to_run is None:
                    # 404 Not Found
                    self.send_response(404)
                    self.send_header("Content-type", "text/html; charset=utf-8")
                    self.end_headers()
                    self.wfile.write(bytes("<h1>404 Not Found</h1>", "utf8"))
                    return

                # Get the actual task
                try:
                    task_to_run = interp_instance.environment.get(task_name_to_run)
                except Exception:
                    self.send_response(500)
                    self.send_header("Content-type", "text/html; charset=utf-8")
                    self.end_headers()
                    self.wfile.write(bytes(f"<h1>500 Internal Server Error</h1><p>Task '{task_name_to_run}' not found.</p>", "utf8"))
                    return

                if not isinstance(task_to_run, TaskNode) or len(task_to_run.parameters) != 1:
                    self.send_response(500)
                    self.send_header("Content-type", "text/html; charset=utf-8")
                    self.end_headers()
                    self.wfile.write(bytes(f"<h1>500 Internal Server Error</h1><p>Task '{task_name_to_run}' must be a task taking exactly 1 parameter.</p>", "utf8"))
                    return

                # Execute the Aayu task
                task_env = Environment(interp_instance.environment)
                task_env.define(task_to_run.parameters[0], req_map)
                
                previous_env = interp_instance.environment
                try:
                    interp_instance.environment = task_env
                    interp_instance.current_request = self
                    interp_instance.cookies_to_set = []
                    
                    for statement in task_to_run.body:
                        interp_instance.evaluate(statement)
                    # If it didn't return anything
                    result = ""
                    content_type = "text/html; charset=utf-8"
                    status_code = 200
                except ReturnException as r:
                    if isinstance(r.value, AayuJSONResponse):
                        result = r.value.data_str
                        content_type = "application/json"
                        status_code = 200
                    elif isinstance(r.value, AayuHTMLResponse):
                        result = r.value.data_str
                        content_type = "text/html; charset=utf-8"
                        # Handle redirect or auth errors implicitly? Wait, if it says 401 we should send 401...
                        # For simplicity, if it contains 401 Unauthorized, set status 401
                        status_code = 401 if "401 Unauthorized" in result else 200
                    elif isinstance(r.value, AayuTextResponse):
                        result = r.value.data_str
                        content_type = "text/plain; charset=utf-8"
                        status_code = 200
                    else:
                        result = str(r.value)
                        content_type = "text/html; charset=utf-8"
                        status_code = 200
                except AAYURuntimeError as e:
                    result = f"<h1>500 Internal Server Error</h1><p>{e.message}</p>"
                    content_type = "text/html; charset=utf-8"
                    status_code = 500
                finally:
                    interp_instance.environment = previous_env
                    interp_instance.current_request = None

                    print(f"DEBUG: WRITING RESULT: {result}")

                    self.send_response(status_code)
                    self.send_header("Content-type", content_type)
                
                # Check for cookies to set
                if hasattr(interp_instance, 'cookies_to_set'):
                    for header_name, header_value in interp_instance.cookies_to_set:
                        self.send_header(header_name, header_value)
                        
                self.end_headers()
                self.wfile.write(bytes(result, "utf8"))

            def do_GET(self):
                self.handle_request()
                
            def do_POST(self):
                self.handle_request()

        if node.handler_name:
            print(f"Starting Aayu Web Server on port {port} using handler '{node.handler_name}'...")
        else:
            print(f"Starting Aayu Web Router on port {port}...")

        server = HTTPServer(("", port), AayuHTTPRequestHandler)
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down server.")
            server.server_close()
