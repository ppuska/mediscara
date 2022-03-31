// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from interfaces:msg/VisionControl.idl
// generated code does not contain a copyright notice

#ifndef INTERFACES__MSG__DETAIL__VISION_CONTROL__STRUCT_H_
#define INTERFACES__MSG__DETAIL__VISION_CONTROL__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

// Struct defined in msg/VisionControl in the package interfaces.
typedef struct interfaces__msg__VisionControl
{
  bool home;
  bool measure_pcb;
  bool measure_label;
} interfaces__msg__VisionControl;

// Struct for a sequence of interfaces__msg__VisionControl.
typedef struct interfaces__msg__VisionControl__Sequence
{
  interfaces__msg__VisionControl * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} interfaces__msg__VisionControl__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // INTERFACES__MSG__DETAIL__VISION_CONTROL__STRUCT_H_
