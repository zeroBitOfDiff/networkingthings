
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
> multiprocessing and AsyncIO
* use the primitives that we get from multiprocessing module
* run an asyncIO event loop on each child process
* use the multiprocessing queues as communication from the parent to the child processes
* this will beef up AsyncIO 
    * ie, if we have 100 concurrent requests on a single async process, we can have 1000 concurrent requests if we had 10 processes running in parrallel. 
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
```
# example boiler plate for AsyncIO w/ multiprocessing
# tx,rx work queue and result queue
async def run_loop(tx,rx):
    limit = 10
    pending = set()
    while True:
        while len(pending) < limit:
            task = tx.get_nowait()
            fn, args, kwargs = task
            pending.add(fn(*args, **kwargs))
        
        done, pending = await asyncio.wait(pending, ...)
        for future in done:
            rx.put_nowait(await future)

def bootstrap(tx,rx):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(run_loop(tx,rx))

def main():
    p = multiprocessing.Process(
        target = bootstrap,
        args = (tx, rx)
    )
    p.start()
```
> a little nicer
* create a pool class that automatically instanctiates the child processes
* a helper function within class that can queue an individual item of work
* the helper function could give a unique integer Id for the task back as the result
* we then could have a a helper function that awaits the result given the task ID
* also if we reframe around a map/reduce style workload we will see significant optimization
* https://github.com/omnilib/aiomultiprocess
```
class Pool:
    async def queue(self, fn, *args, **kwargs) -> int: ...
    async def result(self, id) -> Any: ...

    async def map(self, fn, items):
        task_ids = [
            await self.queue(fn, (item,), {})
            for item in items
        ]
    return [
        await self.result(task_id)
        for task_id in task_ids
    ]
```
```
# implementing pool class

async def fetch_url(url):
    return await aiohttp.request('GET', url)

async def fetch_all(urls):
    async with Pool() as pool:
        results = await pool.map(fetch_url, urls)

```