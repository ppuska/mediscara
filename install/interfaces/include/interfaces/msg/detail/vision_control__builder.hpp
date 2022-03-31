// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from interfaces:msg/VisionControl.idl
// generated code does not contain a copyright notice

#ifndef INTERFACES__MSG__DETAIL__VISION_CONTROL__BUILDER_HPP_
#define INTERFACES__MSG__DETAIL__VISION_CONTROL__BUILDER_HPP_

#include "interfaces/msg/detail/vision_control__struct.hpp"
#include <rosidl_runtime_cpp/message_initialization.hpp>
#include <algorithm>
#include <utility>


namespace interfaces
{

namespace msg
{

namespace builder
{

class Init_VisionControl_measure_label
{
public:
  explicit Init_VisionControl_measure_label(::interfaces::msg::VisionControl & msg)
  : msg_(msg)
  {}
  ::interfaces::msg::VisionControl measure_label(::interfaces::msg::VisionControl::_measure_label_type arg)
  {
    msg_.measure_label = std::move(arg);
    return std::move(msg_);
  }

private:
  ::interfaces::msg::VisionControl msg_;
};

class Init_VisionControl_measure_pcb
{
public:
  explicit Init_VisionControl_measure_pcb(::interfaces::msg::VisionControl & msg)
  : msg_(msg)
  {}
  Init_VisionControl_measure_label measure_pcb(::interfaces::msg::VisionControl::_measure_pcb_type arg)
  {
    msg_.measure_pcb = std::move(arg);
    return Init_VisionControl_measure_label(msg_);
  }

private:
  ::interfaces::msg::VisionControl msg_;
};

class Init_VisionControl_home
{
public:
  Init_VisionControl_home()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_VisionControl_measure_pcb home(::interfaces::msg::VisionControl::_home_type arg)
  {
    msg_.home = std::move(arg);
    return Init_VisionControl_measure_pcb(msg_);
  }

private:
  ::interfaces::msg::VisionControl msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::interfaces::msg::VisionControl>()
{
  return interfaces::msg::builder::Init_VisionControl_home();
}

}  // namespace interfaces

#endif  // INTERFACES__MSG__DETAIL__VISION_CONTROL__BUILDER_HPP_
