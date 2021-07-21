import asyncio

async def simulatedFetcher(url,delay):
    await asyncio.sleep(delay)
    print(f"Fetched { url } after { delay }")
    return f"<html>{ url }"

def main():
    loop = asyncio.get_event_loop()
    results = loop.run_until_complete(asyncio.gather(
        simulatedFetcher('http://google.com',4),
        simulatedFetcher('http://bbc.co.uk',3),
    ))
    print(results)
if __name__ == "__main__":
    main()

    
    


