// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from interfaces:msg/Error.idl
// generated code does not contain a copyright notice

#ifndef INTERFACES__MSG__DETAIL__ERROR__BUILDER_HPP_
#define INTERFACES__MSG__DETAIL__ERROR__BUILDER_HPP_

#include "interfaces/msg/detail/error__struct.hpp"
#include <rosidl_runtime_cpp/message_initialization.hpp>
#include <algorithm>
#include <utility>


namespace interfaces
{

namespace msg
{

namespace builder
{

class Init_Error_error_msg
{
public:
  explicit Init_Error_error_msg(::interfaces::msg::Error & msg)
  : msg_(msg)
  {}
  ::interfaces::msg::Error error_msg(::interfaces::msg::Error::_error_msg_type arg)
  {
    msg_.error_msg = std::move(arg);
    return std::move(msg_);
  }

private:
  ::interfaces::msg::Error msg_;
};

class Init_Error_error_code
{
public:
  explicit Init_Error_error_code(::interfaces::msg::Error & msg)
  : msg_(msg)
  {}
  Init_Error_error_msg error_code(::interfaces::msg::Error::_error_code_type arg)
  {
    msg_.error_code = std::move(arg);
    return Init_Error_error_msg(msg_);
  }

private:
  ::interfaces::msg::Error msg_;
};

class Init_Error_node_name
{
public:
  Init_Error_node_name()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_Error_error_code node_name(::interfaces::msg::Error::_node_name_type arg)
  {
    msg_.node_name = std::move(arg);
    return Init_Error_error_code(msg_);
  }

private:
  ::interfaces::msg::Error msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::interfaces::msg::Error>()
{
  return interfaces::msg::builder::Init_Error_node_name();
}

}  // namespace interfaces

#endif  // INTERFACES__MSG__DETAIL__ERROR__BUILDER_HPP_
