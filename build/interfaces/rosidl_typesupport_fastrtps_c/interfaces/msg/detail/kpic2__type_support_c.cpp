// generated from rosidl_typesupport_fastrtps_c/resource/idl__type_support_c.cpp.em
// with input from interfaces:msg/KPIC2.idl
// generated code does not contain a copyright notice
#include "interfaces/msg/detail/kpic2__rosidl_typesupport_fastrtps_c.h"


#include <cassert>
#include <limits>
#include <string>
#include "rosidl_typesupport_fastrtps_c/identifier.h"
#include "rosidl_typesupport_fastrtps_c/wstring_conversion.hpp"
#include "rosidl_typesupport_fastrtps_cpp/message_type_support.h"
#include "interfaces/msg/rosidl_typesupport_fastrtps_c__visibility_control.h"
#include "interfaces/msg/detail/kpic2__struct.h"
#include "interfaces/msg/detail/kpic2__functions.h"
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


using _KPIC2__ros_msg_type = interfaces__msg__KPIC2;

static bool _KPIC2__cdr_serialize(
  const void * untyped_ros_message,
  eprosima::fastcdr::Cdr & cdr)
{
  if (!untyped_ros_message) {
    fprintf(stderr, "ros message handle is null\n");
    return false;
  }
  const _KPIC2__ros_msg_type * ros_message = static_cast<const _KPIC2__ros_msg_type *>(untyped_ros_message);
  // Field name: availability
  {
    cdr << ros_message->availability;
  }

  // Field name: performance
  {
    cdr << ros_message->performance;
  }

  // Field name: quality
  {
    cdr << ros_message->quality;
  }

  return true;
}

static bool _KPIC2__cdr_deserialize(
  eprosima::fastcdr::Cdr & cdr,
  void * untyped_ros_message)
{
  if (!untyped_ros_message) {
    fprintf(stderr, "ros message handle is null\n");
    return false;
  }
  _KPIC2__ros_msg_type * ros_message = static_cast<_KPIC2__ros_msg_type *>(untyped_ros_message);
  // Field name: availability
  {
    cdr >> ros_message->availability;
  }

  // Field name: performance
  {
    cdr >> ros_message->performance;
  }

  // Field name: quality
  {
    cdr >> ros_message->quality;
  }

  return true;
}

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_interfaces
size_t get_serialized_size_interfaces__msg__KPIC2(
  const void * untyped_ros_message,
  size_t current_alignment)
{
  const _KPIC2__ros_msg_type * ros_message = static_cast<const _KPIC2__ros_msg_type *>(untyped_ros_message);
  (void)ros_message;
  size_t initial_alignment = current_alignment;

  const size_t padding = 4;
  const size_t wchar_size = 4;
  (void)padding;
  (void)wchar_size;

  // field.name availability
  {
    size_t item_size = sizeof(ros_message->availability);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }
  // field.name performance
  {
    size_t item_size = sizeof(ros_message->performance);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }
  // field.name quality
  {
    size_t item_size = sizeof(ros_message->quality);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }

  return current_alignment - initial_alignment;
}

static uint32_t _KPIC2__get_serialized_size(const void * untyped_ros_message)
{
  return static_cast<uint32_t>(
    get_serialized_size_interfaces__msg__KPIC2(
      untyped_ros_message, 0));
}

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_interfaces
size_t max_serialized_size_interfaces__msg__KPIC2(
  bool & full_bounded,
  size_t current_alignment)
{
  size_t initial_alignment = current_alignment;

  const size_t padding = 4;
  const size_t wchar_size = 4;
  (void)padding;
  (void)wchar_size;
  (void)full_bounded;

  // member: availability
  {
    size_t array_size = 1;

    current_alignment += array_size * sizeof(uint64_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint64_t));
  }
  // member: performance
  {
    size_t array_size = 1;

    current_alignment += array_size * sizeof(uint64_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint64_t));
  }
  // member: quality
  {
    size_t array_size = 1;

    current_alignment += array_size * sizeof(uint64_t) +
      eprosima::fastcdr::Cdr::alignment(current_alignment, sizeof(uint64_t));
  }

  return current_alignment - initial_alignment;
}

static size_t _KPIC2__max_serialized_size(bool & full_bounded)
{
  return max_serialized_size_interfaces__msg__KPIC2(
    full_bounded, 0);
}


static message_type_support_callbacks_t __callbacks_KPIC2 = {
  "interfaces::msg",
  "KPIC2",
  _KPIC2__cdr_serialize,
  _KPIC2__cdr_deserialize,
  _KPIC2__get_serialized_size,
  _KPIC2__max_serialized_size
};

static rosidl_message_type_support_t _KPIC2__type_support = {
  rosidl_typesupport_fastrtps_c__identifier,
  &__callbacks_KPIC2,
  get_message_typesupport_handle_function,
};

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, interfaces, msg, KPIC2)() {
  return &_KPIC2__type_support;
}

#if defined(__cplusplus)
}
#endif
