// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from interfaces:msg/MarkerStatus.idl
// generated code does not contain a copyright notice

#ifndef INTERFACES__MSG__DETAIL__MARKER_STATUS__STRUCT_H_
#define INTERFACES__MSG__DETAIL__MARKER_STATUS__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

// Struct defined in msg/MarkerStatus in the package interfaces.
typedef struct interfaces__msg__MarkerStatus
{
  bool marking_successful;
  double marking_duration;
} interfaces__msg__MarkerStatus;

// Struct for a sequence of interfaces__msg__MarkerStatus.
typedef struct interfaces__msg__MarkerStatus__Sequence
{
  interfaces__msg__MarkerStatus * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} interfaces__msg__MarkerStatus__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // INTERFACES__MSG__DETAIL__MARKER_STATUS__STRUCT_H_
