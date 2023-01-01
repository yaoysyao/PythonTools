from yaoysTools.uniqueid.snowflake import snowFlakeId

"""
        初始化
        :param datacenter_id: 数据中心（机器区域）ID
        :param worker_id: 机器ID
        :param sequence: 序号
        """
worker = snowFlakeId(1, 2, 0)
for x in range(1, 10):
    print(worker.get_id())
