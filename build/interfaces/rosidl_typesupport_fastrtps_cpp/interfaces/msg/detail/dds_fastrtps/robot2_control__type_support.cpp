// generated from rosidl_typesupport_fastrtps_cpp/resource/idl__type_support.cpp.em
// with input from interfaces:msg/Robot2Control.idl
// generated code does not contain a copyright notice
#include "interfaces/msg/detail/robot2_control__rosidl_typesupport_fastrtps_cpp.hpp"
#include "interfaces/msg/detail/robot2_control__struct.hpp"

#include <limits>
#include <stdexcept>
#include <string>
#include "rosidl_typesupport_cpp/message_type_support.hpp"
#include "rosidl_typesupport_fastrtps_cpp/identifier.hpp"
#include "rosidl_typesupport_fastrtps_cpp/message_type_support.h"
#include "rosidl_typesupport_fastrtps_cpp/message_type_support_decl.hpp"
#include "rosidl_typesupport_fastrtps_cpp/wstring_conversion.hpp"
#include "fastcdr/Cdr.h"


// forward declaration of message dependencies and their conversion functions

namespace interfaces
{

namespace msg
{

namespace typesupport_fastrtps_cpp
{

bool
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_interfaces
cdr_serialize(
  const interfaces::msg::Robot2Control & ros_message,
  eprosima::fastcdr::Cdr & cdr)
{
  // Member: home
  cdr << (ros_message.home ? true : false);
  // Member: start_marking
  cdr << (ros_message.start_marking ? true : false);
  return true;
}

bool
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_interfaces
cdr_deserialize(
  eprosima::fastcdr::Cdr & cdr,
  interfaces::msg::Robot2Control & ros_message)
{
  // Member: home
  {
    uint8_t tmp;
    cdr >> tmp;
    ros_message.home = tmp ? true : false;
  }

  // Member: start_marking
  {
    uint8_t tmp;
    cdr >> tmp;
    ros_message.start_marking = tmp ? true : false;
  }

  return true;
}

size_t
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_interfaces
get_serialized_size(
  const interfaces::msg::Robot2Control & ros_message,
  size_t current_alignment)
{
  size_t initial_alignment = current_alignment;

  const size_t padding = 4;
  const size_t wchar_size = 4;
  (void)padding;
  (void)wchar_size;

  // Member: home
  {
    size_t item_size = sizeof(ros_message.home);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }
  // Member: start_marking
  {
    size_t item_size = sizeof(ros_message.start_marking);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }

  return current_alignment - initial_alignment;
}

size_t
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_interfaces
max_serialized_size_Robot2Control(
  bool & full_bounded,
  size_t current_alignment)
{
  size_t initial_alignment = current_alignment;

  const size_t padding = 4;
  const size_t wchar_size = 4;
  (void)padding;
  (void)wchar_size;
  (void)full_bounded;


  // Member: home
  {
    size_t array_size = 1;

    current_alignment += array_size * sizeof(uint8_t);
  }

  // Member: start_marking
  {
    size_t array_size = 1;

    current_alignment += array_size * sizeof(uint8_t);
  }

  return current_alignment - initial_alignment;
}

static bool _Robot2Control__cdr_serialize(
  const void * untyped_ros_message,
  eprosima::fastcdr::Cdr & cdr)
{
  auto typed_message =
    static_cast<const interfaces::msg::Robot2Control *>(
    untyped_ros_message);
  return cdr_serialize(*typed_message, cdr);
}

static bool _Robot2Control__cdr_deserialize(
  eprosima::fastcdr::Cdr & cdr,
  void * untyped_ros_message)
{
  auto typed_message =
    static_cast<interfaces::msg::Robot2Control *>(
    untyped_ros_message);
  return cdr_deserialize(cdr, *typed_message);
}

static uint32_t _Robot2Control__get_serialized_size(
  const void * untyped_ros_message)
{
  auto typed_message =
    static_cast<const interfaces::msg::Robot2Control *>(
    untyped_ros_message);
  return static_cast<uint32_t>(get_serialized_size(*typed_message, 0));
}

static size_t _Robot2Control__max_serialized_size(bool & full_bounded)
{
  return max_serialized_size_Robot2Control(full_bounded, 0);
}

static message_type_support_callbacks_t _Robot2Control__callbacks = {
  "interfaces::msg",
  "Robot2Control",
  _Robot2Control__cdr_serialize,
  _Robot2Control__cdr_deserialize,
  _Robot2Control__get_serialized_size,
  _Robot2Control__max_serialized_size
};

static rosidl_message_type_support_t _Robot2Control__handle = {
  rosidl_typesupport_fastrtps_cpp::typesupport_identifier,
  &_Robot2Control__callbacks,
  get_message_typesupport_handle_function,
};

}  // namespace typesupport_fastrtps_cpp

}  // namespace msg

}  // namespace interfaces

namespace rosidl_typesupport_fastrtps_cpp
{

template<>
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_EXPORT_interfaces
const rosidl_message_type_support_t *
get_message_type_support_handle<interfaces::msg::Robot2Control>()
{
  return &interfaces::msg::typesupport_fastrtps_cpp::_Robot2Control__handle;
}

}  // namespace rosidl_typesupport_fastrtps_cpp

#ifdef __cplusplus
extern "C"
{
#endif

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, interfaces, msg, Robot2Control)() {
  return &interfaces::msg::typesupport_fastrtps_cpp::_Robot2Control__handle;
}

#ifdef __cplusplus
}
#endif
