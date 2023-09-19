import asyncio

from product_parser_async.steps import get_all_categories, get_all_products,all_products
import time


async def main():
    task = asyncio.create_task(get_all_categories())
    await task
    task = asyncio.create_task(get_all_products())
    await task


if __name__ == '__main__':
    current = time.time()
    asyncio.run(main())
    print(time.time() - current)
    print(all_products)

