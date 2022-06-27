/*
 * main.cpp

 *
 *  Created on: 2018/01/17
 *      Author: yoneken
 */
#include <mainpp.h>
#include <ros.h>
#include <std_msgs/String.h>
#include <geometry_msgs/Twist.h>
#include <iostream>
#include <array>

using std::array;

float demandx=0;
float demandz=0;
float demandy=0;

int vx = 0;
int vz = 0;
int vy = 0;

void cmd_vel_cb( const geometry_msgs::Twist& twist){
  demandx = twist.linear.x;
  demandz = twist.linear.z;
  demandy = twist.linear.y;
}
/*
std::array<int, 3> vars() {
	int vx = (int)demandx;
	int vz = (int)demandz;
	int vy = (int)demandy;
    return {vx,vy,vz};
}
*/

ros::NodeHandle nh;

std_msgs::String str_msg;
ros::Subscriber<geometry_msgs::Twist> sub("cmd_vel", cmd_vel_cb );

ros::Publisher chatter("chatter", &str_msg);
char hello[] = "Hello world!";

void HAL_UART_TxCpltCallback(UART_HandleTypeDef *huart){
  nh.getHardware()->flush();
}

void HAL_UART_RxCpltCallback(UART_HandleTypeDef *huart){
  nh.getHardware()->reset_rbuf();
}

void setup(void)
{
  nh.initNode();
  nh.subscribe(sub);
  nh.advertise(chatter);
}

void loop(void)
{
  HAL_GPIO_TogglePin(GPIOB, GPIO_PIN_3);

  str_msg.data = hello;
  chatter.publish(&str_msg);
  nh.spinOnce();

  HAL_Delay(1000);
}
