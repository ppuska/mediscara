// generated from rosidl_typesupport_fastrtps_c/resource/idl__type_support_c.cpp.em
// with input from interfaces:msg/Robot2Control.idl
// generated code does not contain a copyright notice
#include "interfaces/msg/detail/robot2_control__rosidl_typesupport_fastrtps_c.h"


#include <cassert>
#include <limits>
#include <string>
#include "rosidl_typesupport_fastrtps_c/identifier.h"
#include "rosidl_typesupport_fastrtps_c/wstring_conversion.hpp"
#include "rosidl_typesupport_fastrtps_cpp/message_type_support.h"
#include "interfaces/msg/rosidl_typesupport_fastrtps_c__visibility_control.h"
#include "interfaces/msg/detail/robot2_control__struct.h"
#include "interfaces/msg/detail/robot2_control__functions.h"
#include "fastcdr/Cdr.h"

#ifndef _WIN32
# pragma GCC diagnostic push
# pragma GCC diagnostic ignored "-Wunused-parameter"
# ifdef __clang__
#  pragma clang diagnostic ignored "-Wdeprecated-register"
#  pragma clang diagnostic ignored "-Wreturn-type-c-linkage"
# endif
#endif
#ifndef _WIN32
# pragma GCC diagnostic pop
#endif

// includes and forward declarations of message dependencies and their conversion functions

#if defined(__cplusplus)
extern "C"
{
#endif


// forward declare type support functions


using _Robot2Control__ros_msg_type = interfaces__msg__Robot2Control;

static bool _Robot2Control__cdr_serialize(
  const void * untyped_ros_message,
  eprosima::fastcdr::Cdr & cdr)
{
  if (!untyped_ros_message) {
    fprintf(stderr, "ros message handle is null\n");
    return false;
  }
  const _Robot2Control__ros_msg_type * ros_message = static_cast<const _Robot2Control__ros_msg_type *>(untyped_ros_message);
  // Field name: home
  {
    cdr << (ros_message->home ? true : false);
  }

  // Field name: start_marking
  {
    cdr << (ros_message->start_marking ? true : false);
  }

  return true;
}

static bool _Robot2Control__cdr_deserialize(
  eprosima::fastcdr::Cdr & cdr,
  void * untyped_ros_message)
{
  if (!untyped_ros_message) {
    fprintf(stderr, "ros message handle is null\n");
    return false;
  }
  _Robot2Control__ros_msg_type * ros_message = static_cast<_Robot2Control__ros_msg_type *>(untyped_ros_message);
  // Field name: home
  {
    uint8_t tmp;
    cdr >> tmp;
    ros_message->home = tmp ? true : false;
  }

  // Field name: start_marking
  {
    uint8_t tmp;
    cdr >> tmp;
    ros_message->start_marking = tmp ? true : false;
  }

  return true;
}

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_interfaces
size_t get_serialized_size_interfaces__msg__Robot2Control(
  const void * untyped_ros_message,
  size_t current_alignment)
{
  const _Robot2Control__ros_msg_type * ros_message = static_cast<const _Robot2Control__ros_msg_type *>(untyped_ros_message);
  (void)ros_message;
  size_t initial_alignment = current_alignment;

  const size_t padding = 4;
  const size_t wchar_size = 4;
  (void)padding;
  (void)wchar_size;

  // field.name home
  {
    size_t item_size = sizeof(ros_message->home);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }
  // field.name start_marking
  {
    size_t item_size = sizeof(ros_message->start_marking);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }

  return current_alignment - initial_alignment;
}

static uint32_t _Robot2Control__get_serialized_size(const void * untyped_ros_message)
{
  return static_cast<uint32_t>(
    get_serialized_size_interfaces__msg__Robot2Control(
      untyped_ros_message, 0));
}

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_interfaces
size_t max_serialized_size_interfaces__msg__Robot2Control(
  bool & full_bounded,
  size_t current_alignment)
{
  size_t initial_alignment = current_alignment;

  const size_t padding = 4;
  const size_t wchar_size = 4;
  (void)padding;
  (void)wchar_size;
  (void)full_bounded;

  // member: home
  {
    size_t array_size = 1;

    current_alignment += array_size * sizeof(uint8_t);
  }
  // member: start_marking
  {
    size_t array_size = 1;

    current_alignment += array_size * sizeof(uint8_t);
  }

  return current_alignment - initial_alignment;
}

static size_t _Robot2Control__max_serialized_size(bool & full_bounded)
{
  return max_serialized_size_interfaces__msg__Robot2Control(
    full_bounded, 0);
}


static message_type_support_callbacks_t __callbacks_Robot2Control = {
  "interfaces::msg",
  "Robot2Control",
  _Robot2Control__cdr_serialize,
  _Robot2Control__cdr_deserialize,
  _Robot2Control__get_serialized_size,
  _Robot2Control__max_serialized_size
};

static rosidl_message_type_support_t _Robot2Control__type_support = {
  rosidl_typesupport_fastrtps_c__identifier,
  &__callbacks_Robot2Control,
  get_message_typesupport_handle_function,
};

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, interfaces, msg, Robot2Control)() {
  return &_Robot2Control__type_support;
}

#if defined(__cplusplus)
}
#endif
