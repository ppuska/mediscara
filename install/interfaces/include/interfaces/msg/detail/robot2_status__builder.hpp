// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from interfaces:msg/Robot2Status.idl
// generated code does not contain a copyright notice

#ifndef INTERFACES__MSG__DETAIL__ROBOT2_STATUS__BUILDER_HPP_
#define INTERFACES__MSG__DETAIL__ROBOT2_STATUS__BUILDER_HPP_

#include "interfaces/msg/detail/robot2_status__struct.hpp"
#include <rosidl_runtime_cpp/message_initialization.hpp>
#include <algorithm>
#include <utility>


namespace interfaces
{

namespace msg
{

namespace builder
{

class Init_Robot2Status_error
{
public:
  explicit Init_Robot2Status_error(::interfaces::msg::Robot2Status & msg)
  : msg_(msg)
  {}
  ::interfaces::msg::Robot2Status error(::interfaces::msg::Robot2Status::_error_type arg)
  {
    msg_.error = std::move(arg);
    return std::move(msg_);
  }

private:
  ::interfaces::msg::Robot2Status msg_;
};

class Init_Robot2Status_waiting
{
public:
  explicit Init_Robot2Status_waiting(::interfaces::msg::Robot2Status & msg)
  : msg_(msg)
  {}
  Init_Robot2Status_error waiting(::interfaces::msg::Robot2Status::_waiting_type arg)
  {
    msg_.waiting = std::move(arg);
    return Init_Robot2Status_error(msg_);
  }

private:
  ::interfaces::msg::Robot2Status msg_;
};

class Init_Robot2Status_running
{
public:
  explicit Init_Robot2Status_running(::interfaces::msg::Robot2Status & msg)
  : msg_(msg)
  {}
  Init_Robot2Status_waiting running(::interfaces::msg::Robot2Status::_running_type arg)
  {
    msg_.running = std::move(arg);
    return Init_Robot2Status_waiting(msg_);
  }

private:
  ::interfaces::msg::Robot2Status msg_;
};

class Init_Robot2Status_power
{
public:
  Init_Robot2Status_power()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_Robot2Status_running power(::interfaces::msg::Robot2Status::_power_type arg)
  {
    msg_.power = std::move(arg);
    return Init_Robot2Status_running(msg_);
  }

private:
  ::interfaces::msg::Robot2Status msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::interfaces::msg::Robot2Status>()
{
  return interfaces::msg::builder::Init_Robot2Status_power();
}

}  // namespace interfaces

#endif  // INTERFACES__MSG__DETAIL__ROBOT2_STATUS__BUILDER_HPP_
