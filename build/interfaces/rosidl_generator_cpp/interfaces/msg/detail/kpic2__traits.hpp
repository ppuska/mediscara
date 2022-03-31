// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from interfaces:msg/KPIC2.idl
// generated code does not contain a copyright notice

#ifndef INTERFACES__MSG__DETAIL__KPIC2__TRAITS_HPP_
#define INTERFACES__MSG__DETAIL__KPIC2__TRAITS_HPP_

#include "interfaces/msg/detail/kpic2__struct.hpp"
#include <rosidl_runtime_cpp/traits.hpp>
#include <stdint.h>
#include <type_traits>

namespace rosidl_generator_traits
{

template<>
inline const char * data_type<interfaces::msg::KPIC2>()
{
  return "interfaces::msg::KPIC2";
}

template<>
inline const char * name<interfaces::msg::KPIC2>()
{
  return "interfaces/msg/KPIC2";
}

template<>
struct has_fixed_size<interfaces::msg::KPIC2>
  : std::integral_constant<bool, true> {};

template<>
struct has_bounded_size<interfaces::msg::KPIC2>
  : std::integral_constant<bool, true> {};

template<>
struct is_message<interfaces::msg::KPIC2>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // INTERFACES__MSG__DETAIL__KPIC2__TRAITS_HPP_
