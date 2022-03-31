// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from interfaces:msg/Error.idl
// generated code does not contain a copyright notice

#ifndef INTERFACES__MSG__DETAIL__ERROR__STRUCT_H_
#define INTERFACES__MSG__DETAIL__ERROR__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

// Include directives for member types
// Member 'node_name'
// Member 'error_msg'
#include "rosidl_runtime_c/string.h"

// Struct defined in msg/Error in the package interfaces.
typedef struct interfaces__msg__Error
{
  rosidl_runtime_c__String node_name;
  int64_t error_code;
  rosidl_runtime_c__String error_msg;
} interfaces__msg__Error;

// Struct for a sequence of interfaces__msg__Error.
typedef struct interfaces__msg__Error__Sequence
{
  interfaces__msg__Error * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} interfaces__msg__Error__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // INTERFACES__MSG__DETAIL__ERROR__STRUCT_H_
