cmake_minimum_required(VERSION 2.8.3)
project(master_msgs)
find_package(catkin REQUIRED 
  roscpp
  rospy
  std_msgs
  sensor_msgs
  geometry_msgs
  message_generation
)

add_message_files(
  FILES
  arm_auto_status.msg
  arm_Orders.msg
  connection.msg
  current.msg
  goal.msg
  imu_Magnetism.msg
  imu_Speed.msg
  position.msg
  pots.msg
  rpm.msg
  traction_Orders.msg
  sensibility.msg
  geociencia.msg
  batteries.msg
  PID.msg
  OFDM.msg
)


add_service_files(
  FILES
  service_enable.srv
)

generate_messages(
  DEPENDENCIES
  std_msgs
  geometry_msgs
)


catkin_package(
  CATKIN_DEPENDS 
  message_runtime
  roscpp
  rospy
  std_msgs
  geometry_msgs
)



