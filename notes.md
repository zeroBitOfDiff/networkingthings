![alt text](https://files.realpython.com/media/sockets-loopback-interface.44fa30c53c70.jpg)


> Applications use the loopback interface to communicate with other processes running on the host and for security and isolation from the external network. Since it’s internal and accessible only from within the host, it’s not exposed.



> Note: Security precautions and best practices still apply, even if your application isn’t “security-sensitive.” If your application accesses the network, it should be secured and maintained. This means, at a minimum:

* System software updates and security patches are applied regularly, including Python. Are you using any third party libraries? If so, make sure those are checked and updated too.

* If possible, use a dedicated or host-based firewall to restrict connections to trusted systems only.

* What DNS servers are configured? Do you trust them and their administrators?

* Make sure that request data is sanitized and validated as much as possible prior to calling other code that processes it. Use (fuzz) tests for this and run them regularly.

