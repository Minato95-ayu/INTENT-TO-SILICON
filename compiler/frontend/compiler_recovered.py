"""
=============================================================================
FILE: compiler_recovered.py
PURPOSE: Part of the AAYU Intent-to-Silicon project
=============================================================================
This file is part of the AAYU (Aayu) Intent-to-Silicon Programming Language.
The AAYU language enables developers to write code using natural language
intentions, which are compiled to optimized backend code.

For beginners: This file handles part of the aayu intent-to-silicon project.
To understand the project architecture, see the ARCHITECTURE_FREEZE.md file.
=============================================================================
"""

Created At: 2026-06-29T07:25:45Z
Completed At: 2026-06-29T07:25:46Z
File Path: `file:///d:/intent-to-silicon-research/INTENT-TO-SILICON/prototype/language/compiler.py`
Total Lines: 755
Total Bytes: 31149
Showing lines 1 to 755
The following code has been modified to include a line number before every line, in the format: <line_number>: <original_line>. Please note that any changes targeting the original code should remove the line number, colon, and leading space.
1: from ast_nodes import *

2: from ir import Opcode, Instruction, Bytecode

3: 

4: class AAYUCompiler:

5:     def __init__(self, filename: str = ""):

6:         self.bytecode = Bytecode()

7:         self.loop_counter = 0

8:         self.filename = filename

9:         self.current_line = None

10:         self.ui_generator = None

11:         self.entity_registry = {}

12:         

13:     def _add_constant(self, value) -> int:

14:         if value in self.bytecode.constants:

15:             return self.bytecode.constants.index(value)

16:         self.bytecode.constants.append(value)

17:         return len(self.bytecode.constants) - 1

18:         

19:     def _add_name(self, name: str) -> int:

20:         if name in self.bytecode.names:

21:             return self.bytecode.names.index(name)

22:         self.bytecode.names.append(name)

23:         return len(self.bytecode.names) - 1

24:         

25:     def _emit(self, opcode: Opcode, operand: int = None) -> int:

26:         self.bytecode.instructions.append(

27:             Instruction(opcode, operand, line=self.current_line, file=self.filename)

28:         )

29:         return len(self.bytecode.instructions) - 1

30:         

31:     def compile(self, node: Node) -> Bytecode:

32:         self.bytecode.file = self.filename

33:         self.visit(node)

34:         return self.bytecode

35:         

36:     def visit(self, node: Node):

37:         old_line = self.current_line

38:         if hasattr(node, 'line') and node.line is not None:

39:             self.current_line = node.line

40:             

41:         method_name = f'visit_{type(node).__name__}'

42:         visitor = getattr(self, method_name, self.generic_visit)

43:         try:

44:             return visitor(node)

45:         finally:

46:             self.current_line = old_line

47:         

48:     def generic_visit(self, node: Node):

49:         raise NotImplementedError(f"No visit_{type(node).__name__} method defined in compiler")

50:         

51: 

52:     def visit_BlockNode(self, node: BlockNode):

53:         for stmt in node.statements:

54:             self.visit(stmt)

55: 

56:     def visit_ProgramNode(self, node: ProgramNode):

57:         for stmt in node.statements:

58:             self.visit(stmt)

59:         self._emit(Opcode.RETURN)

60: 

61:     def visit_ImportNode(self, node: ImportNode):

62:         pass

63: 

64:     def visit_ModuleDeclarationNode(self, node: ModuleDeclarationNode):

65:         pass

66: 

67:     def visit_UseNode(self, node: UseNode):

68:         import os

69:         from errors import AAYUError

70:         from lexer import Lexer

71:         from parser import Parser

72:         

73:         module_name = node.module

74:         

75:         # Check standard package directory

76:         package_dir = os.path.join(".aayu", "packages", module_name)

77:         module_file = os.path.join(package_dir, "main.aayu")

78:         

79:         if not os.path.exists(module_file):

80:             # Fallback to single file import if user wants to import a local file

81:             if os.path.exists(f"{module_name}.aayu"):

82:                 module_file = f"{module_name}.aayu"

83:             else:

84:                 line = node.line if hasattr(node, 'line') else 1

85:                 raise AAYUError("Import Error", f"Module '{module_name}' not found.", line, f"Did you forget to run 'aayu install {module_name}'?")

86:                 

87:         with open(module_file, "r", encoding="utf-8") as f:

88:             source = f.read()

89:             

90:         lexer = Lexer(source)

91:         parser = Parser(lexer.tokenize(), filename=module_file)

92:         ast = parser.parse()

93:         

94:         # Compile the included AST inline

95:         self.visit(ast)

96:             

97:     def visit_NumberNode(self, node: NumberNode):

98:         idx = self._add_constant(node.value)

99:         self._emit(Opcode.LOAD_CONST, idx)

100:         

101:     def visit_TextNode(self, node: TextNode):

102:         idx = self._add_constant(node.value)

103:         self._emit(Opcode.LOAD_CONST, idx)

104:         

105:     def _get_name(self, node: Node) -> str:

106:         if getattr(node, 'symbol', None):

107:             return f"sym_{node.symbol.id}"

108:         return node.name

109: 

110:     def visit_VariableNode(self, node: VariableNode):

111:         idx = self._add_name(self._get_name(node))

112:         self._emit(Opcode.LOAD_VAR, idx)

113:         

114:     def visit_DeclarationNode(self, node: DeclarationNode):

115:         self.visit(node.value)

116:         idx = self._add_name(self._get_name(node))

117:         self._emit(Opcode.STORE_VAR, idx)

118: 

119:     def visit_FunctionDeclNode(self, node: FunctionDeclNode):

120:         child_compiler = AAYUCompiler(filename=self.filename)

121:         child_compiler.bytecode.name = self._get_name(node)

122:         

123:         if hasattr(node, 'func_scope'):

124:             param_names = []

125:             for p in node.parameters:

126:                 sym = node.func_scope.lookup(p, current_only=True)

127:                 if sym:

128:                     param_names.append(f"sym_{sym.id}")

129:                 else:

130:                     param_names.append(p)

131:             child_compiler.bytecode.parameters = param_names

132:         else:

133:             child_compiler.bytecode.parameters = node.parameters

134:         

135:         # Compile function body

136:         for stmt in node.body:

137:             child_compiler.visit(stmt)

138:             

139:         # Ensure function always returns

140:         child_compiler._emit(Opcode.LOAD_CONST, child_compiler._add_constant(None))

141:         child_compiler._emit(Opcode.RETURN)

142:         

143:         func_bytecode = child_compiler.bytecode

144:         

145:         const_idx = self._add_constant(func_bytecode)

146:         self._emit(Opcode.LOAD_CONST, const_idx)

147:         

148:         name_idx = self._add_name(self._get_name(node))

149:         self._emit(Opcode.STORE_VAR, name_idx)

150:         

151:     def visit_BuiltinFunctionNode(self, node: BuiltinFunctionNode):

152:         # Load the function object from variable

153:         name_idx = self._add_name(self._get_name(node))

154:         self._emit(Opcode.LOAD_VAR, name_idx)

155:             

156:         # Load arguments

157:         for arg in node.arguments:

158:             self.visit(arg)

159:             

160:         # Emit CALL

161:         self._emit(Opcode.CALL, len(node.arguments))

162:         

163: 

164:     def visit_UnaryExpressionNode(self, node: UnaryExpressionNode):

165:         self.visit(node.right)

166:         if node.operator in ('-', 'minus'):

167:             self._emit(Opcode.NEG)

168:         elif node.operator == 'not':

169:             self._emit(Opcode.NOT)

170: 

171: 

172:     def visit_LogicalExpressionNode(self, node: LogicalExpressionNode):

173:         self.visit(node.left)

174:         if node.operator == "and":

175:             jump_idx = self._emit(Opcode.JUMP_IF_FALSE, 0)

176:             # Pop left operand if true, to evaluate right operand

177:             self._emit(Opcode.POP)

178:             self.visit(node.right)

179:             # Patch jump

180:             self.bytecode.instructions[jump_idx].operand = len(self.bytecode.instructions) - jump_idx - 1

181:         elif node.operator == "or":

182:             jump_idx = self._emit(Opcode.JUMP_IF_TRUE, 0) # Need JUMP_IF_TRUE opcode

183:             self._emit(Opcode.POP)

184:             self.visit(node.right)

185:             self.bytecode.instructions[jump_idx].operand = len(self.bytecode.instructions) - jump_idx - 1

186: 

187:     def visit_BinaryExpressionNode(self, node: BinaryExpressionNode):

188:         self.visit(node.left)

189:         self.visit(node.right)

190:         

191:         if node.operator in ('is', 'equals', 'equal to', '==', 'EQUAL'):

192:             self._emit(Opcode.EQ)

193:         elif node.operator in ('less', 'less than', '<', 'LESS'):

194:             self._emit(Opcode.LT)

195:         elif node.operator in ('greater', 'greater than', '>', 'GREATER'):

196:             self._emit(Opcode.GT)

197:         elif node.operator in ('<=', 'LTE'):

198:             self._emit(Opcode.LE)

199:         elif node.operator in ('>=', 'GTE'):

200:             self._emit(Opcode.GE)

201:         elif node.operator in ('!=', 'NOT_EQ'):

202:             self._emit(Opcode.NE)

203:         elif node.operator in ('plus', '+', 'PLUS'):

204:             self._emit(Opcode.ADD)

205:         elif node.operator in ('minus', '-', 'MINUS'):

206:             self._emit(Opcode.SUB)

207:         elif node.operator in ('times', '*', 'TIMES'):

208:             self._emit(Opcode.MUL)

209:         elif node.operator in ('divided by', '/', 'DIVIDE'):

210:             self._emit(Opcode.DIV)

211:         elif node.operator in ('modulo', '%', 'MOD'):

212:             self._emit(Opcode.MOD)

213:             

214:     def visit_IfNode(self, node: IfNode):

215:         self.visit(node.condition)

216:         

217:         # Emit JUMP_IF_FALSE with placeholder

218:         jump_if_false_idx = len(self.bytecode.instructions)

219:         self._emit(Opcode.JUMP_IF_FALSE, 0)

220:         

221:         for stmt in node.body:

222:             self.visit(stmt)

223:             

224:         if node.else_body:

225:             jump_forward_idx = len(self.bytecode.instructions)

226:             self._emit(Opcode.JUMP, 0)

227:             

228:             # Patch JUMP_IF_FALSE to jump here

229:             self.bytecode.instructions[jump_if_false_idx].operand = len(self.bytecode.instructions) - jump_if_false_idx

230:             

231:             for stmt in node.else_body:

232:                 self.visit(stmt)

233:                 

234:             # Patch JUMP to jump here

235:             self.bytecode.instructions[jump_forward_idx].operand = len(self.bytecode.instructions) - jump_forward_idx

236:         else:

237:             # Patch JUMP_IF_FALSE to jump here

238:             self.bytecode.instructions[jump_if_false_idx].operand = len(self.bytecode.instructions) - jump_if_false_idx

239: 

240:     def visit_WhileNode(self, node: WhileNode):

241:         start_idx = len(self.bytecode.instructions)

242:         self.visit(node.condition)

243:         

244:         jump_if_false_idx = len(self.bytecode.instructions)

245:         self._emit(Opcode.JUMP_IF_FALSE, 0)

246:         

247:         for stmt in node.body:

248:             self.visit(stmt)

249:             

250:         # Jump back to start_idx

251:         offset = start_idx - len(self.bytecode.instructions)

252:         self._emit(Opcode.JUMP, offset)

253:         

254:         # Patch JUMP_IF_FALSE

255:         self.bytecode.instructions[jump_if_false_idx].operand = len(self.bytecode.instructions) - jump_if_false_idx

256:         

257:     def visit_TaskNode(self, node: TaskNode):

258:         # Compile task body in a new compiler context

259:         task_compiler = AAYUCompiler(filename=self.filename)

260:         task_bytecode = task_compiler.compile(ProgramNode(node.body))

261:         

262:         # Ensure the bytecode ends with a RETURN

263:         if not task_bytecode.instructions or task_bytecode.instructions[-1].opcode != Opcode.RETURN:

264:             none_idx = task_compiler._add_constant(None)

265:             task_compiler._emit(Opcode.LOAD_CONST, none_idx)

266:             task_compiler._emit(Opcode.RETURN)

267:             

268:         task_bytecode.parameters = node.parameters

269:         task_bytecode.name = node.name

270:         

271:         # Add to parent constant pool and emit code to register the task variable

272:         const_idx = self._add_constant(task_bytecode)

273:         name_idx = self._add_name(node.name)

274:         

275:         self._emit(Opcode.LOAD_CONST, const_idx)

276:         self._emit(Opcode.STORE_VAR, name_idx)

277:         

278:     def visit_RunNode(self, node: RunNode):

279:         # Push arguments to stack

280:         for arg in node.arguments:

281:             self.visit(arg)

282:             

283:         # Load the task object

284:         name_idx = self._add_name(node.name)

285:         self._emit(Opcode.LOAD_VAR, name_idx)

286:         

287:         # Call task with number of arguments as operand

288:         self._emit(Opcode.CALL_TASK, len(node.arguments))

289: 

290:     def visit_AssignmentNode(self, node: AssignmentNode):

291:         if isinstance(node.target, VariableNode):

292:             self.visit(node.value)

293:             idx = self._add_name(node.target.name)

294:             self._emit(Opcode.STORE_VAR, idx)

295:         else:

296:             raise NotImplementedError("Only variable assignment is supported in the VM compiler.")

297: 

298:     def visit_ReturnNode(self, node: ReturnNode):

299:         if node.value:

300:             self.visit(node.value)

301:         else:

302:             self._emit(Opcode.LOAD_CONST, self._add_constant(None))

303:         self._emit(Opcode.RETURN)

304: 

305:     def visit_ListLiteralNode(self, node: Node):

306:         for el in node.elements:

307:             self.visit(el)

308:         self._emit(Opcode.MAKE_LIST, len(node.elements))

309: 

310:     def visit_MapLiteralNode(self, node: Node):

311:         for k, v in node.elements:

312:             self.visit(k)

313:             self.visit(v)

314:         self._emit(Opcode.MAKE_MAP, len(node.elements))

315: 

316:     def visit_ListDeclarationNode(self, node: ListDeclarationNode):

317:         self._emit(Opcode.BUILD_LIST, 0)

318:         idx = self._add_name(node.name)

319:         self._emit(Opcode.STORE_VAR, idx)

320: 

321:     def visit_ListInitializationNode(self, node: ListInitializationNode):

322:         self.visit(node.value)

323:         idx = self._add_name(node.name)

324:         self._emit(Opcode.STORE_VAR, idx)

325: 

326:     def visit_AddToListNode(self, node: AddToListNode):

327:         self.visit(node.item)

328:         idx = self._add_name(node.list_name)

329:         self._emit(Opcode.LOAD_VAR, idx)

330:         self._emit(Opcode.ADD_TO_LIST)

331:         self._emit(Opcode.POP)

332: 

333:     def visit_MapDeclarationNode(self, node: MapDeclarationNode):

334:         self._emit(Opcode.BUILD_MAP, 0)

335:         idx = self._add_name(node.name)

336:         self._emit(Opcode.STORE_VAR, idx)

337: 

338:     def visit_SetInMapNode(self, node: SetInMapNode):

339:         self.visit(node.value)

340:         self.visit(node.key)

341:         idx = self._add_name(node.map_name)

342:         self._emit(Opcode.LOAD_VAR, idx)

343:         self._emit(Opcode.MAP_SET)

344: 

345:     def visit_GetFromMapNode(self, node: GetFromMapNode):

346:         self.visit(node.key)

347:         idx = self._add_name(node.map_name)

348:         self._emit(Opcode.LOAD_VAR, idx)

349:         self._emit(Opcode.GET_ITEM)

350: 

351:     def visit_EntityDeclarationNode(self, node: EntityDeclarationNode):

352:         self.entity_registry[node.name] = node.fields

353: 

354:         name_idx = self._add_constant(node.name)

355:         self._emit(Opcode.LOAD_CONST, name_idx)

356: 

357:         fields_idx = self._add_constant(node.fields)

358:         self._emit(Opcode.LOAD_CONST, fields_idx)

359:         

360:         fn_idx = self._add_name("db_register_entity")

361:         self._emit(Opcode.LOAD_VAR, fn_idx)

362:         

363:         self._emit(Opcode.CALL_TASK, 2)

364:         self._emit(Opcode.POP)

365: 

366:     def visit_CreateEntityNode(self, node: CreateEntityNode):

367:         name_idx = self._add_constant(node.entity_name)

368:         self._emit(Opcode.LOAD_CONST, name_idx)

369:         

370:         map_idx = self._add_name(node.data_map)

371:         self._emit(Opcode.LOAD_VAR, map_idx)

372:         

373:         fn_idx = self._add_name("db_create")

374:         self._emit(Opcode.LOAD_VAR, fn_idx)

375:         

376:         self._emit(Opcode.CALL_TASK, 2)

377:         self._emit(Opcode.POP)

378: 

379:     def visit_FindEntityNode(self, node: FindEntityNode):

380:         name_idx = self._add_constant(node.entity_name)

381:         self._emit(Opcode.LOAD_CONST, name_idx)

382:         

383:         field_idx = self._add_constant(node.condition_field)

384:         self._emit(Opcode.LOAD_CONST, field_idx)

385:         

386:         if node.condition_value:

387:             self.visit(node.condition_value)

388:         else:

389:             self._emit(Opcode.LOAD_CONST, self._add_constant(None))

390:             

391:         fn_idx = self._add_name("db_find")

392:         self._emit(Opcode.LOAD_VAR, fn_idx)

393:         

394:         self._emit(Opcode.CALL_TASK, 3)

395: 

396:     def visit_UpdateEntityNode(self, node: UpdateEntityNode):

397:         name_idx = self._add_constant(node.entity_name)

398:         self._emit(Opcode.LOAD_CONST, name_idx)

399:         

400:         field_idx = self._add_constant(node.condition_field)

401:         self._emit(Opcode.LOAD_CONST, field_idx)

402:         

403:         self.visit(node.condition_value)

404:         

405:         map_idx = self._add_name(node.data_map)

406:         self._emit(Opcode.LOAD_VAR, map_idx)

407:         

408:         fn_idx = self._add_name("db_update")

409:         self._emit(Opcode.LOAD_VAR, fn_idx)

410:         

411:         self._emit(Opcode.CALL_TASK, 4)

412:         self._emit(Opcode.POP)

413: 

414:     def visit_DeleteEntityNode(self, node: DeleteEntityNode):

415:         name_idx = self._add_constant(node.entity_name)

416:         self._emit(Opcode.LOAD_CONST, name_idx)

417:         

418:         field_idx = self._add_constant(node.condition_field)

419:         self._emit(Opcode.LOAD_CONST, field_idx)

420:         

421:         self.visit(node.condition_value)

422:         

423:         fn_idx = self._add_name("db_delete")

424:         self._emit(Opcode.LOAD_VAR, fn_idx)

425:         

426:         self._emit(Opcode.CALL_TASK, 3)

427:         self._emit(Opcode.POP)

428: 

429:     def visit_JsonSerializeNode(self, node: JsonSerializeNode):

430:         self.visit(node.data)

431:         

432:         fn_idx = self._add_name("json_serialize")

433:         self._emit(Opcode.LOAD_VAR, fn_idx)

434:         

435:         self._emit(Opcode.CALL_TASK, 1)

436: 

437:     def visit_RenderExpressionNode(self, node: RenderExpressionNode):

438:         self.visit(node.template_path)

439:         

440:         if node.context_map_name:

441:             map_idx = self._add_name(node.context_map_name)

442:             self._emit(Opcode.LOAD_VAR, map_idx)

443:         else:

444:             self._emit(Opcode.LOAD_CONST, self._add_constant(None))

445:             

446:         fn_idx = self._add_name("render_template")

447:         self._emit(Opcode.LOAD_VAR, fn_idx)

448:         self._emit(Opcode.CALL_TASK, 2)

449: 

450:     def visit_RouteNode(self, node: RouteNode):

451:         self.visit(node.path)

452:         method_idx = self._add_constant(node.method)

453:         self._emit(Opcode.LOAD_CONST, method_idx)

454:         handler_idx = self._add_constant(node.handler_name)

455:         self._emit(Opcode.LOAD_CONST, handler_idx)

456:         fn_idx = self._add_name("http_route")

457:         self._emit(Opcode.LOAD_VAR, fn_idx)

458:         self._emit(Opcode.CALL_TASK, 3)

459:         self._emit(Opcode.POP)

460: 

461:     def visit_FormGetNode(self, node: FormGetNode):

462:         self.visit(node.key)

463:         idx = self._add_name(node.req_name)

464:         self._emit(Opcode.LOAD_VAR, idx)

465:         fn_idx = self._add_name("http_form_get")

466:         self._emit(Opcode.LOAD_VAR, fn_idx)

467:         self._emit(Opcode.CALL_TASK, 2)

468: 

469:     def visit_ServeNode(self, node: ServeNode):

470:         self.visit(node.port)

471:         if node.handler_name:

472:             idx = self._add_constant(node.handler_name)

473:             self._emit(Opcode.LOAD_CONST, idx)

474:         else:

475:             self._emit(Opcode.LOAD_CONST, self._add_constant(None))

476:             

477:         fn_idx = self._add_name("http_serve")

478:         self._emit(Opcode.LOAD_VAR, fn_idx)

479:         self._emit(Opcode.CALL_TASK, 2)

480:         self._emit(Opcode.POP)

481: 

482:     def visit_ForEachNode(self, node: ForEachNode):

483:         loop_id = self.loop_counter

484:         self.loop_counter += 1

485:         

486:         coll_name = f"_coll_{loop_id}"

487:         idx_name = f"_idx_{loop_id}"

488:         

489:         # 1. Evaluate collection and store it in _coll_{id}

490:         self.visit(node.collection)

491:         coll_idx = self._add_name(coll_name)

492:         self._emit(Opcode.STORE_VAR, coll_idx)

493:         

494:         # 2. Store 0.0 in _idx_{id}

495:         self._emit(Opcode.LOAD_CONST, self._add_constant(0.0))

496:         idx_idx = self._add_name(idx_name)

497:         self._emit(Opcode.STORE_VAR, idx_idx)

498:         

499:         # 3. Mark condition check index

500:         cond_ip = len(self.bytecode.instructions)

501:         

502:         # 4. Check index < len(collection)

503:         self._emit(Opcode.LOAD_VAR, idx_idx)

504:         self._emit(Opcode.LOAD_VAR, coll_idx)

505:         len_fn_idx = self._add_name("collection_len")

506:         self._emit(Opcode.LOAD_VAR, len_fn_idx)

507:         self._emit(Opcode.CALL_TASK, 1)

508:         self._emit(Opcode.LESS)

509:         

510:         # 5. Jump if false placeholder

511:         jump_if_false_idx = len(self.bytecode.instructions)

512:         self._emit(Opcode.JUMP_IF_FALSE, 0)

513:         

514:         # 6. Fetch b = collection[index] and store in node.iterator

515:         self._emit(Opcode.LOAD_VAR, idx_idx)

516:         self._emit(Opcode.LOAD_VAR, coll_idx)

517:         self._emit(Opcode.GET_ITEM)

518:         iterator_idx = self._add_name(node.iterator)

519:         self._emit(Opcode.STORE_VAR, iterator_idx)

520:         

521:         # 7. Compile loop body

522:         for stmt in node.body:

523:             self.visit(stmt)

524:             

525:         # 8. Increment index: index = index + 1

526:         self._emit(Opcode.LOAD_VAR, idx_idx)

527:         self._emit(Opcode.LOAD_CONST, self._add_constant(1.0))

528:         self._emit(Opcode.ADD)

529:         self._emit(Opcode.STORE_VAR, idx_idx)

530:         

531:         # 9. Jump backward to cond_ip

532:         offset = len(self.bytecode.instructions) - cond_ip

533:         self._emit(Opcode.JUMP_BACKWARD, offset)

534:         

535:         # 10. Patch condition check jump

536:         self.bytecode.instructions[jump_if_false_idx].operand = len(self.bytecode.instructions) - jump_if_false_idx

537: 

538:     def visit_CreateAccountNode(self, node: CreateAccountNode):

539:         map_idx = self._add_name(node.data_map_name)

540:         self._emit(Opcode.LOAD_VAR, map_idx)

541:         fn_idx = self._add_name("auth_create_account")

542:         self._emit(Opcode.LOAD_VAR, fn_idx)

543:         self._emit(Opcode.CALL_TASK, 1)

544:         self._emit(Opcode.POP)

545: 

546:     def visit_LoginNode(self, node: LoginNode):

547:         map_idx = self._add_name(node.user_map_name)

548:         self._emit(Opcode.LOAD_VAR, map_idx)

549:         fn_idx = self._add_name("auth_login")

550:         self._emit(Opcode.LOAD_VAR, fn_idx)

551:         self._emit(Opcode.CALL_TASK, 1)

552:         self._emit(Opcode.POP)

553: 

554:     def visit_LogoutNode(self, node: LogoutNode):

555:         req_idx = self._add_name(node.req_name)

556:         self._emit(Opcode.LOAD_VAR, req_idx)

557:         fn_idx = self._add_name("auth_logout")

558:         self._emit(Opcode.LOAD_VAR, fn_idx)

559:         self._emit(Opcode.CALL_TASK, 1)

560:         self._emit(Opcode.POP)

561: 

562:     def visit_GuardSessionNode(self, node: GuardSessionNode):

563:         fn_idx = self._add_name("auth_guard_session")

564:         self._emit(Opcode.LOAD_VAR, fn_idx)

565:         self._emit(Opcode.CALL_TASK, 0)

566:         self._emit(Opcode.POP)

567:         self._emit(Opcode.POP)

568: 

569:     def visit_UIComponentNode(self, node: UIComponentNode):

570:         if not self.ui_generator:

571:             from ui_generator import UIGenerator

572:             self.ui_generator = UIGenerator(entity_registry=self.entity_registry)

573:         else:

574:             self.ui_generator.entity_registry = self.entity_registry

575:         self.ui_generator.register_component(node)

576: 

577:     def visit_UIPageNode(self, node: UIPageNode):

578:         if not self.ui_generator:

579:             from ui_generator import UIGenerator

580:             self.ui_generator = UIGenerator(entity_registry=self.entity_registry)

581:         else:

582:             self.ui_generator.entity_registry = self.entity_registry

583:         self.ui_generator.generate_page(node)

584: 

585:     def visit_RoleDefNode(self, node):

586:         name_idx = self._add_constant(node.name)

587:         self._emit(Opcode.LOAD_CONST, name_idx)

588:         

589:         fn_idx = self._add_name("db_register_role")

590:         self._emit(Opcode.LOAD_VAR, fn_idx)

591:         self._emit(Opcode.CALL_TASK, 1)

592:         self._emit(Opcode.POP)

593: 

594:     def visit_AllowDefNode(self, node):

595:         role_idx = self._add_constant(node.role)

596:         self._emit(Opcode.LOAD_CONST, role_idx)

597:         

598:         action_idx = self._add_constant(node.action)

599:         self._emit(Opcode.LOAD_CONST, action_idx)

600:         

601:         entity_idx = self._add_constant(node.target_entity)

602:         self._emit(Opcode.LOAD_CONST, entity_idx)

603:         

604:         fn_idx = self._add_name("db_register_permission")

605:         self._emit(Opcode.LOAD_VAR, fn_idx)

606:         self._emit(Opcode.CALL_TASK, 3)

607:         self._emit(Opcode.POP)

608: 

609:     def visit_WorkflowDefNode(self, node):

610:         name_idx = self._add_constant(node.name)

611:         self._emit(Opcode.LOAD_CONST, name_idx)

612:         

613:         entity_idx = self._add_constant(node.entity_name)

614:         self._emit(Opcode.LOAD_CONST, entity_idx)

615:         

616:         # Serialize steps as comma-separated string for MVP

617:         steps_str = ",".join([s.name for s in node.steps])

618:         steps_idx = self._add_constant(steps_str)

619:         self._emit(Opcode.LOAD_CONST, steps_idx)

620:         

621:         fn_idx = self._add_name("db_register_workflow")

622:         self._emit(Opcode.LOAD_VAR, fn_idx)

623:         self._emit(Opcode.CALL_TASK, 3)

624:         self._emit(Opcode.POP)

625: 

626:     def visit_RelationDefNode(self, node):

627:         e1_idx = self._add_constant(node.entity1)

628:         self._emit(Opcode.LOAD_CONST, e1_idx)

629:         

630:         rel_type_idx = self._add_constant(node.rel_type)

631:         self._emit(Opcode.LOAD_CONST, rel_type_idx)

632:         

633:         e2_idx = self._add_constant(node.entity2)

634:         self._emit(Opcode.LOAD_CONST, e2_idx)

635:         

636:         fn_idx = self._add_name("db_register_relation")

637:         self._emit(Opcode.LOAD_VAR, fn_idx)

638:         self._emit(Opcode.CALL_TASK, 3)

639:         self._emit(Opcode.POP)

640: 

641:     def visit_CrudNode(self, node):

642:         from ast_nodes import (

643:             UIPageNode, UIElementNode, TextNode, VariableNode, 

644:             TaskNode, MapDeclarationNode, DeclarationNode, FindEntityNode, SetInMapNode, 

645:             ReturnNode, RenderExpressionNode, RouteNode, FormGetNode, CreateEntityNode

646:         )

647:         entity_name = node.entity_name

648:         page_name = f"{entity_name}Admin"

649:         

650:         # 1. UI Page

651:         page_node = UIPageNode(name=page_name, elements=[

652:             UIElementNode(element_type="dashboard", children=[

653:                 UIElementNode(element_type="sidebar", children=[

654:                     UIElementNode(element_type="text", value=TextNode(f"{entity_name} Management"))

655:                 ]),

656:                 UIElementNode(element_type="column", children=[

657:                     UIElementNode(element_type="navbar"),

658:                     UIElementNode(element_type="row", children=[

659:                         UIElementNode(element_type="table", value=VariableNode(name=entity_name)),

660:                         UIElementNode(element_type="form", value=VariableNode(name=entity_name))

661:                     ])

662:                 ])

663:             ])

664:         ])

665:         self.visit(page_node)

666:         

667:         # 2. GET Route Task

668:         get_task_name = f"__crud_get_{entity_name.lower()}"

669:         get_body = [

670:             MapDeclarationNode(name="context"),

671:             DeclarationNode(var_type="any", name="records", value=FindEntityNode(entity_name=entity_name)),

672:             SetInMapNode(key=TextNode(entity_name), value=VariableNode("records"), map_name="context"),

673:             ReturnNode(value=RenderExpressionNode(template_path=TextNode(page_name + ".html"), context_map_name="context"))

674:         ]

675:         self.visit(TaskNode(name=get_task_name, parameters=["req"], body=get_body))

676:         self.visit(RouteNode(path=TextNode(f"/{entity_name.lower()}s"), handler_name=get_task_name, method="GET"))

677:         

678:         # 3. POST Route Task

679:         post_task_name = f"__crud_post_{entity_name.lower()}"

680:         post_body = [

681:             MapDeclarationNode(name="data")

682:         ]

683:         

684:         if entity_name in self.entity_registry:

685:             for field in self.entity_registry[entity_name]:

686:                 fname = field['name']

687:                 if fname in ['created_at', 'updated_at', 'id']: continue

688:                 post_body.append(DeclarationNode(var_type="any", name=f"val_{fname}", value=FormGetNode(key=TextNode(fname), req_name="req")))

689:                 post_body.append(SetInMapNode(key=TextNode(fname), value=VariableNode(f"val_{fname}"), map_name="data"))

690:                 

691:         post_body.append(CreateEntityNode(entity_name=entity_name, data_map="data"))

692:         

693:         # Re-render

694:         post_body.append(MapDeclarationNode(name="context"))

695:         post_body.append(DeclarationNode(var_type="any", name="records", value=FindEntityNode(entity_name=entity_name)))

696:         post_body.append(SetInMapNode(key=TextNode(entity_name), value=VariableNode("records"), map_name="context"))

697:         post_body.append(ReturnNode(value=RenderExpressionNode(template_path=TextNode(page_name + ".html"), context_map_name="context")))

698:         

699:         self.visit(TaskNode(name=post_task_name, parameters=["req"], body=post_body))

700:         self.visit(RouteNode(path=TextNode(f"/{entity_name.lower()}s/create"), handler_name=post_task_name, method="POST"))

701: 

702:         # 4. PUT Route Task

703:         put_task_name = f"__crud_put_{entity_name.lower()}"

704:         put_body = [

705:             MapDeclarationNode(name="data")

706:         ]

707:         if entity_name in self.entity_registry:

708:             for field in self.entity_registry[entity_name]:

709:                 fname = field['name']

710:                 if fname in ['created_at', 'updated_at', 'id']: continue

711:                 put_body.append(DeclarationNode(var_type="any", name=f"val_{fname}", value=FormGetNode(key=TextNode(fname), req_name="req")))

712:                 put_body.append(SetInMapNode(key=TextNode(fname), value=VariableNode(f"val_{fname}"), map_name="data"))

713:         

714:         put_body.append(DeclarationNode(var_type="any", name="id_val", value=FormGetNode(key=TextNode("id"), req_name="req")))

715:         put_body.append(UpdateEntityNode(entity_name=entity_name, condition_field="id", condition_value=VariableNode("id_val"), data_map="data"))

716:         

717:         put_body.append(MapDeclarationNode(name="context"))

718:         put_body.append(DeclarationNode(var_type="any", name="records", value=FindEntityNode(entity_name=entity_name)))

719:         put_body.append(SetInMapNode(key=TextNode(entity_name), value=VariableNode("records"), map_name="context"))

720:         put_body.append(ReturnNode(value=RenderExpressionNode(template_path=TextNode(page_name + ".html"), context_map_name="context")))

721:         

722:         self.visit(TaskNode(name=put_task_name, parameters=["req"], body=put_body))

723:         self.visit(RouteNode(path=TextNode(f"/{entity_name.lower()}s/update"), handler_name=put_task_name, method="PUT"))

724: 

725:         # 5. DELETE Route Task

726:         del_task_name = f"__crud_delete_{entity_name.lower()}"

727:         del_body = []

728:         del_body.append(DeclarationNode(var_type="any", name="id_val", value=FormGetNode(key=TextNode("id"), req_name="req")))

729:         del_body.append(DeleteEntityNode(entity_name=entity_name, condition_field="id", condition_value=VariableNode("id_val")))

730:         

731:         del_body.append(MapDeclarationNode(name="context"))

732:         del_body.append(DeclarationNode(var_type="any", name="records", value=FindEntityNode(entity_name=entity_name)))

733:         del_body.append(SetInMapNode(key=TextNode(entity_name), value=VariableNode("records"), map_name="context"))

734:         del_body.append(ReturnNode(value=RenderExpressionNode(template_path=TextNode(page_name + ".html"), context_map_name="context")))

735:         

736:         self.visit(TaskNode(name=del_task_name, parameters=["req"], body=del_body))

737:         self.visit(RouteNode(path=TextNode(f"/{entity_name.lower()}s/delete"), handler_name=del_task_name, method="DELETE"))

738: 

739: 

740: if __name__ == "__main__":

741:     from lexer import Lexer

742:     from parser import Parser

743:     code = '''

744:     text name is "Ayush".

745:     show name.

746:     '''

747:     lexer = Lexer(code)

748:     parser = Parser(lexer.tokenize())

749:     ast = parser.parse()

750:     

751:     compiler = AAYUCompiler()

752:     bytecode = compiler.compile(ast)

753:     

754:     print(bytecode.format())

755: 
The above content shows the entire, complete file contents of the requested file.
