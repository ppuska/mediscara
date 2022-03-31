// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from interfaces:msg/MarkerStatus.idl
// generated code does not contain a copyright notice

#ifndef INTERFACES__MSG__DETAIL__MARKER_STATUS__BUILDER_HPP_
#define INTERFACES__MSG__DETAIL__MARKER_STATUS__BUILDER_HPP_

#include "interfaces/msg/detail/marker_status__struct.hpp"
#include <rosidl_runtime_cpp/message_initialization.hpp>
#include <algorithm>
#include <utility>


namespace interfaces
{

namespace msg
{

namespace builder
{

class Init_MarkerStatus_marking_duration
{
public:
  explicit Init_MarkerStatus_marking_duration(::interfaces::msg::MarkerStatus & msg)
  : msg_(msg)
  {}
  ::interfaces::msg::MarkerStatus marking_duration(::interfaces::msg::MarkerStatus::_marking_duration_type arg)
  {
    msg_.marking_duration = std::move(arg);
    return std::move(msg_);
  }

private:
  ::interfaces::msg::MarkerStatus msg_;
};

class Init_MarkerStatus_marking_successful
{
public:
  Init_MarkerStatus_marking_successful()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_MarkerStatus_marking_duration marking_successful(::interfaces::msg::MarkerStatus::_marking_successful_type arg)
  {
    msg_.marking_successful = std::move(arg);
    return Init_MarkerStatus_marking_duration(msg_);
  }

private:
  ::interfaces::msg::MarkerStatus msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::interfaces::msg::MarkerStatus>()
{
  return interfaces::msg::builder::Init_MarkerStatus_marking_successful();
}

}  // namespace interfaces

#endif  // INTERFACES__MSG__DETAIL__MARKER_STATUS__BUILDER_HPP_
