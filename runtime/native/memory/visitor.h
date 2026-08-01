#ifndef AAYU_VISITOR_H
#define AAYU_VISITOR_H

#include "object.h"

// Forward declaration
struct sVisitor;

typedef void (*AayuVisitCallback)(struct sAayuObject* child, struct sVisitor* visitor);
typedef void (*AayuDestroyCallback)(struct sAayuObject* obj);

typedef struct sVisitor {
    void* context;
    AayuVisitCallback visit_child; // Function to call for each child object found
} AayuVisitor;

typedef struct {
    AayuVisitCallback visit_children;
    AayuDestroyCallback destroy;
} AayuTypeInfo;

#define MAX_OBJECT_TYPES 64
extern AayuTypeInfo aayu_type_registry[MAX_OBJECT_TYPES];

// Register type handlers (called during VM initialization)
void aayu_visitor_init(void);

// Core dispatch function for any object
void aayu_visit_children(struct sAayuObject* obj, AayuVisitor* visitor);
void aayu_destroy_object(struct sAayuObject* obj);

#endif // AAYU_VISITOR_H
