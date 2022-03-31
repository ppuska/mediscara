// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from interfaces:msg/Robot2Control.idl
// generated code does not contain a copyright notice

#ifndef INTERFACES__MSG__DETAIL__ROBOT2_CONTROL__BUILDER_HPP_
#define INTERFACES__MSG__DETAIL__ROBOT2_CONTROL__BUILDER_HPP_

#include "interfaces/msg/detail/robot2_control__struct.hpp"
#include <rosidl_runtime_cpp/message_initialization.hpp>
#include <algorithm>
#include <utility>


namespace interfaces
{

namespace msg
{

namespace builder
{

class Init_Robot2Control_start_marking
{
public:
  explicit Init_Robot2Control_start_marking(::interfaces::msg::Robot2Control & msg)
  : msg_(msg)
  {}
  ::interfaces::msg::Robot2Control start_marking(::interfaces::msg::Robot2Control::_start_marking_type arg)
  {
    msg_.start_marking = std::move(arg);
    return std::move(msg_);
  }

private:
  ::interfaces::msg::Robot2Control msg_;
};

class Init_Robot2Control_home
{
public:
  Init_Robot2Control_home()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_Robot2Control_start_marking home(::interfaces::msg::Robot2Control::_home_type arg)
  {
    msg_.home = std::move(arg);
    return Init_Robot2Control_start_marking(msg_);
  }

private:
  ::interfaces::msg::Robot2Control msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::interfaces::msg::Robot2Control>()
{
  return interfaces::msg::builder::Init_Robot2Control_home();
}

}  // namespace interfaces

#endif  // INTERFACES__MSG__DETAIL__ROBOT2_CONTROL__BUILDER_HPP_
