# RabbitMQ Output in Flexget

This is intended to be an output to rabbitMQ for flexget.
Since I want to use RabbitMQ more and more for my own applications, I felt that it was a good idea to also have Flexget talking over RabbitMQ.

## How to install

First of all, install the requirement(s).
* You need to have flexget installed (within the same virtualenv)
* You need to have pika installed (tested with version 0.10.0)

Place rabbitmq.py in your plugins folder, e.g. ~/.config/flexget/plugins/

Configure accordingly to the documentation.

## Configuration

You configure it according the provided table here.
All configuration is done in the main flexget config.

| Name | Description | Default | Required |
| ------------- | ----------- | ----------- | ----------- |
| host | The host that RabbitMQ is running on | localhost | no |
| port | RabbitMQ server port | 5672 | no |
| username | The username for RabbitMQ | guest | no |
| password | The password for RabbitMQ | guest | no |
| exchange | Which RabbitMQ exchange to use | '' | no |
| routing_key | The routing key to use for the message | | yes |
| delivery_mode | Which deliverymode that should be used | 2 | no |
| queue_name | The name of the queue to use for the message | | yes |
| queue_durable | If the queue should be durable | True | no |
| body | How the message should be formatted (accepts Jinja2) | "{{series_name}} {{series_id}}" | no |

## License

The MIT License

Copyright (C) 2015 Niclas "Cromigon" Björner

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
