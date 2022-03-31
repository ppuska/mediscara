// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from interfaces:msg/Robot2Control.idl
// generated code does not contain a copyright notice

#ifndef INTERFACES__MSG__DETAIL__ROBOT2_CONTROL__STRUCT_H_
#define INTERFACES__MSG__DETAIL__ROBOT2_CONTROL__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

// Struct defined in msg/Robot2Control in the package interfaces.
typedef struct interfaces__msg__Robot2Control
{
  bool home;
  bool start_marking;
} interfaces__msg__Robot2Control;

// Struct for a sequence of interfaces__msg__Robot2Control.
typedef struct interfaces__msg__Robot2Control__Sequence
{
  interfaces__msg__Robot2Control * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} interfaces__msg__Robot2Control__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // INTERFACES__MSG__DETAIL__ROBOT2_CONTROL__STRUCT_H_
