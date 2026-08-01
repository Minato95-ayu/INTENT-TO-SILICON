#include "gc.h"
#include "visitor.h"
#include "manager.h"
#include "allocator.h"
#include <stdlib.h>
#include <stdio.h>

static GrayStack gray_stack;

#define FLAG_IS_MARKED 1

void aayu_gc_init(void) {
    gray_stack.count = 0;
    gray_stack.capacity = 1024;
    gray_stack.objects = (AayuObject**)aayu_persistent_alloc(sizeof(AayuObject*) * gray_stack.capacity);
    aayu_visitor_init();
}

void aayu_gc_destroy(void) {
    if (gray_stack.objects) {
        aayu_persistent_free(gray_stack.objects);
        gray_stack.objects = NULL;
    }
    gray_stack.count = 0;
    gray_stack.capacity = 0;
}

static void push_gray(AayuObject* obj, AayuVisitor* visitor) {
    if (!obj) return;
    
    if (!is_heap_object(obj)) return; // Ignore persistent/constant pool memory
    
    // If already marked, ignore
    if (obj->flags & FLAG_IS_MARKED) return;
    
    // Mark it
    obj->flags |= FLAG_IS_MARKED;
    
    // Push to gray stack
    if (gray_stack.count >= gray_stack.capacity) {
        gray_stack.capacity *= 2;
        gray_stack.objects = (AayuObject**)realloc(gray_stack.objects, sizeof(AayuObject*) * gray_stack.capacity);
    }
    
    gray_stack.objects[gray_stack.count++] = obj;
}

static void mark_roots(VM* vm, AayuVisitor* visitor) {
    // 1. VM Stack
    for (int i = 0; i < vm->sp; i++) {
        int type = vm->stack[i].type;
        if (type == TYPE_ARRAY || type == TYPE_DICT) {
            push_gray(vm->stack[i].value.obj, visitor);
        } else if (type == TYPE_STRING) {
            if (vm->stack[i].value.s_val) {
                AayuRawBuffer* buf = (AayuRawBuffer*)((uint8_t*)vm->stack[i].value.s_val - offsetof(AayuRawBuffer, data));
                push_gray((AayuObject*)buf, visitor);
            }
        }
    }
    
    // 2. Call Frames (for future closures)
    // 3. Globals
    for (int i = 0; i < STATE_MAX; i++) {
        int type = vm->state[i].type;
        if (type == TYPE_ARRAY || type == TYPE_DICT) {
            push_gray(vm->state[i].value.obj, visitor);
        } else if (type == TYPE_STRING) {
            if (vm->state[i].value.s_val) {
                AayuRawBuffer* buf = (AayuRawBuffer*)((uint8_t*)vm->state[i].value.s_val - offsetof(AayuRawBuffer, data));
                push_gray((AayuObject*)buf, visitor);
            }
        }
    }
    
    // 4. Modules (TODO)
    // 5. Native Handles (TODO)
    // 6. Runtime Constants (String constants point to persistent pool, not heap)
}

static void trace_references(AayuVisitor* visitor) {
    while (gray_stack.count > 0) {
        AayuObject* obj = gray_stack.objects[--gray_stack.count];
        aayu_visit_children(obj, visitor);
    }
}

static void sweep(void) {
    AayuObject** object = &gc_objects;
    while (*object != NULL) {
        if (!((*object)->flags & FLAG_IS_MARKED)) {
            // Unmarked object: Unlink and Destroy
            AayuObject* unreached = *object;
            *object = unreached->next;
            
            aayu_destroy_object(unreached);
            memory_stats.live_objects--;
            
            // Push into Free Lists for O(1) reuse!
            aayu_free_object(unreached);
        } else {
            // Unmark for next GC cycle
            (*object)->flags &= ~FLAG_IS_MARKED;
            object = &(*object)->next;
        }
    }
}

void aayu_gc_collect(VM* vm) {
    if (!vm) return;
    
    AayuVisitor visitor;
    visitor.context = NULL;
    visitor.visit_child = push_gray;
    
    mark_roots(vm, &visitor);
    trace_references(&visitor);
    sweep();
}
