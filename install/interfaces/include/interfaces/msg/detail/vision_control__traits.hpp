// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from interfaces:msg/VisionControl.idl
// generated code does not contain a copyright notice

#ifndef INTERFACES__MSG__DETAIL__VISION_CONTROL__TRAITS_HPP_
#define INTERFACES__MSG__DETAIL__VISION_CONTROL__TRAITS_HPP_

#include "interfaces/msg/detail/vision_control__struct.hpp"
#include <rosidl_runtime_cpp/traits.hpp>
#include <stdint.h>
#include <type_traits>

namespace rosidl_generator_traits
{

template<>
inline const char * data_type<interfaces::msg::VisionControl>()
{
  return "interfaces::msg::VisionControl";
}

template<>
inline const char * name<interfaces::msg::VisionControl>()
{
  return "interfaces/msg/VisionControl";
}

template<>
struct has_fixed_size<interfaces::msg::VisionControl>
  : std::integral_constant<bool, true> {};

template<>
struct has_bounded_size<interfaces::msg::VisionControl>
  : std::integral_constant<bool, true> {};

template<>
struct is_message<interfaces::msg::VisionControl>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // INTERFACES__MSG__DETAIL__VISION_CONTROL__TRAITS_HPP_
