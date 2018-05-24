def showUavMsg(recDict):
    uavs = recDict["UAV_we"]
    for uav in uavs:
        print("uav_no:",uav["no"])
        print("type:",uav["type"])
        print("x:",uav["x"])
        print("y:",uav["y"])
        print("z:",uav["z"])
        print("status:",uav["status"])
def showGoodsMsg(recDict):
    goods  = recDict["goods"]
    for item in goods:
        print("goods_no:",item["no"])
        
        print("start_x:",item["start_x"])
        print("start_y:",item["start_y"])
        print("start_time",item["start_time"])
        print("end_x:",item["end_x"])
        print("end_y:",item["end_y"])
        print("status:",item["status"])
def showMapInfo(recDict):
    print("h_low:",recDict["h_low"])
    print("h_high:",recDict["h_high"])
    print("building:",recDict["building"])
    print("fog:",recDict["fog"])