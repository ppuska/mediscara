// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from interfaces:msg/Robot2Status.idl
// generated code does not contain a copyright notice

#ifndef INTERFACES__MSG__DETAIL__ROBOT2_STATUS__STRUCT_HPP_
#define INTERFACES__MSG__DETAIL__ROBOT2_STATUS__STRUCT_HPP_

#include <rosidl_runtime_cpp/bounded_vector.hpp>
#include <rosidl_runtime_cpp/message_initialization.hpp>
#include <algorithm>
#include <array>
#include <memory>
#include <string>
#include <vector>


#ifndef _WIN32
# define DEPRECATED__interfaces__msg__Robot2Status __attribute__((deprecated))
#else
# define DEPRECATED__interfaces__msg__Robot2Status __declspec(deprecated)
#endif

namespace interfaces
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct Robot2Status_
{
  using Type = Robot2Status_<ContainerAllocator>;

  explicit Robot2Status_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->power = false;
      this->running = false;
      this->waiting = false;
      this->error = false;
    }
  }

  explicit Robot2Status_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    (void)_alloc;
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->power = false;
      this->running = false;
      this->waiting = false;
      this->error = false;
    }
  }

  // field types and members
  using _power_type =
    bool;
  _power_type power;
  using _running_type =
    bool;
  _running_type running;
  using _waiting_type =
    bool;
  _waiting_type waiting;
  using _error_type =
    bool;
  _error_type error;

  // setters for named parameter idiom
  Type & set__power(
    const bool & _arg)
  {
    this->power = _arg;
    return *this;
  }
  Type & set__running(
    const bool & _arg)
  {
    this->running = _arg;
    return *this;
  }
  Type & set__waiting(
    const bool & _arg)
  {
    this->waiting = _arg;
    return *this;
  }
  Type & set__error(
    const bool & _arg)
  {
    this->error = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    interfaces::msg::Robot2Status_<ContainerAllocator> *;
  using ConstRawPtr =
    const interfaces::msg::Robot2Status_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<interfaces::msg::Robot2Status_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<interfaces::msg::Robot2Status_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      interfaces::msg::Robot2Status_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<interfaces::msg::Robot2Status_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      interfaces::msg::Robot2Status_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<interfaces::msg::Robot2Status_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<interfaces::msg::Robot2Status_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<interfaces::msg::Robot2Status_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__interfaces__msg__Robot2Status
    std::shared_ptr<interfaces::msg::Robot2Status_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__interfaces__msg__Robot2Status
    std::shared_ptr<interfaces::msg::Robot2Status_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const Robot2Status_ & other) const
  {
    if (this->power != other.power) {
      return false;
    }
    if (this->running != other.running) {
      return false;
    }
    if (this->waiting != other.waiting) {
      return false;
    }
    if (this->error != other.error) {
      return false;
    }
    return true;
  }
  bool operator!=(const Robot2Status_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct Robot2Status_

// alias to use template instance with default allocator
using Robot2Status =
  interfaces::msg::Robot2Status_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace interfaces

#endif  // INTERFACES__MSG__DETAIL__ROBOT2_STATUS__STRUCT_HPP_
