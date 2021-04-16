## single connections

![alt text](https://files.realpython.com/media/sockets-loopback-interface.44fa30c53c70.jpg)

> Applications use the loopback interface to communicate with other processes running on the host and for security and isolation from the external network. Since it’s internal and accessible only from within the host, it’s not exposed.
> send() returns the number of bytes sent, which may be less than the size of the data passed in
> Applications are responsible for checking that all data has been sent
> using sendall()
* Unlike send(), this method continues to send data from bytes until either all data has been sent or an error occurs. None is returned on success

## multiple connections
* How do we handle multiple connections concurrently
* We need to call send() and recv() until all data is sent or received

> concurrency 
* https://docs.python.org/3/library/asyncio.html
* he traditional choice is to use threads.
    * https://docs.python.org/3/library/threading.html
> asyncio uses single-threaded cooperative multitasking and an event loop to manage tasks.
> With select(), allows you to check for I/O completion on more than one socket.
    * allows you to check for I/O completion on more than one socket.
> John Reese - Thinking Outside the GIL with AsyncIO and Multiprocessing - PyCon 2018
* https://youtu.be/0kXaLh8Fz3k
* multiprocessing in python comes with its own gil
* pool.map
* con: 
    * each process can only execute one task at a time
> AsyncIO
* based on futures
* faster than threads
* massive i/o concurrency
> AsyncIO rework
* make function into co routine instead of regular function
* when you call a co-routine you're not actually starting the execution of the function immediately. You're just getting a future back. It's only once you start to await that future that the co-routine will start getting scheduled for execution on the event loop. 
* essentially if the co-routine is called twice, it does not start to executie immediately because it returns the futures. We can then use the asyncIO gather helper which will do an await on all the futures you give it at the same time. Once those futures have completed, then it gives you the results back from those futures. 
>asyncIO con
* still limited by GIL ( only running on one process )
* beware timeouts and queue length
> ideal
* we want the io concurrency of asyncIO
* processing concurrency of multi-processing
> GIL
* global interpreter lock
* piece of python runtime that prevents multiple threads from executing on the VM at the same time
* it also prevents concurent memory access to python objects

```
import asyncio

async def main():
    print('Hello ...')
    await asyncio.sleep(1)
    print('... World!')

# Python 3.7+
asyncio.run(main())
```

## addendum
> Note: Security precautions and best practices still apply, even if your application isn’t “security-sensitive.” If your application accesses the network, it should be secured and maintained. This means, at a minimum:

* System software updates and security patches are applied regularly, including Python. Are you using any third party libraries? If so, make sure those are checked and updated too.

* If possible, use a dedicated or host-based firewall to restrict connections to trusted systems only.

* What DNS servers are configured? Do you trust them and their administrators?

* Make sure that request data is sanitized and validated as much as possible prior to calling other code that processes it. Use (fuzz) tests for this and run them regularly.

> For TLS,
* https://docs.python.org/3/library/ssl.html
