// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from interfaces:msg/Robot2Control.idl
// generated code does not contain a copyright notice

#ifndef INTERFACES__MSG__DETAIL__ROBOT2_CONTROL__STRUCT_HPP_
#define INTERFACES__MSG__DETAIL__ROBOT2_CONTROL__STRUCT_HPP_

#include <rosidl_runtime_cpp/bounded_vector.hpp>
#include <rosidl_runtime_cpp/message_initialization.hpp>
#include <algorithm>
#include <array>
#include <memory>
#include <string>
#include <vector>


#ifndef _WIN32
# define DEPRECATED__interfaces__msg__Robot2Control __attribute__((deprecated))
#else
# define DEPRECATED__interfaces__msg__Robot2Control __declspec(deprecated)
#endif

namespace interfaces
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct Robot2Control_
{
  using Type = Robot2Control_<ContainerAllocator>;

  explicit Robot2Control_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->home = false;
      this->start_marking = false;
    }
  }

  explicit Robot2Control_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    (void)_alloc;
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->home = false;
      this->start_marking = false;
    }
  }

  // field types and members
  using _home_type =
    bool;
  _home_type home;
  using _start_marking_type =
    bool;
  _start_marking_type start_marking;

  // setters for named parameter idiom
  Type & set__home(
    const bool & _arg)
  {
    this->home = _arg;
    return *this;
  }
  Type & set__start_marking(
    const bool & _arg)
  {
    this->start_marking = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    interfaces::msg::Robot2Control_<ContainerAllocator> *;
  using ConstRawPtr =
    const interfaces::msg::Robot2Control_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<interfaces::msg::Robot2Control_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<interfaces::msg::Robot2Control_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      interfaces::msg::Robot2Control_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<interfaces::msg::Robot2Control_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      interfaces::msg::Robot2Control_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<interfaces::msg::Robot2Control_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<interfaces::msg::Robot2Control_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<interfaces::msg::Robot2Control_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__interfaces__msg__Robot2Control
    std::shared_ptr<interfaces::msg::Robot2Control_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__interfaces__msg__Robot2Control
    std::shared_ptr<interfaces::msg::Robot2Control_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const Robot2Control_ & other) const
  {
    if (this->home != other.home) {
      return false;
    }
    if (this->start_marking != other.start_marking) {
      return false;
    }
    return true;
  }
  bool operator!=(const Robot2Control_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct Robot2Control_

// alias to use template instance with default allocator
using Robot2Control =
  interfaces::msg::Robot2Control_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace interfaces

#endif  // INTERFACES__MSG__DETAIL__ROBOT2_CONTROL__STRUCT_HPP_
