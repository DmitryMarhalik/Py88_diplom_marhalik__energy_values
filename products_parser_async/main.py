import asyncio

from products_parser_async.steps import get_all_categories, get_all_products,all_products,categories
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

numb_categories = [str(num) for num in range(1, len(categories) + 1)]
pars_category = dict(zip(categories, numb_categories))
print(pars_category)