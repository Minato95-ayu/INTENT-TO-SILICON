
        elif opcode == Opcode.CREATE_MODEL:
            idx = self.vm.decoder.fetch16(self.vm.registers.ip + 1)
            self.vm.registers.ip += 3
            model_name = self.vm.value_stack.pop()
            fields = self.vm.constant_pool[idx]
            self.vm.database.create_model(model_name, fields)
            
            # Register ORM standard library functions dynamically
            def _save_func(args, vm, m_name=model_name):
                # args[0] is the dictionary to save
                if len(args) > 0 and isinstance(args[0], dict):
                    data = args[0]
                    columns = ", ".join(data.keys())
                    placeholders = ", ".join(["?"] * len(data))
                    query = f"INSERT INTO {m_name} ({columns}) VALUES ({placeholders})"
                    vm.database.execute_query(query, tuple(data.values()))
                    return True
                return False
                
            def _find_func(args, vm, m_name=model_name):
                query = f"SELECT * FROM {m_name}"
                return vm.database.execute_query(query)
                
            self.vm.stdlib.registry.functions[f"db.{model_name}.save"] = _save_func
            self.vm.stdlib.registry.functions[f"db.{model_name}.find"] = _find_func
        elif opcode == Opcode.REGISTER_ROUTE:
            idx = self.vm.decoder.fetch16(self.vm.registers.ip + 1)
            self.vm.registers.ip += 3
            path = self.vm.value_stack.pop()
            methods_meta = self.vm.constant_pool[idx]
            self.vm.api_router.register_route(path, methods_meta)
            self.vm.api_router.start()
            
        elif opcode == Opcode.CHECK_AUTH:
            self.vm.registers.ip += 3
            # Check for authToken in the current state scope
            token = None
            if self.vm.state_scopes:
                # We search from top to bottom
                for scope in reversed(self.vm.state_scopes):
                    if "authToken" in scope.variables:
                        token = scope.variables["authToken"]
                        break
            
            if not token:
                raise KernelError("Unauthorized: Missing auth token", self.vm.registers.ip)
                
            from aayu.runtime.stdlib.modules.auth_lib import verify_jwt
            payload = verify_jwt(token)
            if not payload:
                raise KernelError("Unauthorized: Invalid or expired auth token", self.vm.registers.ip)
                
            # Inject req_user into the local scope so the action can use it
            if self.vm.state_scopes:
                self.vm.state_scopes[-1].define_variable("req_user", payload)
            
        elif opcode == Opcode.RETURN_VALUE:
            if self.vm.state_scopes:
                # We search from top to bottom
                for scope in reversed(self.vm.state_scopes):
                    if "authToken" in scope:
                        token = scope["authToken"]
                        break
            # Inject req_user into the local scope so the action can use it
            if self.vm.state_scopes:
                self.vm.state_scopes[-1]["req_user"] = payload
            # Check for authToken in the current state scope or global state
            token = None
            if self.vm.state_scopes:
                # We search from top to bottom
                for scope in reversed(self.vm.state_scopes):
                    if "authToken" in scope:
                        token = scope["authToken"]
                        break
            if not token and "authToken" in self.vm.state:
                token = self.vm.state["authToken"]
            # Inject req_user into the local scope so the action can use it
            if self.vm.state_scopes:
                self.vm.state_scopes[-1]["req_user"] = payload
            else:
                self.vm.state["req_user"] = payload
        elif opcode == Opcode.BUILD_DICT:
            self.vm.registers.ip += 3
            keys = self.vm.value_stack.pop()
            d = {}
            # print(f"[DEBUG BUILD_DICT] keys: {keys}, stack depth: {self.vm.value_stack.depth()}")
            for key in reversed(keys):
                try:
                    d[key] = self.vm.value_stack.pop()
                except Exception as e:
                    print(f"[DEBUG BUILD_DICT ERROR] Failed popping for key: {key}. Current stack: {self.vm.value_stack.stack}")
                    raise e
            self.vm.value_stack.push(d)
            print(f"[DEBUG BUILD_DICT] keys: {keys}, stack depth: {self.vm.value_stack.depth()}")
        elif opcode == Opcode.CREATE_MODEL:
            idx = self.vm.decoder.fetch16(self.vm.registers.ip + 1)
            self.vm.registers.ip += 3
            model_name = self.vm.value_stack.pop()
            payload = self.vm.constant_pool[idx]
            if isinstance(payload, dict) and "fields" in payload:
                fields = payload["fields"]
                decorators = payload.get("decorators", [])
            else:
                fields = payload
                decorators = []
                
            self.vm.database.create_model(model_name, fields, decorators)