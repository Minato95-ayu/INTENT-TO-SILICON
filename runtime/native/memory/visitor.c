#include "../vm.h"
#include "visitor.h"
#include <stddef.h>

AayuTypeInfo aayu_type_registry[MAX_OBJECT_TYPES];

static void visit_string(AayuObject* obj, AayuVisitor* visitor) {
    // Strings have no children
    (void)obj;
    (void)visitor;
}

static void visit_array(AayuObject* obj, AayuVisitor* visitor) {
    AayuArray* arr = (AayuArray*)obj;
    if (arr->elements) {
        AayuRawBuffer* buf = (AayuRawBuffer*)((uint8_t*)arr->elements - offsetof(AayuRawBuffer, data));
        visitor->visit_child((AayuObject*)buf, visitor);
    }
    for (uint32_t i = 0; i < arr->count; i++) {
        // If element is a heap object, visit it
        int type = arr->elements[i].type;
        if (type == TYPE_ARRAY || type == TYPE_DICT) {
            if (arr->elements[i].value.obj) {
                visitor->visit_child(arr->elements[i].value.obj, visitor);
            }
        } else if (type == TYPE_STRING) {
            if (arr->elements[i].value.s_val) {
                AayuRawBuffer* str_buf = (AayuRawBuffer*)((uint8_t*)arr->elements[i].value.s_val - offsetof(AayuRawBuffer, data));
                visitor->visit_child((AayuObject*)str_buf, visitor);
            }
        }
    }
}

static void visit_dict(AayuObject* obj, AayuVisitor* visitor) {
    AayuDict* dict = (AayuDict*)obj;
    if (dict->entries) {
        AayuRawBuffer* buf = (AayuRawBuffer*)((uint8_t*)dict->entries - offsetof(AayuRawBuffer, data));
        visitor->visit_child((AayuObject*)buf, visitor);
    }
    for (uint32_t i = 0; i < dict->count; i++) {
        if (dict->entries[i].key) {
            AayuRawBuffer* key_buf = (AayuRawBuffer*)((uint8_t*)dict->entries[i].key - offsetof(AayuRawBuffer, data));
            visitor->visit_child((AayuObject*)key_buf, visitor);
        }
        
        int type = dict->entries[i].value.type;
        if (type == TYPE_ARRAY || type == TYPE_DICT) {
            if (dict->entries[i].value.value.obj) {
                visitor->visit_child(dict->entries[i].value.value.obj, visitor);
            }
        } else if (type == TYPE_STRING) {
            if (dict->entries[i].value.value.s_val) {
                AayuRawBuffer* str_buf = (AayuRawBuffer*)((uint8_t*)dict->entries[i].value.value.s_val - offsetof(AayuRawBuffer, data));
                visitor->visit_child((AayuObject*)str_buf, visitor);
            }
        }
    }
}

static void destroy_string(AayuObject* obj) {
    AayuString* str = (AayuString*)obj;
    if (str->chars) {
        // Assume chars are allocated using aayu_alloc_raw or malloc. 
        // We will leave it to Phase 11B.7 Free Lists to actually free memory pages.
        // For now, if they were malloc'd, we free them. But Aayu string chars are allocated via aayu_alloc_raw.
        // So we do nothing to the raw memory in this phase.
    }
}

static void destroy_array(AayuObject* obj) {
    // Array elements are allocated via aayu_alloc_raw
}

static void destroy_dict(AayuObject* obj) {
    // Dict entries are allocated via aayu_alloc_raw
}

static void destroy_native_handle(AayuObject* obj) {
    AayuNativeHandle* handle = (AayuNativeHandle*)obj;
    if (handle->dtor && handle->handle) {
        handle->dtor(handle->handle);
        handle->handle = NULL;
    }
}

static void visit_native_handle(AayuObject* obj, AayuVisitor* visitor) {
    // Native Handles might have attached resources, but initially no AayuObject* children
    (void)obj;
    (void)visitor;
}

void aayu_visitor_init(void) {
    for (int i = 0; i < MAX_OBJECT_TYPES; i++) {
        aayu_type_registry[i].visit_children = NULL;
        aayu_type_registry[i].destroy = NULL;
    }
    
    aayu_type_registry[OBJ_STRING].visit_children = visit_string;
    aayu_type_registry[OBJ_STRING].destroy = destroy_string;
    
    aayu_type_registry[OBJ_ARRAY].visit_children = visit_array;
    aayu_type_registry[OBJ_ARRAY].destroy = destroy_array;
    
    aayu_type_registry[OBJ_DICT].visit_children = visit_dict;
    aayu_type_registry[OBJ_DICT].destroy = destroy_dict;
    
    aayu_type_registry[OBJ_NATIVE_HANDLE].visit_children = visit_native_handle;
    aayu_type_registry[OBJ_NATIVE_HANDLE].destroy = destroy_native_handle;
}

void aayu_visit_children(AayuObject* obj, AayuVisitor* visitor) {
    if (!obj || !visitor) return;
    
    if (obj->type < MAX_OBJECT_TYPES && aayu_type_registry[obj->type].visit_children) {
        aayu_type_registry[obj->type].visit_children(obj, visitor);
    }
}

void aayu_destroy_object(AayuObject* obj) {
    if (!obj) return;
    if (obj->type < MAX_OBJECT_TYPES && aayu_type_registry[obj->type].destroy) {
        aayu_type_registry[obj->type].destroy(obj);
    }
}
