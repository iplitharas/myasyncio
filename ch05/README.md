<!-- TOC -->
  * [SQL async](#sql-async)
  * [Creating a connection pool to run queries concurrently](#creating-a-connection-pool-to-run-queries-concurrently)
  * [Managing transactions with asyncpg](#managing-transactions-with-asyncpg)
  * [Nested transactions](#nested-transactions)
  * [Cursors](#cursors)
  * [Async generators with cursor](#async-generators-with-cursor)
<!-- TOC -->
## SQL async
Assuming we have the following code block,
where we want to execute multiple queries with
`asyncio.gather`

```python
async def main():
    connection = await asyncpg.connect(host='127.0.0.1',
                                       port=5432,
                                       user='postgres',
                                       database='products',
                                       password='password')
    print('Creating the product database...')
    queries = [connection.execute(product_query),
               connection.execute(product_query)]
    results = await asyncio.gather(*queries)
```
This will raise the following exception:
```python
RuntimeError: readexactly() called while another coroutine 
is already waiting for incoming data
```

In the SQL world, one connection means one socket connection to our database.
Since we have only one connection and we’re trying to read the results of multiple 
queries concurrently, we experience an error.
We can resolve this by **creating multiple connections to our database and
executing one query per connection.**

> Since creating connections is resource expensive,
> caching them so we can access them when needed makes sense.
> This is commonly known as a `connection pool`


## Creating a connection pool to run queries concurrently
Since we can only run one query per connection at a time,
we need a mechanism for creating and managing multiple connections.
A **connection pool** does just that.
You can think of a connection pool as a **cache of existing connections** to a 
database instance.
They contain a finite number of connections that we can access 
when we need to run a query.

Using connection pools, we *acquire* connections when we need to run a query.
Acquiring a connection means we ask the pool,
>“Does the pool currently have any connections available?
> If so, give me one so I can run my queries.” 

Connection pools facilitate the reuse of these connections to execute queries.
> In other words, once a connection is acquired from the pool to run a query and 
> that query finishes, we return or “release” it to the pool for others to use.

This is important because establishing a connection with a database is time-expensive .
If we had to create a new connection for every query we wanted to run, 
our application’s performance would quickly degrade.

Since the connection pool has a finite number of connections,
we could be waiting for some time for one to become available,
as other connections may be in use.
This means connection acquisition is an operation that may take time to complete.
If we only have 10 connections in the pool, each of which is in use,
and we ask for another, we’ll need to wait until 1 of the 10 connections
becomes available for our query to execute

To illustrate how this works in terms of asyncio,
let’s imagine we have a connection pool with two connections.
Let’s also imagine we have three coroutines and each runs a query.
We’ll run these three coroutines concurrently as tasks.
With a connection pool set up this way,
the first two coroutines that attempt to run their queries will acquire the 
two available connections and start running their queries.
While this is happening, the third coroutine
will be waiting for a connection to become available.
When either one of the first two coroutines finishes running its query,
it will release its connection and return it to the pool.
This lets the third coroutine acquire it and start using it to run its query

![connection_pool.png](images%2Fconnection_pool.png)
```python
async def main():
    async with asyncpg.create_pool(host='127.0.0.1',
                                   port=5432,
                                   user='postgres',
                                   password='password',
                                   database='products',
                                   min_size=6,
                                   max_size=6) as pool:
 
        await asyncio.gather(query_product(pool),
                             query_product(pool))
```


## Managing transactions with asyncpg
**Transactions** are a core concept in many databases that satisfy the ACID 
(atomic, consistent, isolated, durable) properties. A *transaction* consists of one 
or more SQL statements that are executed as one atomic unit.
If no errors occur when we execute the statements within a transaction, we 
*commit* the statements to the database, making any changes a permanent part of 
the database.
If there are any errors, we *roll back* the statements,
and it is as if none of them ever happened.
In the context of our product database, we may need to roll back a set of updates 
if we attempt to insert a duplicate brand, 
or if we have violated a database constraint we’ve set.

In asyncpg, the easiest way to deal with transactions is to use the `connection.transaction` 
asynchronous context manager to start them.
Then, if there is an exception in the `async with block`,
the transaction will automatically be rolled back.
If everything executes successfully, it will be automatically committed.
```python
import asyncio
import asyncpg
 
async def main():
    connection = await asyncpg.connect(host='127.0.0.1',
                                       port=5432,
                                       user='postgres',
                                       database='products',
                                       password='password')
    async with connection.transaction():
        await connection.execute("INSERT INTO brand "
                                 "VALUES(DEFAULT, 'brand_1')")
        await connection.execute("INSERT INTO brand "
                                 "VALUES(DEFAULT, 'brand_2')")
 
    query = """SELECT brand_name FROM brand
                WHERE brand_name LIKE 'brand%'"""
    brands = await connection.fetch(query)
    print(brands)
 
    await connection.close()
 
asyncio.run(main())
```

## Nested transactions
asyncpg also supports the concept of a **nested transaction** through a Postgres 
feature called savepoints.
Savepoints are defined in Postgres with the `SAVEPOINT`command.
When we define a savepoint, we can roll back to that savepoint and any 
queries executed after the savepoint will roll back, 
but any queries successfully executed before it will not roll back.


## Cursors 
One drawback of the default fetch implementation asynpg provides is that it pulls 
all data from any query we execute into memory.
This means that if we have a query that returns millions of rows,
we’d attempt to transfer that entire set from the database to the requesting machine.
Going back to our product database example,
imagine we’re even more successful and have billions of products available.
It is highly likely that we’ll have some queries that will return very large 
result sets, potentially hurting performance.

Of course, we could apply `LIMIT` statements to our query and paginate things,
and this makes sense for many, if not most, applications.
That said, there is overhead with this approach in that we are sending 
the same query multiple times, potentially creating extra stress on the database.
If we find ourselves hampered by these issues,
it can make sense to **stream results for a particular query only as we need them**.
**This will save on memory consumption at our application lay**er as well as 
save load on the database. However, it does come at the expense of making more 
round trips over the network to the database.

> Postgres supports streaming query results through the concept of *cursors*.
> Consider a cursor as a pointer to where we currently are in iterating through a 
> result set. When we get a single result from a streamed query, 
> we advance the cursor to the next element, and so on, until we have no more results.


## Async generators with cursor 
```python
import asyncpg
import asyncio
 
 
async def main():
    connection = await asyncpg.connect(host='127.0.0.1',
                                       port=5432,
                                       user='postgres',
                                       database='products',
                                       password='password')
    async with connection.transaction():
        query = 'SELECT product_id, product_name from product'
        cursor = await connection.cursor(query)
        await cursor.forward(500)
        products = await cursor.fetch(100)
        for product in products:
            print(product)
 
    await connection.close()
 
 
asyncio.run(main())
```