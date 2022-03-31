// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from interfaces:msg/KPIC2.idl
// generated code does not contain a copyright notice

#ifndef INTERFACES__MSG__DETAIL__KPIC2__STRUCT_HPP_
#define INTERFACES__MSG__DETAIL__KPIC2__STRUCT_HPP_

#include <rosidl_runtime_cpp/bounded_vector.hpp>
#include <rosidl_runtime_cpp/message_initialization.hpp>
#include <algorithm>
#include <array>
#include <memory>
#include <string>
#include <vector>


#ifndef _WIN32
# define DEPRECATED__interfaces__msg__KPIC2 __attribute__((deprecated))
#else
# define DEPRECATED__interfaces__msg__KPIC2 __declspec(deprecated)
#endif

namespace interfaces
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct KPIC2_
{
  using Type = KPIC2_<ContainerAllocator>;

  explicit KPIC2_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->availability = 0.0;
      this->performance = 0.0;
      this->quality = 0.0;
    }
  }

  explicit KPIC2_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    (void)_alloc;
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->availability = 0.0;
      this->performance = 0.0;
      this->quality = 0.0;
    }
  }

  // field types and members
  using _availability_type =
    double;
  _availability_type availability;
  using _performance_type =
    double;
  _performance_type performance;
  using _quality_type =
    double;
  _quality_type quality;

  // setters for named parameter idiom
  Type & set__availability(
    const double & _arg)
  {
    this->availability = _arg;
    return *this;
  }
  Type & set__performance(
    const double & _arg)
  {
    this->performance = _arg;
    return *this;
  }
  Type & set__quality(
    const double & _arg)
  {
    this->quality = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    interfaces::msg::KPIC2_<ContainerAllocator> *;
  using ConstRawPtr =
    const interfaces::msg::KPIC2_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<interfaces::msg::KPIC2_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<interfaces::msg::KPIC2_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      interfaces::msg::KPIC2_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<interfaces::msg::KPIC2_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      interfaces::msg::KPIC2_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<interfaces::msg::KPIC2_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<interfaces::msg::KPIC2_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<interfaces::msg::KPIC2_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__interfaces__msg__KPIC2
    std::shared_ptr<interfaces::msg::KPIC2_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__interfaces__msg__KPIC2
    std::shared_ptr<interfaces::msg::KPIC2_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const KPIC2_ & other) const
  {
    if (this->availability != other.availability) {
      return false;
    }
    if (this->performance != other.performance) {
      return false;
    }
    if (this->quality != other.quality) {
      return false;
    }
    return true;
  }
  bool operator!=(const KPIC2_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct KPIC2_

// alias to use template instance with default allocator
using KPIC2 =
  interfaces::msg::KPIC2_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace interfaces

#endif  // INTERFACES__MSG__DETAIL__KPIC2__STRUCT_HPP_
