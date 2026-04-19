import asyncio
import aiohttp
import json
import pandas as pd
import os

# 1. Limit to 5 concurrent requests
SEMAPHORE_LIMIT = 5
semaphore = asyncio.Semaphore(SEMAPHORE_LIMIT)

def save_to_pandas_csv(new_results, file_path):
    # Convert your new list of dictionaries/data to a DataFrame
    new_df = pd.DataFrame(new_results).transpose()

    # Check if the file already exists
    file_exists = os.path.isfile(file_path)
    new_df.to_csv(file_path, mode='a', index=True, header=not file_exists,index_label="name")


async def safe_fetch(session, url):
    """
    Handles a single request with throttling and error protection.
    """
    # Use the semaphore to control flow
    async with semaphore:
        try:
            async with session.get(url, timeout=10) as response:
                # 2. Handle HTTP Errors (e.g., 404, 500)
                if response.status != 200:
                    print(f"⚠️ Error {response.status} for {url}")
                    return None
                
                # 3. Handle successful data retrieval
                return await response.json()

        except asyncio.TimeoutError:
            print(f"❌ Timeout: {url} took too long to respond.")
        except aiohttp.ClientError as e:
            print(f"❌ Connection Error for {url}: {e}")
        except Exception as e:
            print(f"❌ Unexpected Error: {e}")
            
        return None

async def main():
    urls = [f"https://pokeapi.co/api/v2/berry/{i}" for i in range(1,65)]
    
    async with aiohttp.ClientSession() as session:
        # Create a list of tasks
        tasks = [safe_fetch(session, url) for url in urls]
        
        # Run them all concurrently (but limited by semaphore)
        results = await asyncio.gather(*tasks)
        
        # Filter out None values from errors
        valid_results = [r for r in results if r]
        
        individual_berry_stats = ["growth_time","max_harvest","natural_gift_power","size","smoothness","soil_dryness"]
        berries = {}
        
        for berry in valid_results:
            berry_stat = {}
            for stat_type in individual_berry_stats:
                berry_stat[stat_type] = berry[stat_type]
            
            berries[berry["name"]] = berry_stat


        df = pd.DataFrame(berries)
        save_to_pandas_csv(df, "./data/berries.csv")
        

        with open("./data/berry_info.json","w+") as file:
            json.dump(berries,file,indent=4)

if __name__ == "__main__":
    asyncio.run(main())