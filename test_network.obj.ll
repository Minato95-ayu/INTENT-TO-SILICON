; ModuleID = 'aayu_module'
source_filename = "aayu_module"

@.str.1497247687696 = private unnamed_addr constant [10 x i8] c"127.0.0.1\00", align 1
@.str.1497247688144 = private unnamed_addr constant [10 x i8] c"localhost\00", align 1
@.str.1497247688784 = private unnamed_addr constant [10 x i8] c"127.0.0.1\00", align 1
declare ptr @aayu_ping(...)

declare ptr @aayu_dns_resolve(...)

declare ptr @aayu_tcp_connect(...)

define i32 @main() {
entry_1:
  %v1497247687632 = call ptr @aayu_ping(ptr @.str.1497247687696)
  %v1497247688080 = call ptr @aayu_dns_resolve(ptr @.str.1497247688144)
  %v1497247688720 = call ptr @aayu_tcp_connect(ptr @.str.1497247688784, i32 80)
  ret i32 0
}
