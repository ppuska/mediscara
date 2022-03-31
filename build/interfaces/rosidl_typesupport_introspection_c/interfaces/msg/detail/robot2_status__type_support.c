// generated from rosidl_typesupport_introspection_c/resource/idl__type_support.c.em
// with input from interfaces:msg/Robot2Status.idl
// generated code does not contain a copyright notice

#include <stddef.h>
#include "interfaces/msg/detail/robot2_status__rosidl_typesupport_introspection_c.h"
#include "interfaces/msg/rosidl_typesupport_introspection_c__visibility_control.h"
#include "rosidl_typesupport_introspection_c/field_types.h"
#include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/message_introspection.h"
#include "interfaces/msg/detail/robot2_status__functions.h"
#include "interfaces/msg/detail/robot2_status__struct.h"


#ifdef __cplusplus
extern "C"
{
#endif

void Robot2Status__rosidl_typesupport_introspection_c__Robot2Status_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  interfaces__msg__Robot2Status__init(message_memory);
}

void Robot2Status__rosidl_typesupport_introspection_c__Robot2Status_fini_function(void * message_memory)
{
  interfaces__msg__Robot2Status__fini(message_memory);
}

static rosidl_typesupport_introspection_c__MessageMember Robot2Status__rosidl_typesupport_introspection_c__Robot2Status_message_member_array[4] = {
  {
    "power",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_BOOLEAN,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(interfaces__msg__Robot2Status, power),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "running",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_BOOLEAN,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(interfaces__msg__Robot2Status, running),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "waiting",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_BOOLEAN,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(interfaces__msg__Robot2Status, waiting),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "error",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_BOOLEAN,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(interfaces__msg__Robot2Status, error),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers Robot2Status__rosidl_typesupport_introspection_c__Robot2Status_message_members = {
  "interfaces__msg",  // message namespace
  "Robot2Status",  // message name
  4,  // number of fields
  sizeof(interfaces__msg__Robot2Status),
  Robot2Status__rosidl_typesupport_introspection_c__Robot2Status_message_member_array,  // message members
  Robot2Status__rosidl_typesupport_introspection_c__Robot2Status_init_function,  // function to initialize message memory (memory has to be allocated)
  Robot2Status__rosidl_typesupport_introspection_c__Robot2Status_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t Robot2Status__rosidl_typesupport_introspection_c__Robot2Status_message_type_support_handle = {
  0,
  &Robot2Status__rosidl_typesupport_introspection_c__Robot2Status_message_members,
  get_message_typesupport_handle_function,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_interfaces
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, interfaces, msg, Robot2Status)() {
  if (!Robot2Status__rosidl_typesupport_introspection_c__Robot2Status_message_type_support_handle.typesupport_identifier) {
    Robot2Status__rosidl_typesupport_introspection_c__Robot2Status_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &Robot2Status__rosidl_typesupport_introspection_c__Robot2Status_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif
