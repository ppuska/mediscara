// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from interfaces:msg/Robot2Control.idl
// generated code does not contain a copyright notice

#ifndef INTERFACES__MSG__DETAIL__ROBOT2_CONTROL__TRAITS_HPP_
#define INTERFACES__MSG__DETAIL__ROBOT2_CONTROL__TRAITS_HPP_

#include "interfaces/msg/detail/robot2_control__struct.hpp"
#include <rosidl_runtime_cpp/traits.hpp>
#include <stdint.h>
#include <type_traits>

namespace rosidl_generator_traits
{

template<>
inline const char * data_type<interfaces::msg::Robot2Control>()
{
  return "interfaces::msg::Robot2Control";
}

template<>
inline const char * name<interfaces::msg::Robot2Control>()
{
  return "interfaces/msg/Robot2Control";
}

template<>
struct has_fixed_size<interfaces::msg::Robot2Control>
  : std::integral_constant<bool, true> {};

template<>
struct has_bounded_size<interfaces::msg::Robot2Control>
  : std::integral_constant<bool, true> {};

template<>
struct is_message<interfaces::msg::Robot2Control>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // INTERFACES__MSG__DETAIL__ROBOT2_CONTROL__TRAITS_HPP_
