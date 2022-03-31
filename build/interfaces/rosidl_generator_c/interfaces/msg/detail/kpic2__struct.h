// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from interfaces:msg/KPIC2.idl
// generated code does not contain a copyright notice

#ifndef INTERFACES__MSG__DETAIL__KPIC2__STRUCT_H_
#define INTERFACES__MSG__DETAIL__KPIC2__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

// Struct defined in msg/KPIC2 in the package interfaces.
typedef struct interfaces__msg__KPIC2
{
  double availability;
  double performance;
  double quality;
} interfaces__msg__KPIC2;

// Struct for a sequence of interfaces__msg__KPIC2.
typedef struct interfaces__msg__KPIC2__Sequence
{
  interfaces__msg__KPIC2 * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} interfaces__msg__KPIC2__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // INTERFACES__MSG__DETAIL__KPIC2__STRUCT_H_
