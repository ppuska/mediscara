// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from interfaces:msg/VisionControl.idl
// generated code does not contain a copyright notice

#ifndef INTERFACES__MSG__DETAIL__VISION_CONTROL__STRUCT_HPP_
#define INTERFACES__MSG__DETAIL__VISION_CONTROL__STRUCT_HPP_

#include <rosidl_runtime_cpp/bounded_vector.hpp>
#include <rosidl_runtime_cpp/message_initialization.hpp>
#include <algorithm>
#include <array>
#include <memory>
#include <string>
#include <vector>


#ifndef _WIN32
# define DEPRECATED__interfaces__msg__VisionControl __attribute__((deprecated))
#else
# define DEPRECATED__interfaces__msg__VisionControl __declspec(deprecated)
#endif

namespace interfaces
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct VisionControl_
{
  using Type = VisionControl_<ContainerAllocator>;

  explicit VisionControl_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->home = false;
      this->measure_pcb = false;
      this->measure_label = false;
    }
  }

  explicit VisionControl_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    (void)_alloc;
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->home = false;
      this->measure_pcb = false;
      this->measure_label = false;
    }
  }

  // field types and members
  using _home_type =
    bool;
  _home_type home;
  using _measure_pcb_type =
    bool;
  _measure_pcb_type measure_pcb;
  using _measure_label_type =
    bool;
  _measure_label_type measure_label;

  // setters for named parameter idiom
  Type & set__home(
    const bool & _arg)
  {
    this->home = _arg;
    return *this;
  }
  Type & set__measure_pcb(
    const bool & _arg)
  {
    this->measure_pcb = _arg;
    return *this;
  }
  Type & set__measure_label(
    const bool & _arg)
  {
    this->measure_label = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    interfaces::msg::VisionControl_<ContainerAllocator> *;
  using ConstRawPtr =
    const interfaces::msg::VisionControl_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<interfaces::msg::VisionControl_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<interfaces::msg::VisionControl_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      interfaces::msg::VisionControl_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<interfaces::msg::VisionControl_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      interfaces::msg::VisionControl_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<interfaces::msg::VisionControl_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<interfaces::msg::VisionControl_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<interfaces::msg::VisionControl_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__interfaces__msg__VisionControl
    std::shared_ptr<interfaces::msg::VisionControl_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__interfaces__msg__VisionControl
    std::shared_ptr<interfaces::msg::VisionControl_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const VisionControl_ & other) const
  {
    if (this->home != other.home) {
      return false;
    }
    if (this->measure_pcb != other.measure_pcb) {
      return false;
    }
    if (this->measure_label != other.measure_label) {
      return false;
    }
    return true;
  }
  bool operator!=(const VisionControl_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct VisionControl_

// alias to use template instance with default allocator
using VisionControl =
  interfaces::msg::VisionControl_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace interfaces

#endif  // INTERFACES__MSG__DETAIL__VISION_CONTROL__STRUCT_HPP_
