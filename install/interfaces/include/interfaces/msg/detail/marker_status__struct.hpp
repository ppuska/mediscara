// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from interfaces:msg/MarkerStatus.idl
// generated code does not contain a copyright notice

#ifndef INTERFACES__MSG__DETAIL__MARKER_STATUS__STRUCT_HPP_
#define INTERFACES__MSG__DETAIL__MARKER_STATUS__STRUCT_HPP_

#include <rosidl_runtime_cpp/bounded_vector.hpp>
#include <rosidl_runtime_cpp/message_initialization.hpp>
#include <algorithm>
#include <array>
#include <memory>
#include <string>
#include <vector>


#ifndef _WIN32
# define DEPRECATED__interfaces__msg__MarkerStatus __attribute__((deprecated))
#else
# define DEPRECATED__interfaces__msg__MarkerStatus __declspec(deprecated)
#endif

namespace interfaces
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct MarkerStatus_
{
  using Type = MarkerStatus_<ContainerAllocator>;

  explicit MarkerStatus_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->marking_successful = false;
      this->marking_duration = 0.0;
    }
  }

  explicit MarkerStatus_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    (void)_alloc;
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->marking_successful = false;
      this->marking_duration = 0.0;
    }
  }

  // field types and members
  using _marking_successful_type =
    bool;
  _marking_successful_type marking_successful;
  using _marking_duration_type =
    double;
  _marking_duration_type marking_duration;

  // setters for named parameter idiom
  Type & set__marking_successful(
    const bool & _arg)
  {
    this->marking_successful = _arg;
    return *this;
  }
  Type & set__marking_duration(
    const double & _arg)
  {
    this->marking_duration = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    interfaces::msg::MarkerStatus_<ContainerAllocator> *;
  using ConstRawPtr =
    const interfaces::msg::MarkerStatus_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<interfaces::msg::MarkerStatus_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<interfaces::msg::MarkerStatus_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      interfaces::msg::MarkerStatus_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<interfaces::msg::MarkerStatus_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      interfaces::msg::MarkerStatus_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<interfaces::msg::MarkerStatus_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<interfaces::msg::MarkerStatus_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<interfaces::msg::MarkerStatus_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__interfaces__msg__MarkerStatus
    std::shared_ptr<interfaces::msg::MarkerStatus_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__interfaces__msg__MarkerStatus
    std::shared_ptr<interfaces::msg::MarkerStatus_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const MarkerStatus_ & other) const
  {
    if (this->marking_successful != other.marking_successful) {
      return false;
    }
    if (this->marking_duration != other.marking_duration) {
      return false;
    }
    return true;
  }
  bool operator!=(const MarkerStatus_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct MarkerStatus_

// alias to use template instance with default allocator
using MarkerStatus =
  interfaces::msg::MarkerStatus_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace interfaces

#endif  // INTERFACES__MSG__DETAIL__MARKER_STATUS__STRUCT_HPP_
