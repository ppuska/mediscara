// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from interfaces:msg/KPIC1.idl
// generated code does not contain a copyright notice

#ifndef INTERFACES__MSG__DETAIL__KPIC1__BUILDER_HPP_
#define INTERFACES__MSG__DETAIL__KPIC1__BUILDER_HPP_

#include "interfaces/msg/detail/kpic1__struct.hpp"
#include <rosidl_runtime_cpp/message_initialization.hpp>
#include <algorithm>
#include <utility>


namespace interfaces
{

namespace msg
{

namespace builder
{

class Init_KPIC1_quality
{
public:
  explicit Init_KPIC1_quality(::interfaces::msg::KPIC1 & msg)
  : msg_(msg)
  {}
  ::interfaces::msg::KPIC1 quality(::interfaces::msg::KPIC1::_quality_type arg)
  {
    msg_.quality = std::move(arg);
    return std::move(msg_);
  }

private:
  ::interfaces::msg::KPIC1 msg_;
};

class Init_KPIC1_performance
{
public:
  explicit Init_KPIC1_performance(::interfaces::msg::KPIC1 & msg)
  : msg_(msg)
  {}
  Init_KPIC1_quality performance(::interfaces::msg::KPIC1::_performance_type arg)
  {
    msg_.performance = std::move(arg);
    return Init_KPIC1_quality(msg_);
  }

private:
  ::interfaces::msg::KPIC1 msg_;
};

class Init_KPIC1_availability
{
public:
  Init_KPIC1_availability()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_KPIC1_performance availability(::interfaces::msg::KPIC1::_availability_type arg)
  {
    msg_.availability = std::move(arg);
    return Init_KPIC1_performance(msg_);
  }

private:
  ::interfaces::msg::KPIC1 msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::interfaces::msg::KPIC1>()
{
  return interfaces::msg::builder::Init_KPIC1_availability();
}

}  // namespace interfaces

#endif  // INTERFACES__MSG__DETAIL__KPIC1__BUILDER_HPP_
