from yaoysTools.uniqueid.snowflake import snowFlakeId

worker = snowFlakeId(1, 2, 0)
for x in range(1, 10):
    print(worker.get_id())
