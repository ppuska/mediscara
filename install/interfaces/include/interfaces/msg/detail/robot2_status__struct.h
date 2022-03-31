// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from interfaces:msg/Robot2Status.idl
// generated code does not contain a copyright notice

#ifndef INTERFACES__MSG__DETAIL__ROBOT2_STATUS__STRUCT_H_
#define INTERFACES__MSG__DETAIL__ROBOT2_STATUS__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

// Struct defined in msg/Robot2Status in the package interfaces.
typedef struct interfaces__msg__Robot2Status
{
  bool power;
  bool running;
  bool waiting;
  bool error;
} interfaces__msg__Robot2Status;

// Struct for a sequence of interfaces__msg__Robot2Status.
typedef struct interfaces__msg__Robot2Status__Sequence
{
  interfaces__msg__Robot2Status * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} interfaces__msg__Robot2Status__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // INTERFACES__MSG__DETAIL__ROBOT2_STATUS__STRUCT_H_
